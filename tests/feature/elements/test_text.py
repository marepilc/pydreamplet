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
