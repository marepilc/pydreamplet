# `SquareScale`

The `SquareScale` class maps an input value to an output using a square-root transformation. This is useful when a visual property (e.g., a square's side length) should be proportional to the square root of the area.

## <span class=class></span>`pydreamplet.scales.SquareScale`

```py
SquareScale(
    domain: tuple[float, float],
    output_range: tuple[float, float]
)
```

<span class="param">**Parameters**</span>

- `domain` *(tuple[float, float])*: The input domain (non-negative values).
- `output_range` *(tuple[float, float])*: The target output range.

```py
square = SquareScale((0, 100), (0, 10))
print(square.map(25))  # Maps the square-root of 25 to the output range
```


### <span class="meth"></span>`map`

```py
map(value: float) -> float
```

Scales the value using a square-root transformation.

### <span class="prop"></span>`domain`

Get or set the numeric domain.

### <span class="prop"></span>`output_range`

Get or set the target output range.
