# `Line`

The `Line` class represents an SVG line element. It allows setting start and end coordinates and provides computed properties for its length and angle.

!!! info

    This class inherits from [**`SvgElement`**](svgelement.md).

## <span class=class></span>`pydreamplet.core.Line`

```py
Line(
    x1: float = 0,
    y1: float = 0,
    x2: float = 0,
    y2: float = 0,
    **kwargs
)
```

Initializes a new line with specified start (x1, y1) and end (x2, y2) coordinates.

<span class="param">**Parameters**</span>

- `x1` *(float)*: The x-coordinate of the start point.
- `y1` *(float)*: The y-coordinate of the start point.
- `x2` *(float)*: The x-coordinate of the end point.
- `y2` *(float)*: The y-coordinate of the end point.
- `**kwargs`: Additional attributes for the line.

```py
from pydreamplet import SVG, Line

svg = SVG(200, 200)
svg.append(
    Line(x1=10, y1=190, x2=190, y2=10, stroke="#a00344", stroke_width=5)
)
```

![Result](assets/line_example.svg){.img-light-dark-bg}

### <span class="prop"></span>`x1`, `y1`, `x2`, `y2`

**Getters and Setters:** Retrieve or update the line's coordinates.

```py
print(line.x1, line.y1, line.x2, line.y2)
line.x1 = 10
line.y1 = 10
```

### <span class="prop"></span>`length`

Returns the length of the line calculated using the distance formula.

```py
print(line.length)
```

### <span class="prop"></span>`angle`

Returns the angle (in degrees) of the line relative to the positive x-axis.

```py
print(line.angle)
```
