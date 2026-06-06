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
    rectangles = svg_300.find_all("rect")
    assert isinstance(rectangles, list)
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

    assert svg_300.append(rect1) is svg_300
    assert getattr(rect1, "_parent") is svg_300
    assert len(list(svg_300.element)) == 1
    assert svg_300.remove(rect1) is svg_300
    assert not hasattr(rect1, "_parent")
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


def test_svg_element_copy():
    original = dp.SvgElement("rect", x=10, y=20, width=100, height=50)
    duplicate = original.copy()
    duplicate.x = 30
    assert original.x == 10
    assert duplicate.x == 30
    assert original.y == duplicate.y
    assert original.width == duplicate.width
    assert original.height == duplicate.height
    assert original.element is not duplicate.element
    assert original.element.attrib is not duplicate.element.attrib


def test_copy_preserves_element_class_and_deep_copies_children():
    group = dp.G(id="layer")
    rect = dp.Rect(x=10, y=20, width=30, height=40)
    group.append(rect)

    duplicate = group.copy()
    duplicate_rect = duplicate.find("rect")
    assert isinstance(duplicate, dp.G)
    assert isinstance(duplicate_rect, dp.Rect)
    assert duplicate is not group
    assert duplicate.element is not group.element
    assert duplicate_rect is not None
    assert duplicate_rect.element is not rect.element

    duplicate_rect.x = 99
    assert rect.x == 10
    assert duplicate_rect.x == 99


def test_append_remove_parent_contract_for_multiple_children():
    group = dp.G()
    rect = dp.Rect()
    circle = dp.Circle()

    result = group.append(rect, circle)

    assert result is group
    assert getattr(rect, "_parent") is group
    assert getattr(circle, "_parent") is group
    assert group.remove(rect, circle) is group
    assert not hasattr(rect, "_parent")
    assert not hasattr(circle, "_parent")


def test_find_returns_registered_types_and_none_for_missing_elements():
    svg = dp.SVG(100, 100)
    group = dp.G(id="layer")
    rect = dp.Rect(id="box")
    circle = dp.Circle(id="dot")
    group.append(rect, circle)
    svg.append(group)

    assert isinstance(svg.find("g"), dp.G)
    assert isinstance(svg.find("rect", nested=True, id="box"), dp.Rect)
    assert isinstance(svg.find("circle", nested=True, id="dot"), dp.Circle)
    assert svg.find("ellipse", nested=True) is None


def test_find_returns_live_wrapper_for_existing_element():
    svg = dp.SVG(100, 100)
    rect = dp.Rect(id="box", fill="red")
    svg.append(rect)

    found = svg.find("rect", id="box")
    assert isinstance(found, dp.Rect)
    assert found is not rect
    assert found.element is rect.element

    found.fill = "blue"
    assert rect.fill == "blue"
    assert 'fill="blue"' in svg.to_string(pretty_print=False)


def test_find_all_returns_registered_types_with_filters():
    svg = dp.SVG(100, 100)
    svg.append(
        dp.Rect(class_name="item"),
        dp.Circle(class_name="item"),
        dp.Rect(class_name="other"),
    )

    items = svg.find_all("rect", class_name="item")

    assert isinstance(items, list)
    assert len(items) == 1
    assert isinstance(items[0], dp.Rect)


def test_find_all_returns_live_wrappers_for_existing_elements():
    svg = dp.SVG(100, 100)
    rect = dp.Rect(class_name="item", fill="red")
    svg.append(rect)

    found = svg.find_all("rect", class_name="item")
    found[0].fill = "blue"

    assert found[0].element is rect.element
    assert rect.fill == "blue"
    assert 'fill="blue"' in svg.to_string(pretty_print=False)


def test_has_attr():
    # Test with regular attributes
    rect = dp.Rect(x=10, y=20, width=100, height=50, fill="blue")
    assert rect.has_attr("x") is True
    assert rect.has_attr("y") is True
    assert rect.has_attr("width") is True
    assert rect.has_attr("height") is True
    assert rect.has_attr("fill") is True
    assert rect.has_attr("stroke") is False
    
    # Test underscore to hyphen conversion
    text = dp.Text("hello", font_size="14px", stroke_width="2")
    assert text.has_attr("font_size") is True
    assert text.has_attr("stroke_width") is True
    assert text.has_attr("font-size") is True  # Direct hyphen version should also work
    assert text.has_attr("stroke-width") is True
    assert text.has_attr("line_height") is False
    
    # Test special class_name attribute
    circle = dp.Circle(r=5, class_name="highlight")
    assert circle.has_attr("class_name") is True
    assert circle.has_attr("r") is True
    assert circle.has_attr("id") is False
    
    # Test with element without class_name
    circle_no_class = dp.Circle(r=5)
    assert circle_no_class.has_attr("class_name") is False
    assert circle_no_class.has_attr("r") is True


def test_common_attribute_helpers_are_chainable():
    rect = (
        dp.Rect(width=10, height=20)
        .set_id("main")
        .set_class("highlight")
        .set_fill("red")
        .set_stroke("black", width=2, linecap="round", linejoin="bevel")
        .set_style({"opacity": 0.5, "stroke_width": 3, "display": None})
    )

    assert rect.element.attrib["id"] == "main"
    assert rect.element.attrib["class"] == "highlight"
    assert rect.element.attrib["fill"] == "red"
    assert rect.element.attrib["stroke"] == "black"
    assert rect.element.attrib["stroke-width"] == "2"
    assert rect.element.attrib["stroke-linecap"] == "round"
    assert rect.element.attrib["stroke-linejoin"] == "bevel"
    assert rect.element.attrib["style"] == "opacity: 0.5; stroke-width: 3"


def test_common_attribute_helpers_remove_values_with_none():
    circle = dp.Circle(r=5).set_id("dot").set_class("marker").set_fill("blue")

    circle.set_id(None).set_class(None).set_fill(None).set_style(None)

    assert "id" not in circle.element.attrib
    assert "class" not in circle.element.attrib
    assert "fill" not in circle.element.attrib
    assert "style" not in circle.element.attrib


def test_common_position_and_size_helpers():
    rect = dp.Rect().set_position((10, 20)).set_size(30, 40)
    circle = dp.Circle(r=5).set_position([50, 60])

    assert rect.pos == dp.Vector(10, 20)
    assert rect.width == 30
    assert rect.height == 40
    assert circle.pos == dp.Vector(50, 60)
    assert "x" not in circle.element.attrib
    assert circle.element.attrib["cx"] == "50.0"
    assert circle.element.attrib["cy"] == "60.0"
