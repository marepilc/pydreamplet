# `ColorScale`

The `ColorScale` class creates a color scale that maps a numeric value from a given domain to an interpolated hex color between two specified colors.

## <span class=class></span>`pydreamplet.scales.ColorScale`

<!--skip-->
```py
ColorScale(
    domain: NumericPair,
    output_range: tuple[str, str]
)
```

<span class="param">**Parameters**</span>

- `domain` *(NumericPair)*: The numeric input domain.
- `output_range` *(tuple[str, str])*: A tuple of two hex color strings representing the start and end colors.

```py
from pydreamplet.scales import ColorScale

color_scale = ColorScale((0, 100), ("#ff0000", "#00ff00"))
print(color_scale.map(50))  # Outputs an #7f7f00
```

### <span class="meth"></span>`map`

<!--skip-->
```py
map(value: float) -> str
```

Maps the input numeric value to an interpolated hex color.

### <span class="prop"></span>`domain`

Get or set the numeric domain.

### <span class="prop"></span>`output_range`

Get or set the pair of hex colors.
