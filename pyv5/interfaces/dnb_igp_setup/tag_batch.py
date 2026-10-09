"""Create many DELMIA tags using the faster of in-process VBScript or COM.

Python and CATIA are separate processes. Each ``CreateTag`` / ``SetXYZ`` call is
an out-of-process round trip, and DELMIA rebuilds the tag on every call.
``SystemService.Evaluate`` runs the loop inside CATIA. That is faster once more
than one tag is created.

Passing a ``TagGroup`` created in Python back into Evaluate fails (E_FAIL).
New groups are created in the same script as their tags. Tags added to an
existing group are looked up by product and group name, not by TagGroup COM.
"""

from __future__ import annotations

import time
from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any

from pywintypes import com_error

from pyv5.base.com_out import ComMethodCache, OutDispatchInvoker, call_with_out_dispatch
from pyv5.base.enums import CatScriptLanguage

# Evaluate has a fixed marshalling cost; one tag is cheaper as a COM call.
INPROCESS_MIN_TAGS = 2

_CREATE_GROUP_AND_TAGS_VBS = """
Function create_tag_group_and_tags(factory, groupName, modifyRef, prod, names, xs, ys, zs, yaws, pitches, rolls, types, n)
    Dim oTagGroup, i, oTag, base, idx, probe, tagType
    factory.CreateTagGroup groupName, modifyRef, prod, oTagGroup
    base = 0
    On Error Resume Next
    Err.Clear
    probe = names(0)
    If Err.Number <> 0 Then
        Err.Clear
        base = 1
    End If
    On Error GoTo 0
    For i = 0 To n - 1
        idx = base + i
        oTagGroup.CreateTag oTag
        oTag.SetName CStr(names(idx))
        oTag.SetXYZ xs(idx), ys(idx), zs(idx)
        oTag.SetYPR yaws(idx), pitches(idx), rolls(idx)
        tagType = CStr(types(idx))
        If Len(tagType) > 0 Then
            oTag.SetType tagType
        End If
    Next
    Set create_tag_group_and_tags = oTagGroup
End Function
"""

_ADD_TAGS_TO_NAMED_GROUP_VBS = """
Function add_tags_to_named_group(prod, groupName, names, xs, ys, zs, yaws, pitches, rolls, types, n)
    Dim oTagGroup, i, oTag, base, idx, probe, tagType
    On Error Resume Next
    Err.Clear
    Set oTagGroup = prod.GetItem(groupName)
    If Err.Number <> 0 Then
        Err.Clear
        Set oTagGroup = prod.GetTechnologicalObject(groupName)
    End If
    If Err.Number <> 0 Then
        Err.Clear
        Set oTagGroup = prod.GetTechnologicalObject("TagGroup")
    End If
    On Error GoTo 0
    If oTagGroup Is Nothing Then
        Err.Raise 5, , "TagGroup not found"
    End If
    base = 0
    On Error Resume Next
    Err.Clear
    probe = names(0)
    If Err.Number <> 0 Then
        Err.Clear
        base = 1
    End If
    On Error GoTo 0
    For i = 0 To n - 1
        idx = base + i
        oTagGroup.CreateTag oTag
        oTag.SetName CStr(names(idx))
        oTag.SetXYZ xs(idx), ys(idx), zs(idx)
        oTag.SetYPR yaws(idx), pitches(idx), rolls(idx)
        tagType = CStr(types(idx))
        If Len(tagType) > 0 Then
            oTag.SetType tagType
        End If
    Next
    Set add_tags_to_named_group = oTagGroup
End Function
"""


@dataclass(frozen=True)
class TagPlacement:
    """Pose and name used to create one Tag."""

    name: str
    x: float
    y: float
    z: float
    yaw: float = 0.0
    pitch: float = 0.0
    roll: float = 0.0
    type: str = ""

    @classmethod
    def from_obj(cls, obj: Any) -> TagPlacement:
        if isinstance(obj, TagPlacement):
            return obj
        tag_type = getattr(obj, "type", None) or getattr(obj, "tag_type", "") or ""
        return cls(
            name=obj.name,
            x=float(obj.x),
            y=float(obj.y),
            z=float(obj.z),
            yaw=float(getattr(obj, "yaw", 0.0) or 0.0),
            pitch=float(getattr(obj, "pitch", 0.0) or 0.0),
            roll=float(getattr(obj, "roll", 0.0) or 0.0),
            type=str(tag_type),
        )


def as_placements(tags: Sequence[Any]) -> list[TagPlacement]:
    return [TagPlacement.from_obj(tag) for tag in tags]


def placement_arrays(tags: Sequence[TagPlacement]) -> list:
    """Pack placements into parallel lists for ``SystemService.Evaluate``."""
    return [
        [tag.name for tag in tags],
        [tag.x for tag in tags],
        [tag.y for tag in tags],
        [tag.z for tag in tags],
        [tag.yaw for tag in tags],
        [tag.pitch for tag in tags],
        [tag.roll for tag in tags],
        [tag.type for tag in tags],
    ]


def should_create_in_process(count: int) -> bool:
    return count >= INPROCESS_MIN_TAGS


