import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

import pydreamplet as dp
from pydreamplet.core import XLINK_NS, ns_attr, qname


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


def test_svg_from_file_supports_decimal_viewbox(tmp_path: Path):
    svg_file = tmp_path / "decimal.svg"
    svg_file.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0.5 1.5 200.25 100.75" />',
        encoding="utf-8",
    )

    svg = dp.SVG.from_file(str(svg_file))

    assert svg.w == 200.25
    assert svg.h == 100.75
    assert svg.element.attrib["viewBox"] == "0.5 1.5 200.25 100.75"


def test_svg_from_file_supports_comma_separated_viewbox(tmp_path: Path):
    svg_file = tmp_path / "comma-viewbox.svg"
    svg_file.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0.5,1.5,200.25,100.75" />',
        encoding="utf-8",
    )

    svg = dp.SVG.from_file(str(svg_file))

    assert svg.w == 200.25
    assert svg.h == 100.75


def test_svg_from_file_derives_viewbox_from_dimensions(tmp_path: Path):
    svg_file = tmp_path / "dimensions.svg"
    svg_file.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="320px" height="240px" />',
        encoding="utf-8",
    )

    svg = dp.SVG.from_file(str(svg_file))

    assert svg.w == 320
    assert svg.h == 240
    assert svg.element.attrib["viewBox"] == "0 0 320 240"


def test_svg_from_file_derives_decimal_viewbox_from_dimensions(tmp_path: Path):
    svg_file = tmp_path / "decimal-dimensions.svg"
    svg_file.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="320.5px" height="240.25px" />',
        encoding="utf-8",
    )

    svg = dp.SVG.from_file(str(svg_file))

    assert svg.w == 320.5
    assert svg.h == 240.25
    assert svg.element.attrib["viewBox"] == "0 0 320.5 240.25"


def test_svg_from_file_preserves_existing_root_attributes(tmp_path: Path):
    svg_file = tmp_path / "attrs.svg"
    svg_file.write_text(
        (
            '<svg xmlns="http://www.w3.org/2000/svg" width="320" height="240" '
            'id="logo" data-name="Example" role="img" />'
        ),
        encoding="utf-8",
    )

    svg = dp.SVG.from_file(str(svg_file))

    assert svg.element.attrib["id"] == "logo"
    assert svg.element.attrib["data-name"] == "Example"
    assert svg.element.attrib["role"] == "img"
    assert svg.element.attrib["width"] == "320"
    assert svg.element.attrib["height"] == "240"


def test_svg_from_file_preserves_loaded_namespace_prefixes(tmp_path: Path):
    svg_file = tmp_path / "namespaced.svg"
    svg_file.write_text(
        (
            '<svg xmlns="http://www.w3.org/2000/svg" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'xmlns:serif="http://www.serif.com/" '
            'viewBox="0 0 10 10">'
            '<use xlink:href="#shape" serif:id="copy" />'
            "</svg>"
        ),
        encoding="utf-8",
    )

    svg = dp.SVG.from_file(str(svg_file))
    use = svg.find("use")
    output = svg.to_string(pretty_print=False)

    assert use is not None
    assert use.element.attrib[ns_attr("xlink", "href")] == "#shape"
    assert use.element.attrib[ns_attr("serif", "id")] == "copy"
    assert "xlink:href" in output
    assert "serif:id" in output
    assert "ns0:" not in output


def test_namespaced_attribute_helpers_use_known_prefixes():
    use = dp.SvgElement("use", xlink_href="#shape")

    assert use.element.attrib[f"{{{XLINK_NS}}}href"] == "#shape"
    assert use.xlink_href == "#shape"
    assert use.has_attr("xlink_href") is True

    use.xlink_href = "#other"
    assert use.element.attrib[f"{{{XLINK_NS}}}href"] == "#other"

    use.attrs({"xlink_href": None})
    assert f"{{{XLINK_NS}}}href" not in use.element.attrib


def test_svg_from_file_without_viewbox_or_dimensions_uses_zero_size(tmp_path: Path):
    svg_file = tmp_path / "empty.svg"
    svg_file.write_text('<svg xmlns="http://www.w3.org/2000/svg" />', encoding="utf-8")

    svg = dp.SVG.from_file(str(svg_file))

    assert svg.w == 0
    assert svg.h == 0
    assert "viewBox" not in svg.element.attrib


def test_svg_from_file_raises_for_malformed_xml(tmp_path: Path):
    svg_file = tmp_path / "malformed.svg"
    svg_file.write_text("<svg><rect></svg>", encoding="utf-8")

    with pytest.raises(ET.ParseError):
        dp.SVG.from_file(str(svg_file))


@pytest.mark.parametrize(
    "viewbox, message",
    [
        ("0 0 100", "viewBox must contain 4 numbers"),
        ("0 0 nope 100", "Invalid viewBox values"),
    ],
)
def test_svg_from_file_raises_for_invalid_viewbox(
    tmp_path: Path, viewbox: str, message: str
):
    svg_file = tmp_path / "invalid-viewbox.svg"
    svg_file.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" />',
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match=message):
        dp.SVG.from_file(str(svg_file))


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


def create_sample_svg() -> dp.SVG:
    """
    Create a simple SVG with a single circle element.
    """
    svg = dp.SVG(200, 200)
    # We create a circle element using SvgElement for simplicity.
    circle = dp.SvgElement("circle", cx=100, cy=100, r=50)
    svg.append(circle)
    return svg


def test_to_string_without_pretty_print():
    svg = create_sample_svg()
    unformatted = svg.to_string(pretty_print=False)
    # The unformatted output should not contain newlines.
    assert "\n" not in unformatted, (
        "Unformatted SVG should not contain newline characters."
    )


def test_to_string_with_pretty_print():
    # Create a fresh SVG instance so that the element tree is unmodified.
    svg = create_sample_svg()
    formatted = svg.to_string(pretty_print=True)
    # Check that pretty printed output contains newlines (or more whitespace).
    assert "\n" in formatted, "Pretty printed SVG should contain newline characters."
    # Pretty printed output should be longer due to added whitespace.
    svg_unformatted = create_sample_svg().to_string(pretty_print=False)
    assert len(formatted) > len(svg_unformatted), (
        "Pretty printed SVG should be longer than unformatted SVG."
    )
