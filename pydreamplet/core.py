import math
import re
import xml.etree.ElementTree as ET
from copy import deepcopy
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, ClassVar, Self, cast, overload, override

from pydreamplet.math import Vector
from pydreamplet.path_data import PathBuilder, extract_path_points, normalize_path_commands
from pydreamplet.path_data import path_length, point_at_length, tangent_at_length
from pydreamplet.types import AttributeValue, NumericPair, Real

SVG_NS = "http://www.w3.org/2000/svg"
XML_NS = "http://www.w3.org/XML/1998/namespace"
XLINK_NS = "http://www.w3.org/1999/xlink"
KNOWN_NAMESPACES: dict[str, str] = {
    "": SVG_NS,
    "xml": XML_NS,
    "xlink": XLINK_NS,
}
ET.register_namespace("", SVG_NS)
ET.register_namespace("xlink", XLINK_NS)


def qname(tag: str) -> str:
    return f"{{{SVG_NS}}}{tag}"


def ns_attr(prefix: str, name: str) -> str:
    if prefix not in KNOWN_NAMESPACES:
        raise ValueError(f"Unknown XML namespace prefix: {prefix}")
    return f"{{{KNOWN_NAMESPACES[prefix]}}}{name}"


def _register_namespace(prefix: str, uri: str) -> None:
    KNOWN_NAMESPACES[prefix] = uri
    if prefix != "xml":
        ET.register_namespace(prefix, uri)


def _register_namespaces_from_file(filename: str) -> None:
    for _, namespace in ET.iterparse(filename, events=("start-ns",)):
        prefix, uri = cast(tuple[str, str], namespace)
        _register_namespace(prefix, uri)


type PointLike = Vector | NumericPair


@dataclass(frozen=True)
class BoundingBox:
    x: float
    y: float
    width: float
    height: float

    @property
    def left(self) -> float:
        return self.x

    @property
    def top(self) -> float:
        return self.y

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def bottom(self) -> float:
        return self.y + self.height

    @property
    def center(self) -> Vector:
        return Vector(self.x + self.width / 2, self.y + self.height / 2)


def _format_number(value: Real) -> str:
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return f"{value:g}" if isinstance(value, float) else str(value)


def _coerce_point(value: PointLike, name: str = "point") -> Vector:
    if isinstance(value, Vector):
        return value
    if len(value) != 2:
        raise ValueError(f"{name} must contain exactly 2 numbers")
    x, y = value
    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        raise ValueError(f"{name} must contain only numbers")
    return Vector(x, y)


def _coerce_point_args(
    x: PointLike | Real,
    y: Real | None,
    name: str = "position",
) -> Vector:
    if y is None:
        if isinstance(x, Vector | tuple | list):
            return _coerce_point(x, name)
        raise ValueError(f"{name} requires both x and y values")
    if not isinstance(x, (int, float)):
        raise ValueError(f"{name} x value must be a number")
    return Vector(x, y)


def _bbox_from_points(points: list[Vector]) -> BoundingBox:
    if not points:
        return BoundingBox(0, 0, 0, 0)
    xs = [point.x for point in points]
    ys = [point.y for point in points]
    left = min(xs)
    top = min(ys)
    return BoundingBox(left, top, max(xs) - left, max(ys) - top)


def _points_attribute_to_vectors(points: list[Real]) -> list[Vector]:
    if len(points) % 2 != 0:
        raise ValueError("points must contain an even number of coordinates")
    return [
        Vector(points[index], points[index + 1])
        for index in range(0, len(points), 2)
    ]


def _quadratic_bezier_point(
    p0: Vector, p1: Vector, p2: Vector, t: float
) -> Vector:
    mt = 1 - t
    return Vector(
        mt * mt * p0.x + 2 * mt * t * p1.x + t * t * p2.x,
        mt * mt * p0.y + 2 * mt * t * p1.y + t * t * p2.y,
    )


def _cubic_bezier_point(
    p0: Vector, p1: Vector, p2: Vector, p3: Vector, t: float
) -> Vector:
    mt = 1 - t
    return Vector(
        mt**3 * p0.x
        + 3 * mt * mt * t * p1.x
        + 3 * mt * t * t * p2.x
        + t**3 * p3.x,
        mt**3 * p0.y
        + 3 * mt * mt * t * p1.y
        + 3 * mt * t * t * p2.y
        + t**3 * p3.y,
    )


def _quadratic_bezier_extrema(p0: Vector, p1: Vector, p2: Vector) -> list[float]:
    roots: list[float] = []
    for start, control, end in ((p0.x, p1.x, p2.x), (p0.y, p1.y, p2.y)):
        denominator = start - 2 * control + end
        if denominator == 0:
            continue
        t = (start - control) / denominator
        if 0 < t < 1:
            roots.append(t)
    return roots


def _cubic_bezier_extrema(p0: Vector, p1: Vector, p2: Vector, p3: Vector) -> list[float]:
    roots: list[float] = []
    for start, control1, control2, end in (
        (p0.x, p1.x, p2.x, p3.x),
        (p0.y, p1.y, p2.y, p3.y),
    ):
        a = -start + 3 * control1 - 3 * control2 + end
        b = 2 * (start - 2 * control1 + control2)
        c = control1 - start

        if a == 0:
            if b == 0:
                continue
            t = -c / b
            if 0 < t < 1:
                roots.append(t)
            continue

        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            continue
        sqrt_discriminant = math.sqrt(discriminant)
        for t in (
            (-b + sqrt_discriminant) / (2 * a),
            (-b - sqrt_discriminant) / (2 * a),
        ):
            if 0 < t < 1:
                roots.append(t)
    return roots


def _angle_between(unit_a: tuple[float, float], unit_b: tuple[float, float]) -> float:
    cross = unit_a[0] * unit_b[1] - unit_a[1] * unit_b[0]
    dot = unit_a[0] * unit_b[0] + unit_a[1] * unit_b[1]
    return math.atan2(cross, dot)


def _is_angle_on_arc(angle: float, start_angle: float, delta_angle: float) -> bool:
    tau = math.tau
    if delta_angle >= 0:
        offset = (angle - start_angle) % tau
        return offset <= delta_angle or math.isclose(offset, delta_angle)
    offset = (start_angle - angle) % tau
    return offset <= -delta_angle or math.isclose(offset, -delta_angle)


def _svg_arc_center_parameters(
    start: Vector,
    end: Vector,
    rx: float,
    ry: float,
    x_axis_rotation: float,
    large_arc: bool,
    sweep: bool,
) -> tuple[Vector, float, float, float, float, float] | None:
    rx = abs(rx)
    ry = abs(ry)
    if rx == 0 or ry == 0 or start == end:
        return None

    phi = math.radians(x_axis_rotation % 360)
    cos_phi = math.cos(phi)
    sin_phi = math.sin(phi)
    dx = (start.x - end.x) / 2
    dy = (start.y - end.y) / 2
    x1_prime = cos_phi * dx + sin_phi * dy
    y1_prime = -sin_phi * dx + cos_phi * dy

    radius_check = x1_prime**2 / rx**2 + y1_prime**2 / ry**2
    if radius_check > 1:
        scale = math.sqrt(radius_check)
        rx *= scale
        ry *= scale

    numerator = (
        rx**2 * ry**2
        - rx**2 * y1_prime**2
        - ry**2 * x1_prime**2
    )
    denominator = rx**2 * y1_prime**2 + ry**2 * x1_prime**2
    coefficient = 0.0
    if denominator != 0:
        sign = -1 if large_arc == sweep else 1
        coefficient = sign * math.sqrt(max(0.0, numerator / denominator))

    cx_prime = coefficient * (rx * y1_prime / ry)
    cy_prime = coefficient * (-ry * x1_prime / rx)
    center = Vector(
        cos_phi * cx_prime - sin_phi * cy_prime + (start.x + end.x) / 2,
        sin_phi * cx_prime + cos_phi * cy_prime + (start.y + end.y) / 2,
    )

    start_vector = ((x1_prime - cx_prime) / rx, (y1_prime - cy_prime) / ry)
    end_vector = ((-x1_prime - cx_prime) / rx, (-y1_prime - cy_prime) / ry)
    start_angle = math.atan2(start_vector[1], start_vector[0])
    delta_angle = _angle_between(start_vector, end_vector)
    if not sweep and delta_angle > 0:
        delta_angle -= math.tau
    elif sweep and delta_angle < 0:
        delta_angle += math.tau

    return center, rx, ry, phi, start_angle, delta_angle


