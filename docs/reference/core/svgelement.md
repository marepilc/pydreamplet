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

### <span class="meth"></span>`append`

```py
append(self, child) -> SvgElement
```

Appends a child element to the current element. If the child has an element attribute, it uses that.

### <span class="meth"></span>`remove`

```py
remove(self, child) -> SvgElement
```

Removes a child element from the current element. If the child was wrapped, it removes its underlying element.

### <span class="meth"></span>`tostring`

```py
tostring(self) -> str
```

Returns the SVG element as a string.

### <span class="meth"></span>`find` and `find_all`

```py
find(self, tag: str, nested: bool = False)
find_all(self, tag: str, nested: bool = False)
```

Searches for child elements by tag. If nested is True, the search is recursive.