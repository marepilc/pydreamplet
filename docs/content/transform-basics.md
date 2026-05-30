---
title: Transform basics
description: Move, rotate, and scale SVG elements with groups and vectors.
navigation:
  title: Transform basics
category: guide
---

# Transform Basics

Use transforms when geometry should stay local, but its rendered position,
rotation, or scale should change. In pyDreamplet, the most common pattern is to
append elements to a `G` group and transform the group.

## Local Coordinates

A group creates a local coordinate system for its children. The elements inside
the group can be drawn around `(0, 0)`, then the group can be moved as a single
unit.

```python
import pydreamplet as dp

svg = dp.SVG(540, 360)

origin = dp.G(pos=(svg.w / 2, svg.h / 2))
svg.append(origin)

origin.append(dp.Circle(cx=0, cy=0, r=6, fill="#14b8a6"))
origin.append(
    dp.Line(
        x1=-120,
        y1=0,
        x2=120,
        y2=0,
        stroke="currentColor",
        stroke_width=3,
        opacity=0.45,
    )
)
origin.append(
    dp.Line(
        x1=0,
        y1=-120,
        x2=0,
        y2=120,
        stroke="currentColor",
        stroke_width=3,
        opacity=0.28,
    )
)
```

The group is centered on the canvas, but its children still use coordinates
relative to the group origin.

## Rotation

Set `angle` on a group to rotate everything inside it.

```python
needle = dp.G(angle=-28)
origin.append(needle)

needle.append(
    dp.Rect(
        x=-12,
        y=-118,
        width=24,
        height=110,
        rx=12,
        fill="#38bdf8",
        stroke="currentColor",
        stroke_width=4,
    )
)
```

This keeps the shape simple. The rectangle is still defined vertically around
the local origin, and the group handles the rotation.

## Scale And Pivot

Scaling and rotation happen around the group pivot. The default pivot is
`(0, 0)`, which is usually what you want when the group is drawn around its own
origin.

```python
markers = dp.G(scale=dp.Vector(1.15, 1.15))
origin.append(markers)

for angle in range(0, 360, 45):
    mark = dp.G(angle=angle)
    mark.append(
        dp.Circle(cx=0, cy=-140, r=8, fill="#f83898", stroke="currentColor", stroke_width=3)
    )
    markers.append(mark)
```

When the pivot needs to be somewhere else, set `pivot=(x, y)` explicitly.

## Transform Order

`G` exposes an `order` property for transform composition. The default is
`"trs"`, which applies translation, then rotation, then scale.

```python
badge = dp.G(pos=(430, 96), angle=18, scale=dp.Vector(1.2, 1.2), order="trs")
badge.append(dp.Rect(x=-42, y=-24, width=84, height=48, rx=10, fill="#95cf20"))
badge.append(
    dp.Text(
        "trs",
        x=0,
        y=0,
        fill="currentColor",
        font_size=18,
        text_anchor="middle",
        alignment_baseline="middle",
    )
)

svg.append(badge)
```

Changing the order can produce a visibly different result, especially when
translation, rotation, and non-uniform scale are combined.

::svg-preview{src="/showcase/transform_basics_01.svg" alt="Example SVG generated from the transform basics code"}
::

## Next

Continue with text basics to place, align, and measure SVG text.