def _svg_arc_point(
    center: Vector,
    rx: float,
    ry: float,
    phi: float,
    angle: float,
) -> Vector:
    cos_phi = math.cos(phi)
    sin_phi = math.sin(phi)
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    return Vector(
        center.x + rx * cos_angle * cos_phi - ry * sin_angle * sin_phi,
        center.y + rx * cos_angle * sin_phi + ry * sin_angle * cos_phi,
    )


def _svg_arc_bbox_points(
    start: Vector,
    end: Vector,
    rx: float,
    ry: float,
    x_axis_rotation: float,
    large_arc: bool,
    sweep: bool,
) -> list[Vector]:
    parameters = _svg_arc_center_parameters(
        start, end, rx, ry, x_axis_rotation, large_arc, sweep
    )
    if parameters is None:
        return [end]

    center, rx, ry, phi, start_angle, delta_angle = parameters
    points = [end]
    cos_phi = math.cos(phi)
    sin_phi = math.sin(phi)
    candidate_angles = [
        math.atan2(-ry * sin_phi, rx * cos_phi),
        math.atan2(ry * cos_phi, rx * sin_phi),
    ]

    for angle in candidate_angles:
        for candidate in (angle, angle + math.pi):
            if _is_angle_on_arc(candidate, start_angle, delta_angle):
                points.append(_svg_arc_point(center, rx, ry, phi, candidate))

    return points


class SvgElement:
    _class_registry: ClassVar[dict[str, type["SvgElement"]]] = {}
    element: ET.Element

    @classmethod
    def register(cls, tag: str, subclass: type["SvgElement"]) -> None:
        cls._class_registry[tag] = subclass

    @classmethod
    def from_element(cls, element: ET.Element) -> "SvgElement":
        """
        Create an instance from an ElementTree element.
        Look up the local tag name and use the registered subclass if available.
        """
        local_tag = element.tag.split("}")[-1]
        subclass = cls._class_registry.get(local_tag, cls)
        if (
            subclass is not cls
            and getattr(subclass, "from_element", None) is not SvgElement.from_element
        ):
            return subclass.from_element(element)
        instance = subclass.__new__(subclass)
        instance.element = element
        return instance

    def __init__(self, tag: str, **kwargs: Any) -> None:
        self.element = ET.Element(qname(tag))
        for k, v in self.normalize_attrs(kwargs).items():
            self.element.set(k, str(v))

    @staticmethod
    def normalize_attrs(attrs: dict[str, object]) -> dict[str, object]:
        new_attrs: dict[str, object] = {}
        for k, v in attrs.items():
            if k == "class_name":
                new_attrs["class"] = v
            elif "_" in k:
                prefix, local_name = k.split("_", 1)
                if prefix in KNOWN_NAMESPACES:
                    new_attrs[ns_attr(prefix, local_name)] = v
                else:
                    new_attrs[k.replace("_", "-")] = v
            else:
                new_attrs[k] = v
        return new_attrs

    def attrs(self, attributes: dict[str, object]) -> Self:
        for key, value in self.normalize_attrs(attributes).items():
            if value is None:
                self.element.attrib.pop(key, None)
            else:
                self.element.set(key, str(value))
        return self

    def set_attr(self, name: str, value: AttributeValue) -> Self:
        self.attrs({name: value})
        return self

    def set_id(self, value: str | None) -> Self:
        return self.set_attr("id", value)

    def set_class(self, value: str | None) -> Self:
        return self.set_attr("class_name", value)

    def set_fill(self, value: AttributeValue) -> Self:
        return self.set_attr("fill", value)

    def set_stroke(
        self,
        value: AttributeValue,
        width: AttributeValue = None,
        linecap: str | None = None,
        linejoin: str | None = None,
    ) -> Self:
        attrs: dict[str, object] = {"stroke": value}
        if width is not None:
            attrs["stroke_width"] = width
        if linecap is not None:
            attrs["stroke_linecap"] = linecap
        if linejoin is not None:
            attrs["stroke_linejoin"] = linejoin
        self.attrs(attrs)
        return self

    def set_style(self, value: str | Mapping[str, AttributeValue] | None) -> Self:
        if value is None or isinstance(value, str):
            return self.set_attr("style", value)
        declarations = [
            f"{key.replace('_', '-')}: {style_value}"
            for key, style_value in value.items()
            if style_value is not None
        ]
        return self.set_attr("style", "; ".join(declarations))

    def set_position(self, x: PointLike | Real, y: Real | None = None) -> Self:
        point = _coerce_point_args(x, y)
        tag = self.element.tag.split("}")[-1]
        attr_x, attr_y = ("cx", "cy") if tag in {"circle", "ellipse"} else ("x", "y")
        self.attrs({attr_x: point.x, attr_y: point.y})
        return self

    def set_size(self, width: AttributeValue, height: AttributeValue) -> Self:
        self.attrs({"width": width, "height": height})
        return self

    def append(self, *children: Any) -> Self:
        for child in children:
            if hasattr(child, "element"):
                self.element.append(child.element)
                # Track the parent on the child.
                child._parent = self
            else:
                self.element.append(child)
        return self

    def remove(self, *children: Any) -> Self:
        for child in children:
            if hasattr(child, "element"):
                self.element.remove(child.element)
                if hasattr(child, "_parent"):
                    del child._parent
            else:
                self.element.remove(child)
        return self

    def to_string(self, pretty_print: bool = True) -> str:
        if pretty_print:
            element_copy = deepcopy(self.element)
            ET.indent(element_copy)
            return ET.tostring(element_copy, encoding="unicode")
        return ET.tostring(self.element, encoding="unicode")

    @override
    def __str__(self) -> str:
        return self.to_string(pretty_print=False)

    def __getattr__(self, name: str) -> str | int | float:
        if name == "class_name":
            if "class" in self.element.attrib:
                return self.element.attrib["class"]
            raise AttributeError(
                f"{type(self).__name__!r} object has no attribute 'class_name'"
            )
        attr_name = self._normalize_attr_name(name)
        if attr_name in self.element.attrib:
            val = self.element.attrib[attr_name]
            # Don't auto-convert id attribute to preserve leading zeros
            if attr_name == "id":
                return val
            try:
                if "." not in val and "e" not in val.lower():
                    return int(val)
                else:
                    return float(val)
            except ValueError:
                return val
        raise AttributeError(
            f"{type(self).__name__!r} object has no attribute {name!r}"
        )

    @override
    def __setattr__(self, name: str, value: object):
        # Map "class_name" to the SVG "class" attribute.
        if name == "class_name":
            attr_name = "class"
            if value is None:
                self.element.attrib.pop(attr_name, None)
            else:
                self.element.set(attr_name, str(value))
            return

        if name == "element" or name.startswith("_") or hasattr(type(self), name):
            object.__setattr__(self, name, value)
        else:
            attr_name = self._normalize_attr_name(name)
            if value is None:
                self.element.attrib.pop(attr_name, None)
            else:
                self.element.set(attr_name, str(value))

    @staticmethod
    def _normalize_attr_name(name: str) -> str:
        if "_" in name:
            prefix, local_name = name.split("_", 1)
            if prefix in KNOWN_NAMESPACES:
                return ns_attr(prefix, local_name)
        return name.replace("_", "-")

    def has_attr(self, name: str) -> bool:
        """
        Check if the element has the specified attribute.

        Args:
            name: The attribute name (underscores will be converted to hyphens)

        Returns:
            True if the attribute exists, False otherwise
        """
        if name == "class_name":
            return "class" in self.element.attrib
        attr_name = self._normalize_attr_name(name)
        return attr_name in self.element.attrib

    def find(
        self, tag: str, nested: bool = False, id: str | None = None
    ) -> "SvgElement | None":
        # Build the XPath for the tag.
        xpath = ".//" + qname(tag) if nested else qname(tag)
        # If an id is provided, add an attribute filter.
        if id is not None:
            xpath += f"[@id='{id}']"
        found = self.element.find(xpath)
        if found is not None:
            return SvgElement.from_element(found)
        return None

    def find_all(
        self, tag: str, nested: bool = False, class_name: str | None = None
    ) -> list["SvgElement"]:
        # Build the XPath for the tag.
        xpath = ".//" + qname(tag) if nested else qname(tag)
        # If a class is provided, add an attribute filter.
        if class_name is not None:
            xpath += f"[@class='{class_name}']"
        found_list = self.element.findall(xpath)
        return [SvgElement.from_element(el) for el in found_list]

    def copy(self) -> Self:
        """
        Create a deep copy of this SvgElement.
        The new copy has a deep-copied ElementTree element, so modifications
        to the copy won't affect the original.
        """
        # Create a deep copy of the element.
        new_element = deepcopy(self.element)
        # Create a new instance without calling __init__
        new_instance = self.__class__.__new__(self.__class__)
        new_instance.element = new_element
        return cast(Self, new_instance)


