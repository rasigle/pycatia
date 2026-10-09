"""Helpers for CATIA/DELMIA COM methods with ``[out] IDispatch`` arguments."""

from __future__ import annotations

from typing import Any

from pywintypes import com_error


def _oleobj(com_object: Any) -> Any:
    return getattr(com_object, "_oleobj_", com_object)


def _dispid(oleobj: Any, method_name: str) -> int:
    dispid = oleobj.GetIDsOfNames(0, method_name)
    if isinstance(dispid, (tuple, list)):
        return dispid[0]
    return dispid


def _as_dispatch(value: Any) -> Any:
    from win32com.client import Dispatch

    try:
        return Dispatch(value)
    except (TypeError, ValueError, AttributeError, com_error):
        return value


class OutDispatchInvoker:
    """Create many objects on one COM factory without repeating type lookup.

    Dispids and the working ByRef VARIANT type are resolved on the first
    successful call and reused.
    """

    def __init__(self, com_object: Any):
        self._ole = _oleobj(com_object)
        self._dispids: dict[str, int] = {}
        self._out_type: int | None = None

    def _dispid_of(self, method_name: str) -> int:
        dispid = self._dispids.get(method_name)
        if dispid is None:
            dispid = _dispid(self._ole, method_name)
            self._dispids[method_name] = dispid
        return dispid

    def create(self, method_name: str, *args: Any) -> Any:
        import pythoncom
        from win32com.client import VARIANT

        dispid = self._dispid_of(method_name)
        flags = pythoncom.DISPATCH_METHOD
        types = (
            (self._out_type,)
            if self._out_type is not None
            else (
                pythoncom.VT_DISPATCH | pythoncom.VT_BYREF,
                pythoncom.VT_VARIANT | pythoncom.VT_BYREF,
                pythoncom.VT_UNKNOWN | pythoncom.VT_BYREF,
            )
        )
        errors: list[BaseException] = []
        for vartype in types:
            if vartype is None:
                continue
            out = VARIANT(vartype, None)
            try:
                result = self._ole.Invoke(dispid, 0, flags, True, *args, out)
            except (TypeError, ValueError, com_error) as exc:
                errors.append(exc)
                continue
            value = getattr(out, "value", None)
            if value is not None:
                self._out_type = vartype
                return value
            if result is not None and not isinstance(result, (int, bool)):
                self._out_type = vartype
                return result
        if errors:
            raise errors[-1]
        raise RuntimeError(
            f"{method_name!r} did not return a COM object on the output argument"
        )


class ComMethodCache:
    """Cache method dispids shared by all instances of one COM coclass."""

    def __init__(self) -> None:
        self._dispids: dict[str, int] = {}

    def call(self, com_object: Any, method_name: str, *args: Any) -> Any:
        import pythoncom

        ole = _oleobj(com_object)
        dispid = self._dispids.get(method_name)
        if dispid is None:
            dispid = _dispid(ole, method_name)
            self._dispids[method_name] = dispid
        return ole.Invoke(dispid, 0, pythoncom.DISPATCH_METHOD, False, *args)


def call_with_out_dispatch(com_object: Any, method_name: str, *args: Any) -> Any:
    """Call a V5 ``Sub`` that creates an object via an ``[out]`` argument.

    win32com late binding uses ``InvokeTypes``, which tries to convert the
    output argument to an ``IDispatch`` and raises
    ``TypeError: The Python instance can not be converted to a COM object``.
    This helper calls ``IDispatch.Invoke`` with a ByRef VARIANT instead.
    """
    created = OutDispatchInvoker(com_object).create(method_name, *args)
    return _as_dispatch(created)
