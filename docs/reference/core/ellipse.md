# `Ellipse`

The `Ellipse` class represents an SVG ellipse element. It supports setting the center position.

!!! info

    This class inherites from [**`SvgElement`**](svgelement.md).

## <span class=class></span>`pydreamplet.core.Ellipse`

```py
Ellipse(**kwargs)
```

Initializes a new ellipse. If `pos` is provided, it sets the center coordinates.

<span class="param">**Parameters**</span>

- `**kwargs`: Attributes for the ellipse, including `pos` (a Vector) and other properties (e.g., `rx`, `ry`).

```py
ellipse = Ellipse(pos=Vector(100, 80), rx=40, ry=20, fill="green")
```

### <span class="prop"></span>`pos`

**Getter:** Returns the center of the ellipse as a Vector.

**Setter:** Updates the center coordinates.

```py
print(ellipse.pos)
ellipse.pos = Vector(120, 90)
```