class Defs(SvgElement):
    def __init__(self, **kwargs: Any):
        super().__init__("defs", **kwargs)


class SvgDefinition(SvgElement):
    @property
    def id_ref(self) -> str:
        return f"url(#{self.id})"


class Stop(SvgElement):
    def __init__(
        self,
        offset: AttributeValue,
        color: str | None = None,
        opacity: AttributeValue = None,
        **kwargs: Any,
    ):
        if color is not None:
            kwargs["stop_color"] = color
        if opacity is not None:
            kwargs["stop_opacity"] = opacity
        super().__init__("stop", offset=offset, **kwargs)


class LinearGradient(SvgDefinition):
    def __init__(
        self,
        id: str | None = None,
        *,
        x1: AttributeValue = None,
        y1: AttributeValue = None,
        x2: AttributeValue = None,
        y2: AttributeValue = None,
        **kwargs: Any,
    ):
        if id is not None:
            kwargs["id"] = id
        for key, value in {"x1": x1, "y1": y1, "x2": x2, "y2": y2}.items():
            if value is not None:
                kwargs[key] = value
        super().__init__("linearGradient", **kwargs)

    def add_stop(
        self,
        offset: AttributeValue,
        color: str,
        opacity: AttributeValue = None,
        **kwargs: Any,
    ) -> Self:
        self.append(Stop(offset, color, opacity, **kwargs))
        return self


class RadialGradient(SvgDefinition):
    def __init__(
        self,
        id: str | None = None,
        *,
        cx: AttributeValue = None,
        cy: AttributeValue = None,
        r: AttributeValue = None,
        fx: AttributeValue = None,
        fy: AttributeValue = None,
        **kwargs: Any,
    ):
        if id is not None:
            kwargs["id"] = id
        attrs = {"cx": cx, "cy": cy, "r": r, "fx": fx, "fy": fy}
        for key, value in attrs.items():
            if value is not None:
                kwargs[key] = value
        super().__init__("radialGradient", **kwargs)

    def add_stop(
        self,
        offset: AttributeValue,
        color: str,
        opacity: AttributeValue = None,
        **kwargs: Any,
    ) -> Self:
        self.append(Stop(offset, color, opacity, **kwargs))
        return self


class Pattern(SvgDefinition):
    def __init__(self, id: str | None = None, **kwargs: Any):
        if id is not None:
            kwargs["id"] = id
        super().__init__("pattern", **kwargs)


class Mask(SvgDefinition):
    def __init__(self, id: str | None = None, **kwargs: Any):
        if id is not None:
            kwargs["id"] = id
        super().__init__("mask", **kwargs)


class ClipPath(SvgDefinition):
    def __init__(self, id: str | None = None, **kwargs: Any):
        if id is not None:
            kwargs["id"] = id
        super().__init__("clipPath", **kwargs)


class Filter(SvgDefinition):
    def __init__(self, id: str | None = None, **kwargs: Any):
        if id is not None:
            kwargs["id"] = id
        super().__init__("filter", **kwargs)


class Matrix2D:
    def __init__(
        self,
        a: Real = 1,
        b: Real = 0,
        c: Real = 0,
        d: Real = 1,
        e: Real = 0,
        f: Real = 0,
    ):
        self.a = float(a)
        self.b = float(b)
        self.c = float(c)
        self.d = float(d)
        self.e = float(e)
        self.f = float(f)

    @classmethod
    def identity(cls) -> "Matrix2D":
        return cls()

    @classmethod
    def translate(cls, x: Real, y: Real = 0) -> "Matrix2D":
        return cls(1, 0, 0, 1, x, y)

    @classmethod
    def scale(cls, x: Real, y: Real | None = None) -> "Matrix2D":
        return cls(x, 0, 0, x if y is None else y, 0, 0)

    @classmethod
    def scale_at(cls, x: Real, y: Real | None, cx: Real, cy: Real) -> "Matrix2D":
        return (
            cls.translate(cx, cy)
            .multiply(cls.scale(x, y))
            .multiply(cls.translate(-cx, -cy))
        )

    @classmethod
    def rotate(cls, angle: Real) -> "Matrix2D":
        radians = math.radians(angle)
        cos = math.cos(radians)
        sin = math.sin(radians)
        return cls(cos, sin, -sin, cos, 0, 0)

    @classmethod
    def skew_x(cls, angle: Real) -> "Matrix2D":
        return cls(1, 0, math.tan(math.radians(angle)), 1, 0, 0)

    @classmethod
    def skew_y(cls, angle: Real) -> "Matrix2D":
        return cls(1, math.tan(math.radians(angle)), 0, 1, 0, 0)

    def multiply(self, other: "Matrix2D") -> "Matrix2D":
        return Matrix2D(
            self.a * other.a + self.c * other.b,
            self.b * other.a + self.d * other.b,
            self.a * other.c + self.c * other.d,
            self.b * other.c + self.d * other.d,
            self.a * other.e + self.c * other.f + self.e,
            self.b * other.e + self.d * other.f + self.f,
        )

    def apply(self, x: Real, y: Real) -> Vector:
        return Vector(
            self.a * x + self.c * y + self.e,
            self.b * x + self.d * y + self.f,
        )

    def as_tuple(self) -> tuple[float, float, float, float, float, float]:
        return self.a, self.b, self.c, self.d, self.e, self.f

    @override
    def __str__(self) -> str:
        values = " ".join(_format_number(value) for value in self.as_tuple())
        return f"matrix({values})"

    @override
    def __repr__(self) -> str:
        values = ", ".join(_format_number(value) for value in self.as_tuple())
        return f"Matrix2D({values})"


