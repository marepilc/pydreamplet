import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

import pydreamplet as dp
from pydreamplet.core import qname


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


def test_style_overwrite(tmp_path: Path):
    # Create a temporary CSS file with non-minified content.
    css_file = tmp_path / "style.css"
    css_content = "body { background-color: white; }"
    css_file.write_text(css_content, encoding="utf-8")

    # Create an SVG instance.
    svg = dp.SVG(400, 300)

    # Manually add an existing style element.
    old_style = dp.SvgElement("style")
    old_style.element.text = "old style"
    svg.append(old_style)

    # Call the new style method with overwrite=True and no minification.
    svg.style(str(css_file), overwrite=True, minify=False)

    # Collect all style elements in the SVG.
    style_elements = [child for child in svg.element if child.tag == qname("style")]

    # Assert that only one style element exists (old one was removed).
    assert len(style_elements) == 1, (
        "Expected existing style elements to be overwritten."
    )

    # Assert that the new style element is inserted as the first child.
    assert svg.element[0].tag == qname("style"), (
        "New style element should be the first child."
    )

    # Assert that the CSS content is exactly as in the file.
    assert style_elements[0].text == css_content, (
        "Style content should match the file content when minify is False."
    )


def test_style_append(tmp_path: Path):
    # Create a temporary CSS file.
    css_file = tmp_path / "style.css"
    css_content = "body { background-color: white; }"
    css_file.write_text(css_content, encoding="utf-8")

    # Create an SVG instance.
    svg = dp.SVG(400, 300)

    # Manually add an existing style element.
    old_style = dp.SvgElement("style")
    old_style.element.text = "old style"
    svg.append(old_style)

    # Call the new style method with overwrite=False.
    svg.style(str(css_file), overwrite=False, minify=False)

    # Collect all style elements.
    style_elements = [child for child in svg.element if child.tag == qname("style")]

    # Assert that there are now two style elements.
    assert len(style_elements) == 2, (
        "Expected a new style element to be appended without removing the old one."
    )

    # Assert that the new style element is appended at the end.
    assert svg.element[-1].tag == qname("style"), (
        "New style element should be appended at the end."
    )

    # Assert that the new style element has the correct CSS content.
    assert style_elements[-1].text == css_content, (
        "Appended style content should match the file content."
    )


def test_style_minify(tmp_path: Path):
    # Create a temporary CSS file with content that needs minification.
    css_file = tmp_path / "style.css"
    css_content = (
        "/* comment */\nbody {\n    background-color: white;\n    color: black;\n}\n"
    )
    css_file.write_text(css_content, encoding="utf-8")

    # Create an SVG instance.
    svg = dp.SVG(400, 300)

    # Call the new style method with minify=True.
    svg.style(str(css_file), overwrite=True, minify=True)

    # The minify_css function in our implementation should produce this output.
    expected_minified = "body{background-color:white;color:black;}"

    # Collect the style element.
    style_elements = [child for child in svg.element if child.tag == qname("style")]
    assert len(style_elements) == 1, "Expected one style element after overwriting."

    # Assert that the CSS content has been minified correctly.
    assert style_elements[0].text == expected_minified, (
        f"Expected minified CSS: {expected_minified}, but got: {style_elements[0].text}"
    )
