import pytest

import pydreamplet as dp


def test_bounding_box_properties():
    bbox = dp.BoundingBox(10, 20, 30, 40)

    assert bbox.left == 10
    assert bbox.top == 20
    assert bbox.right == 40
    assert bbox.bottom == 60
    assert bbox.center == dp.Vector(25, 40)


def test_circle_bbox():
    circle = dp.Circle(pos=(10, 20), r=5)

    assert circle.bbox == dp.BoundingBox(5, 15, 10, 10)


def test_ellipse_bbox():
    ellipse = dp.Ellipse(pos=(10, 20), rx=5, ry=8)

    assert ellipse.bbox == dp.BoundingBox(5, 12, 10, 16)


def test_rect_bbox():
    rect = dp.Rect(pos=(10, 20), width=30, height=40)

    assert rect.bbox == dp.BoundingBox(10, 20, 30, 40)


def test_rect_bbox_normalizes_negative_dimensions():
    rect = dp.Rect(x=10, y=20, width=-30, height=-40)

    assert rect.bbox == dp.BoundingBox(-20, -20, 30, 40)


def test_line_bbox():
    line = dp.Line(10, 20, -5, 40)

    assert line.bbox == dp.BoundingBox(-5, 20, 15, 20)


def test_polygon_bbox():
    polygon = dp.Polygon(points=[0, 0, 10, 20, -5, 8])

    assert polygon.bbox == dp.BoundingBox(-5, 0, 15, 20)


def test_polyline_bbox():
    polyline = dp.Polyline(points=[0, 0, 10, 20, -5, 8])

    assert polyline.bbox == dp.BoundingBox(-5, 0, 15, 20)


def test_empty_polygon_and_polyline_bbox():
    assert dp.Polygon(points=[]).bbox == dp.BoundingBox(0, 0, 0, 0)
    assert dp.Polyline(points=[]).bbox == dp.BoundingBox(0, 0, 0, 0)


def test_odd_points_bbox_raises_value_error():
    with pytest.raises(ValueError, match="even number"):
        dp.Polygon(points=[0, 0, 10])


def test_linear_path_bbox_supports_relative_commands():
    path = dp.Path("M10 20 h100 v50 h-100 z")

    assert path.bbox == dp.BoundingBox(10, 20, 100, 50)


def test_quadratic_path_bbox_includes_curve_extrema():
    path = dp.Path("M0 0 Q50 100 100 0")

    assert path.bbox == dp.BoundingBox(0, 0, 100, 50)


def test_smooth_quadratic_path_bbox_reflects_previous_control_point():
    path = dp.Path("M0 0 Q50 100 100 0 T200 0")

    assert path.bbox == dp.BoundingBox(0, -50, 200, 100)


def test_cubic_path_bbox_includes_curve_extrema():
    path = dp.Path("M0 0 C0 100 100 100 100 0")

    assert path.bbox.x == pytest.approx(0)
    assert path.bbox.y == pytest.approx(0)
    assert path.bbox.width == pytest.approx(100)
    assert path.bbox.height == pytest.approx(75)


def test_smooth_cubic_path_bbox_reflects_previous_control_point():
    path = dp.Path("M0 0 C0 100 100 100 100 0 S200 -100 200 0")

    assert path.bbox.x == pytest.approx(0)
    assert path.bbox.y == pytest.approx(-75)
    assert path.bbox.width == pytest.approx(200)
    assert path.bbox.height == pytest.approx(150)


def test_empty_path_bbox():
    assert dp.Path("").bbox == dp.BoundingBox(0, 0, 0, 0)


def test_arc_path_bbox_for_sweep_direction():
    clockwise = dp.Path("M10 0 A10 10 0 0 1 -10 0")
    counter_clockwise = dp.Path("M10 0 A10 10 0 0 0 -10 0")

    assert clockwise.bbox == dp.BoundingBox(-10, 0, 20, 10)
    assert counter_clockwise.bbox.x == pytest.approx(-10)
    assert counter_clockwise.bbox.y == pytest.approx(-10)
    assert counter_clockwise.bbox.width == pytest.approx(20)
    assert counter_clockwise.bbox.height == pytest.approx(10)


def test_large_arc_path_bbox_includes_axis_extrema():
    path = dp.Path("M10 0 A10 10 0 1 1 0 -10")

    assert path.bbox == dp.BoundingBox(-10, -10, 20, 20)


def test_arc_path_bbox_scales_too_small_radii():
    path = dp.Path("M0 0 A1 1 0 0 1 10 0")

    assert path.bbox.x == pytest.approx(0)
    assert path.bbox.y == pytest.approx(-5)
    assert path.bbox.width == pytest.approx(10)
    assert path.bbox.height == pytest.approx(5)


def test_rotated_ellipse_arc_path_bbox():
    path = dp.Path("M10 0 A20 10 90 0 1 -10 0")

    assert path.bbox.x == pytest.approx(-10)
    assert path.bbox.y == pytest.approx(0)
    assert path.bbox.width == pytest.approx(20)
    assert path.bbox.height == pytest.approx(20)


def test_zero_radius_arc_path_bbox_falls_back_to_line_endpoint():
    path = dp.Path("M0 0 A0 10 0 0 1 20 30")

    assert path.bbox == dp.BoundingBox(0, 0, 20, 30)
