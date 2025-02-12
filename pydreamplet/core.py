import math
import re
import xml.etree.ElementTree as ET

from IPython.display import SVG as IPythonSVG
from IPython.display import display

from pydreamplet.constants import PI
from pydreamplet.math import Vector

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)


def qname(tag):
    return f"{{{SVG_NS}}}{tag}"


# -----------------------------------------------------------------------------
# Base SVG element with a registry so that find/find_all wrap elements with the
# appropriate specialized class.
# -----------------------------------------------------------------------------
class SvgElement:
    _class_registry = {}

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
        for key, value in self.normalize_attrs(attributes).items():
            self.element.set(key, value)
        return self

    def append(self, child):
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

    def tostring(self):
        return ET.tostring(self.element, encoding="unicode")

    def __str__(self):
        return self.tostring()

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
            self.element.set(name.replace("_", "-"), str(value))

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


# -----------------------------------------------------------------------------
# Transformable mixin used ONLY for group (<g>) elements.
# This version always outputs transforms in fixed order:
# translate, then rotate, then scale.
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Transformable mixin used ONLY for group (<g>) elements.
# This version always outputs transforms in the fixed order:
#   1. rotate
#   2. translate
#   3. scale
# -----------------------------------------------------------------------------
class Transformable:
    def __init__(
        self,
        pos: Vector = None,
        scale: Vector = None,
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


# -----------------------------------------------------------------------------
# The root SVG element.
# -----------------------------------------------------------------------------
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
        self.attrs(
            {
                "viewBox": vb,
                "width": f"{viewbox[0]}px",
                "height": f"{viewbox[1]}px",
            }
        )

    @property
    def width(self):
        viewbox = [int(v) for v in self.element.get("viewBox").split(" ")]
        return viewbox[2] - viewbox[0]

    @property
    def height(self):
        viewbox = [int(v) for v in self.element.get("viewBox").split(" ")]
        return viewbox[3] - viewbox[1]

    def display(self):
        display(IPythonSVG(self.tostring()))

    def save(self, filename):
        with open(filename, "w") as f:
            f.write(self.tostring())


# -----------------------------------------------------------------------------
# Group element <g> uses Transformable to control its translation, rotation, and scaling.
# -----------------------------------------------------------------------------
class G(Transformable, SvgElement):
    def __init__(
        self, pos: Vector = None, scale: Vector = None, angle: float = 0, **kwargs
    ):
        SvgElement.__init__(self, "g", **kwargs)
        Transformable.__init__(self, pos=pos, scale=scale, angle=angle)

    def remove(self, child):
        # Remove the specified child using the base method.
        super().remove(child)
        # If the group is now empty and it has a parent, remove the group from its parent.
        if len(self.element) == 0 and hasattr(self, "_parent"):
            parent = self._parent
            parent.remove(self)
        return self

    def attrs(self, attributes):
        if "transform" in attributes:
            transform_str = attributes.pop("transform")
            # Parse the transform string similar to from_element
            pos = Vector(0, 0)
            angle = 0
            scale = Vector(1, 1)
            m_rotate = re.search(r"rotate\(([^)]+)\)", transform_str)
            if m_rotate:
                try:
                    angle = float(m_rotate.group(1))
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
            # Update the element attribute from the internal state.
            self._update_transform()
        # Call the parent method for any other attributes.
        super().attrs(attributes)
        return self

    @classmethod
    def from_element(cls, element: ET.Element):
        instance = cls.__new__(cls)
        instance.element = element
        # Parse the transform attribute (same as before)
        transform = element.get("transform", "")
        pos = Vector(0, 0)
        angle = 0
        scale = Vector(1, 1)
        m_rotate = re.search(r"rotate\(([^)]+)\)", transform)
        if m_rotate:
            try:
                angle = float(m_rotate.group(1))
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
        instance._update_transform()
        return instance


# -----------------------------------------------------------------------------
# Animate element.
# -----------------------------------------------------------------------------
class Animate(SvgElement):
    def __init__(self, **kwargs):
        super().__init__("animate", **kwargs)
        self._repeat_count: int | str = "indefinite"
        self._values: list[int] = []
        self.attrs(
            {
                "attributeType": "XML",
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


# -----------------------------------------------------------------------------
# Shape and text elements (do not use transform); their position is controlled by native attributes.
# -----------------------------------------------------------------------------
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
        return PI * self.radius**2


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


class Text(SvgElement):
    def __init__(self, initial_text="", **kwargs):
        super().__init__("text", **kwargs)
        if "pos" in kwargs:
            pos = kwargs.pop("pos")
            self.element.set("x", str(pos.x))
            self.element.set("y", str(pos.y))
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
                    tspan.set("dy", str(dy_val))
                tspan.text = line
                self.element.append(tspan)
        else:
            self.element.text = new_text


class TextOnPath(SvgElement):
    def __init__(self, initial_text="", path="", text_path_args=None, **kwargs):
        super().__init__("text", **kwargs)
        object.__setattr__(self, "text_path", SvgElement("textPath"))
        if text_path_args is None:
            text_path_args = {}
        if path:
            text_path_args.setdefault("href", path)
        self.text_path.attrs(text_path_args)
        self.append(self.text_path)
        self.content = initial_text

    @property
    def content(self) -> str:
        return self.text_path.element.text or ""

    @content.setter
    def content(self, new_text: str):
        self.text_path.element.text = new_text


# -----------------------------------------------------------------------------
# Register element classes so that find/find_all returns the proper type.
# -----------------------------------------------------------------------------
SvgElement.register("g", G)
SvgElement.register("circle", Circle)
SvgElement.register("ellipse", Ellipse)
SvgElement.register("rect", Rect)
SvgElement.register("path", Path)
SvgElement.register("line", Line)
SvgElement.register("text", Text)
SvgElement.register("textPath", TextOnPath)
