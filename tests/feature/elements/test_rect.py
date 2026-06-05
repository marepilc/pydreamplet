import pydreamplet as dp


def test_rect_pos_constructor_does_not_emit_pos_attribute():
    rect = dp.Rect(pos=dp.Vector(10, 20), width=30, height=40)

    assert rect.pos.x == 10
    assert rect.pos.y == 20
    assert rect.element.attrib["x"] == "10.0"
    assert rect.element.attrib["y"] == "20.0"
    assert "pos=" not in str(rect)


def test_rect_accepts_tuple_pos_and_typed_constructor_args():
    rect = dp.Rect(pos=(10, 20), width=30, height=40, fill="red")

    assert rect.pos == dp.Vector(10, 20)
    assert rect.width == 30
    assert rect.height == 40
    assert rect.element.attrib["fill"] == "red"


def test_rect_pos_setter_accepts_point_like_values():
    rect = dp.Rect(width=30, height=40)

    rect.pos = [10, 20]

    assert rect.pos == dp.Vector(10, 20)


def test_rect_numeric_properties_support_arithmetic_and_setters():
    rect = dp.Rect(x=10, y=20, width=30, height=40)

    assert rect.x + rect.width == 40
    assert rect.y + rect.height == 60

    rect.x = 15
    rect.y = 25
    rect.width = 35
    rect.height = 45

    assert rect.pos == dp.Vector(15, 25)
    assert rect.element.attrib["width"] == "35"
    assert rect.element.attrib["height"] == "45"
