import math

import pytest

import pydreamplet as dp


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
