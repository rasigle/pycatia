from unittest.mock import MagicMock

from pyv5.base.enums import CatScriptLanguage
from pyv5.base.nothing import _VBA_NOTHING, VBANothing, com_or_nothing, vba_nothing


def test_vba_nothing_is_a_false_sentinel():
    assert isinstance(vba_nothing, VBANothing)
    assert vba_nothing is vba_nothing
    assert not vba_nothing
    assert repr(vba_nothing) == "vba_nothing"
    assert vba_nothing is not None
    assert not isinstance(vba_nothing, str)


def test_com_or_nothing_unwraps_com_object():
    wrapper = MagicMock()
    wrapper.com_object = object()
    application = MagicMock()

    assert com_or_nothing(wrapper, application) is wrapper.com_object
    application.system_service.evaluate.assert_not_called()


def test_com_or_nothing_evaluates_vba_nothing():
    application = MagicMock()
    nothing_com = object()
    application.system_service.evaluate.return_value = nothing_com

    assert com_or_nothing(vba_nothing, application) is nothing_com
    application.system_service.evaluate.assert_called_once_with(
        _VBA_NOTHING,
        CatScriptLanguage.CATVBScriptLanguage,
        "N",
        [],
    )
