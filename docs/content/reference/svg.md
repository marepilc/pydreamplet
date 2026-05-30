---
title: SVG
description: Root SVG document, viewBox dimensions, attributes, output, and loading.
navigation:
  title: SVG
category: reference
---

# SVG

`SVG` represents the root `<svg>` element. It manages the `viewBox`, default output dimensions, child elements, file loading, and file output.

`SVG` inherits the general element API from `SvgElement`, so it also supports attribute access, tree operations, searching, copying, and serialization.

## Import

```python
import pydreamplet as dp
```

## Signatures

```python
dp.SVG(width: Real, height: Real, **kwargs)
dp.SVG(x: Real, y: Real, width: Real, height: Real, **kwargs)
dp.SVG(viewbox: tuple[Real, ...] | list[Real], **kwargs)
```

`viewbox` can be a tuple or list with either two or four numeric values.

In the public type aliases, `Real` means `int | float` and `AttributeValue` means `str | int | float | None`.

```python
dp.SVG((540, 360))
dp.SVG([0, 0, 540, 360])
```

## Constructor Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `width` | `Real` | yes, in the 2-value form | The viewBox width. Also used as the default SVG `width` attribute with a `px` suffix. |
| `height` | `Real` | yes, in the 2-value form | The viewBox height. Also used as the default SVG `height` attribute with a `px` suffix. |
| `x` | `Real` | yes, in the 4-value form | The minimum x coordinate of the viewBox. |
| `y` | `Real` | yes, in the 4-value form | The minimum y coordinate of the viewBox. |
| `viewbox` | `tuple/list of Real` | yes, in the sequence form | A 2-item or 4-item sequence. |
| `**kwargs` | `Any` | no | Additional SVG attributes. Underscores are converted to hyphens, except known namespace prefixes. Values are serialized to SVG attributes. |

The constructor accepts only two or four viewBox values. Passing any other count raises `ValueError`.

```python
dp.SVG(540)              # ValueError
dp.SVG(0, 0, 540)        # ValueError
dp.SVG("540", "360")     # ValueError
```

## Created Attributes

Every constructed `SVG` receives these attributes:

| Attribute | Source | Example |
| --- | --- | --- |
| `viewBox` | The provided viewBox values. | `"0 0 540 360"` |
| `width` | `width` kwarg or default from viewBox width. | `"540px"` |
| `height` | `height` kwarg or default from viewBox height. | `"360px"` |

```python
svg = dp.SVG(540, 360)

print(svg.viewBox)  # 0 0 540 360
print(svg.width)    # 540px
print(svg.height)   # 360px
```

The root namespace is emitted by ElementTree when the SVG is serialized.

```python
print(str(dp.SVG(120, 80)))
# <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 80" width="120px" height="80px" />
```

## ViewBox Forms

Use two values for the common `0 0 width height` coordinate system.

```python
svg = dp.SVG(540, 360)

print(svg.viewBox)  # 0 0 540 360
```

Use four values when the coordinate system has an explicit origin.

```python
svg = dp.SVG(-270, -180, 540, 360)

print(svg.viewBox)  # -270 -180 540 360
```

The four-value form is useful for centered coordinate systems.

```python
svg = dp.SVG(-100, -100, 200, 200)
svg.append(dp.Circle(cx=0, cy=0, r=40, fill="#14b8a6"))
```

## Width And Height

The `width` and `height` attributes control the rendered output size. They do not change drawing coordinates.

```python
svg = dp.SVG(540, 360, width=1080, height=720)

print(svg.viewBox)  # 0 0 540 360
print(svg.width)    # 1080
print(svg.height)   # 720
```

You can also update them later because SVG attributes are exposed as Python attributes.

```python
svg.width = 720
svg.height = 480
```

## Properties

### `w`

```python
svg.w -> float
```

Returns the viewBox width.

```python
svg = dp.SVG(300, 200, width=900, height=600)

print(svg.w)      # 300.0
print(svg.width)  # 900
```

If the SVG has no `viewBox`, `w` falls back to the numeric part of the `width` attribute. If that cannot be parsed, it returns `0.0`. A malformed `viewBox` raises `ValueError`.

### `h`

```python
svg.h -> float
```

Returns the viewBox height.

```python
svg = dp.SVG(300, 200, width=900, height=600)

print(svg.h)       # 200.0
print(svg.height)  # 600
```

If the SVG has no `viewBox`, `h` falls back to the numeric part of the `height` attribute. If that cannot be parsed, it returns `0.0`. A malformed `viewBox` raises `ValueError`.

## Attribute Handling

`SVG` inherits dynamic attribute handling from `SvgElement`.

You can pass SVG attributes as keyword arguments.

```python
svg = dp.SVG(
    540,
    360,
    id="hero",
    class_name="chart",
    preserve_aspect_ratio="xMidYMid meet",
)

print(svg.id)                    # hero
print(svg.class_name)            # chart
print(svg.preserve_aspect_ratio) # xMidYMid meet
```

Attribute names are normalized:

