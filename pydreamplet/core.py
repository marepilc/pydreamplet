import math
import re
import xml.etree.ElementTree as ET
from copy import deepcopy
from typing import Any, Optional

from IPython.display import SVG as IPythonSVG
from IPython.display import display

from pydreamplet.math import Vector

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)


def qname(tag):
    return f"{{{SVG_NS}}}{tag}"


class SvgElement:
    _class_registry: dict[str, Any] = {}

    @classmethod
    def register(cls, tag: str, subclass: type) -> None:
        cls._class_registry[tag] = subclass

    @classmethod
    def from_element(cls, element: ET.Element):
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

    def __init__(self, tag, **kwargs):
        object.__setattr__(self, "element", ET.Element(qname(tag)))
        for k, v in self.normalize_attrs(kwargs).items():
            self.element.set(k, str(v))

    @staticmethod
    def normalize_attrs(attrs):
        return {k.replace("_", "-"): str(v) for k, v in attrs.items()}

    def attrs(self, attributes):
        for key, value in attributes.items():
            attr_key = key.replace("_", "-")
            if value is None:
                self.element.attrib.pop(attr_key, None)
            else:
                self.element.set(attr_key, str(value))
        return self

    def append(self, *children):
        for child in children:
            if hasattr(child, "element"):
                self.element.append(child.element)
                # Track the parent on the child.
                child._parent = self
            else:
                self.element.append(child)
        return self

    def remove(self, child):
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

    def __str__(self):
        return self.to_string(pretty_print=False)

    def __getattr__(self, name):
        attr_name = name.replace("_", "-")
        if attr_name in self.element.attrib:
            val = self.element.attrib[attr_name]
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

    def __setattr__(self, name, value):
        if name == "element" or name.startswith("_") or hasattr(type(self), name):
            object.__setattr__(self, name, value)
        else:
            attr_name = name.replace("_", "-")
            if value is None:
                self.element.attrib.pop(attr_name, None)
            else:
                self.element.set(attr_name, str(value))

    def find(self, tag, nested=False):
        if nested:
            found = self.element.find(".//" + qname(tag))
        else:
            found = self.element.find(qname(tag))
        if found is not None:
            return SvgElement.from_element(found)
        return None

    def find_all(self, tag, nested=False):
        if nested:
            found_list = self.element.findall(".//" + qname(tag))
        else:
            found_list = self.element.findall(qname(tag))
        return (SvgElement.from_element(el) for el in found_list)


