from pydreamplet import Path
from pydreamplet.markers import ARROW_BASIC, ARROW_CONVEX, Marker


def test_marker_default_attributes():
    marker = Marker("arrow", ARROW_BASIC, 10, 10)
    # Check marker element attributes
    assert marker.element.get("id") == "arrow"
    assert marker.element.get("markerWidth") == "10"
    assert marker.element.get("markerHeight") == "10"
    assert marker.element.get("viewBox") == "0 0 10 10"
    assert marker.element.get("refX") == "5"
    assert marker.element.get("refY") == "5"
    assert marker.element.get("orient") == "auto-start-reverse"

    # Check that the marker has a child path element
    path = marker.find("path")
    assert path is not None
    assert isinstance(path, Path)

    # Check the default properties of the path
    assert path.d == ARROW_BASIC
    assert path.fill == "#000000"
    assert path.stroke == "none"
    assert path.stroke_width == 1


def test_marker_d_property():
    marker = Marker("arrow", ARROW_BASIC, 10, 10)
    # Change the path data
    marker.d = ARROW_CONVEX
    # Verify that the d property returns the updated value
    assert marker.d == ARROW_CONVEX
    # Verify that the underlying path's d attribute is updated
    path = marker.find("path")
    assert path.d == ARROW_CONVEX


def test_marker_fill_property():
    marker = Marker("arrow", ARROW_BASIC, 10, 10)
    # Default fill should be "#000000"
    assert marker.fill == "#000000"
    # Update the fill property
    marker.fill = "#ff0000"
    assert marker.fill == "#ff0000"
    # Verify the underlying path's fill attribute is updated
    path = marker.find("path")
    assert path.fill == "#ff0000"


def test_marker_stroke_property():
    marker = Marker("arrow", ARROW_BASIC, 10, 10)
    # Default stroke should be "none"
    assert marker.stroke == "none"
    # Update the stroke property
    marker.stroke = "#00ff00"
    assert marker.stroke == "#00ff00"
    # Verify the underlying path's stroke attribute is updated
    path = marker.find("path")
    assert path.stroke == "#00ff00"


def test_marker_stroke_width_property():
    marker = Marker("arrow", ARROW_BASIC, 10, 10)
    # Default stroke width should be "1"
    assert marker.stroke_width == 1
    # Update the stroke width property
    marker.stroke_width = "2"
    assert marker.stroke_width == 2
    # Verify the underlying path's stroke-width attribute is updated
    path = marker.find("path")
    assert path.stroke_width == 2


def test_marker_id_ref():
    marker = Marker("arrow", ARROW_BASIC, 10, 10)
    # The id_ref property should return a URL reference for the marker id
    assert marker.id_ref == "url(#arrow)"
