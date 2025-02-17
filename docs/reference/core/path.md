# `Path`

The `Path` class represents an SVG path element. It allows you to set the path data and provides computed properties based on the coordinates within the path.

!!! info

    This class inherits from [**`SvgElement`**](svgelement.md).

## <span class=class></span>`pydreamplet.core.Path`

```py
Path(d: str = "", **kwargs)
```

Initializes a new path with an optional d attribute containing path commands.

<span class="param">**Parameters**</span>

- `d` *(str, optional)*: The path data string.
- `**kwargs`: Additional attributes for the path element.

```py
path = Path(d="M10 20 L110 20 L110 70 L10 70 Z", fill="none", stroke="black")
```

### <span class="prop"></span>`d`

**Getter:** Returns the path data string.

**Setter:** Updates the path data.

```py
print(path.d)
path.d = "M0 0 L50 50"
```

### <span class="prop"></span>`width`

Returns the width of the path based on the extracted coordinates.

### <span class="prop"></span>`height`

Returns the height of the path based on the extracted coordinates.

### <span class="prop"></span>`center`

Returns the center point of the path as a [`Vector`](../math/vector.md).