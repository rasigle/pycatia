"""CATIA enumeration name tuples, derived from :mod:`pyv5.base.enums`.

Each IntEnum in :mod:`pyv5.base.enums` is exported here as a tuple of member
names using the historic snake_case identifier (for example ``CatPaperSize``
becomes ``cat_paper_size``). Prefer the IntEnum classes.
"""

from __future__ import annotations

import re
from enum import IntEnum

from pyv5.base import enums as _enums


def _tuple_name(class_name: str) -> str:
    name = class_name.replace("3D", "_3d").replace("2D", "_2d")
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    return re.sub(r"_+", "_", name).lower().strip("_")


__all__: list[str] = []
for _name, _obj in vars(_enums).items():
    if isinstance(_obj, type) and issubclass(_obj, IntEnum) and _obj is not IntEnum:
        _key = _tuple_name(_name)
        globals()[_key] = tuple(member.name for member in _obj)
        __all__.append(_key)

__all__.sort()
