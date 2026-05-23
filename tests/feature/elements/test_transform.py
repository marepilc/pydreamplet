import pytest

import pydreamplet as dp


def test_transform_serializes_supported_functions():
    transforms = [
        dp.Transform.translate(10, 20),
        dp.Transform.rotate(45, 5, 6),
        dp.Transform.scale(2, 3),
        dp.Transform.skew_x(15),
        dp.Transform.skew_y(25),
        dp.Transform.matrix(1, 0, 0, 1, 10, 20),
    ]

    assert [str(transform) for transform in transforms] == [
        "translate(10 20)",
        "rotate(45,5,6)",
        "scale(2 3)",
        "skewX(15)",
        "skewY(25)",
        "matrix(1 0 0 1 10 20)",
    ]


def test_transform_list_parse_preserves_order_and_commas():
    transforms = dp.TransformList.parse(
        "translate(10, 20) skewX(15) rotate(45, 5, 6) scale(2)"
    )

    assert [transform.name for transform in transforms.transforms] == [
        "translate",
        "skewX",
        "rotate",
        "scale",
    ]
    assert str(transforms) == "translate(10 20) skewX(15) rotate(45,5,6) scale(2)"


def test_transform_list_rejects_malformed_values():
    with pytest.raises(ValueError, match="Invalid translate transform values"):
        dp.TransformList.parse("translate(foo 20)")


def test_transform_list_rejects_unsupported_functions():
    with pytest.raises(ValueError, match="Unsupported transform function"):
        dp.TransformList.parse("perspective(1)")


def test_transform_validates_arity():
    with pytest.raises(ValueError, match="matrix transform expects 6 values"):
        dp.Transform("matrix", 1, 0, 0, 1, 10)
