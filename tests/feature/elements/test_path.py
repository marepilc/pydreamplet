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
    with pytest.raises(ValueError):
        _ = dp.Path(d).w
