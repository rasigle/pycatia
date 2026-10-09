from enum import IntEnum

from pyv5 import CatPaperSize, CatScriptLanguage
from pyv5.base.enumeration_types import cat_paper_size, cat_script_language
from pyv5.base.enums import CatPaperSize as BaseCatPaperSize


def test_root_exports_base_enums():
    assert CatPaperSize is BaseCatPaperSize
    assert issubclass(CatPaperSize, IntEnum)
    assert CatScriptLanguage.CATVBScriptLanguage == 0


def test_enumeration_types_match_intenum_members():
    assert cat_paper_size == tuple(member.name for member in CatPaperSize)
    assert cat_script_language == tuple(member.name for member in CatScriptLanguage)
