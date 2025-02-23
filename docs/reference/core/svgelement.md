# `SvgElement`

The `SvgElement` class serves as the base for all SVG elements. It wraps an ElementTree element, provides a registry for specialized classes, and offers methods for managing attributes, children, and searching within the SVG tree.

## <span class="class"></span>`pydreamplet.core.SVG`

```py
SvgElement (self, tag, **kwargs)
```

Initializes a new SVG element with the specified tag and attributes.

<span class="param">**Parameters**</span>

- `tag` *(str)*: The SVG tag name.
- `**kwargs`: Additional attributes for the element.

```py
elem = SvgElement("rect", fill="red")
print(elem)  # Outputs the XML representation of the element.
```

### <span class="meth"></span>`register`

```py
SvgElement.register(tag: str, subclass: type) -> None
```

Registers a specialized subclass for a given SVG tag. This is needed only for registration the SVG element classes, created by the user. Probably you will not need to us it.

### <span class="meth"></span>`from_element`

```py
SvgElement.from_element(element: ET.Element)
```

Creates an instance from an ElementTree element, using the registered subclass if available.

```py
import xml.etree.ElementTree as ET
elem = ET.Element("rect")
svg_elem = SvgElement.from_element(elem)
```

### <span class="meth"></span>`attrs`

```py
attrs(self, attributes: dict) -> SvgElement
```

Sets multiple attributes on the element.

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

### <span class="meth"></span>`append`

```py
append(self, *children) -> SvgElement
```

Appends a child element to the current element. Returns self, allowing method chaining.

### <span class="meth"></span>`remove`

```py
remove(self, child) -> SvgElement
```

Removes a child element from the current element. If the child was wrapped, it removes its underlying element.

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

```py
to_string(self, pretty_print: bool = True) -> str
```

Returns the SVG element as a string. If pretty_print is set to `True`, the output is formatted with indentation for improved readability (using Python’s built-in `ET.indent` available from Python 3.9 onward).

### <span class="meth"></span>`find` and `find_all`

```py
find(self, tag: str, nested: bool = False, id: Optional[str] = None)
find_all(self, tag: str, nested: bool = False, class_name: Optional[str] = None)
```

Searches for child elements by tag. If `nested` is `True`, the search is recursive.

For `find`, if an `id` is provided, only the element with that matching id will be returned.
For `find_all`, if a `class_name` is provided, only elements with that matching class attribute will be returned.
