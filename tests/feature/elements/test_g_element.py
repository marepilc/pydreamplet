import pydreamplet as dp


def test_g_element_transformation(svg_300, two_rectangles):
    rect1, rect2 = two_rectangles

    g = dp.G()
    g.append(rect1).append(rect2)
    svg_300.append(g)
    assert str(svg_300).find("transform") == -1
    g.pos = dp.Vector(20, 20)
    assert 'transform="translate(20 20)"' in str(svg_300)
    assert g.angle == 0
    g.attrs({"transform": "translate(10 12)"})
    assert g.pos.y == 12


def test_g_element_find(svg_300, two_rectangles):
    rect1, rect2 = two_rectangles
    svg_300.append(rect1).append(rect2)
    first_rect = svg_300.find("rect")
    assert first_rect.pos.x == 0
    assert first_rect.width == 10


def test_g_element_append_remove(svg_300, two_rectangles):
    rect1, rect2 = two_rectangles

    g = dp.G()
    g.append(rect1).append(rect2)
    svg_300.append(g)
    assert len(list(svg_300.element)) == 1
    g.remove(rect1)
    assert len(list(svg_300.element)) == 1
    g.remove(rect2)
    assert len(list(svg_300.element)) == 0

def test_g_transformation_order(svg_300):
    g = dp.G()
    g.pos = dp.Vector(20, 20)
    g.angle = 45
    g.scale = dp.Vector(2, 2)
    svg_300.append(g)
    assert 'transform="translate(20 20) rotate(45) scale(2 2)"' in str(svg_300)
    g.order = "rts"
    assert 'transform="rotate(45) translate(20 20) scale(2 2)"' in str(svg_300)