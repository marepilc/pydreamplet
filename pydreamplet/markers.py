from numbers import Real

from pydreamplet import Path, SvgElement

ARROW = "M2.499 5 L1.565 1.7 L8.435 5 L1.565 8.3 Z"
ARROW_BASIC = "M0 1.91 10 5 0 8.09V1.91Z"
ARROW_CONCAVE = "M0 8.09a22.48 22.48 0 0 0 0-6.18C2.862 3.396 6.241 4.382 10 5c-3.759.618-7.138 1.604-10 3.09Z"
ARROW_CONVEX = (
    "M.505 5 0 1.91C1.453 1.908 6.391 2.989 10 5 6.391 7.011 1.453 8.092 0 8.09L.505 5Z"
)
ARROW_SIMPLE = "M3.596 5 .768 2.172 2.182.757 6.424 5 2.182 9.243.768 7.828 3.596 5Z"
CROSS = d = (
    "M1.667 3.333L3.333 1.667L5 3.333L6.667 1.667L8.333 3.333L6.667 5L8.333 6.667L6.667 8.333L5 6.667L3.333 8.333L1.667 6.667L3.333 5L1.667 3.333Z"
)
DIAMOND = "M5 1.91 8.09 5 5 8.09 1.91 5 5 1.91Z"
DOT = "M 9.09 5 A 4.09 4.09 0 1 0 0.91 5 A 4.09 4.09 0 1 0 9.09 5 Z"
SQUARE = "M1.91 1.91h6.18v6.18H1.91z"
TICK_BOTTOM = "M4 5h2v5H4z"
TICK_HORIZONTAL = "M2.5 4h5v2h-5z"
TICK_LEFT = "M0 4h5v2H0z"
TICK_RIGHT = "M5 4h5v2H5z"
TICK_TOP = "M4 0h2v5H4z"
TICK_VERTICAL = "M4 2.5h2v5H4z"


class Marker(SvgElement):
    def __init__(self, id: str, d: str, width: Real, height: Real, **kwargs):
        super().__init__("marker")
        self._id = id
        self._d = d
        defaults = {
            "id": id,
            "markerWidth": str(width),
            "markerHeight": str(height),
            "viewBox": "0 0 10 10",
            "refX": kwargs.get("refX", "5"),
            "refY": kwargs.get("refY", "5"),
            "orient": kwargs.get("orient", "0"),
        }
        path_defaults = {
            "fill": kwargs.get("fill", "#000000"),
            "stroke": kwargs.get("stroke", "none"),
            "stroke-width": kwargs.get("stroke-width", "1"),
        }
        for key, value in defaults.items():
            self.element.set(key, value)

        marker_path = Path(d=d)
        marker_path.attrs({key: value for key, value in path_defaults.items()})
        self.append(marker_path)

    @property
    def d(self):
        return self._d

    @d.setter
    def d(self, value):
        self._d = value
        path_element = self.find("path")
        if path_element is not None:
            path_element.d = value

    @property
    def fill(self):
        path_element = self.find("path")
        if path_element is not None:
            return path_element.fill
        return None

    @fill.setter
    def fill(self, value):
        path_element = self.find("path")
        if path_element is not None:
            path_element.fill = value

    @property
    def stroke(self):
        path_element = self.find("path")
        if path_element is not None:
            return path_element.stroke
        return None

    @stroke.setter
    def stroke(self, value):
        path_element = self.find("path")
        if path_element is not None:
            path_element.stroke = value

    @property
    def stroke_width(self):
        path_element = self.find("path")
        if path_element is not None:
            return path_element.stroke_width
        return None

    @stroke_width.setter
    def stroke_width(self, value):
        path_element = self.find("path")
        if path_element is not None:
            path_element.stroke_width = value

    @property
    def id_ref(self):
        return f"url(#{self._id})"


SvgElement.register("marker", Marker)
