---
title: Colors
description: Reference for color helpers exported from pydreamplet and pydreamplet.colors.
navigation:
  title: Colors
category: reference
---

# Colors

Color helpers convert colors, blend hex values, and generate palettes.

The most commonly used helpers are exported from top-level `pydreamplet`:

```python
import pydreamplet as dp
```

Lower-level legacy helpers are still available from `pydreamplet.colors`.

## Theme

`Theme` stores reusable font settings and color tokens. With no arguments it
uses built-in defaults.

```python
theme = dp.Theme()

assert theme.font_family == "sans-serif"
assert theme.font_size == 14
assert theme.blue == "#1447e6"
assert theme.color is theme.colors
```

Pass a JSON file path to override part or all of the default theme:

```json
{
  "font": {
    "fontFamily": "Roboto",
    "fontSize": 12,
    "fontWeight": 400,
    "lineHeight": 1.5
  },
  "colors": {
    "ink": "#18181b",
    "surface": "#e4e4e7",
    "brand": "#1447e6"
  }
}
```

```python
theme = dp.Theme("themes/light.json")
theme.font_family = "Roboto"
theme.font_size = 12
theme.font_weight = 600

theme.brand = (212, 136, 113)
theme.muted = (212, 136, 113, 0.5)
theme.gray = 128

assert theme.brand == "#d48871"
assert theme.muted == "rgba(212, 136, 113, 0.5)"
assert theme.gray == "#808080"
assert theme.colors.brand == "#d48871"
assert theme.colors["surface"] == "#e4e4e7"
```

`Color` is the token container used by `Theme.colors`. It supports attribute
access, mapping access, custom tokens, hex strings, CSS color strings, grayscale
integers, RGB tuples, and RGBA tuples. `Theme` also exposes color tokens
directly, so `theme.amber` is equivalent to `theme.colors.amber`.

## Visual Example

```python
import pydreamplet as dp

palette = dp.generate_colors("#db45f9", n=8)

svg = dp.SVG(360, 120)

for index, color in enumerate(palette):
    svg.append(
        dp.Rect(x=20 + index * 40, y=24, width=34, height=52, rx=6, fill=color),
        dp.Text(str(index + 1), x=37 + index * 40, y=96, font_size=13, text_anchor="middle", fill="currentColor"),
    )
```

::svg-preview{src="/showcase/ref_colors_palette.svg" alt="Eight generated color swatches from a base color."}
::

## Top-Level Helpers

```python
Theme(path: str | Path | None = None)
Color(**values: ColorInput)
hex_to_rgb(hex_color: str) -> tuple[int, int, int]
rgb_to_hex(rgb: tuple[int, int, int]) -> str
color2rgba(c: ColorInput, alpha: float = 1) -> str
blend_colors(color1: ColorInput, color2: ColorInput, proportion: float) -> str
blend(color1: ColorInput, color2: ColorInput, proportion: float) -> str
random_color() -> str
generate_colors(base_color: str, n: int = 10) -> list[str]
```

### `hex_to_rgb`

Converts a six-digit hex color to an RGB tuple. The leading `#` is optional.
Three-digit shorthand is not accepted by this helper.

```python
assert dp.hex_to_rgb("#ffffff") == (255, 255, 255)
assert dp.hex_to_rgb("000000") == (0, 0, 0)
```

Invalid lengths raise `ValueError`.

### `rgb_to_hex`

Converts an RGB tuple to a lowercase hex string.

```python
assert dp.rgb_to_hex((0, 0, 255)) == "#0000ff"
```

### `color2rgba`

Converts a hex string, grayscale integer, or three-number RGB sequence to CSS
`rgba(...)`.

```python
assert dp.color2rgba((255, 0, 0), alpha=0.5) == "rgba(255, 0, 0, 0.5)"
assert dp.color2rgba(128, alpha=0.75) == "rgba(128, 128, 128, 0.75)"
assert dp.color2rgba("#00ff00", alpha=0.3) == "rgba(0, 255, 0, 0.3)"
```

RGB channels and alpha are constrained to their valid ranges.

### `blend_colors`

Blends two supported color values. `proportion=0` returns the first color and
`proportion=1` returns the second. Proportions outside `[0, 1]` are constrained.
Opaque blends return hex. Blends involving alpha return `rgba(...)`.

```python
assert dp.blend_colors("#123456", "#abcdef", 0) == "#123456"
assert dp.blend_colors((0, 0, 0), 255, 0.5) in ("#7f7f7f", "#808080")
assert dp.blend_colors((212, 136, 113, 0.5), "#000000", 0) == "rgba(212, 136, 113, 0.5)"
assert dp.blend("invalid", "#abcdef", 0.5) == "#000000"
```

`blend` remains available as the shorter legacy name.

### `random_color`

Returns a random six-digit hex color string.

```python
color = dp.random_color()

assert color.startswith("#")
assert len(color) == 7
```

### `generate_colors`

Generates `n` colors by preserving the base color's lightness and saturation and
rotating hue evenly around the color wheel.

```python
palette = dp.generate_colors("#db45f9", n=5)

assert len(palette) == 5
assert palette[0].lower() == "#db45f9"
```

## Module Helpers

These helpers are available from `pydreamplet.colors`, but are not exported from
top-level `pydreamplet`.

```python
from pydreamplet.colors import hexStr, random_int, str2rgb
```

| Helper | Signature | Notes |
| --- | --- | --- |
| `hexStr` | `(n: int) -> str` | Formats an integer as a two-digit lowercase hex string. |
| `random_int` | `(min_val: int, max_val: int) -> int` | Inclusive random integer helper. |
| `str2rgb` | `(col: str) -> dict[str, int]` | Accepts `#RRGGBB` and `#RGB`; invalid input returns black. |

```python
from pydreamplet.colors import hexStr, str2rgb

assert hexStr(16) == "10"
assert str2rgb("#f00") == {"r": 255, "g": 0, "b": 0}
assert str2rgb("notacolor") == {"r": 0, "g": 0, "b": 0}
```
