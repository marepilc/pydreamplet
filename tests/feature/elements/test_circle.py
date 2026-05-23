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


def test_circle_area():
    circle = dp.Circle(cx=10, cy=20, r=5)
    assert circle.area == pytest.approx(78.54, 0.01)
    circle.r = 10
    assert circle.area == pytest.approx(314.16, 0.01)
