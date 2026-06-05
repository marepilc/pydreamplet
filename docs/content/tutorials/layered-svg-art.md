---
title: Layered SVG Art
description: Build layered and animated SVG artwork with arcs, groups, gradients, and animations.
navigation:
  title: Layered SVG art
category: tutorials
---

# Layered SVG Art

This tutorial builds an SVG artwork with two layers: blended arc segments in the
front and an animated gradient circle behind them.

## Imports and Colors

```python
import pydreamplet as dp
from pydreamplet.colors import blend
from pydreamplet.shapes import ring

color1 = "#e2cbc5"
color2 = "#691016"
color3 = "#92a1c2"
color4 = "#082137"
```

## Canvas and Layers

Create the canvas and two groups. The first group is appended first, so it is
painted behind the arc layer.

```python
svg = dp.SVG(600, 600, width="300px", height="300px")

circle_layer = dp.G()
arc_layer = dp.G()
svg.append(circle_layer, arc_layer)
```

## Arc Segments

The top half uses `ring()` paths from 180 to 360 degrees. Each iteration shifts
the center, reduces the radius, and blends the fill color.

```python
x = svg.w / 2
blend_prop = 0
radius = 200
radius_delta = radius / 6

for _ in range(6):
    arc = dp.Path(
        d=ring(
            x,
            svg.h / 2,
            inner_radius=0,
            outer_radius=radius,
            start_angle=180,
            end_angle=360,
        ),
        fill=blend(color1, color2, blend_prop),
    )
    arc_layer.append(arc)

    x -= radius_delta
    radius -= radius_delta
    blend_prop += 1 / 6
```

::svg-preview{src="/showcase/tutorial_layered_art_top.svg" alt="Top half arc segments with a fixed left edge and decreasing radius."}
::

The bottom half mirrors that idea and blends a second pair of colors.

```python
x = svg.w / 2
blend_prop = 0
radius = 200

for _ in range(6):
    arc = dp.Path(
        d=ring(
            x,
            svg.h / 2,
            inner_radius=0,
            outer_radius=radius,
            start_angle=0,
            end_angle=180,
        ),
        fill=blend(color3, color4, blend_prop),
    )
    arc_layer.append(arc)

    x += radius_delta
    radius -= radius_delta
    blend_prop += 1 / 6
```

::svg-preview{src="/showcase/tutorial_layered_art_arcs.svg" alt="Top and bottom arc segments layered together."}
::

## Animated Circle

`Animate` writes SVG `<animate>` elements. The first animation moves the dashed
stroke; the second changes the circle radius.

```python
circle = dp.Circle(
    cx=svg.w / 2,
    cy=svg.h / 2,
    r=250,
    fill="none",
    stroke="currentColor",
    stroke_width=5,
    stroke_dasharray="20,15",
    stroke_dashoffset=20,
)

dash_animation = dp.Animate("stroke-dashoffset", dur="2s")
dash_animation.values = [0, 100]

radius_animation = dp.Animate("r", dur="2s")
radius_animation.values = [250, 200, 250]

circle.append(dash_animation, radius_animation)
circle_layer.append(circle)
```

::svg-preview{src="/showcase/tutorial_layered_art_circle.svg" alt="Animated dashed circle showing the radius pulse before it is placed behind the arcs."}
::

## Gradient Fill

Use `ensure_defs()` and `LinearGradient` for reusable SVG definitions. The
gradient's `url` property returns the `url(#...)` reference used by `fill`.

```python
defs = svg.ensure_defs()

gradient = dp.LinearGradient(id="art-gradient", gradientTransform="rotate(90)")
gradient.add_stop("0%", color3)
gradient.add_stop("100%", color1)
defs.append(gradient)

circle.fill = gradient.url
circle.stroke = "#6b7280"

svg.save("layered-art.svg")
```

::svg-preview{src="/showcase/tutorial_layered_art_final.svg" alt="Final layered SVG artwork with blended arcs and a gradient circle."}
::
