import xml.etree.ElementTree as ET

import pytest

import pydreamplet as dp
from pydreamplet.core import qname


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


def test_g_pivot_applies_to_rotation_and_scale():
    g = dp.G(pivot=dp.Vector(10, 20), angle=30, scale=dp.Vector(2, 3))

    assert (
        g.element.attrib["transform"]
        == "rotate(30,10,20) translate(10 20) scale(2 3) translate(-10 -20)"
    )


def test_g_pivoted_scale_respects_transform_order():
    g = dp.G(
        pos=dp.Vector(5, 6),
        scale=dp.Vector(2, 2),
        pivot=dp.Vector(10, 20),
        order="st",
    )

    assert (
        g.element.attrib["transform"]
        == "translate(10 20) scale(2 2) translate(-10 -20) translate(5 6)"
    )


def test_g_from_element_restores_pivot_from_pivoted_scale():
    element = ET.Element(
        qname("g"),
        {"transform": "translate(10 20) scale(2 3) translate(-10 -20)"},
    )

    g = dp.G.from_element(element)

    assert g.pivot == dp.Vector(10, 20)
    assert g.scale == dp.Vector(2, 3)
    assert (
        g.element.attrib["transform"]
        == "translate(10 20) scale(2 3) translate(-10 -20)"
    )

    g.pivot = dp.Vector(30, 40)
    assert (
        g.element.attrib["transform"]
        == "translate(30 40) scale(2 3) translate(-30 -40)"
    )


def test_g_attrs_transform_raises_for_malformed_supported_transform():
    g = dp.G()

    with pytest.raises(ValueError, match="Invalid translate transform values"):
        g.attrs({"transform": "translate(foo 12)"})


def test_g_attrs_preserves_non_legacy_transform_functions():
    g = dp.G()

    g.attrs({"transform": "skewX(20)"})

    assert g.element.attrib["transform"] == "skewX(20)"
    assert g.pos == dp.Vector(0, 0)


def test_g_from_element_parses_comma_separated_transform():
    element = ET.Element(qname("g"), {"transform": "translate(10, 12) scale(2)"})

    g = dp.G.from_element(element)

    assert g.pos == dp.Vector(10, 12)
    assert g.scale == dp.Vector(2, 2)


def test_g_from_element_preserves_transform_order_with_extra_functions():
    element = ET.Element(
        qname("g"),
        {"transform": "translate(10 12) skewX(20) rotate(30) matrix(1 0 0 1 5 6)"},
    )

    g = dp.G.from_element(element)

    assert g.pos == dp.Vector(10, 12)
    assert g.angle == 30
    assert (
        g.element.attrib["transform"]
        == "translate(10 12) skewX(20) rotate(30) matrix(1 0 0 1 5 6)"
    )

    g.pos = dp.Vector(20, 24)

    assert (
        g.element.attrib["transform"]
        == "translate(20 24) skewX(20) rotate(30) matrix(1 0 0 1 5 6)"
    )


def test_g_pivoted_scale_is_preserved_with_extra_transform_functions():
    g = dp.G()
    g.attrs({"transform": "skewX(20)"})

    g.pivot = dp.Vector(10, 20)
    g.scale = dp.Vector(3, 3)

    assert (
        g.element.attrib["transform"]
        == "translate(10 20) scale(3 3) translate(-10 -20) skewX(20)"
    )


def test_g_from_element_raises_for_malformed_supported_transform():
    element = ET.Element(qname("g"), {"transform": "rotate(foo)"})

    with pytest.raises(ValueError, match="Invalid rotate transform values"):
        dp.G.from_element(element)
