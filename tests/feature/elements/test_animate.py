from pydreamplet.core import SVG_NS, Animate


def test_default_values():
    anim = Animate("opacity")
    assert anim.element.tag == f"{{{SVG_NS}}}animate"

    attrib = anim.element.attrib
    assert attrib.get("dur") == "2s"
    assert attrib.get("attributeType") == "XML"
    assert attrib.get("attributeName") == "opacity"
    assert attrib.get("repeatCount") == "indefinite"
    assert "values" not in attrib


def test_with_values_and_repeat_count():
    anim = Animate("opacity", repeatCount="5", values=[0, 1, 0.5], dur="3s")
    attrib = anim.element.attrib
    assert attrib.get("dur") == "3s"
    assert attrib.get("attributeName") == "opacity"
    assert attrib.get("repeatCount") == "5"
    assert attrib.get("values") == "0;1;0.5"


def test_setter_properties():
    anim = Animate("opacity", values=[0, 1, 0.5])
    anim.repeat_count = "10"
    assert anim.element.get("repeatCount") == "10"
    anim.values = [1, 2, 3]
    assert anim.element.get("values") == "1;2;3"
    assert anim.values == [1, 2, 3]


def test_non_list_values():
    anim = Animate("opacity", values="not a list")
    assert anim._values == []
    assert "values" not in anim.element.attrib