class Transformable:
    """
    Mixin for applying transforms to an SVG element.
    The fixed order of operations is:
      1. rotate
      2. translate
      3. scale

    Note: Classes using this mixin must provide an `element` attribute.
    """

    element: ET.Element

    def __init__(
        self,
        pos: Optional[Vector] = None,
        scale: Optional[Vector] = None,
        angle: float = 0,
        *args,
        **kwargs,
    ):
        self._pos = pos if pos is not None else Vector(0, 0)
        self._scale = scale if scale is not None else Vector(1, 1)
        self._angle = angle
        self._update_transform()

    def _update_transform(self) -> None:
        parts = []
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
    def pos(self, value: Vector) -> None:
        self._pos = value
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
    @classmethod
    def from_element(cls, element: ET.Element):
        local_tag = element.tag.split("}")[-1]
        subclass = cls._class_registry.get(local_tag, cls)
        if subclass is not cls:
            return subclass.from_element(element)
        instance = cls.__new__(cls)
        instance.element = element
        return instance

    @classmethod
    def from_file(cls, filename):
        tree = ET.parse(filename)
        root = tree.getroot()
        instance = cls(tuple(map(int, root.get("viewBox").split())))
        instance.element = root
        return instance

    def __init__(self, *viewbox, **kwargs):
        if len(viewbox) == 1 and isinstance(viewbox[0], (tuple, list)):
            viewbox = viewbox[0]
        if len(viewbox) not in (2, 4):
            raise ValueError("viewbox must be a tuple or list of 2 or 4 numbers")
        super().__init__("svg", **kwargs)
        if len(viewbox) == 4:
            vb = f"{viewbox[0]} {viewbox[1]} {viewbox[2]} {viewbox[3]}"
        else:
            vb = f"0 0 {viewbox[0]} {viewbox[1]}"

        if "width" not in kwargs:
            kwargs["width"] = f"{viewbox[0]}px"
        if "height" not in kwargs:
            kwargs["height"] = f"{viewbox[1]}px"
        self.attrs(
            {
                "viewBox": vb,
                "width": kwargs.pop("width"),
                "height": kwargs.pop("height"),
            }
        )

    @property
    def w(self):
        viewbox = [int(v) for v in self.element.get("viewBox").split(" ")]
        return viewbox[2]

    @property
    def h(self):
        viewbox = [int(v) for v in self.element.get("viewBox").split(" ")]
        return viewbox[3]

    def style(
        self, file_path: str, overwrite: bool = True, minify: bool = True
    ) -> None:
        """
        Add a <style> element to the SVG from an external CSS file.

        If overwrite is True, any existing <style> elements are removed and the new one
        is inserted as the first element of the SVG. Otherwise, the style element is appended.

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

    def display(self):
        display(IPythonSVG(self.to_string()))

    def save(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.to_string())


class G(Transformable, SvgElement):
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
        pos: Optional[Vector] = None,
        scale: Optional[Vector] = None,
        angle: float = 0,
        pivot: Optional[Vector] = None,
        order: str = "trs",
        **kwargs,
    ):
        # Set _order and _pivot before calling the base __init__ to avoid issues.
        self._order = order
        self._pivot = pivot if pivot is not None else Vector(0, 0)
        SvgElement.__init__(self, "g", **kwargs)
        Transformable.__init__(self, pos=pos, scale=scale, angle=angle)
        self._update_transform()

    @property
    def pivot(self):
        return self._pivot

    @pivot.setter
    def pivot(self, value: Vector):
        self._pivot = value
        self._update_transform()

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, value: str):
        self._order = value
        self._update_transform()

    def remove(self, child):
        super().remove(child)
        if len(self.element) == 0 and hasattr(self, "_parent"):
            parent = self._parent
            parent.remove(self)
        return self

    def attrs(self, attributes):
        if "order" in attributes:
            self.order = attributes.pop("order")  # use property setter
        if "pivot" in attributes:
            pivot_str = attributes.pop("pivot")
            try:
                parts = pivot_str.replace(",", " ").split()
                if len(parts) >= 2:
                    self.pivot = Vector(float(parts[0]), float(parts[1]))
            except Exception:
                pass

        if "transform" in attributes:
            transform_str = attributes.pop("transform")
            pos = Vector(0, 0)
            angle = 0
            scale = Vector(1, 1)
            pivot = Vector(0, 0)
            m_rotate = re.search(r"rotate\(([^)]+)\)", transform_str)
            if m_rotate:
                try:
                    parts = m_rotate.group(1).replace(",", " ").split()
                    if len(parts) >= 1:
                        angle = float(parts[0])
                    if len(parts) >= 3:
                        pivot = Vector(float(parts[1]), float(parts[2]))
                except Exception:
                    pass
            m_translate = re.search(r"translate\(([^)]+)\)", transform_str)
            if m_translate:
                try:
                    parts = m_translate.group(1).split()
                    if len(parts) >= 2:
                        pos = Vector(float(parts[0]), float(parts[1]))
                except Exception:
                    pass
            m_scale = re.search(r"scale\(([^)]+)\)", transform_str)
            if m_scale:
                try:
                    parts = m_scale.group(1).split()
                    if len(parts) == 1:
                        s = float(parts[0])
                        scale = Vector(s, s)
                    elif len(parts) >= 2:
                        scale = Vector(float(parts[0]), float(parts[1]))
                except Exception:
                    pass
            self._pos = pos
            self._angle = angle
            self._scale = scale
            # Use parsed pivot only if not already set.
            if not hasattr(self, "_pivot") or self._pivot is None:
                self._pivot = pivot
            self._update_transform()
        super().attrs(attributes)
        return self

    def _update_transform(self):
        # Check if all transformations are at their default values.
        if (
            self._pos == Vector(0, 0)
            and self._angle == 0
            and self._scale == Vector(1, 1)
        ):
            # Remove any existing transform attribute and exit.
            if "transform" in self.element.attrib:
                del self.element.attrib["transform"]
            return

        parts = []
        for op in self._order:
            if op == "t" and self._pos != Vector(0, 0):
                parts.append(f"translate({self._pos.x} {self._pos.y})")
            elif op == "r" and self._angle != 0:
                if self._pivot and (self._pivot.x != 0 or self._pivot.y != 0):
                    parts.append(
                        f"rotate({self._angle},{self._pivot.x},{self._pivot.y})"
                    )
                else:
                    parts.append(f"rotate({self._angle})")
            elif op == "s" and self._scale != Vector(1, 1):
                parts.append(f"scale({self._scale.x} {self._scale.y})")
        # Set the transform attribute only if there is at least one transform.
        if parts:
            self.element.set("transform", " ".join(parts))
        else:
            if "transform" in self.element.attrib:
                del self.element.attrib["transform"]

    @classmethod
    def from_element(cls, element: ET.Element):
        instance = cls.__new__(cls)
        instance.element = element
        transform = element.get("transform", "")
        pos = Vector(0, 0)
        angle: float = 0
        scale = Vector(1, 1)
        pivot = Vector(0, 0)
        m_rotate = re.search(r"rotate\(([^)]+)\)", transform)
        if m_rotate:
            try:
                parts = m_rotate.group(1).replace(",", " ").split()
                if len(parts) >= 1:
                    angle = float(parts[0])
                if len(parts) >= 3:
                    pivot = Vector(float(parts[1]), float(parts[2]))
            except Exception:
                pass
        m_translate = re.search(r"translate\(([^)]+)\)", transform)
        if m_translate:
            try:
                parts = m_translate.group(1).split()
                if len(parts) >= 2:
                    pos = Vector(float(parts[0]), float(parts[1]))
            except Exception:
                pass
        m_scale = re.search(r"scale\(([^)]+)\)", transform)
        if m_scale:
            try:
                parts = m_scale.group(1).split()
                if len(parts) == 1:
                    s = float(parts[0])
                    scale = Vector(s, s)
                elif len(parts) >= 2:
                    scale = Vector(float(parts[0]), float(parts[1]))
            except Exception:
                pass
        instance._pos = pos
        instance._angle = angle
        instance._scale = scale
        instance._pivot = pivot
        instance._order = element.get("order", "trs")
        instance._update_transform()
        return instance


class Animate(SvgElement):
    def __init__(self, attr: str, **kwargs):
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
    def repeat_count(self, value):
        self._repeat_count = value
        self.attrs({"repeatCount": value})

    @property
    def values(self) -> list[str]:
        return self._values

    @values.setter
    def values(self, value):
        self._values = value
        self.attrs({"values": ";".join([str(v) for v in value])})


class Circle(SvgElement):
    def __init__(self, **kwargs):
        super().__init__("circle", **kwargs)
        if "pos" in kwargs:
            pos = kwargs.pop("pos")
            self.element.set("cx", str(pos.x))
            self.element.set("cy", str(pos.y))

    @property
    def pos(self) -> Vector:
        return Vector(
            float(self.element.get("cx", "0")), float(self.element.get("cy", "0"))
        )

    @pos.setter
    def pos(self, value: Vector) -> None:
        self.element.set("cx", str(value.x))
        self.element.set("cy", str(value.y))

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


class Ellipse(SvgElement):
    def __init__(self, **kwargs):
        super().__init__("ellipse", **kwargs)
        if "pos" in kwargs:
            pos = kwargs.pop("pos")
            self.element.set("cx", str(pos.x))
            self.element.set("cy", str(pos.y))

    @property
    def pos(self) -> Vector:
        return Vector(
            float(self.element.get("cx", "0")), float(self.element.get("cy", "0"))
        )

    @pos.setter
    def pos(self, value: Vector) -> None:
        self.element.set("cx", str(value.x))
        self.element.set("cy", str(value.y))


class Rect(SvgElement):
    def __init__(self, **kwargs):
        super().__init__("rect", **kwargs)
        if "pos" in kwargs:
            pos = kwargs.pop("pos")
            self.element.set("x", str(pos.x))
            self.element.set("y", str(pos.y))

    @property
    def pos(self) -> Vector:
        return Vector(
            float(self.element.get("x", "0")), float(self.element.get("y", "0"))
        )

    @pos.setter
    def pos(self, value: Vector) -> None:
        self.element.set("x", str(value.x))
        self.element.set("y", str(value.y))

    @property
    def width(self):
        return float(self.element.get("width", 0))

    @property
    def height(self):
        return float(self.element.get("height", 0))


class Path(SvgElement):
    def __init__(self, d: str = "", **kwargs):
        super().__init__("path", **kwargs)
        self.d = d

    @property
    def d(self) -> str:
        return self.element.get("d", "")

    @d.setter
    def d(self, value: str) -> None:
        self.element.set("d", value)

    def _get_coordinates(self):
        """
        Parse the path 'd' attribute to extract all numbers and group them into (x, y) pairs.
        This is a simplistic parser that assumes the path string is composed of commands that use
        coordinate pairs (e.g., "M10 20 L110 20 L110 70 L10 70 Z").
        """
        # Find all numbers (including floats and scientific notation)
        numbers = re.findall(r"[-+]?\d*\.?\d+(?:e[-+]?\d+)?", self.d)
        coords = [float(num) for num in numbers]
        if len(coords) % 2 != 0:
            raise ValueError(
                "Path 'd' attribute does not contain pairs of coordinates."
            )
        points = [Vector(coords[i], coords[i + 1]) for i in range(0, len(coords), 2)]
        return points

    @property
    def width(self) -> float:
        points = self._get_coordinates()
        if not points:
            return 0
        xs = [p.x for p in points]
        return max(xs) - min(xs)

    @property
    def height(self) -> float:
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


class Line(SvgElement):
    def __init__(self, x1=0, y1=0, x2=0, y2=0, **kwargs):
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


class Polygon(SvgElement):
    def __init__(self, points: list[int | float], **kwargs):
        super().__init__("polygon", **kwargs)
        self._points = points
        self._update_element()

    @property
    def points(self) -> list[int | float]:
        return self._points

    @points.setter
    def points(self, value: list[int | float]) -> None:
        self._points = value
        self._update_element()

    def _update_element(self):
        """Update the SVG 'points' attribute correctly."""
        formatted_points = " ".join(
            [
                f"{self._points[i]},{self._points[i + 1]}"
                for i in range(0, len(self._points), 2)
            ]
        )
        self.element.set("points", formatted_points)


class Polyline(SvgElement):
    def __init__(self, points: list[int | float], **kwargs):
        super().__init__("polyline", **kwargs)
        self._points = points
        self._update_element()

    @property
    def points(self) -> list[int | float]:
        return self._points

    @points.setter
    def points(self, value: list[int | float]) -> None:
        self._points = value
        self._update_element()

    def _update_element(self):
        """Update the SVG 'points' attribute correctly."""
        formatted_points = " ".join(
            [
                f"{self._points[i]},{self._points[i + 1]}"
                for i in range(0, len(self._points), 2)
            ]
        )
        self.element.set("points", formatted_points)


class Text(SvgElement):
    def __init__(self, initial_text="", **kwargs):
        super().__init__("text", **kwargs)
        if "pos" in kwargs:
            pos = kwargs.pop("pos")
            self.element.set("x", str(pos.x))
            self.element.set("y", str(pos.y))
        if "v_space" in kwargs:
            self._v_space = kwargs.pop("v_space")
        else:
            self._v_space = None
        self._raw_text = initial_text
        if initial_text:
            self.content = initial_text

    @property
    def pos(self) -> Vector:
        return Vector(
            float(self.element.get("x", "0")), float(self.element.get("y", "0"))
        )

    @pos.setter
    def pos(self, value: Vector) -> None:
        self.element.set("x", str(value.x))
        self.element.set("y", str(value.y))

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
    def font_size(self) -> float:
        """
        Returns the numeric part of the font-size attribute.
        """
        fs = self.element.get("font-size", "16px")
        match = re.match(r"([0-9]+(?:\.[0-9]+)?)", fs)
        if match:
            return float(match.group(1))
        return 16.0

    @font_size.setter
    def font_size(self, value: str) -> None:
        """
        Sets the font-size attribute. If no unit is present in the provided value,
        "px" is appended.
        """
        # If no alphabetical characters (units) are present, default to px.
        if not re.search(r"[a-zA-Z]", value):
            value = f"{value}px"
        self.element.set("font-size", value)


class TextOnPath(SvgElement):
    def __init__(self, initial_text="", path_id="", text_path_args=None, **kwargs):
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
    def font_size(self) -> float:
        """
        Returns the numeric part of the font-size attribute.
        """
        fs = self.element.get("font-size", "16px")
        match = re.match(r"([0-9]+(?:\.[0-9]+)?)", fs)
        if match:
            return float(match.group(1))
        return 16.0

    @font_size.setter
    def font_size(self, value: str) -> None:
        """
        Sets the font-size attribute on the text element. If no unit is provided,
        "px" is used as default.
        """
        if not re.search(r"[a-zA-Z]", value):
            value = f"{value}px"
        self.element.set("font-size", value)


# -----------------------------------------------------------------------------
# Register element classes so that find/find_all returns the proper type.
# -----------------------------------------------------------------------------
SvgElement.register("g", G)
SvgElement.register("circle", Circle)
SvgElement.register("ellipse", Ellipse)
SvgElement.register("rect", Rect)
SvgElement.register("path", Path)
SvgElement.register("polygon", Polygon)
SvgElement.register("polyline", Polyline)
SvgElement.register("line", Line)
SvgElement.register("text", Text)
SvgElement.register("textPath", TextOnPath)
