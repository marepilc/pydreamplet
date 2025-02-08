import xml.etree.ElementTree as ET

from IPython.display import SVG as IPythonSVG
from IPython.display import display

from pydreamplet.constants import PI

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)


def qname(tag):
    return f"{{{SVG_NS}}}{tag}"


class SvgElement:
    def __init__(self, tag, **kwargs):
        # Use object.__setattr__ to avoid triggering our custom __setattr__
        object.__setattr__(self, "element", ET.Element(qname(tag)))
        for k, v in self.normalize_attrs(kwargs).items():
            self.element.set(k, str(v))

    @staticmethod
    def normalize_attrs(attrs):
        """Convert keys replacing underscores with hyphens."""
        return {k.replace("_", "-"): str(v) for k, v in attrs.items()}

    def attrs(self, attributes):
        for key, value in self.normalize_attrs(attributes).items():
            self.element.set(key, value)
        return self

    def append(self, child):
        if hasattr(child, "element"):
            self.element.append(child.element)
        else:
            self.element.append(child)

    def remove(self, child):
        if hasattr(child, "element"):
            self.element.remove(child.element)
        else:
            self.element.remove(child)

    def tostring(self):
        return ET.tostring(self.element, encoding="unicode")

    def __str__(self):
        return self.tostring()

    def __getattr__(self, name):
        # This is only called if the attribute wasn't found normally.
        attr_name = name.replace("_", "-")
        if attr_name in self.element.attrib:
            val = self.element.attrib[attr_name]
            # Try to convert to a number if possible.
            try:
                # If there's no decimal point or exponent, convert to int.
                if "." not in val and "e" not in val.lower():
                    return int(val)
                else:
                    return float(val)
            except ValueError:
                # If conversion fails, return the original string.
                return val
        raise AttributeError(
            f"{type(self).__name__!r} object has no attribute {name!r}"
        )

    def __setattr__(self, name, value):
        # If the attribute is one of our internal attributes or methods,
        # set it normally. Otherwise, store it as an SVG attribute.
        if name == "element" or name.startswith("_") or hasattr(type(self), name):
            object.__setattr__(self, name, value)
        else:
            # Convert underscores to hyphens for attribute names.
            self.element.set(name.replace("_", "-"), str(value))


class SVG(SvgElement):
    def __init__(
        self, dimensions=(300, 300), viewbox: tuple[int] | None = None, **kwargs
    ):
        """
        Create an SVG root element.

        Parameters:
          dimensions: tuple with 2 numbers [width, height] (e.g. (300, 300))
          viewbox: tuple of 2 or 4 numbers.
                   - If 2 numbers, treated as [width, height] with origin (0, 0).
                   - If 4 numbers, treated as [minX, minY, width, height].
        """
        super().__init__("svg", **kwargs)
        self.attrs({"width": dimensions[0], "height": dimensions[1]})
        if not viewbox:
            vb = f"0 0 {dimensions[0]} {dimensions[1]}"
        else:
            if len(viewbox) == 4:
                vb = f"{viewbox[0]} {viewbox[1]} {viewbox[2]} {viewbox[3]}"
            elif len(viewbox) == 2:
                vb = f"0 0 {viewbox[0]} {viewbox[1]}"
            else:
                raise ValueError("viewbox must be a list or tuple of 2 or 4 numbers")
        self.attrs({"viewBox": vb})

    def display(self):
        display(IPythonSVG(self.tostring()))

    def save(self, filename):
        with open(filename, "w") as f:
            f.write(self.tostring())


class Animate(SvgElement):
    def __init__(self, **kwargs):
        """
        Create an animate element. Accepts attributes like attributeName, from, to, etc.
        """
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


class Circle(SvgElement):
    def __init__(self, **kwargs):
        """
        Create a circle element. Accepts attributes like cx, cy, r, etc.
        """
        super().__init__("circle", **kwargs)

    @property
    def radius(self):
        return float(self.element.get("r", 0))

    @property
    def center(self):
        return (float(self.element.get("cx", 0)), float(self.element.get("cy", 0)))

    @property
    def diameter(self):
        return self.radius * 2

    @property
    def area(self):
        return PI * self.radius**2


class Ellipse(SvgElement):
    def __init__(self, **kwargs):
        """
        Create an ellipse element. Accepts attributes like cx, cy, rx, ry, etc.
        """
        super().__init__("ellipse", **kwargs)


class Rect(SvgElement):
    def __init__(self, **kwargs):
        """
        Create a rectangle element. Accepts attributes like x, y, width, height, etc.
        """
        super().__init__("rect", **kwargs)


class Text(SvgElement):
    def __init__(self, initial_text="", **kwargs):
        """
        Create a text element.

        Args:
          initial_text: The initial text to display.
          kwargs: Additional SVG attributes (e.g. font_family, font_size, font_weight).
        """
        super().__init__("text", **kwargs)
        self._raw_text = initial_text
        if initial_text:
            self.content = initial_text  # Use the property setter

    @property
    def content(self) -> str:
        """Return the current text content (raw string)."""
        return self._raw_text

    @content.setter
    def content(self, new_text: str):
        """Update the text content and rebuild child <tspan> elements as needed."""
        self._raw_text = new_text
        # Clear any existing child elements.
        for child in list(self.element):
            self.element.remove(child)

        if "\n" in new_text:
            self.element.text = None
            lines = new_text.split("\n")
            for i, line in enumerate(lines):
                tspan = ET.Element(qname("tspan"))
                # For the first line, if x and y exist on the parent, set them.
                if i == 0:
                    if "x" in self.element.attrib:
                        tspan.set("x", self.element.attrib["x"])
                    if "y" in self.element.attrib:
                        tspan.set("y", self.element.attrib["y"])
                else:
                    # For subsequent lines, copy x and add a dy offset.
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
            # For single-line text, set the text directly.
            self.element.text = new_text

    # def dimensions(self, measurer: TypographyMeasurer) -> tuple[float, float]:
    #     """
    #     Returns the (width, height) of the text element using the TypographyMeasurer.
    #     Uses the stored raw text and relevant font attributes.
    #     """
    #     font_family = self.element.attrib.get("font-family", "Arial")
    #     try:
    #         font_size = float(self.element.attrib.get("font-size", "16"))
    #     except ValueError:
    #         font_size = 16
    #     try:
    #         font_weight = int(self.element.attrib.get("font-weight", 400))
    #     except ValueError:
    #         font_weight = 400

    #     return measurer.measure_text(
    #         self._raw_text, font_family, font_weight, font_size
    #     )

    # def width(self, measurer: TypographyMeasurer) -> float:
    #     """Return the width of the text element."""
    #     return self.dimensions(measurer)[0]

    # def height(self, measurer: TypographyMeasurer) -> float:
    #     """Return the height of the text element."""
    #     return self.dimensions(measurer)[1]