@contextmanager
def quiet_application(application: Any) -> Iterator[None]:
    """Skip redraw and UI while creating many tags."""
    if application is None:
        yield
        return
    refresh = application.refresh_display
    interactive = application.interactive
    try:
        application.refresh_display = False
        application.interactive = False
        yield
    finally:
        application.interactive = interactive
        application.refresh_display = refresh


def evaluate_vbs(application: Any, script: str, function_name: str, args: list) -> Any:
    return application.system_service.evaluate(
        script.strip(),
        CatScriptLanguage.CATVBScriptLanguage,
        function_name,
        args,
    )


def create_tag_group_com(
    factory: Any, name: str, modify_reference: bool, product: Any
) -> Any:
    from pyv5.interfaces.dnb_igp_setup.tag_group import TagGroup

    return TagGroup(
        call_with_out_dispatch(
            factory.tag_group_factory,
            "CreateTagGroup",
            name,
            modify_reference,
            product.com_object,
        )
    )


def create_tags_via_com(tag_group: Any, tags: Sequence[TagPlacement]) -> None:
    creator = OutDispatchInvoker(tag_group.com_object)
    setters = ComMethodCache()
    for tag in tags:
        created = creator.create("CreateTag")
        setters.call(created, "SetName", tag.name)
        setters.call(created, "SetXYZ", tag.x, tag.y, tag.z)
        setters.call(created, "SetYPR", tag.yaw, tag.pitch, tag.roll)
        if tag.type:
            setters.call(created, "SetType", tag.type)


def _parent_product(tag_group: Any) -> Any | None:
    from pyv5.interfaces.product_structure.product import Product

    try:
        parent = tag_group.com_object.Parent
    except (AttributeError, com_error):
        return None
    if parent is None:
        return None
    try:
        return Product(parent)
    except (TypeError, ValueError, com_error):
        return None


def _wrap_tag_group(created: Any) -> Any:
    from pyv5.interfaces.dnb_igp_setup.tag_group import TagGroup

    return TagGroup(created)


def create_tag_group_with_tags(
    factory: Any,
    name: str,
    modify_reference: bool,
    product: Any,
    tags: Sequence[Any],
) -> Any:
    """Create a TagGroup and its tags, using in-process Evaluate when faster."""
    placements = as_placements(tags)
    application = factory.application
    logger = factory.logger
    started = time.perf_counter()
    used = "com"
    tag_group = None
    with quiet_application(application):
        if should_create_in_process(len(placements)):
            try:
                names, xs, ys, zs, yaws, pitches, rolls, types = placement_arrays(
                    placements
                )
                created = evaluate_vbs(
                    application,
                    _CREATE_GROUP_AND_TAGS_VBS,
                    "create_tag_group_and_tags",
                    [
                        factory.com_object,
                        name,
                        modify_reference,
                        product.com_object,
                        names,
                        xs,
                        ys,
                        zs,
                        yaws,
                        pitches,
                        rolls,
                        types,
                        len(placements),
                    ],
                )
                tag_group = _wrap_tag_group(created)
                used = "in-process"
            except com_error as exc:
                logger.warning(
                    "In-process tag creation failed (%s); falling back to per-tag "
                    "COM calls.",
                    exc,
                )
        if tag_group is None:
            tag_group = create_tag_group_com(factory, name, modify_reference, product)
            create_tags_via_com(tag_group, placements)
            used = "com"
    logger.info(
        "Created %s tags in TagGroup '%s' in %.2fs (%s).",
        len(placements),
        name,
        time.perf_counter() - started,
        used,
    )
    return tag_group


def add_tags_to_group(
    tag_group: Any, tags: Sequence[Any], product: Any | None = None
) -> None:
    """Add tags to an existing TagGroup, using in-process Evaluate when faster."""
    placements = as_placements(tags)
    if not placements:
        return
    if product is None:
        product = _parent_product(tag_group)
    application = tag_group.application
    logger = tag_group.logger
    started = time.perf_counter()
    used = "com"
    with quiet_application(application):
        if should_create_in_process(len(placements)) and product is not None:
            try:
                names, xs, ys, zs, yaws, pitches, rolls, types = placement_arrays(
                    placements
                )
                evaluate_vbs(
                    application,
                    _ADD_TAGS_TO_NAMED_GROUP_VBS,
                    "add_tags_to_named_group",
                    [
                        product.com_object,
                        tag_group.name,
                        names,
                        xs,
                        ys,
                        zs,
                        yaws,
                        pitches,
                        rolls,
                        types,
                        len(placements),
                    ],
                )
                used = "in-process"
            except com_error as exc:
                logger.warning(
                    "In-process tag creation failed (%s); falling back to per-tag "
                    "COM calls.",
                    exc,
                )
                create_tags_via_com(tag_group, placements)
                used = "com"
        else:
            create_tags_via_com(tag_group, placements)
            used = "com"
    logger.info(
        "Created %s tags in TagGroup '%s' in %.2fs (%s).",
        len(placements),
        getattr(tag_group, "name", ""),
        time.perf_counter() - started,
        used,
    )
