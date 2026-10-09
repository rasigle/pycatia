"""Turn a string into numbered tag samples in human writing order."""

from __future__ import annotations

import math
from dataclasses import dataclass

from create_text_tags_support.stroke_font import get_glyph

_EPS = 1e-9


@dataclass(frozen=True)
class TagSample:
    """One robot tag along the written string."""

    index: int
    name: str
    x: float
    y: float
    z: float
    yaw: float
    pitch: float
    roll: float
    char: str
    stroke: int


def _dedupe(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    cleaned: list[tuple[float, float]] = []
    for point in points:
        if not cleaned or math.hypot(point[0] - cleaned[-1][0], point[1] - cleaned[-1][1]) > _EPS:
            cleaned.append(point)
    return cleaned


def _polyline_length(points: list[tuple[float, float]]) -> float:
    return sum(
        math.hypot(points[i + 1][0] - points[i][0], points[i + 1][1] - points[i][1])
        for i in range(len(points) - 1)
    )


def _point_tangent_at(
    points: list[tuple[float, float]], distance: float
) -> tuple[float, float, float, float]:
    remaining = distance
    for i in range(len(points) - 1):
        x0, y0 = points[i]
        x1, y1 = points[i + 1]
        seg_len = math.hypot(x1 - x0, y1 - y0)
        if seg_len < _EPS:
            continue
        if remaining <= seg_len + _EPS:
            t = 0.0 if seg_len < _EPS else min(1.0, max(0.0, remaining / seg_len))
            tx, ty = (x1 - x0) / seg_len, (y1 - y0) / seg_len
            return x0 + t * (x1 - x0), y0 + t * (y1 - y0), tx, ty
        remaining -= seg_len
    x0, y0 = points[-2]
    x1, y1 = points[-1]
    seg_len = math.hypot(x1 - x0, y1 - y0)
    if seg_len < _EPS:
        return x1, y1, 1.0, 0.0
    return x1, y1, (x1 - x0) / seg_len, (y1 - y0) / seg_len


def sample_stroke(points: list[tuple[float, float]], spacing: float) -> list[tuple[float, float, float, float]]:
    """Sample a polyline at ``spacing``, always including the start and end."""
    pts = _dedupe(points)
    if not pts:
        return []
    if len(pts) == 1:
        return [(pts[0][0], pts[0][1], 1.0, 0.0)]
    if spacing <= 0:
        raise ValueError("interpolation spacing must be greater than 0")

    total = _polyline_length(pts)
    distances = [0.0]
    cursor = spacing
    while cursor < total - _EPS:
        distances.append(cursor)
        cursor += spacing
    if total - distances[-1] > _EPS:
        distances.append(total)
    return [_point_tangent_at(pts, distance) for distance in distances]


def _layout_strokes(text: str, tracking: float) -> tuple[list[tuple[str, int, list[tuple[float, float]]]], list[str]]:
    """Place glyph strokes in font space, left to right.

    Returns a list of (char, stroke_index, polyline) and unknown characters.
    """
    placed: list[tuple[str, int, list[tuple[float, float]]]] = []
    unknown: list[str] = []
    cursor = 0.0
    for char in text:
        glyph, is_fallback = get_glyph(char)
        if is_fallback:
            unknown.append(char)
        advance, strokes = glyph
        for stroke_index, stroke in enumerate(strokes):
            placed.append(
                (
                    char,
                    stroke_index,
                    [(cursor + x, y) for x, y in stroke],
                )
            )
        cursor += advance + tracking
    return placed, unknown


def _bbox(polylines: list[list[tuple[float, float]]]) -> tuple[float, float, float, float]:
    xs = [x for stroke in polylines for x, _y in stroke]
    ys = [y for stroke in polylines for _x, y in stroke]
    return min(xs), min(ys), max(xs), max(ys)


def _scale_factors(
    min_x: float,
    min_y: float,
    max_x: float,
    max_y: float,
    width: float | None,
    height: float | None,
    default_height: float,
) -> tuple[float, float]:
    span_x = max(max_x - min_x, _EPS)
    span_y = max(max_y - min_y, _EPS)
    if width is not None and height is not None:
        return width / span_x, height / span_y
    if width is not None:
        scale = width / span_x
        return scale, scale
    if height is not None:
        scale = height / span_y
        return scale, scale
    scale = default_height / span_y
    return scale, scale


def layout_text_tags(
    text: str,
    interpolation: float,
    width: float | None = None,
    height: float | None = None,
    origin: tuple[float, float, float] = (0.0, 0.0, 0.0),
    tracking: float = 0.08,
    default_height: float = 100.0,
) -> tuple[list[TagSample], list[str]]:
    """Build numbered tag samples that depict ``text``.

    Parameters
    ----------
    text:
        The string to write, left to right.
    interpolation:
        Distance between neighbouring tags along each stroke (model units, usually mm).
    width, height:
        Overall size of the tag cloud after layout. If only one is given the
        aspect ratio of the font is kept. If both are given the cloud is scaled
        independently in X and Y. If neither is given ``default_height`` is used.
    origin:
        World-space lower-left of the final bounding box.
    tracking:
        Extra gap between glyphs, in cap-height units.
    default_height:
        Height used when neither ``width`` nor ``height`` is set.

    Returns
    -------
    samples, unknown_chars
        Samples are ordered and named in writing order. ``unknown_chars`` lists
        characters drawn with the fallback box.
    """
    if interpolation <= 0:
        raise ValueError("interpolation must be greater than 0")
    if not text:
        return [], []

    placed, unknown = _layout_strokes(text, tracking)
    polylines = [stroke for _char, _idx, stroke in placed if stroke]
    if not polylines:
        return [], unknown

    min_x, min_y, max_x, max_y = _bbox(polylines)
    sx, sy = _scale_factors(min_x, min_y, max_x, max_y, width, height, default_height)
    ox, oy, oz = origin

    samples: list[TagSample] = []
    for char, stroke_index, stroke in placed:
        world = [
            (ox + (x - min_x) * sx, oy + (y - min_y) * sy) for x, y in stroke
        ]
        for x, y, tx, ty in sample_stroke(world, interpolation):
            index = len(samples) + 1
            samples.append(
                TagSample(
                    index=index,
                    name=f"T{index:04d}",
                    x=x,
                    y=y,
                    z=oz,
                    yaw=math.atan2(ty, tx),
                    pitch=0.0,
                    roll=0.0,
                    char=char,
                    stroke=stroke_index,
                )
            )
    return samples, unknown
