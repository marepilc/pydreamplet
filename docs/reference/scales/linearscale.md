# `LinearScale`

The `LinearScale` class maps a numeric value from a specified domain to an output range using a linear transformation.

## <span class=class></span>`pydreamplet.scales.LinearScale`

```py
LinearScale(
    domain: tuple[float, float],
    output_range: tuple[float, float]
)
```

<span class="param">**Parameters**</span>

- `domain` *(tuple[float, float])*: The input domain as a minimum and maximum value.
- `output_range` *(tuple[float, float])*: The target output range.

```py
scale = LinearScale((0, 100), (0, 1))
print(scale.map(50))  # Output: 0.5
print(scale.invert(0.75))  # Output: 75.0
```

### <span class="meth"></span>`map`

```py
map(value: float) -> float
```

Scales a value from the domain to the output range.

### <span class="meth"></span>`invert`

```py
invert(value: float) -> float
```

Maps a value from the output range back to the domain.

### <span class="prop"></span>`domain`

Get or set the input domain.

### <span class="prop"></span>`output_range`

Get or set the target output range.