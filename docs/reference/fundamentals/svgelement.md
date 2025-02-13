# `SvgElement` class

The `SvgElement` class is a lightweight wrapper around an ElementTree element, designed to simplify working with SVG elements by providing convenient methods for setting attributes, appending children, and converting the element to a string.

## <span class="class"></span> `pydreamplet.SVG`

```py
SvgElement (self, tag, **kwargs)
```

Initializes the element with the specified tag and attributes. Attributes provided as keyword arguments have their underscores replaced with hyphens.

### Attributes

This class has no attributes

### Methods

#### <span class="method"></span> `from_element(element)`

Class Method. Creates a new SvgElement by wrapping an existing ElementTree element.


#### <span class="method"></span> `normalize_attrs(attrs)`

Static Method. Converts a dictionary of attribute names by replacing underscores with hyphens.

#### <span class="method"></span> `attrs(attributes)`

Sets multiple attributes on the element using a dictionary.

#### <span class="method"></span> `append(child)`

Appends a child element. The child can be another SvgElement or a raw ElementTree element.

#### <span class="method"></span> `remove(child)`

Removes a child element from the current element.

#### <span class="method"></span> `tostring()`

Returns a Unicode string representation of the element.

#### `__getattr__(name)`
Provides attribute-style access to the SVG element's attributes, converting numeric strings to numbers when possible.

#### `__setattr__(name, value)`
Sets an attribute on the SVG element, converting underscores in attribute names to hyphens.

## Usage Example

```py linenums="1"
from pydreamplet import SvgElement

# Create a new SVG rectangle element with specific attributes.
rect = SvgElement("rect", width="100", height="50", fill="blue")
print(rect)
# Outputs: <rect xmlns="http://www.w3.org/2000/svg" width="100" height="50" fill="blue" />
```