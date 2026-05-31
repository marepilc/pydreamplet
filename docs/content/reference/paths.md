---
title: Paths
description: Reference for Path, PathBuilder, path parsing, normalization, linear measurement, and bounding boxes.
navigation:
  title: Paths
category: reference
---

# Paths

`Path` wraps the SVG `<path>` element. Use it for custom contours, data-driven
geometry, generated symbols, routes, curves, and any shape that is easier to
describe with SVG path commands than with a predefined element.

`Path` inherits [`SvgElement`](/reference/svg-element), so it supports dynamic
attributes, style helpers, child operations, search, copying, and serialization.

## Import

```python
import pydreamplet as dp
```

## Type Names

| Type | Meaning |
| --- | --- |
| `Real` | `int | float` |
| `Vector` | `pydreamplet.math.Vector` |

## Path

```python
dp.Path(d: str | dp.PathBuilder = "", **kwargs)
```

`d` can be an SVG path data string or a `PathBuilder`. Extra keyword arguments
become SVG attributes.

```python
path = dp.Path(
    "M40 120 L120 40 L200 120 Z",
    fill="#14b8a6",
    stroke="currentColor",
    stroke_width=5,
)
```

The first positional argument sets the SVG `d` attribute.

```python
print(path.d)  # M40 120 L120 40 L200 120 Z
```

### `d`

```python
path.d -> str
path.d = str | dp.PathBuilder
```

Gets or sets path data.

```python
path.d = "M20 20 H120 V80 H20 Z"
```

When assigned a `PathBuilder`, `Path` stores the builder output string.

```python
path.d = dp.PathBuilder().move_to(20, 20).line_to(120, 80).close()
```

### `w`, `h`, and `center`

```python
path.w -> float
path.h -> float
path.center -> Vector
```

These properties are based on explicit coordinates extracted from normalized
path data. They are useful for rough placement and simple generated paths.

```python
path = dp.Path("M10 20 L110 20 L110 70 Z")

print(path.w)       # 100.0
print(path.h)       # 50.0
print(path.center)  # Vector(x=60.0, y=45.0)
```

For precise geometry, prefer `bbox`.

### `bbox`

```python
path.bbox -> dp.BoundingBox
```

Returns a bounding box for paths made from `M`, `L`, `H`, `V`, `C`, `S`, `Q`,
`T`, `A`, and `Z` commands. Curve and arc bounds are computed from geometric
extrema, not only from endpoints.

```python
path = dp.Path("M10 20 h100 v50 h-100 z")
box = path.bbox

print(box)  # BoundingBox(x=10.0, y=20.0, width=100.0, height=50.0)
```

Malformed path data raises `ValueError`.

### Linear Measurement

```python
path.length -> float
path.point_at(distance: Real) -> Vector
path.tangent_at(distance: Real) -> Vector
```

These helpers are backed by `path_length()`, `point_at_length()`, and
`tangent_at_length()`.

```python
route = dp.Path("M0 0 L10 0 L10 10")

print(route.length)         # 20.0
print(route.point_at(15))   # Vector(x=10.0, y=5.0)
print(route.tangent_at(15)) # Vector(x=0.0, y=1.0)
```

Measurement currently supports linear commands only: `M`, `L`, `H`, `V`, and
`Z`. Curves and arcs raise `ValueError` in measurement functions.

```python
curve = dp.Path("M0 0 C10 0 20 10 30 10")

try:
    curve.length
except ValueError:
    print("curves are not supported by linear measurement")
```

Distances below zero clamp to the start of the path. Distances past the total
length return the final point or last nonzero tangent.

## PathBuilder

```python
dp.PathBuilder()
```

`PathBuilder` builds SVG path data with chainable methods. Methods ending in
`_to` create absolute commands; methods ending in `_by` create relative
commands.

```python
data = (
    dp.PathBuilder()
    .move_to(40, 120)
    .line_to(120, 40)
    .line_to(200, 120)
    .close()
)

path = dp.Path(data, fill="#14b8a6")
```

```python
print(data.to_string())  # M40 120 L120 40 L200 120 Z
print(str(data))         # M40 120 L120 40 L200 120 Z
```

### Move And Line Commands

| Method | SVG command | Description |
| --- | --- | --- |
| `move_to(x, y)` | `M` | Move to an absolute point. |
| `move_by(dx, dy)` | `m` | Move relative to the current point. |
| `line_to(x, y)` | `L` | Draw a line to an absolute point. |
| `line_by(dx, dy)` | `l` | Draw a relative line. |
| `horizontal_to(x)` | `H` | Draw a horizontal line to absolute x. |
| `horizontal_by(dx)` | `h` | Draw a relative horizontal line. |
| `vertical_to(y)` | `V` | Draw a vertical line to absolute y. |
| `vertical_by(dy)` | `v` | Draw a relative vertical line. |
| `close()` | `Z` | Close the current subpath. |

### Curve Commands

