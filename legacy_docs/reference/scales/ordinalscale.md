# `OrdinalScale`

The `OrdinalScale` class maps categorical values to a set of output values in a cyclic (repeating) fashion. This is useful for assigning properties like colors in order.

## <span class=class></span>`pydreamplet.scales.OrdinalScale`

<!--skip-->
```py
OrdinalScale(domain: list[Any], output_range: list)
```

<span class="param">**Parameters**</span>

- `domain` *(list[Any])*: A list of categorical values (distinct).
- `output_range` *(list)*: A list of output values (e.g., colors) to map to, which are reused cyclically.

```py
from pydreamplet.scales import OrdinalScale

ordinal = OrdinalScale(["apple", "banana", "cherry"], ["red", "yellow"])
print(ordinal.map("cherry"))  # Output: "red" (wraps around)
```

### <span class="meth"></span>`map`

<!--skip-->
```py
map(value: Any) -> object
```

Returns the mapped output value for the given domain value.

### <span class="prop"></span>`domain`

Get or set the list of categories.

### <span class="prop"></span>`output_range`

Get or set the list of output values.
