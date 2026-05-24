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


def test_empty_path_bbox():
    assert dp.Path("").bbox == dp.BoundingBox(0, 0, 0, 0)


def test_path_bbox_raises_for_non_linear_commands():
    with pytest.raises(ValueError, match="linear commands"):
        _ = dp.Path("M0 0 C10 20 30 40 50 60").bbox