| Python name | SVG attribute |
| --- | --- |
| `class_name` | `class` |
| `stroke_width` | `stroke-width` |
| `preserve_aspect_ratio` | `preserve-aspect-ratio` |
| `xml_space` | namespaced XML attribute |
| `xlink_href` | namespaced XLink attribute |

Assigning `None` removes an attribute.

```python
svg.id = "draft"
svg.id = None

print(svg.has_attr("id"))  # False
```

String values that look like numbers are converted when read through dynamic attributes. The `id` attribute is always kept as a string.

```python
svg.opacity = 0.5
svg.tabindex = 1
svg.id = "001"

print(svg.opacity)   # 0.5
print(svg.tabindex)  # 1
print(svg.id)        # 001
```

## Core Methods

### `from_element`

```python
dp.SVG.from_element(element: xml.etree.ElementTree.Element) -> dp.SVG
```

Creates an `SVG` wrapper around an existing `xml.etree.ElementTree.Element`.

```python
import xml.etree.ElementTree as ET
import pydreamplet as dp

element = ET.Element("{http://www.w3.org/2000/svg}svg")
element.set("viewBox", "0 0 120 80")
element.set("width", "120px")
element.set("height", "80px")

svg = dp.SVG.from_element(element)
```

This method does not rebuild the element or apply constructor defaults. It wraps the element as it is.

### `from_file`

```python
dp.SVG.from_file(filename: str) -> dp.SVG
```

Parses an existing SVG file and returns an `SVG` instance.

```python
from importlib.resources import files
from pydreamplet import SVG, resources

svg = SVG.from_file(files(resources) / "hummingbird.svg").attrs(
    {"width": 96, "height": 84}
)
svg.find("path").fill = "darkgreen"
```

<img src="/showcase/svg_from_file_example.svg" alt="Loaded hummingbird SVG" width="96" height="84" class="mx-auto mt-6 block" />

Namespaces declared in the source file are registered before serialization. This helps prefixes such as `xlink` or custom source prefixes round-trip without being rewritten to generated prefixes.

If the source SVG has numeric `width` and `height` but no `viewBox`, `from_file()` adds a matching viewBox.

```xml
<svg width="120px" height="80px"></svg>
```

After loading:

```python
svg = dp.SVG.from_file("icon.svg")

print(svg.viewBox)  # 0 0 120 80
print(svg.w)        # 120.0
print(svg.h)        # 80.0
```

Only simple numeric lengths are used for the fallback. Values such as `"120px"`, `"120"`, and `"100%"` can be parsed for their leading numeric part. Non-numeric values cannot produce a fallback viewBox.

### `ensure_defs`

```python
svg.ensure_defs() -> dp.Defs
```

Returns the first existing `<defs>` child. If none exists, creates one as the first child and returns it.

```python
svg = dp.SVG(300, 200)
defs = svg.ensure_defs()

gradient = dp.LinearGradient(id="accent", x1="0%", y1="0%", x2="100%", y2="0%")
gradient.add_stop("0%", "#14b8a6")
gradient.add_stop("100%", "#38bdf8")

defs.append(gradient)
```

The returned `Defs` object is a live wrapper around the SVG tree. Mutating it changes the SVG.

### `style`

```python
svg.style(file_path: str, overwrite: bool = True, minify: bool = True) -> None
```

Loads CSS from `file_path` and inserts it as a `<style>` element.

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `file_path` | `str` | required | Path to a CSS file. |
| `overwrite` | `bool` | `True` | Removes existing direct `<style>` children and inserts the new style as the first child. |
| `minify` | `bool` | `True` | Removes comments, collapses whitespace, and trims spacing around common CSS punctuation before insertion. |

```python
svg = dp.SVG(200, 200)
svg.append(dp.Circle(cx=100, cy=100, r=50, class_name="mark"))

svg.style("drawing.css")
```

Example `drawing.css`:

```css
.mark {
  fill: #14b8a6;
  stroke: currentColor;
  stroke-width: 8;
}
```

When `overwrite=False`, the new style is appended after existing children.

```python
svg.style("base.css")
svg.style("theme.css", overwrite=False)
```

### `display`

```python
svg.display() -> None
```

Displays the SVG in an IPython environment.

```python
svg.display()
```

This method requires the optional notebook dependencies. If they are not installed, it raises `RuntimeError` with installation instructions.

```bash
pip install "pydreamplet[notebook]"
```

```bash
uv add pydreamplet --extra notebook
```

### `save`

```python
svg.save(filename: str, pretty_print: bool = False) -> None
```

Writes the SVG markup to a file using UTF-8.

```python
svg.save("drawing.svg")
```

By default, `save()` writes compact markup. Pass `pretty_print=True` for indented output.

```python
svg.save("drawing.svg", pretty_print=True)
```

## Inherited Element Methods

### `attrs`

```python
svg.attrs(attributes: dict[str, object]) -> dp.SVG
```

Sets multiple attributes and returns the SVG instance.

```python
svg.attrs({
    "id": "chart",
    "role": "img",
    "aria_label": "Generated chart",
})
```

Values set to `None` remove the corresponding attribute.

```python
svg.attrs({"role": None})
```

### `set_attr`

