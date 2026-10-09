from pyv5.base.com_out import ComMethodCache, OutDispatchInvoker, call_with_out_dispatch


class _FakeOle:
    def __init__(self, created):
        self.created = created
        self.calls = []

    def GetIDsOfNames(self, lcid, name):
        assert lcid == 0
        return 42

    def Invoke(self, dispid, lcid, flags, want_result, *args):
        self.calls.append((dispid, args))
        if args:
            out = args[-1]
            if hasattr(out, "value"):
                out.value = self.created
                return None
        return self.created


class _FakeCom:
    def __init__(self, created):
        self._oleobj_ = _FakeOle(created)


def test_call_with_out_dispatch_reads_variant_value():
    sentinel = object()
    com = _FakeCom(sentinel)
    assert call_with_out_dispatch(com, "CreateTagGroup", "name", False) is sentinel
    assert com._oleobj_.calls[0][0] == 42


def test_out_dispatch_invoker_reuses_working_variant_type():
    sentinel = object()
    com = _FakeCom(sentinel)
    invoker = OutDispatchInvoker(com)
    assert invoker.create("CreateTag") is sentinel
    assert invoker.create("CreateTag") is sentinel
    assert invoker._out_type is not None
    assert len(com._oleobj_.calls) == 2


def test_com_method_cache_resolves_dispid_once():
    ole = _FakeOle(None)

    class Tag:
        _oleobj_ = ole

    cache = ComMethodCache()
    cache.call(Tag(), "SetXYZ", 1.0, 2.0, 3.0)
    cache.call(Tag(), "SetXYZ", 4.0, 5.0, 6.0)
    assert cache._dispids["SetXYZ"] == 42
    assert len(ole.calls) == 2


def test_call_with_out_dispatch_uses_method_return_if_variant_empty():
    sentinel = object()

    class Ole(_FakeOle):
        def Invoke(self, dispid, lcid, flags, want_result, *args):
            return sentinel

    com = _FakeCom(None)
    com._oleobj_ = Ole(None)
    assert call_with_out_dispatch(com, "CreateTag") is sentinel
