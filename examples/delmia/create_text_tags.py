"""
Create Text Tags

Description
===========
Creates a TagGroup of robot tags that depict a user-defined string, for example
"EngroTec Consulting". Tags are placed along print-style glyph strokes in the
order a person would write the string, and are numbered in that order.

The interpolation value is the distance between neighbouring tags along each
stroke. Optional overall width and height scale the finished tag cloud.

Requirements
============
python >= 3.9
pyv5
DELMIA / CATIA V5 running with an open CATProcess or CATProduct.
The Device Task Definition (robotics) workbench must be available so that
TagGroupFactory can be obtained from the selected Product.

Usage
=====
Edit the defaults below, or pass them on the command line::

    python create_text_tags.py --text "EngroTec Consulting" --interpolation 5 --width 500 --height 80

    python create_text_tags.py --dry-run

Select the product that should own the TagGroup when prompted.

Documentation
=============
https://pyv5.readthedocs.io
"""

import argparse
import csv
import re
import sys
from collections.abc import Sequence

from pywintypes import com_error

from examples.delmia.create_text_tags_support.layout import TagSample, layout_text_tags
from pyv5 import v5
from pyv5.base.cat_logger import create_logger
from pyv5.interfaces.dnb_igp_setup.tag_batch import TagPlacement
from pyv5.interfaces.dnb_igp_setup.tag_group_factory import TagGroupFactory
from pyv5.interfaces.product_structure.product import Product

# User-defined defaults. Command-line flags override these.
TEXT = "Happy Robotics"
INTERPOLATION = 10.0
WIDTH = 2000.0
HEIGHT = 300
ORIGIN = (0.0, 0.0, 0.0)
TAG_TYPE = "Manufacturing"

logger = create_logger()


def v5_object_name(text: str) -> str:
    """Build a CATIA/DELMIA object name from ``text``.

    Names must start with a letter and cannot contain spaces.
    """
    cleaned = re.sub(r"[^A-Za-z0-9_]", "_", text.strip())
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    if not cleaned:
        cleaned = "TagGroup"
    if not cleaned[0].isalpha():
        cleaned = "G_" + cleaned
    return cleaned


def _select_owner_product(document) -> Product | None:
    selection = document.selection
    status = selection.select_element2(
        ("Product",),
        "Select the product that will own the TagGroup.",
        True,
    )
    if status == "Cancel":
        logger.info("Selection cancelled. Exiting.")
        return None
    if selection.count2 < 1:
        return None
    return Product(selection.item2(1).value.com_object)


def _tag_group_factory(product: Product) -> TagGroupFactory:
    try:
        return TagGroupFactory(product.get_technological_object("TagGroupFactory"))
    except com_error as exc:
        raise RuntimeError(
            "Could not get TagGroupFactory from the selected product. "
            "Open a robotics / Device Task Definition document and select a Product "
            "that can own tags."
        ) from exc


def write_samples_csv(path: str, samples: Sequence[TagSample]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["index", "name", "char", "stroke", "x", "y", "z", "yaw", "pitch", "roll"])
        for sample in samples:
            writer.writerow(
                [
                    sample.index,
                    sample.name,
                    sample.char,
                    sample.stroke,
                    sample.x,
                    sample.y,
                    sample.z,
                    sample.yaw,
                    sample.pitch,
                    sample.roll,
                ]
            )


def placements_from_samples(
    samples: Sequence[TagSample], tag_type: str = TAG_TYPE
) -> list[TagPlacement]:
    return [
        TagPlacement(
            name=sample.name,
            x=sample.x,
            y=sample.y,
            z=sample.z,
            yaw=sample.yaw,
            pitch=sample.pitch,
            roll=sample.roll,
            type=tag_type,
        )
        for sample in samples
    ]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a TagGroup of robot tags that write a string."
    )
    parser.add_argument("--text", default=TEXT, help="String the tags should depict.")
    parser.add_argument(
        "--interpolation",
        type=float,
        default=INTERPOLATION,
        help="Distance between neighbouring tags along each stroke (mm).",
    )
    parser.add_argument(
        "--width",
        type=float,
        default=WIDTH,
        help="Overall tag-cloud width in mm. Omit with --no-width to keep font aspect from --height.",
    )
    parser.add_argument(
        "--height",
        type=float,
        default=HEIGHT,
        help="Overall tag-cloud height in mm. Omit with --no-height to keep font aspect from --width.",
    )
    parser.add_argument("--no-width", action="store_true", help="Do not scale to a target width.")
    parser.add_argument("--no-height", action="store_true", help="Do not scale to a target height.")
    parser.add_argument("--origin-x", type=float, default=ORIGIN[0])
    parser.add_argument("--origin-y", type=float, default=ORIGIN[1])
    parser.add_argument("--origin-z", type=float, default=ORIGIN[2])
    parser.add_argument(
        "--tag-type",
        default=TAG_TYPE,
        help="Tag frame type: Manufacturing, Design, Tool, Base, or Custom.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the planned tags without connecting to CATIA/DELMIA.",
    )
    parser.add_argument(
        "--csv",
        default="",
        help="Optional path to write the planned tag coordinates as CSV.",
    )
    return parser.parse_args(argv)


def build_samples(args: argparse.Namespace) -> tuple[list[TagSample], list[str], str]:
    width = None if args.no_width else args.width
    height = None if args.no_height else args.height
    samples, unknown = layout_text_tags(
        text=args.text,
        interpolation=args.interpolation,
        width=width,
        height=height,
        origin=(args.origin_x, args.origin_y, args.origin_z),
    )
    return samples, unknown, v5_object_name(args.text)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    samples, unknown, group_name = build_samples(args)

    if unknown:
        logger.warning("No stroke font for %s; those characters use a fallback box.", unknown)
    if not samples:
        logger.error("No tags to create for text %r.", args.text)
        return 1

    logger.info(
        "Planned %s tags in TagGroup '%s' for %r (interpolation=%s).",
        len(samples),
        group_name,
        args.text,
        args.interpolation,
    )

    if args.csv:
        write_samples_csv(args.csv, samples)
        logger.info("Wrote tag coordinates to %s.", args.csv)

    if args.dry_run:
        for sample in samples:
            logger.info(
                "%s  %s  stroke %s  (%.3f, %.3f, %.3f)",
                sample.name,
                sample.char,
                sample.stroke,
                sample.x,
                sample.y,
                sample.z,
            )
        return 0

    application = v5()
    document = application.active_document
    if document is None:
        logger.error("No active document. Open a CATProcess or CATProduct in DELMIA/CATIA.")
        return 1

    product = _select_owner_product(document)
    if product is None:
        return 1

    factory = _tag_group_factory(product)
    factory.create_tag_group(
        group_name,
        False,
        product,
        tags=placements_from_samples(samples, args.tag_type),
    )
    logger.info("Finished creating %s tags in TagGroup '%s'.", len(samples), group_name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
