# `Polygon`

The `Polygon` class represents an SVG polygon element. It allows setting a list of points and automatically formats these into the SVG-compatible `"x,y x,y …"` string.

!!! info

    This class inherits from [**`SvgElement`**](svgelement.md).

## <span class=class></span>`pydreamplet.core.Polygon`

```py
Polygon(
    points: list[Real],
    **kwargs
)
```

Initializes a new polygon with the specified vertices. The points must be provided as a list of numbers where every two elements represent the x and y coordinates of a vertex.

<span class="param">**Parameters**</span>

- `points` *(list[Real])*: A list of numbers representing the polygon's vertices, for example: `[x1, y1, x2, y2, x3, y3, ...]`.
- `**kwargs`: Additional attributes for the polygon element.

```py
from pydreamplet import SVG, Polygon

svg = SVG(200, 200)
svg.append(Polygon([10, 10, 100, 180, 150, 50], fill="#a00344"))
```

![Result](assets/polygon_example.svg){.img-light-dark-bg}

### <span class="prop"></span>`points`

**Getters and Setters:** Retrieve or update the polygon's points. When setting new points, the list is automatically formatted into a string where each vertex is expressed as `"x,y"` and each pair is separated by a space.

```py
print(polygon.points)  # [0, 0, 50, 50, 100, 0]
polygon.points = [0, 0, 0, 20, 20, 20, 20, 0]
```

When the `points` setter is called, the underlying SVG element's `points` attribute is updated to: `points="0,0 0,20 20,20 20,0"`.