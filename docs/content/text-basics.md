---
title: Text basics
description: Place, align, and measure SVG text elements.
navigation:
  title: Text basics
category: guide
---

# Text Basics

Use `Text` for labels, captions, annotations, and chart typography. Text is an
SVG element, so it uses the same attribute model as shapes.

## Placing Text

Create text with content and place it with `x` and `y` or `pos`.

```python
import pydreamplet as dp

svg = dp.SVG(540, 360)

title = dp.Text(
    "pyDreamplet",
    x=svg.w / 2,
    y=92,
    fill="currentColor",
    font_size=44,
    font_weight=700,
    text_anchor="middle",
)

svg.append(title)
```

The `x` and `y` attributes define the text anchor point, not the top-left
corner of a text box.

## Alignment

Use `text_anchor` for horizontal alignment and `alignment_baseline` for vertical
alignment.

```python
center = dp.G(pos=(svg.w / 2, svg.h / 2))
svg.append(center)

center.append(dp.Circle(cx=0, cy=0, r=86, fill="#14b8a6", opacity=0.18))
center.append(dp.Line(-110, 0, 110, 0, stroke="currentColor", opacity=0.35))
center.append(dp.Line(0, -70, 0, 70, stroke="currentColor", opacity=0.35))

center.append(
    dp.Text(
        "centered",
        x=0,
        y=0,
        fill="currentColor",
        font_size=26,
        text_anchor="middle",
        alignment_baseline="middle",
    )
)
```

For labels next to marks, change the anchor instead of manually estimating text
width.

```python
center.append(
    dp.Text(
        "start",
        x=102,
        y=0,
        fill="#f83898",
        font_size=18,
        text_anchor="start",
        alignment_baseline="middle",
    )
)
```

::svg-preview{src="/showcase/text_basics_01.svg" alt="Example SVG generated from the text basics code"}
::

## Multiline Text

`Text` accepts newline characters. Use `v_space` to control the vertical spacing
between lines.

```python
note = dp.Text(
    "vector graphics\nwith code",
    x=svg.w / 2,
    y=292,
    fill="currentColor",
    font_size=20,
    text_anchor="middle",
    v_space=26,
)

svg.append(note)
```

## Measuring Text

When layout depends on text dimensions, use `TypographyMeasurer`. It can read
font properties from a `Text` element.

```python
from pydreamplet.typography import TypographyMeasurer

label = dp.Text(
    "Measured label",
    font_family="Arial",
    font_size=18,
    font_weight=400,
)

measurer = TypographyMeasurer()
width, height = measurer.measure_text(label)
```

Measurements are layout estimates. Browser rendering can differ slightly
between operating systems, fonts, and SVG viewers.

## Next

Continue with the reference section for API-level details.
