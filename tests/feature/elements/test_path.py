import math

import pytest

import pydreamplet as dp
from pydreamplet.path_data import (
    PathCommand,
    iter_path_segments,
    normalize_path_data,
    path_length,
    point_at_length,
    parse_path_data,
    tangent_at_length,
)


def test_path_properties():
    # Create a path for a rectangle with top-left (10, 20) and bottom-right (110, 70)
    d = "M10 20 L110 20 L110 70 L10 70 Z"
    path = dp.Path(d)
    # Width should be 100 (110 - 10) and height 50 (70 - 20)
    assert math.isclose(path.w, 100)
    assert math.isclose(path.h, 50)
    center = path.center
    # Center should be (60, 45)
    assert math.isclose(center.x, 60)
    assert math.isclose(center.y, 45)


def test_empty_path_properties():
    # With no coordinates, width and height should be 0 and center at (0,0)
    path = dp.Path("")
    assert path.w == 0
    assert path.h == 0
    center = path.center
    assert center.x == 0
    assert center.y == 0


def test_path_with_single_point():
    # A path where all coordinates are the same should have zero width/height.
    d = "M50 50 L50 50"
    path = dp.Path(d)
    assert path.w == 0
    assert path.h == 0
    center = path.center
    assert center.x == 50
    assert center.y == 50


def test_path_invalid_coordinates():
    # An odd number of coordinates should raise a ValueError
    d = "M10 20 L30"  # Missing a y coordinate for the second point.
    with pytest.raises(ValueError, match="incomplete command parameters"):
        _ = dp.Path(d).w


def test_path_relative_commands():
    path = dp.Path("M10 20 h100 v50 h-100 z")

    assert path.w == 100
    assert path.h == 50
    assert path.center == dp.Vector(60, 45)


def test_path_curve_uses_explicit_control_and_end_points():
    path = dp.Path("M0 0 C10 20 30 40 50 60")

    assert path.w == 50
    assert path.h == 60
    assert path.center == dp.Vector(25, 30)


def test_path_arc_uses_endpoint_not_radii_or_flags():
    path = dp.Path("M0 0 A50 25 0 0 1 100 10")

    assert path.w == 100
    assert path.h == 10
    assert path.center == dp.Vector(50, 5)


def test_path_repeated_move_coordinates_are_treated_as_lines():
    path = dp.Path("M10 20 110 20 110 70 10 70 Z")

    assert path.w == 100
    assert path.h == 50
    assert path.center == dp.Vector(60, 45)


def test_path_supports_scientific_notation_and_compact_negative_values():
    path = dp.Path("M1e2-5e1L.5-.25")

    assert path.w == 99.5
    assert path.h == 49.75
    assert path.center == dp.Vector(50.25, -25.125)


def test_path_smooth_and_quadratic_commands_include_control_and_end_points():
    path = dp.Path("M0 0 Q10 20 30 40 T50 60 S70 80 90 100")

    assert path.w == 90
    assert path.h == 100
    assert path.center == dp.Vector(45, 50)


def test_path_relative_arc_uses_relative_endpoint():
    path = dp.Path("M10 10 a50 25 0 0 1 100 10")

    assert path.w == 100
    assert path.h == 10
    assert path.center == dp.Vector(60, 15)


def test_path_close_command_resets_current_point_for_following_relative_commands():
    path = dp.Path("M10 10 L20 10 Z l5 5")

    assert path.w == 10
    assert path.h == 5
    assert path.center == dp.Vector(15, 12.5)


def test_path_data_must_start_with_command():
    with pytest.raises(ValueError, match="must start with a path command"):
        _ = dp.Path("10 20").w


def test_path_builder_serializes_absolute_commands():
    builder = (
        dp.PathBuilder()
        .move_to(0, 0)
        .line_to(10, 20)
        .horizontal_to(30)
        .vertical_to(40)
        .curve_to(1, 2, 3, 4, 5, 6)
        .smooth_curve_to(7, 8, 9, 10)
        .quadratic_to(11, 12, 13, 14)
        .smooth_quadratic_to(15, 16)
        .arc_to(20, 30, 0, False, True, 50, 60)
        .close()
    )

    assert builder.to_string() == (
        "M0 0 L10 20 H30 V40 C1 2 3 4 5 6 S7 8 9 10 "
        "Q11 12 13 14 T15 16 A20 30 0 0 1 50 60 Z"
    )


def test_path_builder_serializes_relative_commands():
    builder = (
        dp.PathBuilder()
        .move_to(0, 0)
        .move_by(1, 2)
        .line_by(10, 20)
        .horizontal_by(30)
        .vertical_by(40)
        .curve_by(1, 2, 3, 4, 5, 6)
        .smooth_curve_by(7, 8, 9, 10)
        .quadratic_by(11, 12, 13, 14)
        .smooth_quadratic_by(15, 16)
        .arc_by(20, 30, 0, False, True, 50, 60)
        .close()
    )

    assert builder.to_string() == (
        "M0 0 m1 2 l10 20 h30 v40 c1 2 3 4 5 6 s7 8 9 10 "
        "q11 12 13 14 t15 16 a20 30 0 0 1 50 60 Z"
    )


