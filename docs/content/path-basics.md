---
title: Path basics
description: Build custom SVG contours with Path and PathBuilder.
navigation:
  title: Path basics
category: guide
---

# Path Basics

Use `Path` when a shape is easier to describe as a sequence of drawing
commands than as a predefined element such as `Circle`, `Rect`, or `Line`.

## Path Data

SVG paths are stored in the `d` attribute. You can pass that data directly as a
string when you already have the path data.

```python
import pydreamplet as dp

svg = dp.SVG(540, 360)

diamond = dp.Path(
    "M270 92 L316 138 L270 184 L224 138 Z",
    fill="#14b8a6",
    stroke="currentColor",
    stroke_width=5,
)

svg.append(diamond)
```

The path starts with `M` for move, uses `L` for line segments, and closes with
`Z`.

## PathBuilder

For paths written in Python, `PathBuilder` keeps the sequence readable and
avoids hand-building the `d` string.

```python
import pydreamplet as dp

svg = dp.SVG(540, 360)

wave_data = (
    dp.PathBuilder()
    .move_to(70, 220)
    .curve_to(150, 80, 230, 80, 270, 180)
    .smooth_curve_to(390, 280, 470, 140)
)

wave = dp.Path(
    wave_data,
    fill="none",
    stroke="currentColor",
    stroke_width=8,
    stroke_linecap="round",
)

svg.append(wave)
```

`curve_to()` creates a cubic Bézier curve with two control points and an end
point. `smooth_curve_to()` continues from the previous curve and infers the
first control point.

## Reusable Shape Functions

A small function can return path data for a reusable shape. This keeps geometry
separate from styling.

```python
def diamond_path(cx, cy, r):
    return (
        dp.PathBuilder()
        .move_to(cx, cy - r)
        .line_to(cx + r, cy)
        .line_to(cx, cy + r)
        .line_to(cx - r, cy)
        .close()
    )


diamond = dp.Path(
    diamond_path(270, 138, 46),
    fill="#14b8a6",
    stroke="currentColor",
    stroke_width=5,
    opacity=0.92,
)

svg.append(diamond)
```

::svg-preview{src="/showcase/path_basics_01.svg" alt="Example SVG generated from the path basics code"}
::

## Measuring Linear Paths

For paths made of straight segments, `Path` exposes simple measurement helpers.

```python
route = dp.Path(
    dp.PathBuilder()
    .move_to(70, 220)
    .line_to(270, 180)
    .line_to(470, 140)
)

midpoint = route.point_at(route.length / 2)
direction = route.tangent_at(route.length / 2)
```

`point_at()` returns a `Vector` on the path, and `tangent_at()` returns the
local direction at that distance.

## Next

The next guide page should cover transforms, grouping, and coordinate systems
in more depth.
