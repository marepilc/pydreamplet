import pydreamplet as dp


def test_ellipse_pos_constructor_does_not_emit_pos_attribute():
    ellipse = dp.Ellipse(pos=dp.Vector(10, 20), rx=5, ry=8)

    assert ellipse.pos.x == 10
    assert ellipse.pos.y == 20
    assert ellipse.element.attrib["cx"] == "10.0"
    assert ellipse.element.attrib["cy"] == "20.0"
    assert "pos=" not in str(ellipse)
