# `Transformable`

The Transformable mixin adds transformation capabilities—translation, rotation, and scaling—to SVG elements. It is intended for use with group elements.

For parsing and serializing raw SVG transform strings, use `Transform` and `TransformList`.

## <span class=class></span>`pydreamplet.core.Transform`

<!--skip-->
```py
Transform(name: str, *values)
```

Represents one SVG transform function. Supported function names are `matrix`, `translate`, `scale`, `rotate`, `skewX`, and `skewY`.

```py
import pydreamplet as dp

transform = dp.Transform.rotate(45, 10, 20)
print(str(transform))  # rotate(45,10,20)
```

Convenience constructors are available:

- `Transform.translate(x, y=0)`
- `Transform.scale(x, y=None)`
- `Transform.rotate(angle, cx=None, cy=None)`
- `Transform.skew_x(angle)`
- `Transform.skew_y(angle)`
- `Transform.matrix(a, b, c, d, e, f)`

## <span class=class></span>`pydreamplet.core.TransformList`

<!--skip-->
```py
TransformList.parse(value: str) -> TransformList
```

Parses a transform attribute while preserving transform order.

```py
import pydreamplet as dp

transforms = dp.TransformList.parse("translate(10, 20) skewX(15) rotate(45)")
print(str(transforms))  # translate(10 20) skewX(15) rotate(45)
```

## <span class=class></span>`pydreamplet.core.Transformable`

<!--skip-->
<!--skip-->
```py
Transformable(
    pos: Vector = None,
    scale: Vector = None,
    angle: float = 0,
    *args,
    **kwargs
)
```

Initializes transformation properties with position, scale, and rotation angle.

<span class="param">**Parameters**</span>

- `pos` *(Vector, optional)*: Position vector (default: (0, 0)).
- `scale` *(Vector, optional)*: Scale vector (default: (1, 1)).
- `angle` *(float)*: Rotation angle (default: 0).

<!--skip-->
```py
t = Transformable(pos=Vector(10, 20), scale=Vector(2, 2), angle=45)
```

### <span class="prop"></span>`pos`
**Getter:** Returns the current position as a Vector.

**Setter:** Updates the position and refreshes the transform.

<!--skip-->
```py
print(t.pos)
t.pos = Vector(30, 40)
```

### <span class="prop"></span>`scale`

**Getter:** Returns the current scale as a Vector.

**Setter:** Updates the scale and refreshes the transform.

<!--skip-->
```py
print(t.scale)
t.scale = Vector(1, 1)
```

### <span class="prop"></span>`angle`

**Getter:** Returns the current rotation angle.

**Setter:** Updates the angle and refreshes the transform.

<!--skip-->
```py
print(t.angle)
t.angle = 90
```
