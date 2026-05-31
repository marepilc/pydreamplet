---
title: Typography
description: System font lookup and text measurement with HarfBuzz and fontTools.
navigation:
  title: Typography
category: reference
---

# Typography

The `pydreamplet.typography` module resolves installed font files and measures
text with HarfBuzz shaping plus fontTools line metrics. Use it when generated
layout depends on text dimensions.

Typography utilities are imported from `pydreamplet.typography`.

```python
from pydreamplet.typography import TypographyMeasurer, get_system_font_path
```

## Visual Example

This example measures a `Text` element and draws the measured box behind it. Use
an explicit `font_path` when reproducible dimensions matter, because system font
lookup depends on the machine where the code runs.

```python
import pydreamplet as dp
from pydreamplet.typography import TypographyMeasurer, get_system_font_path

font_path = get_system_font_path("Arial", 400)
if font_path is None:
    raise RuntimeError("Arial is not available on this system.")

label = dp.Text(
    "pyDreamplet",
    x=32,
    y=78,
    font_family="Arial",
    font_size=32,
    font_weight=400,
    fill="currentColor",
)

measurer = TypographyMeasurer(font_path=font_path)
width, height = measurer.measure_text(label)

svg = dp.SVG(300, 140)
svg.append(
    dp.Rect(
        x=label.x,
        y=label.y - height * 0.78,
        width=width,
        height=height,
        fill="none",
        stroke="#14b8a6",
        stroke_width=2,
        stroke_dasharray="5 4",
    ),
    dp.Line(label.x, label.y, label.x + width, label.y, stroke="#f83898", stroke_width=2),
    label,
    dp.Text(f"{width:.1f} x {height:.1f}", x=32, y=116, font_size=12, fill="currentColor"),
)
```

::svg-preview{src="/showcase/ref_typography_measure.svg" alt="Measured text with a dashed bounding box and baseline."}
::

## get_system_font_path

```python
get_system_font_path(
    font_family: str,
    weight: int = 400,
    weight_tolerance: int = 100,
) -> str | None
```

Searches common system font directories for a `.ttf` or `.otf` file whose name
records contain `font_family`. If the font has an `OS/2` table, its
`usWeightClass` must be within `weight_tolerance` of `weight`.

```python
font_path = get_system_font_path("Arial", 700)

if font_path is None:
    print("Font not found")
else:
    print(font_path)
```

The lookup is intentionally environment-dependent. For stable output in a
project or CI job, pass a known font file path to `TypographyMeasurer`.

## TypographyMeasurer

```python
TypographyMeasurer(dpi: float = 72.0, font_path: str | None = None)
```

`dpi` controls point-to-pixel conversion. At the default `72.0`, one point maps
to one pixel. `font_path` can be set once so later measurements do not need a
system font lookup.

```python
measurer = TypographyMeasurer(font_path="assets/fonts/Inter-Regular.ttf")
```

## measure_text

```python
measure_text(
    text: str | TextElementLike,
    *,
    font_family: str | None = None,
    weight: int | None = None,
    font_size: Real | str | None = None,
) -> tuple[float, float]
```

Measures shaped text width and line-metric height in pixels. `text` can be a
plain string or an element with a string `content` property, such as `Text`.

For plain strings, provide `font_family` and `weight` unless the measurer already
has `font_path`.

```python
measurer = TypographyMeasurer()
width, height = measurer.measure_text(
    "Hello\nWorld",
    font_family="Arial",
    weight=400,
    font_size=16,
)
```

For `Text` elements, `measure_text()` reads `content`, `font_family`,
`font_weight`, and `font_size` from the element when those values are not passed
explicitly. `font_size` may be numeric or a string with a leading number, such as
`"16px"` or `"10.5pt"`.

```python
label = dp.Text("Measured label")
label.font_family = "Arial"
label.font_size = "16px"
label.font_weight = 400

width, height = TypographyMeasurer().measure_text(label)
```

Multiline text uses the widest shaped line and one line height per line.

```python
single_width, single_height = measurer.measure_text(
    "Line",
    font_family="Arial",
    weight=400,
    font_size=16,
)
multi_width, multi_height = measurer.measure_text(
    "Line\nLine",
    font_family="Arial",
    weight=400,
    font_size=16,
)

assert multi_width == single_width
assert multi_height == single_height * 2
```

`measure_text()` raises `ValueError` when no font path can be resolved and
raises `TypeError` when the input is neither a string nor a text-like element.