```python
svg.set_attr(name: str, value: AttributeValue) -> dp.SVG
```

Sets a single attribute and returns the SVG instance.

```python
svg.set_attr("data-state", "ready")
```

### `set_id`

```python
svg.set_id(value: str | None) -> dp.SVG
```

Sets or removes the `id` attribute.

```python
svg.set_id("main-svg")
svg.set_id(None)
```

### `set_class`

```python
svg.set_class(value: str | None) -> dp.SVG
```

Sets or removes the SVG `class` attribute.

```python
svg.set_class("responsive")
```

### `set_fill`

```python
svg.set_fill(value: AttributeValue) -> dp.SVG
```

Sets the `fill` attribute on the root SVG element.

```python
svg.set_fill("none")
```

For most drawings, fill is usually set on child shapes instead of the root.

### `set_stroke`

```python
svg.set_stroke(
    value: AttributeValue,
    width: AttributeValue = None,
    linecap: str | None = None,
    linejoin: str | None = None,
) -> dp.SVG
```

Sets `stroke` and optional stroke-related attributes on the root SVG element.

```python
svg.set_stroke("currentColor", width=2, linecap="round", linejoin="round")
```

This writes `stroke`, `stroke-width`, `stroke-linecap`, and `stroke-linejoin`.

### `set_style`

```python
svg.set_style(value: str | Mapping[str, AttributeValue] | None) -> dp.SVG
```

Sets the inline `style` attribute. A string is used directly.

```python
svg.set_style("display: block; max-width: 100%")
```

When passed a dictionary, underscores in property names become hyphens and `None` values are skipped.

```python
svg.set_style({
    "display": "block",
    "max_width": "100%",
    "background": None,
})
```

Passing `None` removes the inline `style` attribute.

### `set_position`

```python
svg.set_position(x: PointLike | Real, y: Real | None = None) -> dp.SVG
```

Sets `x` and `y` attributes on the root SVG element. If the first argument is a point-like object, `y` can be omitted.

```python
svg.set_position(24, 32)
```

This is usually more useful for nested SVG fragments than for the top-level document.

### `set_size`

```python
svg.set_size(width: AttributeValue, height: AttributeValue) -> dp.SVG
```

Sets the rendered `width` and `height` attributes. It does not change the `viewBox`.

```python
svg.set_size(720, 480)
```

### `append`

```python
svg.append(*children) -> dp.SVG
```

Appends one or more children to the SVG and returns the SVG instance.

```python
svg.append(
    dp.Rect(x=40, y=40, width=160, height=96, rx=12, fill="#38bdf8"),
    dp.Circle(cx=260, cy=88, r=48, fill="#95cf20"),
)
```

Children can be pyDreamplet objects with an `.element` attribute or raw ElementTree elements.

### `remove`

```python
svg.remove(*children) -> dp.SVG
```

Removes one or more children and returns the SVG instance.

```python
circle = dp.Circle(cx=100, cy=100, r=40)
svg.append(circle)
svg.remove(circle)
```

### `to_string`

```python
svg.to_string(pretty_print: bool = True) -> str
```

Serializes the SVG to a string.

```python
markup = svg.to_string()
compact = svg.to_string(pretty_print=False)
```

`str(svg)` is equivalent to `svg.to_string(pretty_print=False)`.

### `has_attr`

```python
svg.has_attr(name: str) -> bool
```

Returns `True` when the normalized attribute exists.

```python
svg.id = "chart"

print(svg.has_attr("id"))          # True
print(svg.has_attr("class_name"))  # False
```

### `find`

```python
svg.find(tag: str, nested: bool = False, id: str | None = None)
```

Finds the first matching child and wraps it in the registered pyDreamplet class when possible.

```python
svg.append(dp.G(id="marks"))

group = svg.find("g", id="marks")
```

By default, only direct children are searched. Use `nested=True` to search descendants.

```python
circle = svg.find("circle", nested=True)
```

### `find_all`

```python
svg.find_all(tag: str, nested: bool = False, class_name: str | None = None) -> list
```

Finds all matching children and wraps them in registered pyDreamplet classes when possible.

```python
marks = svg.find_all("circle", nested=True, class_name="mark")
```

### `copy`

```python
svg.copy() -> dp.SVG
```

Returns a deep copy of the SVG wrapper and the underlying ElementTree element. Mutating the copy does not affect the original.

```python
base = dp.SVG(200, 200)
variant = base.copy()

variant.width = 400
```

## Common Patterns

Create a larger rendered SVG while keeping a stable coordinate system.

```python
svg = dp.SVG(540, 360, width=1080, height=720)
```

Use `svg.w` and `svg.h` for center-based placement.

```python
label = dp.Text(
    "pyDreamplet",
    x=svg.w / 2,
    y=svg.h / 2,
    text_anchor="middle",
    alignment_baseline="middle",
)
```

Load an SVG, edit a path, and save a copy.

```python
svg = dp.SVG.from_file("logo.svg")

path = svg.find("path", nested=True)
if path:
    path.fill = "currentColor"

svg.save("logo-current-color.svg", pretty_print=True)
```
