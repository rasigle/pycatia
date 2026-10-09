"""Generate Sphinx automodule pages from the pyv5 package tree.

Output lives in docs/source/api/ and is gitignored. Sphinx runs this from
docs/source/conf.py on every build.

    uv run python scripts/documentation/generate_api.py
"""

from __future__ import annotations

import shutil
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_ROOT = REPO_ROOT / "pyv5"
DOCS_SOURCE = REPO_ROOT / "docs" / "source"
API_ROOT = DOCS_SOURCE / "api"


def module_qualname(py_file: Path) -> str:
    return ".".join(py_file.relative_to(PACKAGE_ROOT.parent).with_suffix("").parts)


def package_qualname(py_file: Path) -> str:
    return ".".join(py_file.relative_to(PACKAGE_ROOT.parent).parent.parts)


def pascal_label(stem: str) -> str:
    return "".join(part[:1].upper() + part[1:] for part in stem.split("_") if part)


def index_stem(package: str) -> str:
    if package == "pyv5":
        return "index_pyv5"
    return "index_" + package.removeprefix("pyv5.").replace(".", "_")


def collect_modules() -> dict[str, list[Path]]:
    grouped: dict[str, list[Path]] = defaultdict(list)
    for py_file in sorted(PACKAGE_ROOT.rglob("*.py")):
        if py_file.name == "__init__.py" or "__pycache__" in py_file.parts:
            continue
        grouped[package_qualname(py_file)].append(py_file)
    return grouped


def rst_relpath(py_file: Path) -> str:
    return "/".join(py_file.relative_to(PACKAGE_ROOT.parent).with_suffix("").parts)


def write_module_page(py_file: Path, labels_used: dict[str, str]) -> None:
    qual = module_qualname(py_file)
    dest = API_ROOT / Path(*qual.split(".")).with_suffix(".rst")
    dest.parent.mkdir(parents=True, exist_ok=True)

    label = pascal_label(py_file.stem)
    if label in labels_used and labels_used[label] != qual:
        label = pascal_label(py_file.parent.name) + label
    labels_used[label] = qual

    dest.write_text(
        f".. _{label}:\n\n"
        f"{qual}\n"
        f"{'=' * len(qual)}\n\n"
        f".. automodule:: {qual}\n"
        f"    :members:\n",
        encoding="utf-8",
        newline="\n",
    )


def write_package_index(package: str, py_files: list[Path]) -> str:
    stem = index_stem(package)
    title = package
    lines = [
        f"{title}\n",
        f"{'=' * len(title)}\n\n",
        ".. toctree::\n",
        "   :maxdepth: 1\n",
        "   :caption: Contents:\n\n",
    ]
    for py_file in py_files:
        lines.append(f"   {rst_relpath(py_file)}\n")
    (API_ROOT / f"{stem}.rst").write_text("".join(lines), encoding="utf-8", newline="\n")
    return stem


def write_api_index(index_stems: list[str]) -> None:
    body = [
        "API\n",
        "=========\n\n",
        "This part of the documentation covers all the interfaces of pyv5.\n\n",
        "The entry point for most pyv5 use cases is to do the following.\n\n",
        ">>> from pyv5 import v5\n\n",
        "This creates an instance of the :ref:`Application<Application>` object.\n\n",
        ".. toctree::\n",
        "   :maxdepth: 1\n",
        "   :caption: Contents:\n\n",
    ]
    for stem in index_stems:
        body.append(f"   {stem}\n")
    (API_ROOT / "index.rst").write_text("".join(body), encoding="utf-8", newline="\n")


def main() -> None:
    grouped = collect_modules()
    if not grouped:
        raise SystemExit(f"No Python modules found under {PACKAGE_ROOT}")

    if API_ROOT.exists():
        shutil.rmtree(API_ROOT)
    API_ROOT.mkdir(parents=True)

    labels_used: dict[str, str] = {}
    for py_files in grouped.values():
        for py_file in py_files:
            write_module_page(py_file, labels_used)

    def sort_key(package: str) -> tuple[int, str]:
        if package == "pyv5":
            return (0, package)
        if package == "pyv5.base":
            return (1, package)
        return (2, package)

    index_stems = [
        write_package_index(package, grouped[package])
        for package in sorted(grouped, key=sort_key)
    ]
    write_api_index(index_stems)
    print(f"Wrote {sum(len(v) for v in grouped.values())} API pages under {API_ROOT}")


if __name__ == "__main__":
    main()
