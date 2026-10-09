import logging
from types import SimpleNamespace
from unittest.mock import MagicMock

from pywintypes import com_error

from pyv5.interfaces.dnb_igp_setup.tag_batch import (
    TagPlacement,
    add_tags_to_group,
    as_placements,
    create_tag_group_with_tags,
    placement_arrays,
    quiet_application,
    should_create_in_process,
)


def _placements(count: int) -> list[TagPlacement]:
    return [
        TagPlacement(name=f"T{i:04d}", x=float(i), y=0.0, z=0.0, type="Manufacturing")
        for i in range(1, count + 1)
    ]


def _factory(application) -> SimpleNamespace:
    return SimpleNamespace(
        com_object=object(),
        tag_group_factory=object(),
        application=application,
        logger=logging.getLogger("pyv5.test.tag_batch"),
    )


def test_placement_arrays_match_tag_count():
    tags = _placements(3)
    names, xs, ys, zs, yaws, pitches, rolls, types = placement_arrays(tags)
    assert names == ["T0001", "T0002", "T0003"]
    assert xs == [1.0, 2.0, 3.0]
    assert types == ["Manufacturing"] * 3
    assert yaws == [0.0, 0.0, 0.0]


def test_as_placements_accepts_duck_typed_samples():
    sample = SimpleNamespace(
        name="T0001", x=1, y=2, z=3, yaw=0.1, pitch=0.0, roll=0.0, tag_type="Design"
    )
    placed = as_placements([sample])[0]
    assert placed.name == "T0001"
    assert placed.x == 1.0
    assert placed.type == "Design"


def test_should_create_in_process_threshold():
    assert should_create_in_process(0) is False
    assert should_create_in_process(1) is False
    assert should_create_in_process(2) is True


def test_quiet_application_restores_flags():
    app = SimpleNamespace(refresh_display=True, interactive=True)
    with quiet_application(app):
        assert app.refresh_display is False
        assert app.interactive is False
    assert app.refresh_display is True
    assert app.interactive is True


def test_create_tag_group_uses_evaluate_for_many_tags(monkeypatch):
    created = object()
    evaluate = MagicMock(return_value=created)
    com_group = MagicMock()
    monkeypatch.setattr(
        "pyv5.interfaces.dnb_igp_setup.tag_batch.evaluate_vbs", evaluate
    )
    monkeypatch.setattr(
        "pyv5.interfaces.dnb_igp_setup.tag_batch.create_tag_group_com",
        MagicMock(return_value=com_group),
    )
    monkeypatch.setattr(
        "pyv5.interfaces.dnb_igp_setup.tag_batch.create_tags_via_com", MagicMock()
    )
    wrap = MagicMock(side_effect=lambda value: value)
    monkeypatch.setattr("pyv5.interfaces.dnb_igp_setup.tag_batch._wrap_tag_group", wrap)

    app = SimpleNamespace(refresh_display=True, interactive=True)
    product = SimpleNamespace(com_object=object())
    result = create_tag_group_with_tags(
        _factory(app), "EngroTec_Consulting", False, product, _placements(2)
    )

    assert result is created
    evaluate.assert_called_once()
    assert evaluate.call_args.args[2] == "create_tag_group_and_tags"
    assert app.refresh_display is True


def test_create_tag_group_uses_com_for_one_tag(monkeypatch):
    evaluate = MagicMock()
    com_group = object()
    monkeypatch.setattr(
        "pyv5.interfaces.dnb_igp_setup.tag_batch.evaluate_vbs", evaluate
    )
    monkeypatch.setattr(
        "pyv5.interfaces.dnb_igp_setup.tag_batch.create_tag_group_com",
        MagicMock(return_value=com_group),
    )
    via_com = MagicMock()
    monkeypatch.setattr(
        "pyv5.interfaces.dnb_igp_setup.tag_batch.create_tags_via_com", via_com
    )

    app = SimpleNamespace(refresh_display=True, interactive=True)
    product = SimpleNamespace(com_object=object())
    result = create_tag_group_with_tags(
        _factory(app), "G", False, product, _placements(1)
    )

    assert result is com_group
    evaluate.assert_not_called()
    via_com.assert_called_once()


