# `Ellipse`

The `Ellipse` class represents an SVG ellipse element. It supports setting the center position.

!!! info

    This class inherits from [**`SvgElement`**](svgelement.md).

## <span class=class></span>`pydreamplet.core.Ellipse`

```py
Ellipse(**kwargs)
```

Initializes a new ellipse. If `pos` is provided, it sets the center coordinates.

<span class="param">**Parameters**</span>

- `**kwargs`: Attributes for the ellipse, including `pos` (a [`Vector`](../math/vector.md)) and other properties (e.g., `rx`, `ry`).

```py
from pydreamplet import SVG, Ellipse, Vector

svg = SVG(200, 200)
svg.append(Ellipse(pos=Vector(100, 100), rx=60, ry=40, fill="#a00344"))
```

![Result](assets/ellipse_example.svg){.img-light-dark-bg}

### <span class="prop"></span>`pos`

**Getter:** Returns the center of the ellipse as a [`Vector`](../math/vector.md).

**Setter:** Updates the center coordinates.

```py
print(ellipse.pos)
ellipse.pos = Vector(120, 90)
```
