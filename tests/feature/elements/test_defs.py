import pydreamplet as dp


def test_ensure_defs_creates_defs_as_first_child():
    svg = dp.SVG(100, 100)
    rect = dp.Rect(width=10, height=10)
    svg.append(rect)

    defs = svg.ensure_defs()

    assert isinstance(defs, dp.Defs)
    assert getattr(defs, "_parent") is svg
    assert list(svg.element)[0] is defs.element
    assert list(svg.element)[1] is rect.element


def test_ensure_defs_reuses_existing_defs():
    svg = dp.SVG(100, 100)
    defs = dp.Defs(id="resources")
    svg.append(defs)

    found = svg.ensure_defs()

    assert found.element is defs.element
    assert found.id == "resources"
    assert len(svg.find_all("defs")) == 1


def test_linear_gradient_add_stop_and_url_ref():
    gradient = (
        dp.LinearGradient("fade", x1="0%", y1="0%", x2="100%", y2="0%")
        .add_stop("0%", "#000", opacity=0.25)
        .add_stop("100%", "#fff")
    )

    stops = gradient.find_all("stop")

    assert gradient.url == "url(#fade)"
    assert gradient.id_ref == "url(#fade)"
    assert gradient.element.attrib["x1"] == "0%"
    assert gradient.element.attrib["x2"] == "100%"
    assert len(stops) == 2
    assert isinstance(stops[0], dp.Stop)
    assert stops[0].offset == "0%"
    assert stops[0].stop_color == "#000"
    assert stops[0].stop_opacity == 0.25


def test_radial_gradient_add_stop():
    gradient = dp.RadialGradient("glow", cx="50%", cy="50%", r="40%")

    assert gradient.add_stop("0%", "#fff") is gradient
    stop = gradient.find("stop")
    assert isinstance(stop, dp.Stop)
    assert stop.stop_color == "#fff"
    assert gradient.url == "url(#glow)"
    assert gradient.id_ref == "url(#glow)"


def test_definition_elements_are_registered_and_live():
    svg = dp.SVG(100, 100)
    gradient = dp.LinearGradient("fade").add_stop("0%", "#000")
    svg.ensure_defs().append(gradient)

    found_gradient = svg.find("linearGradient", nested=True, id="fade")
    found_stop = svg.find("stop", nested=True)

    assert isinstance(found_gradient, dp.LinearGradient)
    assert isinstance(found_stop, dp.Stop)
    assert found_gradient.element is gradient.element

    found_stop.stop_color = "#333"
    stop = gradient.find("stop")
    assert isinstance(stop, dp.Stop)
    assert stop.stop_color == "#333"


def test_resource_definition_wrappers_create_expected_tags():
    resources = [
        (dp.Pattern("tiles"), "pattern"),
        (dp.Mask("fade-mask"), "mask"),
        (dp.ClipPath("clip"), "clipPath"),
        (dp.Filter("shadow"), "filter"),
    ]

    for resource, tag in resources:
        assert resource.element.tag.endswith(tag)
        assert resource.url == f"url(#{resource.id})"
        assert resource.id_ref == f"url(#{resource.id})"
