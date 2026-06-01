---
title: SvgElement
description: Shared SVG element wrapper, dynamic attributes, tree operations, search, copying, and serialization.
navigation:
  title: SvgElement
category: reference
---

# SvgElement

`SvgElement` is the base wrapper used by pyDreamplet SVG objects. It owns an
`xml.etree.ElementTree.Element`, normalizes Python-friendly attribute names, and
provides the shared API for attributes, children, search, copying, and output.

Most users meet this API through concrete classes such as `SVG`, `G`, `Rect`,
`Circle`, `Path`, and `Text`. Use `SvgElement` directly when pyDreamplet does not
ship a specialized wrapper for an SVG tag.

## Import

```python
import pydreamplet as dp
```

## Signature

```python
dp.SvgElement(tag: str, **kwargs)
```

```python
filter_node = dp.SvgElement("feDropShadow", dx=0, dy=4, stdDeviation=3)
```

## Constructor Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `tag` | `str` | yes | Local SVG tag name, without the SVG namespace. |
| `**kwargs` | `Any` | no | SVG attributes. Names are normalized in the same way as `attrs()`. |

## Type Names

The signatures on this page use the same type names as the current source:

| Type | Meaning |
| --- | --- |
| `Real` | `int \| float` |
| `AttributeValue` | `str \| int \| float \| None` |
| `PointLike` | `Vector \| tuple[Real, Real] \| list[Real]` |
| `Self` | The concrete element type the method was called on. |

`SvgElement` creates namespaced SVG elements, so serializing an element includes
the root SVG namespace when needed.

```python
node = dp.SvgElement("rect", x=10, y=20, width=80, height=40)

print(str(node))
# <rect xmlns="http://www.w3.org/2000/svg" x="10" y="20" width="80" height="40" />
```

The `pydreamplet.core` module also exposes namespace constants and helpers used
by the wrapper layer:

| Name | Meaning |
| --- | --- |
| `SVG_NS` | SVG namespace URI. |
| `XML_NS` | XML namespace URI. |
| `XLINK_NS` | XLink namespace URI. |
| `qname(tag)` | Expands an SVG tag name to ElementTree namespace form. |
| `ns_attr(prefix, name)` | Expands an XML or XLink attribute name. |

These helpers are useful when mixing pyDreamplet wrappers with raw
`xml.etree.ElementTree` elements.

## Attribute Names

Keyword and dictionary attribute names use Python identifiers. pyDreamplet maps
common Python names to SVG names:

| Python name | SVG attribute |
| --- | --- |
| `class_name` | `class` |
| `stroke_width` | `stroke-width` |
| `font_size` | `font-size` |
| `preserve_aspect_ratio` | `preserve-aspect-ratio` |
| `xml_space` | XML namespaced `space` attribute |
| `xlink_href` | XLink namespaced `href` attribute |

```python
rect = dp.Rect(
    x=20,
    y=20,
    width=120,
    height=70,
    class_name="panel",
    stroke_width=3,
)

print(rect.class_name)    # panel
print(rect.stroke_width)  # 3
```

Dynamic attribute reads convert simple numeric strings to `int` or `float`.
`id` is always returned as a string so leading zeroes are preserved.

```python
mark = dp.Circle(id="001", cx=50, cy=50, r=12, opacity=0.75)

print(mark.id)       # 001
print(mark.opacity)  # 0.75
```

Assigning `None` removes an attribute.

```python
mark.fill = "#14b8a6"
mark.fill = None

print(mark.has_attr("fill"))  # False
```

## Attribute Methods

### `attrs`

```python
element.attrs(attributes: dict[str, object]) -> Self
```

Sets several attributes and returns the same object for chaining.

```python
rect = dp.Rect().attrs({
    "x": 24,
    "y": 32,
    "width": 160,
    "height": 90,
    "fill": "#14b8a6",
    "stroke_width": 4,
})
```

Values set to `None` remove the corresponding attribute.

```python
rect.attrs({"stroke_width": None})
```

### `set_attr`

```python
element.set_attr(name: str, value: AttributeValue) -> Self
```

