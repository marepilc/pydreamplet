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
