from pydreamplet.core import SVG_NS, Animate, AnimateTransform


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


def test_animate_transform_default_values():
    anim = AnimateTransform("rotate")

    assert anim.element.tag == f"{{{SVG_NS}}}animateTransform"

    attrib = anim.element.attrib
    assert attrib.get("dur") == "2s"
    assert attrib.get("attributeName") == "transform"
    assert attrib.get("type") == "rotate"
    assert attrib.get("repeatCount") == "indefinite"


def test_animate_transform_with_values_and_from():
    anim = AnimateTransform(
        "rotate",
        from_=0,
        to=360,
        values=[0, 180, 360],
        dur="8s",
        repeatCount="3",
    )

    attrib = anim.element.attrib
    assert attrib.get("from") == "0"
    assert attrib.get("to") == "360"
    assert attrib.get("values") == "0;180;360"
    assert attrib.get("dur") == "8s"
    assert attrib.get("repeatCount") == "3"


def test_animate_transform_setter_properties():
    anim = AnimateTransform("scale", values=[1, 2, 1])
    anim.repeat_count = "10"
    anim.values = [1, 1.5, 1]

    assert anim.element.get("repeatCount") == "10"
    assert anim.element.get("values") == "1;1.5;1"
    assert anim.values == [1, 1.5, 1]
