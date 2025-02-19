import xml.etree.ElementTree as ET

import pytest

import pydreamplet as dp


def test_svg_dimensions(svg_300, two_rectangles):
    root = ET.fromstring(str(svg_300))
    assert root.attrib.get("viewBox") == "0 0 300 300"


@pytest.mark.parametrize(
    "args, expected_viewbox",
    [
        ((600, 600), "0 0 600 600"),
        ((10, 20, 600, 600), "10 20 600 600"),
    ],
)
def test_svg_viewbox(args, expected_viewbox):
    svg = dp.SVG(*args)
    root = ET.fromstring(str(svg))
    assert root.attrib.get("viewBox") == expected_viewbox


def test_svg_find(svg_300, two_rectangles):
    rect1, rect2 = two_rectangles
    svg_300.append(rect1).append(rect2)
    first_rect = svg_300.find("rect")
    assert first_rect.pos.x == 0
    assert first_rect.width == 10


def test_svg_find_all(svg_300, two_rectangles):
    rect1, rect2 = two_rectangles
    svg_300.append(rect1).append(rect2)
    rectangles = list(svg_300.find_all("rect"))
    assert len(rectangles) == 2
    assert rectangles[1].pos.x == 50


def test_svg_append_remove(svg_300, two_rectangles):
    rect1, rect2 = two_rectangles

    svg_300.append(rect1)
    assert len(list(svg_300.element)) == 1
    svg_300.remove(rect1)
    assert len(list(svg_300.element)) == 0

    svg_300.append(rect1).append(rect2)
    assert len(list(svg_300.element)) == 2
    svg_300.remove(rect1)
    assert len(list(svg_300.element)) == 1
    svg_300.remove(rect2)
    assert len(list(svg_300.element)) == 0


def test_attribute_normalization():
    # Passing font_size should become font-size.
    rect = dp.Text("test", x=5, y=5, font_size=12, fill="green")
    assert "font-size" in rect.element.attrib
    assert rect.element.attrib["font-size"] == "12"


def test_append_multiple_elements():
    svg = dp.SVG(300, 300)
    rect1 = dp.Rect(x=10, y=10, width=20, height=20)
    rect2 = dp.Rect(x=50, y=50, width=20, height=20)
    svg.append(rect1, rect2)
    assert len(list(svg.find_all("rect"))) == 2