class Transform:
    _arities: ClassVar[dict[str, tuple[int, ...]]] = {
        "matrix": (6,),
        "translate": (1, 2),
        "scale": (1, 2),
        "rotate": (1, 3),
        "skewX": (1,),
        "skewY": (1,),
    }

    def __init__(self, name: str, *values: Real):
        if name not in self._arities:
            raise ValueError(f"Unsupported transform function: {name}")
        if len(values) not in self._arities[name]:
            expected = " or ".join(str(arity) for arity in self._arities[name])
            raise ValueError(
                f"{name} transform expects {expected} values, got {len(values)}"
            )
        self.name = name
        self.values = tuple(float(value) for value in values)

    @classmethod
    def translate(cls, x: Real, y: Real = 0) -> "Transform":
        return cls("translate", x, y)

    @classmethod
    def scale(cls, x: Real, y: Real | None = None) -> "Transform":
        return cls("scale", x, x if y is None else y)

    @classmethod
    def rotate(cls, angle: Real, cx: Real | None = None, cy: Real | None = None):
        if cx is None and cy is None:
            return cls("rotate", angle)
        if cx is None or cy is None:
            raise ValueError("rotate pivot requires both cx and cy")
        return cls("rotate", angle, cx, cy)

    @classmethod
    def skew_x(cls, angle: Real) -> "Transform":
        return cls("skewX", angle)

    @classmethod
    def skew_y(cls, angle: Real) -> "Transform":
        return cls("skewY", angle)

    @classmethod
    def matrix(
        cls, a: Real, b: Real, c: Real, d: Real, e: Real, f: Real
    ) -> "Transform":
        return cls("matrix", a, b, c, d, e, f)

    def to_matrix(self) -> Matrix2D:
        if self.name == "matrix":
            return Matrix2D(*self.values)
        if self.name == "translate":
            x = self.values[0]
            y = self.values[1] if len(self.values) == 2 else 0
            return Matrix2D.translate(x, y)
        if self.name == "scale":
            x = self.values[0]
            y = self.values[1] if len(self.values) == 2 else x
            return Matrix2D.scale(x, y)
        if self.name == "rotate":
            angle = self.values[0]
            rotation = Matrix2D.rotate(angle)
            if len(self.values) == 1:
                return rotation
            cx, cy = self.values[1], self.values[2]
            return (
                Matrix2D.translate(cx, cy)
                .multiply(rotation)
                .multiply(Matrix2D.translate(-cx, -cy))
            )
        if self.name == "skewX":
            return Matrix2D.skew_x(self.values[0])
        if self.name == "skewY":
            return Matrix2D.skew_y(self.values[0])
        raise ValueError(f"Unsupported transform function: {self.name}")

    @override
    def __str__(self) -> str:
        separator = "," if self.name == "rotate" and len(self.values) == 3 else " "
        values = separator.join(_format_number(value) for value in self.values)
        return f"{self.name}({values})"

    @override
    def __repr__(self) -> str:
        values = ", ".join(_format_number(value) for value in self.values)
        return f"Transform({self.name!r}, {values})"


class TransformList:
    _transform_re: ClassVar[re.Pattern[str]] = re.compile(r"([A-Za-z][A-Za-z0-9]*)\(([^)]*)\)")

    def __init__(self, transforms: list[Transform] | None = None):
        self.transforms = transforms if transforms is not None else []

    @staticmethod
    def _parse_numbers(transform_name: str, value: str) -> list[float]:
        try:
            return [float(part) for part in value.replace(",", " ").split()]
        except ValueError as exc:
            raise ValueError(
                f"Invalid {transform_name} transform values: {value!r}"
            ) from exc

    @classmethod
    def parse(cls, value: str) -> "TransformList":
        transforms: list[Transform] = []
        pos = 0
        for match in cls._transform_re.finditer(value):
            if value[pos : match.start()].strip():
                raise ValueError(f"Invalid transform syntax: {value!r}")
            name = match.group(1)
            numbers = cls._parse_numbers(name, match.group(2))
            transforms.append(Transform(name, *numbers))
            pos = match.end()
        if value[pos:].strip():
            raise ValueError(f"Invalid transform syntax: {value!r}")
        return cls(transforms)

    def append(self, transform: Transform) -> "TransformList":
        self.transforms.append(transform)
        return self

    def first(self, name: str) -> Transform | None:
        return next(
            (transform for transform in self.transforms if transform.name == name),
            None,
        )

    def find_scale_pivot(self) -> tuple[Vector, int] | None:
        for index in range(len(self.transforms) - 2):
            first = self.transforms[index]
            second = self.transforms[index + 1]
            third = self.transforms[index + 2]
            if (
                first.name == "translate"
                and second.name == "scale"
                and third.name == "translate"
                and len(first.values) == 2
                and len(third.values) == 2
                and first.values[0] == -third.values[0]
                and first.values[1] == -third.values[1]
            ):
                return Vector(first.values[0], first.values[1]), index
        return None

    def replace_first(self, name: str, transform: Transform | None) -> None:
        for index, existing in enumerate(self.transforms):
            if existing.name == name:
                if transform is None:
                    del self.transforms[index]
                else:
                    self.transforms[index] = transform
                return
        if transform is not None:
            self.transforms.append(transform)

    def to_matrix(self) -> Matrix2D:
        matrix = Matrix2D.identity()
        for transform in self.transforms:
            matrix = matrix.multiply(transform.to_matrix())
        return matrix

    @override
    def __str__(self) -> str:
        return " ".join(str(transform) for transform in self.transforms)


class Transformable:
    """
    Mixin for applying transforms to an SVG element.
    The fixed order of operations is:
      1. rotate
      2. translate
      3. scale

    Note: Classes using this mixin must provide an `element` attribute.
    """

    element: ET.Element  # pyright: ignore[reportUninitializedInstanceVariable]

    def __init__(
        self,
        pos: PointLike | None = None,
        scale: Vector | None = None,
        angle: float = 0,
        *args: Any,
        **kwargs: Any,
    ):
        self._pos = _coerce_point(pos, "pos") if pos is not None else Vector(0, 0)
        self._scale = scale if scale is not None else Vector(1, 1)
        self._angle = angle
        self._update_transform()

    def _update_transform(self) -> None:
        parts: list[str] = []
        if self._angle != 0:
            parts.append(f"rotate({self._angle})")
        if self._pos != Vector(0, 0):
            parts.append(f"translate({self._pos.x} {self._pos.y})")
        if self._scale != Vector(1, 1):
            parts.append(f"scale({self._scale.x} {self._scale.y})")
        if parts:
            self.element.set("transform", " ".join(parts))
        else:
            self.element.attrib.pop("transform", None)

    @property
    def pos(self) -> Vector:
        return self._pos

    @pos.setter
    def pos(self, value: PointLike) -> None:
        self._pos = _coerce_point(value, "pos")
        self._update_transform()

    @property
    def scale(self) -> Vector:
        return self._scale

    @scale.setter
    def scale(self, value: Vector) -> None:
        self._scale = value
        self._update_transform()

    @property
    def angle(self) -> float:
        return self._angle

    @angle.setter
    def angle(self, value: float) -> None:
        self._angle = value
        self._update_transform()


