# `BandScale`

The `BandScale` class maps categorical values (strings) to evenly spaced positions within the output range. It allows configuration of inner padding and outer padding.

## <span class=class></span>`pydreamplet.scales.BandScale`

```py
BandScale(
    domain: list[any],
    output_range: tuple[float, float],
    padding: float = 0.1,
    outer_padding: float | None = None
)

```

<span class="param">**Parameters**</span>

- `domain` *(list[any])*: A list of categorical values.
- `output_range` *(tuple[float, float])*: The numeric output range.
- `padding` *(float, optional)*: The inner padding between bands (default: 0.1).
- `outer_padding` *(float, optional)*: The outer padding; defaults to the inner padding if not provided.

```py
band = BandScale(["A", "B", "C"], (0, 300))
print(band.map("B"))  # Outputs the start position for category "B"
print(band.bandwidth)  # Width of each band
```

### <span class="meth"></span>`map`

```py
map(value: any) -> float
```

Returns the starting position of the band for the given categorical value.

### <span class="prop"></span>`bandwidth`

Returns the computed width of each band.

### <span class="prop"></span>`domain`

Get or set the list of categories.

### <span class="prop"></span>`output_range`

Get or set the numeric output range.

### <span class="prop"></span>`padding`

Get or set the inner padding.

### <span class="prop"></span>`outer_padding`

Get or set the outer padding.