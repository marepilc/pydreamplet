import pydreamplet as dp


def test_use_accepts_href_reference():
    use = dp.Use("#heart", fill="red")

    assert use.element.tag.endswith("use")
    assert use.href == "#heart"
    assert use.fill == "red"


def test_use_normalizes_plain_id_to_href_reference():
    use = dp.Use("heart")

    assert use.href == "#heart"


def test_use_accepts_svg_element_reference():
    heart = dp.Path(id="heart")
    use = dp.Use(heart)

    assert use.href == "#heart"


def test_use_href_setter_normalizes_reference():
    use = dp.Use()

    use.href = "heart"

    assert use.href == "#heart"


def test_use_supports_xlink_href_for_legacy_svg():
    use = dp.Use(xlink_href="#heart")

    assert use.xlink_href == "#heart"


def test_use_elements_are_registered_and_live():
    svg = dp.SVG(100, 100)
    use = dp.Use("#heart")
    svg.append(use)

    found = svg.find("use")

    assert isinstance(found, dp.Use)
    assert found.element is use.element