def test_create_tag_group_falls_back_to_com_on_evaluate_error(monkeypatch):
    monkeypatch.setattr(
        "pyv5.interfaces.dnb_igp_setup.tag_batch.evaluate_vbs",
        MagicMock(side_effect=com_error("fail")),
    )
    com_group = object()
    monkeypatch.setattr(
        "pyv5.interfaces.dnb_igp_setup.tag_batch.create_tag_group_com",
        MagicMock(return_value=com_group),
    )
    via_com = MagicMock()
    monkeypatch.setattr(
        "pyv5.interfaces.dnb_igp_setup.tag_batch.create_tags_via_com", via_com
    )

    app = SimpleNamespace(refresh_display=True, interactive=True)
    product = SimpleNamespace(com_object=object())
    result = create_tag_group_with_tags(
        _factory(app), "G", False, product, _placements(5)
    )

    assert result is com_group
    via_com.assert_called_once()


def test_add_tags_looks_up_group_by_name(monkeypatch):
    evaluate = MagicMock(return_value=object())
    via_com = MagicMock()
    monkeypatch.setattr(
        "pyv5.interfaces.dnb_igp_setup.tag_batch.evaluate_vbs", evaluate
    )
    monkeypatch.setattr(
        "pyv5.interfaces.dnb_igp_setup.tag_batch.create_tags_via_com", via_com
    )

    app = SimpleNamespace(refresh_display=True, interactive=True)
    tag_group = SimpleNamespace(
        com_object=object(),
        application=app,
        logger=logging.getLogger("pyv5.test.tag_batch"),
        name="EngroTec_Consulting",
    )
    product = SimpleNamespace(com_object=object())
    add_tags_to_group(tag_group, _placements(2), product)

    evaluate.assert_called_once()
    assert evaluate.call_args.args[2] == "add_tags_to_named_group"
    assert evaluate.call_args.args[3][1] == "EngroTec_Consulting"
    via_com.assert_not_called()


def test_add_tags_empty_is_noop(monkeypatch):
    evaluate = MagicMock()
    monkeypatch.setattr(
        "pyv5.interfaces.dnb_igp_setup.tag_batch.evaluate_vbs", evaluate
    )
    add_tags_to_group(SimpleNamespace(), [])
    evaluate.assert_not_called()


def test_tag_group_factory_create_tag_group_without_tags_uses_com(monkeypatch):
    from pyv5.interfaces.dnb_igp_setup.tag_group_factory import TagGroupFactory

    com_group = object()
    create_com = MagicMock(return_value=com_group)
    create_with = MagicMock()
    monkeypatch.setattr(
        "pyv5.interfaces.dnb_igp_setup.tag_batch.create_tag_group_com", create_com
    )
    monkeypatch.setattr(
        "pyv5.interfaces.dnb_igp_setup.tag_batch.create_tag_group_with_tags",
        create_with,
    )

    factory = TagGroupFactory.__new__(TagGroupFactory)
    product = SimpleNamespace(com_object=object())
    assert factory.create_tag_group("G", False, product) is com_group
    create_com.assert_called_once()
    create_with.assert_not_called()


def test_tag_group_factory_create_tag_group_with_tags_batches(monkeypatch):
    from pyv5.interfaces.dnb_igp_setup.tag_group_factory import TagGroupFactory

    batched = object()
    create_with = MagicMock(return_value=batched)
    monkeypatch.setattr(
        "pyv5.interfaces.dnb_igp_setup.tag_batch.create_tag_group_with_tags",
        create_with,
    )

    factory = TagGroupFactory.__new__(TagGroupFactory)
    product = SimpleNamespace(com_object=object())
    tags = _placements(2)
    assert factory.create_tag_group("G", False, product, tags=tags) is batched
    create_with.assert_called_once()
