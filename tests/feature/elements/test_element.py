import pydreamplet as dp


def test_element_remove_attribute():
    circle = dp.Circle(id="circle")
    assert "id" in str(circle)
    circle.id = None
    assert "id" not in str(circle)

    circle.cx = 10
    assert 'cx="10"' in str(circle)
    circle.attrs({"cx": None})
    assert "cx" not in str(circle)


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


def test_find_and_find_all():
    # Create the main SVG element.
    svg = dp.SvgElement("svg")

    # Create child elements with various id and class_name attributes.
    circle = dp.SvgElement("circle", id="circle1")
    rect1 = dp.SvgElement("rect", class_name="highlight")
    rect2 = dp.SvgElement("rect", class_name="highlight")
    rect3 = dp.SvgElement("rect", class_name="other")
    group = dp.SvgElement("g", id="group1", class_name="group-class")

    # Append the elements to the svg.
    svg.append(circle, rect1, rect2, rect3, group)

    # Test find with an id filter.
    found_circle = svg.find("circle", id="circle1")
    assert found_circle is not None, "find() should return a circle with id 'circle1'"
    assert found_circle.id == "circle1", f"Expected id 'circle1', got {found_circle.id}"

    # Test find_all with a class_name filter.
    found_rects = list(svg.find_all("rect", class_name="highlight"))
    assert len(found_rects) == 2, (
        f"Expected 2 rect elements with class 'highlight', got {len(found_rects)}"
    )


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


def test_remove_multiple_elements():
    svg = dp.SVG(300, 300)
    rect1 = dp.Rect(x=10, y=10, width=20, height=20)
    rect2 = dp.Rect(x=50, y=50, width=20, height=20)
    svg.append(rect1, rect2)
    no_needed_any_more = svg.find_all("rect")
    svg.remove(*no_needed_any_more)
    assert len(list(svg.find_all("rect"))) == 0
