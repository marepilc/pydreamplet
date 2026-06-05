import pydreamplet as dp


def test_ellipse_pos_constructor_does_not_emit_pos_attribute():
    ellipse = dp.Ellipse(pos=dp.Vector(10, 20), rx=5, ry=8)

    assert ellipse.pos.x == 10
    assert ellipse.pos.y == 20
    assert ellipse.element.attrib["cx"] == "10.0"
    assert ellipse.element.attrib["cy"] == "20.0"
    assert "pos=" not in str(ellipse)


def test_ellipse_accepts_tuple_pos_and_typed_constructor_args():
    ellipse = dp.Ellipse(pos=(10, 20), rx=5, ry=8)

    assert ellipse.pos == dp.Vector(10, 20)
    assert ellipse.element.attrib["rx"] == "5"
    assert ellipse.element.attrib["ry"] == "8"


def test_ellipse_pos_setter_accepts_point_like_values():
    ellipse = dp.Ellipse(rx=5, ry=8)

    ellipse.pos = [10, 20]

    assert ellipse.pos == dp.Vector(10, 20)


def test_ellipse_numeric_properties_support_arithmetic_and_setters():
    ellipse = dp.Ellipse(cx=10, cy=20, rx=5, ry=8)

    assert ellipse.cx + ellipse.rx == 15
    assert ellipse.cy + ellipse.ry == 28

    ellipse.cx = 30
    ellipse.cy = 40
    ellipse.rx = 12
    ellipse.ry = 16

    assert ellipse.pos == dp.Vector(30, 40)
    assert ellipse.element.attrib["rx"] == "12"
    assert ellipse.element.attrib["ry"] == "16"
