# Font utilities

This module provides functions and classes for working with system fonts and measuring text dimensions. It includes a utility function to search for a system font file that matches a given font family and weight, as well as a class to measure the width and height of rendered text using the PIL library.


## <span class="func"></span>`get_system_font_path`

```py
get_system_font_path(
    font_family: str,
    weight: int = 400,
    weight_tolerance: int = 100
) -> str | None
```

Searches common system directories for a TrueType or OpenType font file (`.ttf` or `.otf`) that matches the specified `font_family` and is within the desired weight tolerance.

<span class="param">**Parameters**</span>

- `font_family` *(str)*: The desired system font name (e.g., "Arial").
- `weight` *(int, optional)*: The numeric weight (e.g., 400 for regular, 700 for bold; default: 400).
- `weight_tolerance` *(int, optional)*: Allowed difference between the desired weight and the font's actual weight (default: 100).

<span class="returns">**Returns**</span>

*(str | None)*: The full path to the matching font file, or None if no match is found.

```py
path = get_system_font_path("Arial", 400)
if path:
    print("Found font:", path)
else:
    print("Font not found")
```

## <span class="class"></span>`TypographyMeasurer`

The TypographyMeasurer class measures the rendered width and height of text given a specific font and size. It converts point sizes to pixels based on the provided DPI and leverages the PIL library for text measurement.

```py
TypographyMeasurer(dpi: float = 72.0, font_path: str | None = None)
```

<span class="param">**Parameters**</span>

- `dpi` *(float, optional)*: Dots per inch for converting point sizes to pixels (default: 72.0).
- `font_path` *(str | None, optional)*: The path to a font file. If not provided, the system is searched using get_system_font_path.

```py
measurer = TypographyMeasurer(dpi=96)
```

### <span class="meth"></span>`measure_text`

```py
measure_text(
    text: str,
    font_family: str | None = None,
    weight: int | None = None,
    font_size: float = 12.0
) -> tuple[float, float]
```

Measures the width and height (in pixels) of the provided text when rendered in the specified font. Multiline text is supported if newline characters are present.

<span class="param">**Parameters**</span>

- `text` *(str)*: The text to measure.
- `font_family` *(str | None, optional)*: The system font name (e.g., "Arial"). Required if no font_path is already set.
- `weight` *(int | None, optional)*: Numeric weight (e.g., 400 for regular, 700 for bold). Required if no font_path is already set.
- `font_size` *(float, optional)*: The desired font size in points (default: 12.0).

<span class="returns">**Returns**</span>

*(tuple[float, float])*: A tuple (width, height) in pixels.

raises `ValueError`: If the specified font cannot be found (when both `font_path` is not provided and `font_family` or `weight` are missing).

```py
measurer = TypographyMeasurer()
width, height = measurer.measure_text(
    "Hello\nWorld",
    font_family="Arial",
    weight=400,
    font_size=14,
)
print(f"Text dimensions: {width}px x {height}px")
```