def test_path_builder_relative_commands_work_with_path_geometry():
    builder = (
        dp.PathBuilder()
        .move_to(10, 20)
        .line_by(100, 0)
        .vertical_by(50)
        .horizontal_by(-100)
        .close()
    )

    path = dp.Path(builder)

    assert path.d == "M10 20 l100 0 v50 h-100 Z"
    assert path.w == 100
    assert path.h == 50
    assert path.center == dp.Vector(60, 45)


def test_path_accepts_path_builder():
    builder = (
        dp.PathBuilder()
        .move_to(10, 20)
        .line_to(110, 20)
        .line_to(110, 70)
        .close()
    )

    path = dp.Path(builder, fill="none")

    assert path.d == "M10 20 L110 20 L110 70 Z"
    assert path.w == 100
    assert path.h == 50
    assert path.fill == "none"


def test_path_d_setter_accepts_path_builder():
    path = dp.Path()

    path.d = dp.PathBuilder().move_to(0, 0).arc_to(10, 10, 0, 1, 0, 20, 20)

    assert path.d == "M0 0 A10 10 0 1 0 20 20"


def test_parse_path_data_returns_structured_commands():
    commands = parse_path_data("M10 20 30 40 h5 z")

    assert commands == [
        PathCommand("M", (10, 20)),
        PathCommand("L", (30, 40)),
        PathCommand("h", (5,)),
        PathCommand("z", ()),
    ]


def test_normalize_path_data_converts_relative_commands_to_absolute():
    normalized = normalize_path_data(
        "M10 20 l100 0 v50 h-100 c1 2 3 4 5 6 "
        "s7 8 9 10 q11 12 13 14 t15 16 a20 30 0 0 1 50 60 z"
    )

    assert normalized == (
        "M10 20 L110 20 V70 H10 C11 72 13 74 15 76 "
        "S22 84 24 86 Q35 98 37 100 T52 116 A20 30 0 0 1 102 176 Z"
    )


def test_normalize_path_data_keeps_absolute_commands_absolute():
    normalized = normalize_path_data("M10 20 L30 40 H50 V60 A5 6 0 1 0 70 80 Z")

    assert normalized == "M10 20 L30 40 H50 V60 A5 6 0 1 0 70 80 Z"


def test_normalize_path_data_resets_current_point_after_close():
    normalized = normalize_path_data("M10 10 L20 10 Z l5 5")

    assert normalized == "M10 10 L20 10 Z L15 15"


def test_iter_path_segments_returns_linear_segments():
    segments = iter_path_segments("M0 0 L3 4 H10 V10 Z")

    assert [segment.command for segment in segments] == ["L", "H", "V", "Z"]
    assert [segment.start for segment in segments] == [
        dp.Vector(0, 0),
        dp.Vector(3, 4),
        dp.Vector(10, 4),
        dp.Vector(10, 10),
    ]
    assert [segment.end for segment in segments] == [
        dp.Vector(3, 4),
        dp.Vector(10, 4),
        dp.Vector(10, 10),
        dp.Vector(0, 0),
    ]


def test_path_length_measures_linear_commands():
    assert path_length("M0 0 L3 4 H10 V10") == 18


def test_path_length_measures_relative_commands_after_normalization():
    assert path_length("M10 20 h100 v50 h-100 z") == 300


def test_point_at_length_clamps_to_path_extents():
    path_data = "M0 0 L10 0 L10 10"

    assert point_at_length(path_data, -5) == dp.Vector(0, 0)
    assert point_at_length(path_data, 5) == dp.Vector(5, 0)
    assert point_at_length(path_data, 15) == dp.Vector(10, 5)
    assert point_at_length(path_data, 30) == dp.Vector(10, 10)


def test_tangent_at_length_returns_unit_direction():
    path_data = "M0 0 L10 0 L10 10"

    assert tangent_at_length(path_data, 5) == dp.Vector(1, 0)
    assert tangent_at_length(path_data, 15) == dp.Vector(0, 1)
    assert tangent_at_length(path_data, 30) == dp.Vector(0, 1)


def test_path_measurement_rejects_curves_and_arcs_for_now():
    with pytest.raises(ValueError, match="only supports linear commands"):
        path_length("M0 0 C10 20 30 40 50 60")

    with pytest.raises(ValueError, match="only supports linear commands"):
        path_length("M0 0 A10 10 0 0 1 20 20")


def test_path_element_exposes_linear_measurement_helpers():
    path = dp.Path("M0 0 L10 0 L10 10")

    assert path.length == 20
    assert path.point_at(15) == dp.Vector(10, 5)
    assert path.tangent_at(15) == dp.Vector(0, 1)
