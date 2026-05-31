---
title: Shapes
description: Reference for Circle, Ellipse, Rect, Line, Polygon, and Polyline.
navigation:
  title: Shapes
category: reference
---

# Shapes

Shape classes wrap common SVG geometry elements. They all inherit
[`SvgElement`](/reference/svg-element), so they support dynamic attributes,
style helpers, tree operations, search, copying, and serialization.

## Import

```python
import pydreamplet as dp
```

## Point Values

Position arguments accept either separate numeric coordinates or a point-like
value where the API documents `pos`.

```python
from pydreamplet import Vector

dp.Circle(pos=(80, 60), r=30)
dp.Rect(pos=Vector(20, 30), width=120, height=80)
```

`pos` must contain exactly two numbers. For circles and ellipses it maps to
`cx` and `cy`; for rectangles and text it maps to `x` and `y`.

## Bounding Boxes

All shape classes on this page expose `bbox`.

```python
box = dp.Rect(x=20, y=30, width=120, height=80).bbox

print(box.left, box.top, box.right, box.bottom)
```

`bbox` returns `BoundingBox(x, y, width, height)`. It also provides `left`,
`top`, `right`, `bottom`, and `center`.

## Circle

```python
dp.Circle(
    *,
    pos: PointLike | None = None,
    cx: Real | None = None,
    cy: Real | None = None,
    r: Real | None = None,
    **kwargs,
)
```

`Circle` represents `<circle>`.

```python
svg = dp.SVG(220, 140)
circle = dp.Circle(
    pos=(110, 70),
    r=42,
    fill="#14b8a6",
    stroke="currentColor",
    stroke_width=4,
)

svg.append(circle)
```

### Circle Properties

| Property | Description |
| --- | --- |
| `pos` | Center as `Vector`; setting it updates `cx` and `cy`. |
| `radius` | Numeric radius; setting it updates `r`. |
| `center` | Alias for `pos`. |
| `diameter` | `radius * 2`. |
| `area` | Circle area using `math.pi * radius ** 2`. |
| `bbox` | Bounding box derived from center and radius. |

```python
circle.radius = 36
circle.pos = (120, 72)

print(circle.diameter)
```

## Ellipse

```python
dp.Ellipse(
    *,
    pos: PointLike | None = None,
    cx: Real | None = None,
    cy: Real | None = None,
    rx: Real | None = None,
    ry: Real | None = None,
    **kwargs,
)
```

`Ellipse` represents `<ellipse>`.

```python
ellipse = dp.Ellipse(
    pos=(110, 70),
    rx=72,
    ry=34,
    fill="#38bdf8",
)
```

### Ellipse Properties

| Property | Description |
| --- | --- |
| `pos` | Center as `Vector`; setting it updates `cx` and `cy`. |
| `bbox` | Bounding box derived from `cx`, `cy`, `rx`, and `ry`. |

Radius attributes are available through dynamic attributes:

```python
ellipse.rx = 80
ellipse.ry = 28
```

## Rect

```python
dp.Rect(
    *,
    pos: PointLike | None = None,
    x: Real | None = None,
    y: Real | None = None,
    width: Real | None = None,
    height: Real | None = None,
    **kwargs,
)
```

`Rect` represents `<rect>`.

```python
rect = dp.Rect(
    pos=(30, 24),
    width=160,
    height=92,
    rx=10,
    fill="#95cf20",
)
```

### Rect Properties

| Property | Description |
| --- | --- |
| `pos` | Top-left position as `Vector`; setting it updates `x` and `y`. |
| `width` | Numeric width read from the SVG `width` attribute. |
| `height` | Numeric height read from the SVG `height` attribute. |
| `bbox` | Bounding box derived from position and size. Negative sizes are normalized in the returned box. |

Use dynamic attributes or `set_size()` to update size:

```python
rect.set_size(180, 100)
rect.rx = 14
```

## Line

```python
dp.Line(
    x1: Real = 0,
    y1: Real = 0,
    x2: Real = 0,
    y2: Real = 0,
    **kwargs,
)
```

`Line` represents `<line>`.

```python
line = dp.Line(
    24,
    96,
    196,
    36,
    stroke="currentColor",
    stroke_width=6,
    stroke_linecap="round",
)
```

### Line Properties

| Property | Description |
| --- | --- |
| `x1`, `y1`, `x2`, `y2` | Numeric endpoints; setting them updates SVG attributes. |
| `length` | Euclidean distance between endpoints. |
| `angle` | Direction in degrees, normalized to `0 <= angle < 360`. |
| `bbox` | Bounding box covering both endpoints. |

```python
print(line.length)
print(line.angle)
```

## Polygon

```python
dp.Polygon(points: list[Real], **kwargs)
```

`Polygon` represents a closed `<polygon>`.

```python
polygon = dp.Polygon(
    [110, 16, 196, 118, 24, 118],
    fill="#f83898",
)
```

### Polygon Properties

| Property | Description |
| --- | --- |
| `points` | Flat coordinate list: `[x0, y0, x1, y1, ...]`. |
| `bbox` | Bounding box covering all points. |

The point list must contain an even number of coordinates.

```python
polygon.points = [110, 20, 190, 120, 30, 120]
```

## Polyline

```python
dp.Polyline(points: list[Real], **kwargs)
```

`Polyline` represents an open `<polyline>`.

```python
polyline = dp.Polyline(
    [20, 100, 70, 40, 120, 90, 180, 30],
    fill="none",
    stroke="#14b8a6",
    stroke_width=5,
    stroke_linejoin="round",
)
```

### Polyline Properties

| Property | Description |
| --- | --- |
| `points` | Flat coordinate list: `[x0, y0, x1, y1, ...]`. |
| `bbox` | Bounding box covering all points. |

The point list must contain an even number of coordinates.

## Combined Example

```python
svg = dp.SVG(280, 180)

svg.append(
    dp.Rect(x=20, y=24, width=88, height=56, rx=8, fill="#95cf20"),
    dp.Circle(cx=174, cy=52, r=28, fill="#14b8a6"),
    dp.Ellipse(cx=220, cy=126, rx=36, ry=20, fill="#38bdf8"),
    dp.Polyline(
        [28, 138, 72, 106, 118, 136, 162, 98],
        fill="none",
        stroke="currentColor",
        stroke_width=4,
        stroke_linecap="round",
        stroke_linejoin="round",
    ),
)
```

