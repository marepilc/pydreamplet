---
title: Drawing basics
description: Learn the core pyDreamplet drawing workflow with SVG canvases, shapes, attributes, and output.
navigation:
  title: Drawing basics
category: guide
---

# Drawing Basics

pyDreamplet follows the SVG document model. You create a root `SVG`, add
elements to it, configure their attributes, and save or display the result.

## Canvas Size

Create an SVG canvas with a width and height in SVG user units. In most cases,
one user unit maps to one CSS pixel when the file is displayed at its natural
size.

```python
import pydreamplet as dp

svg = dp.SVG(540, 360)
```

The coordinate system starts in the top-left corner. `x` grows to the right and
`y` grows downward.

## Shapes

Append shapes to the canvas in drawing order. Later elements are painted above
earlier elements.

```python
import pydreamplet as dp

svg = dp.SVG(540, 360)

circle = dp.Circle(
    cx=svg.w / 2,
    cy=svg.h / 2,
    r=96,
    fill="#14b8a6",
    stroke="currentColor",
    stroke_width=6,
)

svg.append(circle)
```

## Styling

SVG styling is attribute based. Set `fill`, `stroke`, `stroke_width`, opacity,
and other visual attributes on the element you are creating.

```python
label = dp.Text(
    "pyDreamplet",
    x=svg.w / 2,
    y=svg.h / 2,
    fill="currentColor",
    font_size=28,
    text_anchor="middle",
    alignment_baseline="middle",
)

svg.append(label)
```

Use groups when multiple elements should move, transform, or share structure.

```python
dots = dp.G(pos=(svg.w / 2, svg.h / 2))
dots.append(dp.Circle(cx=-svg.w / 3, cy=0, r=24, fill="#95cf20"))
dots.append(dp.Circle(cx=svg.w / 3, cy=0, r=24, fill="#f83898"))

svg.append(dots)
```

## Output

Save the drawing as an SVG file from scripts.

```python
svg.save("drawing.svg")
```

In notebooks, render the current canvas inline.

```python
svg.display()
```

::svg-preview{src="/showcase/drawing_basis_01.svg" alt="Example SVG generated from the drawing basics code"}
::

## Next

Continue with [Path basics](/path-basics) to build custom contours with
`Path` and `PathBuilder`.
