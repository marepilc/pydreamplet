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

`SVG` also accepts a four-value viewBox. The display width and height default
to the viewBox width and height with a `px` unit.

```python
svg = dp.SVG(10, 10, 540, 360)

print(svg.viewBox)
# 10 10 540 360
```

Override the displayed size separately from the internal coordinate system with
`width` and `height`.

```python
svg = dp.SVG(540, 360, width="1080px", height="720px")
```

Load an existing SVG file with `SVG.from_file()`.

```python
logo = dp.SVG.from_file("logo.svg")
```

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

SVG attribute names that contain hyphens are written with underscores in Python
attribute access and keyword arguments. For example, `stroke_width` serializes
to `stroke-width`.

```python
circle.fill = "none"
circle.stroke = "#14b8a6"
circle.stroke_width = 4
```

Use `attrs()` when you want to set several attributes at once. Keys can use the
same Python-friendly names.

```python
circle.attrs({
    "stroke_width": 6,
    "stroke_linecap": "round",
})
```

Assigning `None` removes an attribute. Use the SVG string `"none"` when you
want to keep the attribute and render no paint.

```python
circle.fill = "none"  # SVG fill="none"
circle.fill = None    # removes the fill attribute
```

Use groups when multiple elements should move, transform, or share structure.

```python
dots = dp.G(pos=(svg.w / 2, svg.h / 2))
dots.append(dp.Circle(cx=-svg.w / 3, cy=0, r=24, fill="#95cf20"))
dots.append(dp.Circle(cx=svg.w / 3, cy=0, r=24, fill="#f83898"))

svg.append(dots)
```

## Generic Elements

Use a dedicated wrapper such as `Circle`, `Rect`, `Path`, `Use`, or `Text` when
one exists. Use `SvgElement` for SVG tags that pyDreamplet does not wrap
directly.

```python
shadow = dp.SvgElement(
    "feDropShadow",
    dx=0,
    dy=4,
    stdDeviation=3,
)
```

Dedicated wrappers can expose extra convenience properties. A generic
`SvgElement("circle")` serializes as a circle, but it does not have
circle-specific helpers such as `area`.

## Tree Operations

`append()` accepts one or more children. Use `find()` and `find_all()` to locate
children by tag, id, or class.

```python
svg = dp.SVG(400, 160)

for index in range(5):
    svg.append(
        dp.Circle(
            cx=80 + index * 60,
            cy=80,
            r=18,
            fill="#14b8a6",
            id=f"dot-{index + 1}",
            class_name="even" if index % 2 == 0 else "odd",
        )
    )

for dot in svg.find_all("circle", class_name="odd"):
    dot.fill = "none"
    dot.stroke = "currentColor"

middle = svg.find("circle", id="dot-3")
if middle is not None:
    svg.remove(middle)
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