Sets or removes one attribute.

```python
rect.set_attr("data-state", "active")
rect.set_attr("data-state", None)
```

### Convenience Setters

```python
element.set_id(value: str | None) -> Self
element.set_class(value: str | None) -> Self
element.set_fill(value: AttributeValue) -> Self
element.set_stroke(value: AttributeValue, width: AttributeValue = None, linecap: str | None = None, linejoin: str | None = None) -> Self
element.set_style(value: str | Mapping[str, AttributeValue] | None) -> Self
element.set_position(x: PointLike | Real, y: Real | None = None) -> Self
element.set_size(width: AttributeValue, height: AttributeValue) -> Self
```

`set_position()` writes `cx` and `cy` for circles and ellipses. For other tags,
it writes `x` and `y`.

```python
circle = dp.Circle(r=18).set_position((40, 50))
rect = dp.Rect().set_position(20, 30).set_size(120, 80)
```

`set_style()` accepts either a CSS string or a dictionary. Dictionary keys use
the same underscore-to-hyphen convention as SVG attributes.

```python
rect.set_style({
    "paint_order": "stroke",
    "vector_effect": "non-scaling-stroke",
})
```

### `normalize_attrs`

```python
dp.SvgElement.normalize_attrs(attrs: dict[str, object]) -> dict[str, object]
```

Returns a new attribute dictionary with Python-friendly names converted to SVG
attribute names. It is the same normalization used by constructors,
`attrs()`, and `set_attr()`.

```python
attrs = dp.SvgElement.normalize_attrs({
    "stroke_width": 2,
    "class_name": "mark",
    "xlink_href": "#shape",
})

print(attrs)
# {'stroke-width': 2, 'class': 'mark', '{http://www.w3.org/1999/xlink}href': '#shape'}
```

## Children

### `append`

```python
element.append(*children) -> Self
```

Appends one or more children and returns the parent.

```python
group = dp.G(id="marks").append(
    dp.Circle(cx=40, cy=40, r=12),
    dp.Circle(cx=80, cy=40, r=12),
)
```

Children can be pyDreamplet wrappers or raw ElementTree elements.

### `remove`

```python
element.remove(*children) -> Self
```

Removes one or more children from the element.

```python
circle = dp.Circle(cx=40, cy=40, r=12)
group.append(circle)
group.remove(circle)
```

## Search

### `find`

```python
element.find(tag: str, nested: bool = False, id: str | None = None)
```

Returns the first matching child, or `None`.

```python
svg = dp.SVG(200, 100)
svg.append(dp.G(id="marks").append(dp.Circle(cx=40, cy=40, r=12)))

group = svg.find("g", id="marks")
circle = svg.find("circle", nested=True)
```

### `find_all`

```python
element.find_all(tag: str, nested: bool = False, class_name: str | None = None) -> list[SvgElement]
```

Returns every matching child.

```python
marks = svg.find_all("circle", nested=True, class_name="mark")
```

Known tags are wrapped in their specialized pyDreamplet classes, so searching
for `"rect"` returns `Rect` objects, searching for `"g"` returns `G` objects,
and so on. Returned wrappers are live views over the existing tree.

## Output

### `to_string`

```python
element.to_string(pretty_print: bool = True) -> str
```

Serializes the element. `str(element)` uses compact output.

```python
pretty = group.to_string()
compact = str(group)
```

### `copy`

```python
element.copy() -> Self
```

Creates a deep copy of the wrapper and its XML subtree.

```python
original = dp.Rect(x=10, y=10, width=80, height=40)
variant = original.copy()
variant.fill = "#f83898"
```

Mutating `variant` does not change `original`.

## Extending The Registry

```python
dp.SvgElement.register(tag: str, subclass: type[SvgElement]) -> None
dp.SvgElement.from_element(element: xml.etree.ElementTree.Element) -> SvgElement
```

pyDreamplet registers its built-in SVG classes at import time. You only need
`register()` when you create your own wrapper class and want `find()` or
`find_all()` to return that class for a custom tag.
