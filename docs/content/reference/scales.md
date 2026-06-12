---
title: Scales
description: Reference for data scale classes exported from pydreamplet.
navigation:
  title: Scales
category: reference
---

# Scales

Scales map data values into visual values such as positions, widths, radii, or
colors.

Scale classes and the `map()` helper are exported from top-level `pydreamplet`.

```python
import pydreamplet as dp
```

## Visual Example

```python
import pydreamplet as dp

values = [12, 35, 24, 50]
labels = ["A", "B", "C", "D"]

x = dp.BandScale(labels, (30, 310), padding=0.2)
y = dp.LinearScale((0, 50), (150, 30))
color = dp.ColorScale((0, 50), ("#14b8a6", "#f83898"))
radius = dp.CircleScale((0, 50), (8, 24))

svg = dp.SVG(340, 180)
svg.append(dp.Line(24, 150, 320, 150, stroke="currentColor", stroke_width=2, opacity=0.35))

for label, value in zip(labels, values):
    cx = x.map(label) + x.bandwidth / 2
    cy = y.map(value)
    svg.append(
        dp.Circle(cx=cx, cy=cy, r=radius.map(value), fill=color.map(value), opacity=0.9),
        dp.Text(label, x=cx, y=168, font_size=14, text_anchor="middle", fill="currentColor"),
    )
```

::svg-preview{src="/showcase/ref_scales_bubbles.svg" alt="Bubble chart generated from band, linear, color, and circle scales."}
::

## map

```python
map(
    value: Real,
    start1: Real,
    stop1: Real,
    start2: Real,
    stop2: Real,
    within_bounds: bool = False,
) -> float
```

Linearly remaps a number from one range to another without creating a scale
instance. Values outside the input range are extrapolated by default. Set
`within_bounds=True` to constrain the result to the target range.

```python
assert dp.map(2, 0, 10, 0, 100) == 20
assert dp.map(11, 0, 10, 0, 100) == 110
assert dp.map(11, 0, 10, 0, 100, within_bounds=True) == 100
```

Reversed input and target ranges are supported. A zero-length input range
raises `ValueError`.

## LinearScale

```python
LinearScale(domain: NumericPair, output_range: NumericPair)
```

Maps a numeric value linearly from `domain` to `output_range`.

| Member | Type | Notes |
| --- | --- | --- |
| `map(value)` | `float -> float` | Maps from domain to output range. |
| `invert(value)` | `float -> float` | Maps from output range back to domain. |
| `domain` | `NumericPair` | Reassigning recalculates the slope. |
| `output_range` | `NumericPair` | Reassigning recalculates the slope. |

```python
scale = dp.LinearScale((0, 10), (0, 100))

assert scale.map(5) == 50
assert scale.invert(50) == 5
```

## BandScale

```python
BandScale(
    domain: list[Any] | tuple[Any, ...] | Iterable[Any],
    output_range: NumericPair,
    padding: float = 0.1,
    outer_padding: float | None = None,
)
```

Maps distinct categorical values to band start positions.

| Member | Type | Notes |
| --- | --- | --- |
| `map(value)` | `Any -> float` | Raises `ValueError` for unknown values. |
| `bandwidth` | `float` | Computed width of one band. |
| `step` | `float` | Distance between band starts. |
| `domain` | `list[Any]` | Values must be distinct on construction. |
| `output_range` | `NumericPair` | Output interval. |
| `padding` | `float` | Inner padding multiplier. |
| `outer_padding` | `float` | Defaults to `padding`. |

```python
scale = dp.BandScale(["a", "b", "c"], (0, 300), padding=0.1)

x = scale.map("b")
width = scale.bandwidth
```

## PointScale

```python
PointScale(
    domain: list[Any] | tuple[Any, ...] | Iterable[Any],
    output_range: NumericPair,
    padding: float = 0.5,
)
```

Maps distinct categorical values to discrete points.

| Member | Type | Notes |
| --- | --- | --- |
| `map(value)` | `Any -> float \| None` | Returns `None` for unknown values. |
| `domain` | `list[Any]` | Must contain at least one distinct value. |
| `output_range` | `NumericPair` | Output interval. |
| `padding` | `float` | Padding at both range ends. |

## OrdinalScale

```python
OrdinalScale(
    domain: list[Any] | tuple[Any, ...] | Iterable[Any],
    output_range: list[Any] | tuple[Any, ...] | Sequence[Any],
)
```

Maps categories to output values in order. If the domain is longer than the
output range, output values repeat cyclically.

```python
scale = dp.OrdinalScale(["a", "b", "c"], ["red", "blue"])

assert scale.map("a") == "red"
assert scale.map("c") == "red"
```

## ColorScale

```python
ColorScale(domain: NumericPair, output_range: tuple[str, str] | list[str])
```

Interpolates between two hex colors and clamps values outside the domain.

```python
scale = dp.ColorScale((0, 100), ("#000000", "#ffffff"))

assert scale.map(50) == "#7f7f7f"
assert scale.map(150) == "#ffffff"
```

`output_range` must contain exactly two colors. Domain endpoints must be
distinct.

## SquareScale

```python
SquareScale(domain: NumericPair, output_range: NumericPair)
```

Maps through a square-root transform. It is useful when a square side length
should represent area.

```python
scale = dp.SquareScale((0, 100), (0, 10))

assert scale.map(25) == 5
```

Domain values must be non-negative and distinct after square-root conversion.

## CircleScale

```python
CircleScale(domain: NumericPair, output_range: NumericPair)
```

Maps values to circle radii so the circle area changes linearly with the input.

```python
scale = dp.CircleScale((0, 100), (5, 10))

radius = scale.map(50)
```

Domain endpoints must be distinct.
