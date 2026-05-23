import pytest

import pydreamplet as dp


def assert_matrix_close(
    matrix: dp.Matrix2D,
    expected: tuple[float, float, float, float, float, float],
):
    assert matrix.as_tuple() == pytest.approx(expected)


def test_matrix2d_multiply_and_apply():
    matrix = dp.Matrix2D.translate(10, 20).multiply(dp.Matrix2D.scale(2, 3))

    assert_matrix_close(matrix, (2, 0, 0, 3, 10, 20))
    assert matrix.apply(5, 6) == dp.Vector(20, 38)
    assert str(matrix) == "matrix(2 0 0 3 10 20)"


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


def test_transform_to_matrix_for_basic_functions():
    assert_matrix_close(dp.Transform.translate(10, 20).to_matrix(), (1, 0, 0, 1, 10, 20))
    assert_matrix_close(dp.Transform.scale(2, 3).to_matrix(), (2, 0, 0, 3, 0, 0))
    assert_matrix_close(dp.Transform.rotate(90).to_matrix(), (0, 1, -1, 0, 0, 0))
    assert_matrix_close(dp.Transform.skew_x(45).to_matrix(), (1, 0, 1, 1, 0, 0))
    assert_matrix_close(dp.Transform.skew_y(45).to_matrix(), (1, 1, 0, 1, 0, 0))


def test_transform_to_matrix_for_rotate_around_point():
    matrix = dp.Transform.rotate(90, 10, 20).to_matrix()

    assert_matrix_close(matrix, (0, 1, -1, 0, 30, 10))
    assert matrix.apply(10, 20) == dp.Vector(10, 20)


def test_transform_list_to_matrix_composes_in_svg_order():
    transforms = dp.TransformList.parse("translate(10 20) rotate(90) scale(2)")
    matrix = transforms.to_matrix()

    assert_matrix_close(matrix, (0, 2, -2, 0, 10, 20))
    assert matrix.apply(1, 0) == dp.Vector(10, 22)
