"""CATIA VBA ``Nothing`` for optional COM object arguments.

Python ``None`` does not marshal as VBA ``Nothing`` (a null ``IDispatch``).
CATIA methods that take an optional object (axis, closing point, tangency,
and similar) expect that COM value and fail if they receive ``None``.

Pass :data:`vba_nothing` at those call sites. Wrappers convert it with
:func:`com_or_nothing`, which asks CATIA to evaluate a one-line VBScript
function that returns ``Nothing``.
"""

from __future__ import annotations

from typing import Any

_VBA_NOTHING = "Function N()\n    Set N = Nothing\nEnd Function\n"


class VBANothing:
    """Sentinel for an omitted CATIA object argument (VBA ``Nothing``).

    Compare with identity: ``value is vba_nothing``. Do not instantiate.
    """

    __slots__ = ()

    def __repr__(self) -> str:
        return "vba_nothing"

    def __bool__(self) -> bool:
        return False


vba_nothing = VBANothing()


def com_or_nothing(value: Any, application: Any) -> Any:
    """Return ``value.com_object``, or CATIA's VBA ``Nothing``.

    :param value: A pyv5 wrapper with ``com_object``, or :data:`vba_nothing`.
    :param application: The CATIA :class:`~pyv5.interfaces.core.application.Application`.
    """
    if value is vba_nothing:
        from pyv5.interfaces.enums import CatScriptLanguage

        return application.system_service.evaluate(
            _VBA_NOTHING,
            CatScriptLanguage.CATVBScriptLanguage,
            "N",
            [],
        )
    return value.com_object
