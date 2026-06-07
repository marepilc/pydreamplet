---
title: Dancing Circles
description: Build an animated radial composition with Theme colors, blended strokes, groups, and SVG animate elements.
navigation:
  title: Dancing circles
category: tutorials
---

# Dancing Circles

This tutorial builds an animated radial composition from repeated circles. Each
circle starts on a ring, grows toward its own radius, moves to the center, and
returns to its starting point.

## Imports and Theme

The composition uses `math` for radial coordinates and `Theme` for Tailwind
inspired default colors.

```python
from math import cos, radians, sin

import pydreamplet as dp

theme = dp.Theme()
```

## Canvas and Layout Values

The SVG is square. The largest possible circle radius is based on half of the
canvas width minus a small margin.

```python
svg = dp.SVG(1024, 1024)
margin = 24
min_radius = 10
circle_count = 32

max_radius = svg.w / 2 - margin
radius_step = (max_radius - min_radius) / (circle_count - 1)
```

`circle_count` controls both the number of circles and the angular spacing. A
higher value makes the ring denser; a lower value makes the individual motion
easier to read.

## Blended Stroke Colors

Create one color for each circle by blending between the theme's pink and sky
tokens. `blend_colors()` accepts theme colors directly, including OKLCH values.

```python
colors = [
    dp.blend_colors(theme.pink, theme.sky, i / circle_count)
    for i in range(circle_count)
]
```

`dp.blend()` remains available as a shorter compatibility alias.

## Centered Group

Instead of adding half of the canvas width and height to every circle, place a
group in the center of the SVG. Every circle can then use coordinates relative
to that center.

```python
g = dp.G(pos=(svg.w / 2, svg.h / 2))
svg.append(g)
```

## Circle Positions

Divide the full circle into equal angles. For each index, compute the angle,
the circle's final radius, and the starting position on the outer ring.

```python
angle_step = 360 / circle_count

for i in range(circle_count):
    angle = radians(i * angle_step)
    r = min_radius + i * radius_step
    final_cx = max_radius * cos(angle)
    final_cy = max_radius * sin(angle)
```

`cos()` gives the x coordinate and `sin()` gives the y coordinate. Multiplying
both by `max_radius` places the circle on the outer ring.

## Animated Circles

Each circle starts with the same small radius. The stroke color comes from the
blended palette, and the fill is transparent.

```python
    circle = dp.Circle(
        pos=(final_cx, final_cy),
        r=min_radius,
        fill=theme.transparent,
        stroke=colors[i],
    )
```

Add three animations: one for radius, one for `cx`, and one for `cy`. The radius
grows and shrinks; the center point moves inward and back out.

```python
    circle.append(dp.Animate("r", values=[min_radius, r, min_radius], dur="5s"))
    circle.append(dp.Animate("cx", values=[final_cx, 0, final_cx], dur="5s"))
    circle.append(dp.Animate("cy", values=[final_cy, 0, final_cy], dur="5s"))
    g.append(circle)
```

## Complete Script

```python
from math import cos, radians, sin

import pydreamplet as dp

theme = dp.Theme()

svg = dp.SVG(1024, 1024)
margin = 24
min_radius = 10
circle_count = 32
max_radius = svg.w / 2 - margin
radius_step = (max_radius - min_radius) / (circle_count - 1)
colors = [
    dp.blend_colors(theme.pink, theme.sky, i / circle_count)
    for i in range(circle_count)
]
g = dp.G(pos=(svg.w / 2, svg.h / 2))
svg.append(g)

angle_step = 360 / circle_count

for i in range(circle_count):
    angle = radians(i * angle_step)
    r = min_radius + i * radius_step
    final_cx = max_radius * cos(angle)
    final_cy = max_radius * sin(angle)

    circle = dp.Circle(
        pos=(final_cx, final_cy),
        r=min_radius,
        fill=theme.transparent,
        stroke=colors[i],
    )
    circle.append(dp.Animate("r", values=[min_radius, r, min_radius], dur="5s"))
    circle.append(dp.Animate("cx", values=[final_cx, 0, final_cx], dur="5s"))
    circle.append(dp.Animate("cy", values=[final_cy, 0, final_cy], dur="5s"))
    g.append(circle)

svg.save("output/dancing_circles.svg")
```

::svg-preview{src="/showcase/dancing_circles_light.svg" alt="Animated radial circle composition with blended pink and sky strokes."}
::
