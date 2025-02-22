import pydreamplet as dp


def test_text_single_line():
    text = dp.Text("Hello, World!", x=10, y=10, font_size=18)
    # Single-line should be directly in text.text and no <tspan> children.
    assert text.element.text == "Hello, World!"
    assert len(list(text.element)) == 0


def test_text_multiline():
    text = dp.Text("", x=10, y=10, font_size=20)
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


def test_text_font_size_with_units():
    # Create a Text element without initially specifying font_size.
    text = dp.Text("Test", x=0, y=0)
    # Set font_size with explicit units.
    text.font_size = "10.5pt"
    # Verify that the attribute is exactly what was provided.
    assert text.element.get("font-size") == "10.5pt"
    # The getter should extract only the numeric part.
    assert text.font_size == 10.5


def test_text_font_size_without_units():
    text = dp.Text("Test", x=0, y=0)
    # Set font_size with a numeric value (as a string) without units.
    text.font_size = "12"
    # Since no unit was provided, "px" is appended.
    assert text.element.get("font-size") == "12px"
    # The getter should return the numeric part.
    assert text.font_size == 12.0


def test_text_on_path_font_size_with_units():
    # Create a TextOnPath element.
    text_path = dp.TextOnPath("Test", path_id="myPath")
    text_path.font_size = "15em"
    # Verify the attribute retains the given unit.
    assert text_path.element.get("font-size") == "15em"
    # The getter returns only the numeric portion.
    assert text_path.font_size == 15.0


def test_text_on_path_font_size_without_units():
    text_path = dp.TextOnPath("Test", path_id="myPath")
    text_path.font_size = "14"
    # "px" should be appended when no unit is provided.
    assert text_path.element.get("font-size") == "14px"
    assert text_path.font_size == 14.0