class SVG(SvgElement):
    @staticmethod
    def _format_number(value: Real) -> str:
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return str(value)

    @staticmethod
    def _parse_svg_length(value: str | None) -> float | None:
        if value is None:
            return None
        match = re.match(r"^\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+))(?:[a-zA-Z%]*)\s*$", value)
        if not match:
            return None
        return float(match.group(1))

    @staticmethod
    def _parse_viewbox(value: str | None) -> tuple[float, float, float, float] | None:
        if value is None:
            return None
        parts = value.replace(",", " ").split()
        if len(parts) != 4:
            raise ValueError(f"viewBox must contain 4 numbers, got {len(parts)}")
        try:
            x, y, width, height = (float(part) for part in parts)
        except ValueError as exc:
            raise ValueError(f"Invalid viewBox values: {value!r}") from exc
        return x, y, width, height

    @classmethod
    def _fallback_viewbox_from_dimensions(
        cls, element: ET.Element
    ) -> tuple[float, float, float, float] | None:
        width = cls._parse_svg_length(element.get("width"))
        height = cls._parse_svg_length(element.get("height"))
        if width is None or height is None:
            return None
        return 0.0, 0.0, width, height

    @classmethod
    @override
    def from_element(cls, element: ET.Element):
        local_tag = element.tag.split("}")[-1]
        subclass = cls._class_registry.get(local_tag, cls)
        if subclass is not cls:
            return subclass.from_element(element)
        instance = cls.__new__(cls)
        instance.element = element
        return instance

    @classmethod
    def from_file(cls, filename: str) -> "SVG":
        _register_namespaces_from_file(filename)
        tree = ET.parse(filename)
        root = tree.getroot()
        viewbox = cls._parse_viewbox(root.get("viewBox"))
        if viewbox is None:
            viewbox = cls._fallback_viewbox_from_dimensions(root)
            if viewbox is not None:
                root.set(
                    "viewBox",
                    " ".join(cls._format_number(value) for value in viewbox),
                )
        instance = cls.__new__(cls)
        instance.element = root
        return instance

    @overload
    def __init__(self, width: Real, height: Real, **kwargs: Any) -> None: ...

    @overload
    def __init__(
        self, x: Real, y: Real, width: Real, height: Real, **kwargs: Any
    ) -> None: ...

    @overload
    def __init__(
        self, viewbox: tuple[Real, ...] | list[Real], **kwargs: Any
    ) -> None: ...

    def __init__(self, *viewbox: Any, **kwargs: Any) -> None:
        # Convert tuple of args to a single sequence if needed
        viewbox_seq: tuple[Real, ...] | list[Real]
        if len(viewbox) == 1 and isinstance(viewbox[0], (tuple, list)):
            # Unpack single tuple/list argument
            viewbox_seq = viewbox[0]  # type: ignore[assignment]
        else:
            # Multiple arguments passed directly
            viewbox_seq = viewbox  # type: ignore[assignment]

        # Validate dimensions
        if len(viewbox_seq) not in (2, 4):
            raise ValueError("viewbox must be a tuple or list of 2 or 4 numbers")

        # Create validated list with Real values
        validated_viewbox: list[Real] = []
        for item in viewbox_seq:
            if isinstance(item, (int, float)):
                validated_viewbox.append(item)
            else:
                raise ValueError(f"viewbox must contain only numbers, got {type(item)}")

        # Determine width and height before passing kwargs to super().__init__
        if len(validated_viewbox) == 4:
            vb = (
                f"{validated_viewbox[0]} {validated_viewbox[1]} "
                f"{validated_viewbox[2]} {validated_viewbox[3]}"
            )
            width = kwargs.pop("width", f"{validated_viewbox[2]}px")
            height = kwargs.pop("height", f"{validated_viewbox[3]}px")
        else:
            vb = f"0 0 {validated_viewbox[0]} {validated_viewbox[1]}"
            width = kwargs.pop("width", f"{validated_viewbox[0]}px")
            height = kwargs.pop("height", f"{validated_viewbox[1]}px")

        super().__init__("svg", **kwargs)

        self.attrs(
            {
                "viewBox": vb,
                "width": width,
                "height": height,
            }
        )

    @property
    def w(self) -> float:
        viewbox = self._parse_viewbox(self.element.get("viewBox"))
        if viewbox is not None:
            return viewbox[2]
        return self._parse_svg_length(self.element.get("width")) or 0.0

    @property
    def h(self) -> float:
        viewbox = self._parse_viewbox(self.element.get("viewBox"))
        if viewbox is not None:
            return viewbox[3]
        return self._parse_svg_length(self.element.get("height")) or 0.0

    def style(
        self, file_path: str, overwrite: bool = True, minify: bool = True
    ) -> None:
        """
        Add a <style> element to the SVG from an external CSS file.

        If overwrite is True, any existing <style> elements are removed and the
        new one is inserted as the first element of the SVG. Otherwise, the
        style element is appended.

        If minify is True, the CSS content is minified before insertion.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            css_content = f.read()

        if minify:

            def minify_css(css: str) -> str:
                # Remove CSS comments.
                css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
                # Remove extra whitespace around symbols.
                css = re.sub(r"\s*([\{\};:,\>])\s*", r"\1", css)
                # Collapse multiple spaces into one.
                css = re.sub(r"\s+", " ", css)
                return css.strip()

            css_content = minify_css(css_content)

        style_elem = SvgElement("style")
        style_elem.element.text = css_content

        if overwrite:
            for child in list(self.element):
                if child.tag == qname("style"):
                    self.element.remove(child)
            self.element.insert(0, style_elem.element)
        else:
            self.append(style_elem)

    def display(self) -> None:
        try:
            from IPython.display import SVG as IPythonSVG  # pyright: ignore[reportMissingImports]
            from IPython.display import display as ipython_display  # pyright: ignore[reportMissingImports, reportUnknownVariableType]
        except ImportError as exc:
            message = " ".join(
                [
                    "SVG.display() requires the optional notebook dependencies.",
                    "Install them with `pip install pydreamplet[notebook]` or",
                    "`uv add pydreamplet --extra notebook`.",
                ]
            )
            raise RuntimeError(
                message
            ) from exc

        ipython_display(IPythonSVG(self.to_string()))

    def save(self, filename: str, pretty_print: bool = False) -> None:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.to_string(pretty_print=pretty_print))

    def ensure_defs(self) -> Defs:
        existing = self.find("defs")
        if isinstance(existing, Defs):
            return existing
        defs = Defs()
        self.element.insert(0, defs.element)
        defs._parent = self
        return defs


class G(Transformable, SvgElement):  # pyright: ignore[reportUnsafeMultipleInheritance]
    """
    Group (<g>) element that combines Transformable behavior with SvgElement.

    Unlike the fixed order in Transformable (rotate, then translate, then scale),
    this class applies transforms based on the `order` attribute.
    By default, `order` is "trs", meaning:
      - translate
      - rotate
      - scale
    """

    def __init__(
        self,
        pos: PointLike | None = None,
        scale: Vector | None = None,
        angle: float = 0,
        pivot: PointLike | None = None,
        order: str = "trs",
        **kwargs: Any,
    ):
        # Set _order and _pivot before calling the base __init__ to avoid issues.
        self._order = order
        self._pivot = _coerce_point(pivot, "pivot") if pivot is not None else Vector(0, 0)
        self._transform_list = TransformList()
        SvgElement.__init__(self, "g", **kwargs)
        Transformable.__init__(self, pos=pos, scale=scale, angle=angle)
        self._update_transform()

    @property
    def pivot(self):
        return self._pivot

    @pivot.setter
    def pivot(self, value: PointLike):
        self._pivot = _coerce_point(value, "pivot")
        self._update_transform()

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, value: str):
        self._order = value
        self._update_transform()

    def remove(self, *children: Any) -> "G":
        super().remove(*children)
        if len(self.element) == 0 and hasattr(self, "_parent"):
            parent = getattr(self, "_parent")
            if isinstance(parent, SvgElement):
                parent.remove(self)
        return self

    @classmethod
    def _parse_transform(
        cls, transform: str
    ) -> tuple[Vector, float, Vector, Vector, TransformList]:
        """
        Parse SVG transform functions into legacy G state and a transform list.

        Malformed values raise ValueError instead of silently resetting to
        defaults. Transforms outside the legacy translate/rotate/scale model
        are preserved in the returned TransformList.
        """
        transform_list = TransformList.parse(transform)
        pos = Vector(0, 0)
        angle = 0.0
        scale = Vector(1, 1)
        pivot = Vector(0, 0)

        scale_pivot = transform_list.find_scale_pivot()
        scale_pivot_indices: set[int] = set()
        if scale_pivot is not None:
            pivot = scale_pivot[0]
            start = scale_pivot[1]
            scale_pivot_indices = {start, start + 2}

        translate = next(
            (
                transform
                for index, transform in enumerate(transform_list.transforms)
                if transform.name == "translate" and index not in scale_pivot_indices
            ),
            None,
        )
        if translate is not None:
            pos = Vector(
                translate.values[0],
                translate.values[1] if len(translate.values) == 2 else 0,
            )

        rotate = transform_list.first("rotate")
        if rotate is not None:
            angle = rotate.values[0]
            if len(rotate.values) == 3:
                pivot = Vector(rotate.values[1], rotate.values[2])

        parsed_scale = transform_list.first("scale")
        if parsed_scale is not None:
            scale = Vector(
                parsed_scale.values[0],
                parsed_scale.values[1]
                if len(parsed_scale.values) == 2
                else parsed_scale.values[0],
            )

        return pos, angle, scale, pivot, transform_list

    def attrs(self, attributes: dict[str, object]) -> "G":
        if "order" in attributes:
            self.order = str(attributes.pop("order"))  # use property setter
        if "pivot" in attributes:
            pivot_str = str(attributes.pop("pivot"))
            parts = TransformList._parse_numbers("pivot", pivot_str)
            if len(parts) != 2:
                raise ValueError(f"pivot expects 2 values, got {len(parts)}")
            self.pivot = Vector(parts[0], parts[1])

        if "transform" in attributes:
            transform_str = str(attributes.pop("transform"))
            pos, angle, scale, pivot, transform_list = self._parse_transform(
                transform_str
            )
            self._pos = pos
            self._angle = angle
            self._scale = scale
            self._pivot = pivot
            self._transform_list = transform_list
            self._update_transform()
        super().attrs(attributes)
        return self

    def _legacy_transforms(self, op: str) -> list[Transform]:
        if op == "t" and self._pos != Vector(0, 0):
            return [Transform.translate(self._pos.x, self._pos.y)]
        if op == "r" and self._angle != 0:
            if self._pivot and (self._pivot.x != 0 or self._pivot.y != 0):
                return [Transform.rotate(self._angle, self._pivot.x, self._pivot.y)]
            return [Transform.rotate(self._angle)]
        if op == "s" and self._scale != Vector(1, 1):
            scale = Transform.scale(self._scale.x, self._scale.y)
            if self._pivot and (self._pivot.x != 0 or self._pivot.y != 0):
                return [
                    Transform.translate(self._pivot.x, self._pivot.y),
                    scale,
                    Transform.translate(-self._pivot.x, -self._pivot.y),
                ]
            return [scale]
        return []

    def _legacy_transform(self, op: str) -> Transform | None:
        transforms = self._legacy_transforms(op)
        if len(transforms) == 1:
            return transforms[0]
        return None

    def _has_extra_transforms(self) -> bool:
        return any(
            transform.name not in {"translate", "rotate", "scale"}
            for transform in self._transform_list.transforms
        )

    def _update_transform(self):
        if self._has_extra_transforms():
            scale_transforms = self._legacy_transforms("s")
            if len(scale_transforms) > 1:
                extras = [
                    transform
                    for transform in self._transform_list.transforms
                    if transform.name not in {"translate", "rotate", "scale"}
                ]
                self._transform_list = TransformList(
                    [
                        transform
                        for op in self._order
                        for transform in self._legacy_transforms(op)
                    ]
                    + extras
                )
            else:
                self._transform_list.replace_first(
                    "translate", self._legacy_transform("t")
                )
                self._transform_list.replace_first("rotate", self._legacy_transform("r"))
                self._transform_list.replace_first("scale", self._legacy_transform("s"))
            transform = str(self._transform_list)
        else:
            transforms = [
                transform
                for op in self._order
                for transform in self._legacy_transforms(op)
            ]
            self._transform_list = TransformList(transforms)
            transform = str(self._transform_list)

        if transform:
            self.element.set("transform", transform)
        else:
            if "transform" in self.element.attrib:
                del self.element.attrib["transform"]

    @classmethod
    @override
    def from_element(cls, element: ET.Element):
        instance = cls.__new__(cls)
        instance.element = element
        transform = element.get("transform", "")
        pos, angle, scale, pivot, transform_list = cls._parse_transform(transform)
        instance._pos = pos
        instance._angle = angle
        instance._scale = scale
        instance._pivot = pivot
        instance._order = element.get("order", "trs")
        instance._transform_list = transform_list
        instance._update_transform()
        return instance


class Animate(SvgElement):
    def __init__(self, attr: str, **kwargs: Any):
        repeat_count = kwargs.pop("repeatCount", "indefinite")
        values_arg = kwargs.pop("values", None)
        dur = kwargs.pop("dur", "2s")
        super().__init__("animate", **kwargs)
        self._repeat_count: int | str = repeat_count
        self._values: list[Any] = []
        if isinstance(values_arg, list):
            self._values = values_arg
            self.attrs({"values": ";".join(str(v) for v in self._values)})
        kwargs.setdefault("dur", "2s")
        self.attrs(
            {
                "dur": dur,
                "attributeType": "XML",
                "attributeName": attr,
                "repeatCount": self._repeat_count,
            }
        )

    @property
    def repeat_count(self) -> int | str:
        return self._repeat_count

    @repeat_count.setter
    def repeat_count(self, value: int | str):
        self._repeat_count = value
        self.attrs({"repeatCount": value})

    @property
    def values(self) -> list[str]:
        return self._values

    @values.setter
    def values(self, value: list[Any]) -> None:
        self._values = value
        self.attrs({"values": ";".join([str(v) for v in value])})


class Circle(SvgElement):
    def __init__(
        self,
        *,
        pos: PointLike | None = None,
        cx: Real | None = None,
        cy: Real | None = None,
        r: Real | None = None,
        **kwargs: Any,
    ):
        if cx is not None:
            kwargs["cx"] = cx
        if cy is not None:
            kwargs["cy"] = cy
        if r is not None:
            kwargs["r"] = r
        super().__init__("circle", **kwargs)
        if pos is not None:
            self.pos = _coerce_point(pos, "pos")

    @property
    def pos(self) -> Vector:
        return Vector(
            float(self.element.get("cx", "0")), float(self.element.get("cy", "0"))
        )

    @pos.setter
    def pos(self, value: PointLike) -> None:
        point = _coerce_point(value, "pos")
        self.element.set("cx", str(point.x))
        self.element.set("cy", str(point.y))

    @property
    def radius(self):
        return float(self.element.get("r", 0))

    @radius.setter
    def radius(self, r: float) -> None:
        self.element.set("r", str(r))

    @property
    def center(self):
        return self.pos

    @property
    def diameter(self):
        return self.radius * 2

    @property
    def area(self):
        return math.pi * self.radius**2

    @property
    def bbox(self) -> BoundingBox:
        radius = self.radius
        center = self.pos
        return BoundingBox(center.x - radius, center.y - radius, radius * 2, radius * 2)


class Ellipse(SvgElement):
    def __init__(
        self,
        *,
        pos: PointLike | None = None,
        cx: Real | None = None,
        cy: Real | None = None,
        rx: Real | None = None,
        ry: Real | None = None,
        **kwargs: Any,
    ):
        if cx is not None:
            kwargs["cx"] = cx
        if cy is not None:
            kwargs["cy"] = cy
        if rx is not None:
            kwargs["rx"] = rx
        if ry is not None:
            kwargs["ry"] = ry
        super().__init__("ellipse", **kwargs)
        if pos is not None:
            self.pos = _coerce_point(pos, "pos")

    @property
    def pos(self) -> Vector:
        return Vector(
            float(self.element.get("cx", "0")), float(self.element.get("cy", "0"))
        )

    @pos.setter
    def pos(self, value: PointLike) -> None:
        point = _coerce_point(value, "pos")
        self.element.set("cx", str(point.x))
        self.element.set("cy", str(point.y))

    @property
    def bbox(self) -> BoundingBox:
        rx = float(self.element.get("rx", 0))
        ry = float(self.element.get("ry", 0))
        center = self.pos
        return BoundingBox(center.x - rx, center.y - ry, rx * 2, ry * 2)


class Rect(SvgElement):
    def __init__(
        self,
        *,
        pos: PointLike | None = None,
        x: Real | None = None,
        y: Real | None = None,
        width: Real | None = None,
        height: Real | None = None,
        **kwargs: Any,
    ):
        if x is not None:
            kwargs["x"] = x
        if y is not None:
            kwargs["y"] = y
        if width is not None:
            kwargs["width"] = width
        if height is not None:
            kwargs["height"] = height
        super().__init__("rect", **kwargs)
        if pos is not None:
            self.pos = _coerce_point(pos, "pos")

    @property
    def pos(self) -> Vector:
        return Vector(
            float(self.element.get("x", "0")), float(self.element.get("y", "0"))
        )

    @pos.setter
    def pos(self, value: PointLike) -> None:
        point = _coerce_point(value, "pos")
        self.element.set("x", str(point.x))
        self.element.set("y", str(point.y))

    @property
    def width(self):
        return float(self.element.get("width", 0))

    @property
    def height(self):
        return float(self.element.get("height", 0))

    @property
    def bbox(self) -> BoundingBox:
        x = self.pos.x
        y = self.pos.y
        width = self.width
        height = self.height
        left = min(x, x + width)
        top = min(y, y + height)
        return BoundingBox(left, top, abs(width), abs(height))


class Path(SvgElement):
    def __init__(self, d: str | PathBuilder = "", **kwargs: Any):
        super().__init__("path", **kwargs)
        self.d = d

    @property
    def d(self) -> str:
        return self.element.get("d", "")

    @d.setter
    def d(self, value: str | PathBuilder) -> None:
        path_data = value.to_string() if isinstance(value, PathBuilder) else value
        self.element.set("d", path_data)

    def _get_coordinates(self) -> list[Vector]:
        return extract_path_points(self.d)

    @property
    def w(self) -> float:
        points = self._get_coordinates()
        if not points:
            return 0
        xs = [p.x for p in points]
        return max(xs) - min(xs)

    @property
    def h(self) -> float:
        points = self._get_coordinates()
        if not points:
            return 0
        ys = [p.y for p in points]
        return max(ys) - min(ys)

    @property
    def center(self) -> Vector:
        points = self._get_coordinates()
        if not points:
            return Vector(0, 0)
        xs = [p.x for p in points]
        ys = [p.y for p in points]
        center_x = (max(xs) + min(xs)) / 2
        center_y = (max(ys) + min(ys)) / 2
        return Vector(center_x, center_y)

    @property
    def length(self) -> float:
        return path_length(self.d)

    def point_at(self, distance: Real) -> Vector:
        return point_at_length(self.d, distance)

    def tangent_at(self, distance: Real) -> Vector:
        return tangent_at_length(self.d, distance)

    @property
    def bbox(self) -> BoundingBox:
        points: list[Vector] = []
        current = Vector(0, 0)
        subpath_start = Vector(0, 0)
        previous_cubic_control: Vector | None = None
        previous_quadratic_control: Vector | None = None
        previous_command = ""

        for command in normalize_path_commands(self.d):
            if command.command == "M":
                current = Vector(command.values[0], command.values[1])
                subpath_start = current
                points.append(current)
                previous_cubic_control = None
                previous_quadratic_control = None
            elif command.command == "L":
                current = Vector(command.values[0], command.values[1])
                points.append(current)
                previous_cubic_control = None
                previous_quadratic_control = None
            elif command.command == "H":
                current = Vector(command.values[0], current.y)
                points.append(current)
                previous_cubic_control = None
                previous_quadratic_control = None
            elif command.command == "V":
                current = Vector(current.x, command.values[0])
                points.append(current)
                previous_cubic_control = None
                previous_quadratic_control = None
            elif command.command == "C":
                control1 = Vector(command.values[0], command.values[1])
                control2 = Vector(command.values[2], command.values[3])
                end = Vector(command.values[4], command.values[5])
                points.append(end)
                for t in _cubic_bezier_extrema(current, control1, control2, end):
                    points.append(_cubic_bezier_point(current, control1, control2, end, t))
                current = end
                previous_cubic_control = control2
                previous_quadratic_control = None
            elif command.command == "S":
                if previous_command in {"C", "S"} and previous_cubic_control is not None:
                    control1 = Vector(
                        2 * current.x - previous_cubic_control.x,
                        2 * current.y - previous_cubic_control.y,
                    )
                else:
                    control1 = current
                control2 = Vector(command.values[0], command.values[1])
                end = Vector(command.values[2], command.values[3])
                points.append(end)
                for t in _cubic_bezier_extrema(current, control1, control2, end):
                    points.append(_cubic_bezier_point(current, control1, control2, end, t))
                current = end
                previous_cubic_control = control2
                previous_quadratic_control = None
            elif command.command == "Q":
                control = Vector(command.values[0], command.values[1])
                end = Vector(command.values[2], command.values[3])
                points.append(end)
                for t in _quadratic_bezier_extrema(current, control, end):
                    points.append(_quadratic_bezier_point(current, control, end, t))
                current = end
                previous_cubic_control = None
                previous_quadratic_control = control
            elif command.command == "T":
                if (
                    previous_command in {"Q", "T"}
                    and previous_quadratic_control is not None
                ):
                    control = Vector(
                        2 * current.x - previous_quadratic_control.x,
                        2 * current.y - previous_quadratic_control.y,
                    )
                else:
                    control = current
                end = Vector(command.values[0], command.values[1])
                points.append(end)
                for t in _quadratic_bezier_extrema(current, control, end):
                    points.append(_quadratic_bezier_point(current, control, end, t))
                current = end
                previous_cubic_control = None
                previous_quadratic_control = control
            elif command.command == "A":
                end = Vector(command.values[5], command.values[6])
                points.extend(
                    _svg_arc_bbox_points(
                        current,
                        end,
                        command.values[0],
                        command.values[1],
                        command.values[2],
                        bool(command.values[3]),
                        bool(command.values[4]),
                    )
                )
                current = end
                previous_cubic_control = None
                previous_quadratic_control = None
            elif command.command == "Z":
                current = subpath_start
                points.append(current)
                previous_cubic_control = None
                previous_quadratic_control = None
            else:
                raise ValueError(f"Unsupported path command: {command.command}")
            previous_command = command.command

        return _bbox_from_points(points)


class Line(SvgElement):
    def __init__(
        self,
        x1: Real = 0,
        y1: Real = 0,
        x2: Real = 0,
        y2: Real = 0,
        **kwargs: Any,
    ):
        super().__init__("line", **kwargs)
        self.element.set("x1", str(x1))
        self.element.set("y1", str(y1))
        self.element.set("x2", str(x2))
        self.element.set("y2", str(y2))

    @property
    def x1(self) -> float:
        return float(self.element.get("x1", "0"))

    @x1.setter
    def x1(self, value: float):
        self.element.set("x1", str(value))

    @property
    def y1(self) -> float:
        return float(self.element.get("y1", "0"))

    @y1.setter
    def y1(self, value: float):
        self.element.set("y1", str(value))

    @property
    def x2(self) -> float:
        return float(self.element.get("x2", "0"))

    @x2.setter
    def x2(self, value: float):
        self.element.set("x2", str(value))

    @property
    def y2(self) -> float:
        return float(self.element.get("y2", "0"))

    @y2.setter
    def y2(self, value: float):
        self.element.set("y2", str(value))

    @property
    def length(self) -> float:
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1
        return math.hypot(dx, dy)

    @property
    def angle(self) -> float:
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1
        angle = math.degrees(math.atan2(dy, dx))
        if angle < 0:
            angle += 360
        return angle

    @property
    def bbox(self) -> BoundingBox:
        return _bbox_from_points(
            [Vector(self.x1, self.y1), Vector(self.x2, self.y2)]
        )


class Polygon(SvgElement):
    def __init__(self, points: list[Real], **kwargs: Any):
        super().__init__("polygon", **kwargs)
        self._points = points
        self._update_element()

    @property
    def points(self) -> list[Real]:
        return self._points

    @points.setter
    def points(self, value: list[Real]) -> None:
        self._points = value
        self._update_element()

    def _update_element(self):
        """Update the SVG 'points' attribute correctly."""
        _points_attribute_to_vectors(self._points)
        formatted_points = " ".join(
            [
                f"{self._points[i]},{self._points[i + 1]}"
                for i in range(0, len(self._points), 2)
            ]
        )
        self.element.set("points", formatted_points)

    @property
    def bbox(self) -> BoundingBox:
        return _bbox_from_points(_points_attribute_to_vectors(self.points))


class Polyline(SvgElement):
    def __init__(self, points: list[Real], **kwargs: Any):
        super().__init__("polyline", **kwargs)
        self._points = points
        self._update_element()

    @property
    def points(self) -> list[Real]:
        return self._points

    @points.setter
    def points(self, value: list[Real]) -> None:
        self._points = value
        self._update_element()

    def _update_element(self):
        """Update the SVG 'points' attribute correctly."""
        _points_attribute_to_vectors(self._points)
        formatted_points = " ".join(
            [
                f"{self._points[i]},{self._points[i + 1]}"
                for i in range(0, len(self._points), 2)
            ]
        )
        self.element.set("points", formatted_points)

    @property
    def bbox(self) -> BoundingBox:
        return _bbox_from_points(_points_attribute_to_vectors(self.points))


class Text(SvgElement):
    def __init__(
        self,
        initial_text: str = "",
        *,
        pos: PointLike | None = None,
        x: Real | None = None,
        y: Real | None = None,
        v_space: Real | None = None,
        **kwargs: Any,
    ):
        # Extract Text-specific kwargs before passing to parent
        if x is not None:
            kwargs["x"] = x
        if y is not None:
            kwargs["y"] = y

        super().__init__("text", **kwargs)

        if pos is not None:
            self.pos = _coerce_point(pos, "pos")

        self._v_space: float | None = v_space
        self._raw_text = initial_text
        if initial_text:
            self.content = initial_text

    @property
    def pos(self) -> Vector:
        return Vector(
            float(self.element.get("x", "0")), float(self.element.get("y", "0"))
        )

    @pos.setter
    def pos(self, value: PointLike) -> None:
        point = _coerce_point(value, "pos")
        self.element.set("x", str(point.x))
        self.element.set("y", str(point.y))

    @property
    def content(self) -> str:
        return self._raw_text

    @content.setter
    def content(self, new_text: str):
        self._raw_text = new_text
        for child in list(self.element):
            self.element.remove(child)
        if "\n" in new_text:
            self.element.text = None
            lines = new_text.split("\n")
            for i, line in enumerate(lines):
                tspan = ET.Element(qname("tspan"))
                if i == 0:
                    if "x" in self.element.attrib:
                        tspan.set("x", self.element.attrib["x"])
                    if "y" in self.element.attrib:
                        tspan.set("y", self.element.attrib["y"])
                else:
                    if "x" in self.element.attrib:
                        tspan.set("x", self.element.attrib["x"])
                    try:
                        dy_val = float(self.element.attrib.get("font-size", 16))
                    except ValueError:
                        dy_val = 16
                    if self._v_space is not None:
                        dy_val = self._v_space
                    tspan.set("dy", str(dy_val))
                tspan.text = line
                self.element.append(tspan)
        else:
            self.element.text = new_text

    @property
    def font_size(self) -> str | int | float:
        """
        Returns the numeric part of the font-size attribute.
        """
        fs = self.element.get("font-size", "16px")
        match = re.match(r"([0-9]+(?:\.[0-9]+)?)", fs)
        if match:
            return float(match.group(1))
        return 16.0

    @font_size.setter
    def font_size(self, value: str | int | float) -> None:
        """
        Sets the font-size attribute. If no unit is present in the provided value,
        "px" is appended.
        """
        value_str = str(value)
        # If no alphabetical characters (units) are present, default to px.
        if not re.search(r"[a-zA-Z]", value_str):
            value_str = f"{value_str}px"
        self.element.set("font-size", value_str)


class TextOnPath(SvgElement):
    text_path: SvgElement  # pyright: ignore[reportUninitializedInstanceVariable]

    def __init__(
        self,
        initial_text: str = "",
        path_id: str = "",
        text_path_args: dict[str, object] | None = None,
        **kwargs: Any,
    ):
        super().__init__("text", **kwargs)
        object.__setattr__(self, "text_path", SvgElement("textPath"))
        if text_path_args is None:
            text_path_args = {}
        if path_id:
            if path_id.startswith("#"):
                text_path_args.setdefault("href", path_id)
            else:
                text_path_args.setdefault("href", f"#{path_id}")
        self.text_path.attrs(text_path_args)
        self.append(self.text_path)
        self.content = initial_text

    @property
    def content(self) -> str:
        return self.text_path.element.text or ""

    @content.setter
    def content(self, new_text: str):
        self.text_path.element.text = new_text

    @property
    def font_size(self) -> str | int | float:
        """
        Returns the numeric part of the font-size attribute.
        """
        fs = self.element.get("font-size", "16px")
        match = re.match(r"([0-9]+(?:\.[0-9]+)?)", fs)
        if match:
            return float(match.group(1))
        return 16.0

    @font_size.setter
    def font_size(self, value: str | int | float) -> None:
        """
        Sets the font-size attribute on the text element. If no unit is provided,
        "px" is used as default.
        """
        value_str = str(value)
        if not re.search(r"[a-zA-Z]", value_str):
            value_str = f"{value_str}px"
        self.element.set("font-size", value_str)


# -----------------------------------------------------------------------------
# Register element classes so that find/find_all returns the proper type.
# -----------------------------------------------------------------------------
SvgElement.register("g", G)
SvgElement.register("defs", Defs)
SvgElement.register("stop", Stop)
SvgElement.register("linearGradient", LinearGradient)
SvgElement.register("radialGradient", RadialGradient)
SvgElement.register("pattern", Pattern)
SvgElement.register("mask", Mask)
SvgElement.register("clipPath", ClipPath)
SvgElement.register("filter", Filter)
SvgElement.register("circle", Circle)
SvgElement.register("ellipse", Ellipse)
SvgElement.register("rect", Rect)
SvgElement.register("path", Path)
SvgElement.register("polygon", Polygon)
SvgElement.register("polyline", Polyline)
SvgElement.register("line", Line)
SvgElement.register("text", Text)
SvgElement.register("textPath", TextOnPath)
