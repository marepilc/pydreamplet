# `LinearScale`

The `LinearScale` class maps a numeric value from a specified domain to an output range using a linear transformation.

## <span class=class></span>`pydreamplet.scales.LinearScale`

<!--skip-->
```py
LinearScale(
    domain: NumericPair,
    output_range: NumericPair
)
```

<span class="param">**Parameters**</span>

- `domain` *(NumericPair)*: The input domain as a minimum and maximum value.
- `output_range` *(NumericPair)*: The target output range.

```py
from pydreamplet.scales import LinearScale

scale = LinearScale((0, 100), (0, 1))
print(scale.map(50))  # Output: 0.5
print(scale.invert(0.75))  # Output: 75.0
```

### <span class="meth"></span>`map`

<!--skip-->
```py
map(value: float) -> float
```

Scales a value from the domain to the output range.

### <span class="meth"></span>`invert`

<!--skip-->
```py
invert(value: float) -> float
```

Maps a value from the output range back to the domain.

### <span class="prop"></span>`domain`

Get or set the input domain.

### <span class="prop"></span>`output_range`

Get or set the target output range.