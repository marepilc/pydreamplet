# `PointScale`

The `PointScale` class maps categorical values to discrete points within the output range, with specified padding at both ends.

## <span class=class></span>`pydreamplet.scales.PointScale`

<!--skip-->
```py
PointScale(
    domain: list[Any],
    output_range: NumericPair,
    padding: float = 0.5
)
```

<span class="param">**Parameters**</span>

- `domain` *(list[Any])*: A list of categorical values (distinct).
- `output_range` *(NumericPair)*: The numeric output range.
- `padding` *(float, optional)*: The amount of padding on each end (default: 0.5).

```py
from pydreamplet.scales import PointScale

point = PointScale(["X", "Y", "Z"], (0, 100))
print(point.map("Y"))  # Outputs the point corresponding to "Y"
```

### <span class="meth"></span>`map`

<!--skip-->
```py
map(value: Any) -> float | None
```

Maps a categorical value to a discrete point; returns None if the value is not in the domain.

### <span class="prop"></span>`domain`

Get or set the list of categories.

### <span class="prop"></span>`output_range`

Get or set the numeric output range.

### <span class="prop"></span>`padding`

Get or set the padding value.
