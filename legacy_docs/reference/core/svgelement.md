# `SvgElement`

The `SvgElement` class serves as the base for all SVG elements. It wraps an ElementTree element, provides a registry for specialized classes, and offers methods for managing attributes, children, and searching within the SVG tree.

## <span class="class"></span>`pydreamplet.core.SVG`

<!--skip-->
```py
SvgElement (self, tag, **kwargs)
```

Initializes a new SVG element with the specified tag and attributes.

<span class="param">**Parameters**</span>

- `tag` *(str)*: The SVG tag name.
- `**kwargs`: Additional attributes for the element.

<!--skip-->
```py
elem = SvgElement("rect", fill="red")
print(elem)  # Outputs the XML representation of the element.
```

### <span class="meth"></span>`register`

<!--skip-->
```py
SvgElement.register(tag: str, subclass: type) -> None
```

Registers a specialized subclass for a given SVG tag. This is needed only for registration the SVG element classes, created by the user. Probably you will not need to us it.

### <span class="meth"></span>`from_element`

<!--skip-->
```py
SvgElement.from_element(element: ET.Element)
```

Creates an instance from an ElementTree element, using the registered subclass if available.

<!--skip-->
```py
import xml.etree.ElementTree as ET
elem = ET.Element("rect")
svg_elem = SvgElement.from_element(elem)
```

### <span class="meth"></span>`attrs`

<!--skip-->
```py
attrs(self, attributes: dict) -> SvgElement
```

Sets multiple attributes on the element.

Underscore names are converted to hyphenated SVG attributes. Known XML namespace prefixes can also be used with underscore syntax: `xlink_href` maps to `xlink:href`.

<!--skip-->
```py
drop_shadow = SvgElement("feDropShadow")
drop_shadow.attrs({
    "id": "shadow",
    "dx": "0.2",
    "dy": "0.4",
    "stdDeviation": "0.2",
})
print(drop_shadow)  # <feDropShadow xmlns="http://www.w3.org/2000/svg" id="shadow" dx="0.2" dy="0.4" stdDeviation="0.2" />
```

<!--skip-->
```py
use = SvgElement("use", xlink_href="#symbol")
```

### <span class="meth"></span>`has_attr`

<!--skip-->
```py
has_attr(self, name: str) -> bool
```

Checks if the element has the specified attribute. Attribute names with underscores are automatically converted to hyphens (e.g., `font_size` becomes `font-size`). The special attribute name `class_name` is mapped to the SVG `class` attribute.

<span class="param">**Parameters**</span>

- `name` *(str)*: The attribute name to check for.

<span class="param">**Returns**</span>

- `bool`: `True` if the attribute exists, `False` otherwise.

<!--skip-->
<!--skip-->
```py
rect = SvgElement("rect", fill="red", stroke_width="2")
print(rect.has_attr("fill"))         # True
print(rect.has_attr("stroke_width")) # True (checks for "stroke-width")
print(rect.has_attr("opacity"))      # False

# Special case for class attribute
text = SvgElement("text", class_name="highlight")
print(text.has_attr("class_name"))   # True
```

### <span class="meth"></span>`append`

<!--skip-->
```py
append(self, *children) -> Self
```

Appends one or more child elements to the current element. Returns self, allowing method chaining. When a wrapped `SvgElement` is appended, the child receives a `_parent` reference to the current element.

### <span class="meth"></span>`remove`

<!--skip-->
```py
remove(self, *children) -> Self
```

Removes one or more child elements from the current element. If a child was wrapped, it removes its underlying element and clears its `_parent` reference.

<!--skip-->
```py
svg = SVG(800, 600, width="400px", height="300px")
g1 = G()
g2 = G()
svg.append(g1, g2)
g1.append(Circle())
g2.append(Rect())

print(svg)
# <svg xmlns="http://www.w3.org/2000/svg" width="400px" height="300px" viewBox="0 0 800 600"><g><circle /></g><g><rect /></g></svg>

svg.remove(g1)
print(svg)
# <svg xmlns="http://www.w3.org/2000/svg" width="400px" height="300px" viewBox="0 0 800 600"><g><rect /></g></svg>
```

### <span class="meth"></span>`to_string`

<!--skip-->
```py
to_string(self, pretty_print: bool = True) -> str
```

Returns the SVG element as a string. If pretty_print is set to `True`, the output is formatted with indentation for improved readability (using Python’s built-in `ET.indent` available from Python 3.9 onward).

### <span class="meth"></span>`find` and `find_all`

<!--skip-->
```py
find(self, tag: str, nested: bool = False, id: str | None = None) -> SvgElement | None
find_all(self, tag: str, nested: bool = False, class_name: str | None = None) -> list[SvgElement]
```

Searches for child elements by tag. If `nested` is `True`, the search is recursive.

For `find`, if an `id` is provided, only the element with that matching id will be returned.
For `find_all`, if a `class_name` is provided, only elements with that matching class attribute will be returned. Registered SVG tags are returned as their specialized pyDreamplet classes, such as `Rect`, `Circle`, or `G`.

The returned objects are live wrappers around the existing XML elements in the SVG tree. Mutating a result from `find()` or `find_all()` mutates the original SVG. Use `copy()` only when you need an independent duplicate.

<!--skip-->
```py
svg = SVG(200, 100)
svg.append(Rect(id="box", x=10, y=10, width=50, height=30, fill="red"))

rect = svg.find("rect", id="box")
rect.fill = "blue"  # Updates the rect inside svg.
```

### <span class="meth"></span>`copy`

<!--skip-->
```py
copy(self) -> Self
```

Creates and returns a deep copy of the current SVG element. The new instance preserves the original pyDreamplet class and has its own separate copy of the underlying ElementTree element and subtree. This ensures that subsequent modifications to the copy do not affect the original element.

For example:

<!--skip-->
```py
original = SvgElement("rect", x=10, y=20, width=100, height=50)
duplicate = original.copy()
duplicate.x = 30  # This change will not affect the original element.
```

Using `copy()` is especially useful when you need to duplicate elements and then modify them independently in your SVG structure.