| Method | SVG command | Description |
| --- | --- | --- |
| `curve_to(x1, y1, x2, y2, x, y)` | `C` | Cubic Bezier curve. |
| `curve_by(dx1, dy1, dx2, dy2, dx, dy)` | `c` | Relative cubic Bezier curve. |
| `smooth_curve_to(x2, y2, x, y)` | `S` | Smooth cubic Bezier curve. |
| `smooth_curve_by(dx2, dy2, dx, dy)` | `s` | Relative smooth cubic Bezier curve. |
| `quadratic_to(x1, y1, x, y)` | `Q` | Quadratic Bezier curve. |
| `quadratic_by(dx1, dy1, dx, dy)` | `q` | Relative quadratic Bezier curve. |
| `smooth_quadratic_to(x, y)` | `T` | Smooth quadratic Bezier curve. |
| `smooth_quadratic_by(dx, dy)` | `t` | Relative smooth quadratic Bezier curve. |

```python
wave = (
    dp.PathBuilder()
    .move_to(40, 100)
    .curve_to(80, 20, 140, 20, 180, 100)
    .smooth_curve_to(260, 180, 300, 100)
)
```

### Arc Commands

```python
builder.arc_to(rx, ry, x_axis_rotation, large_arc, sweep, x, y)
builder.arc_by(rx, ry, x_axis_rotation, large_arc, sweep, dx, dy)
```

`large_arc` and `sweep` accept `bool` or `int`; the builder serializes them as
`0` or `1`.

```python
arc = (
    dp.PathBuilder()
    .move_to(40, 100)
    .arc_to(60, 60, 0, False, True, 160, 100)
)
```

## PathCommand

```python
dp.PathCommand(command: str, values: tuple[float, ...] = ())
```

Represents a parsed path command.

| Property | Description |
| --- | --- |
| `command` | SVG command letter. |
| `values` | Numeric command values. |
| `is_relative` | `True` when `command` is lowercase. |
| `absolute_command` | Uppercase command letter. |
| `to_string()` | Serializes the command. |

```python
command = dp.PathCommand("l", (10.0, 20.0))

print(command.is_relative)     # True
print(command.absolute_command) # L
print(command.to_string())      # l10 20
```

## PathSegment

```python
dp.PathSegment(command: str, start: Vector, end: Vector)
```

Represents a measured linear path segment.

| Property or method | Description |
| --- | --- |
| `length` | Euclidean segment length. |
| `point_at(distance)` | Point at a distance along the segment, clamped to the segment. |
| `tangent` | Unit direction vector, or `Vector(0, 0)` for zero-length segments. |

`PathSegment` is produced by `iter_path_segments()`.

## Parsing And Normalization

### `parse_path_data`

```python
dp.parse_path_data(path_data: str) -> list[dp.PathCommand]
```

Parses SVG path data into `PathCommand` objects. Relative commands are
preserved.

```python
commands = dp.parse_path_data("M10 20 l100 0 v50 z")

print([command.command for command in commands])  # ['M', 'l', 'v', 'z']
```

The parser expands repeated coordinate groups into explicit commands according
to SVG path rules.

```python
commands = dp.parse_path_data("M0 0 10 10 20 0")

print([command.command for command in commands])  # ['M', 'L', 'L']
```

### `normalize_path_commands`

```python
dp.normalize_path_commands(path_data: str) -> list[dp.PathCommand]
```

Converts relative commands to absolute commands while preserving command types
such as `H`, `V`, `C`, `Q`, and `A`.

```python
commands = dp.normalize_path_commands("M10 20 l100 0 v50 h-100 Z")

print([str(command) for command in commands])
# ['M10 20', 'L110 20', 'V70', 'H10', 'Z']
```

### `normalize_path_data`

```python
dp.normalize_path_data(path_data: str) -> str
```

Returns normalized path commands as an SVG path data string.

```python
print(dp.normalize_path_data("M10 20 l100 0 v50 h-100 Z"))
# M10 20 L110 20 V70 H10 Z
```

## Linear Path Functions

```python
dp.iter_path_segments(path_data: str) -> list[dp.PathSegment]
dp.path_length(path_data: str) -> float
dp.point_at_length(path_data: str, distance: Real) -> Vector
dp.tangent_at_length(path_data: str, distance: Real) -> Vector
```

These functions support linear commands only: `M`, `L`, `H`, `V`, and `Z`.

```python
path_data = "M0 0 H10 V10"

segments = dp.iter_path_segments(path_data)
print(len(segments))                    # 2
print(dp.path_length(path_data))         # 20.0
print(dp.point_at_length(path_data, 12)) # Vector(x=10.0, y=2.0)
```

## Coordinate-Based Properties

`Path.w`, `Path.h`, and `Path.center` are based on explicit coordinates from
normalized path data: move and line endpoints, curve control and end points,
horizontal and vertical endpoints, and arc endpoints. Arc radii and flags are
not treated as points.

This is a convenience model for placement. Use `Path.bbox` when you need a
geometric bounding box.
