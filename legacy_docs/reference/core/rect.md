# `Rect`

The `Rect` class represents an SVG rectangle element. It supports setting the position and provides properties for width and height.

!!! info

    This class inherits from [**`SvgElement`**](svgelement.md).

## <span class=class></span>`pydreamplet.core.Rect`

<!--skip-->
```py
Rect(**kwargs)
```

Initializes a new rectangle. If pos is provided, it sets the top-left corner.

<span class="param">**Parameters**</span>

- `**kwargs`: Attributes for the rectangle, including `pos` (a [`Vector`](../math/vector.md)) and other properties (e.g., `width`, `height`).
 
<!--skip-->
```py
from pydreamplet import SVG, Rect, Vector

svg = SVG(200, 200)
svg.append(
    Rect(
        pos=Vector(50, 50),
        width=100,
        height=100,
        fill="#a00344",
    )
)
```

![Example](assets/rect_example.svg){.img-light-dark-bg}

### <span class="prop"></span>`pos`

**Getter**: Returns the position (top-left corner) as a [`Vector`](../math/vector.md).

**Setter:** Updates the position.

<!--skip-->
```py
print(rect.pos)
rect.pos = Vector(20, 20)
```

### <span class="prop"></span>`width`

Returns the width of the rectangle.

### <span class="prop"></span>`height`

Returns the height of the rectangle.