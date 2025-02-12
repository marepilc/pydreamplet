from pydreamplet import SVG, Rect, Text


def test_rect_creation():
    rect = Rect(x=10, y=10, width=100, height=50, fill="red")
    elem = rect.element
    assert elem.tag.endswith("rect")
    assert elem.attrib.get("x") == "10"
    assert elem.attrib.get("y") == "10"
    assert elem.attrib.get("width") == "100"
    assert elem.attrib.get("height") == "50"
    assert elem.attrib.get("fill") == "red"


def test_text_single_line():
    text = Text("Hello, World!", x=10, y=10, font_size=18)
    # Single-line should be directly in text.text and no <tspan> children.
    assert text.element.text == "Hello, World!"
    assert len(list(text.element)) == 0


def test_text_multiline():
    text = Text("", x=10, y=10, font_size=20)
    text.content = "Hello,\nWorld!"
    # When multiline, element.text should be None and two tspans should exist.
    assert text.element.text is None
    tspans = list(text.element)
    assert len(tspans) == 2

    # Check the first <tspan>
    tspan1 = tspans[0]
    assert tspan1.attrib.get("x") == "10"
    assert tspan1.attrib.get("y") == "10"
    assert tspan1.text == "Hello,"

    # Check the second <tspan>
    tspan2 = tspans[1]
    assert tspan2.attrib.get("x") == "10"
    # dy should be set using the parent's font-size (20)
    dy = tspan2.attrib.get("dy")
    # Allow for both "20" or "20.0" as a string
    assert dy in ("20", "20.0")
    assert tspan2.text == "World!"


def test_attribute_normalization():
    # Passing font_size should become font-size.
    rect = Rect(x=5, font_size=12, fill="green")
    assert "font-size" in rect.element.attrib
    assert rect.element.attrib["font-size"] == "12"


def test_append_remove():
    svg = SVG(300, 300)
    rect = Rect(x=10, y=10, width=50, height=50, fill="blue")
    svg.append(rect)
    # After append, there should be one child.
    assert len(list(svg.element)) == 1
    # Remove the child and verify removal.
    svg.remove(rect)
    assert len(list(svg.element)) == 0


def test_full_svg_output():
    svg = SVG(300, 300)
    text = Text("Hello,\nWorld!", x=10, y=10, font_size=18)
    svg.append(text)
    rect = Rect(x=20, y=80, width=60, height=60, fill="pink", stroke="black")
    svg.append(rect)
    xml_str = str(svg)
    # Verify that the essential SVG elements are present.
    assert "<svg" in xml_str
    assert "<text" in xml_str
    assert "<rect" in xml_str
    # Check that <tspan> elements exist because text was multiline.
    assert "<tspan" in xml_str
