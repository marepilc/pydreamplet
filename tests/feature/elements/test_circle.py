import pytest

import pydreamplet as dp


def test_circle_pos():
    circle = dp.Circle(cx=10, cy=20, r=5)
    assert circle.pos.x == 10
    assert circle.pos.y == 20
    circle.pos = dp.Vector(20, 30)
    assert circle.cx == 20
    assert circle.cy == 30
    circle.attrs({"cx": 0, "cy": 0})
    assert circle.pos.x == 0
    assert circle.pos.y == 0


def test_circle_pos_constructor_does_not_emit_pos_attribute():
    circle = dp.Circle(pos=dp.Vector(10, 20), r=5)

    assert circle.pos.x == 10
    assert circle.pos.y == 20
    assert circle.element.attrib["cx"] == "10.0"
    assert circle.element.attrib["cy"] == "20.0"
    assert "pos=" not in str(circle)


def test_circle_accepts_tuple_pos_and_typed_constructor_args():
    circle = dp.Circle(pos=(10, 20), r=5, fill="red")

    assert circle.pos == dp.Vector(10, 20)
    assert circle.radius == 5
    assert circle.element.attrib["fill"] == "red"


def test_circle_pos_setter_accepts_point_like_values():
    circle = dp.Circle(r=5)

    circle.pos = [10, 20]

    assert circle.pos == dp.Vector(10, 20)


def test_circle_area():
    circle = dp.Circle(cx=10, cy=20, r=5)
    assert circle.area == pytest.approx(78.54, 0.01)
    circle.r = 10
    assert circle.area == pytest.approx(314.16, 0.01)


def test_circle_numeric_properties_support_arithmetic_and_setters():
    circle = dp.Circle(cx=80, cy=40, r=12)

    assert circle.cx + circle.radius + 10 == 102
    assert circle.cy + circle.r == 52

    circle.cx = 90
    circle.cy = 50
    circle.radius = 14

    assert circle.pos == dp.Vector(90, 50)
    assert circle.r == 14
    assert circle.element.attrib["cx"] == "90"
    assert circle.element.attrib["cy"] == "50"
    assert circle.element.attrib["r"] == "14"
