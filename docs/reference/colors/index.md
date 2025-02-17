# Color utilities

This module provides various utility functions for color conversion, manipulation, and random color generation.

## <span class="func"></span>`hexStr`

```py
hexStr(n: int) -> str
```

Converts an integer (0-255) to a two-digit hexadecimal string.

<span class="param">**Parameters**</span>

- `n` *(int)*: An integer value between 0 and 255.

```py
print(hexStr(15))  # Output: "0f"
```

## <span class="func"></span>`random_int`

```py
random_int(min_val: int, max_val: int) -> int
```

Returns a random integer N such that min_val <= N <= max_val.

<span class="param">**Parameters**</span>

- `min_val` *(int)*: The minimum value.
- `max_val` *(int)*: The maximum value.

```py
print(random_int(1, 10))  # Output: An integer between 1 and 10
```
## <span class="func"></span>`str2rgb`

```py
str2rgb(col: str) -> dict
```

Converts a hex color string to an RGB dictionary. Accepts strings in the format "#RRGGBB" or "#RGB".
If the input doesn't match, returns `{'r': 0, 'g': 0, 'b': 0}`.

<span class="param">**Parameters**</span>

- `col` *(str)*: A hex color string.

```py
print(str2rgb("#ff0000"))  # Output: {'r': 255, 'g': 0, 'b': 0}
print(str2rgb("#f00"))     # Output: {'r': 255, 'g': 0, 'b': 0}
```

## <span class="func"></span>`hex_to_rgb`

```py
hex_to_rgb(hex_color: str) -> tuple[int, int, int]
```

Converts a hex color string (e.g., "#ff0000") to an (R, G, B) tuple.

<span class="param">**Parameters**</span>

- `hex_color` *(str)*: A hex color string in the format "#RRGGBB".

```py
print(hex_to_rgb("#00ff00"))  # Output: (0, 255, 0)
```

## <span class="func"></span>`rgb_to_hex`

```py
rgb_to_hex(rgb: tuple[int, int, int]) -> str
```

Converts an (R, G, B) tuple to a hex color string.

<span class="param">**Parameters**</span>

- `rgb` *(tuple[int, int, int])*: A tuple representing red, green, and blue values.

```py
print(rgb_to_hex((0, 0, 255)))  # Output: "#0000ff"
```

## <span class="func"></span>`color2rgba`

```py
color2rgba(c, alpha=1) -> str
```

Converts an input color (which can be a list/tuple of three numbers, an integer, or a hex string) and an alpha value to an "rgba(r, g, b, a)" string.

<span class="param">**Parameters**</span>

- `c` *(list/tuple/int/str)*: The input color in one of the supported formats.
- `alpha` *(float, optional)*: The alpha value (default is 1).

```py
print(color2rgba((255, 0, 0), 0.5))   # Output: "rgba(255, 0, 0, 0.5)"
print(color2rgba("#00ff00", 0.75))     # Output: "rgba(0, 255, 0, 0.75)"
```
## <span class="func"></span>`blend`

```py
blend(color1: str, color2: str, proportion: float) -> str
```

Blends two hex color strings by the given proportion.
A proportion of 0 returns color1 and 1 returns color2.
Returns the blended color as a hex string.

<span class="param">**Parameters**</span>

- `color1` *(str)*: The first hex color string.
- `color2` *(str)*: The second hex color string.
- `proportion` *(float)*: The blend proportion (between 0 and 1).

```py
print(blend("#ff0000", "#0000ff", 0.5))  # Output: A blended color, e.g., "#800080"
```

## <span class="func"></span>`random_color`

```py
random_color() -> str
```

Generates a random hex color string.

```py
print(random_color())  # Output: e.g., "#3a5fcd"
```

## <span class="func"></span>`generate_colors`

```py
generate_colors(
    base_color: str,
    n: int = 4,
    harmony: str = "complementary"
) -> list[str]
```

Generates a list of colors based on a selected color harmony. The function takes a base hex color and produces a palette of n colors by applying a specific harmony rule. It supports the following harmonies:

- `complementary:` Uses the base color and its direct opposite on the color wheel.
- `compound:` Uses the base color along with two hues adjacent to its complement (a split-complementary scheme).
- `square:` Produces four colors evenly spaced around the color wheel.
- 
<span class="param">**Parameters**</span>

- `base_color` *(str)*: The starting color in hex format (e.g., "#db45f9").
- `n` *(int)*: The total number of colors to generate.
- `harmony` *(str)*: The color harmony to apply. Supported options are `"complementary"`, `"compound"`, and `"square"`.
- 
<span class="returns">**Returns**</span>

- *(list[str])*: A list of hex color strings representing the generated color palette.

```py
# Example: Generate a complementary palette of 4 colors.
palette = generate_colors(base_color="#db45f9", n=4, harmony="complementary")
print(palette)
# Example output: ['#db45f9', '#f945db', ...]
```

This function leverages color space conversions and lightness variations to create balanced palettes that adhere to the selected harmony.