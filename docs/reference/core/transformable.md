# `Transformable`

The Transformable mixin adds transformation capabilities—translation, rotation, and scaling—to SVG elements. It is intended for use with group elements.

For parsing and serializing raw SVG transform strings, use `Transform` and `TransformList`.

## <span class=class></span>`pydreamplet.core.Matrix2D`

<!--skip-->
```py
Matrix2D(a=1, b=0, c=0, d=1, e=0, f=0)
```

Represents an SVG 2D affine transform matrix in the standard `matrix(a b c d e f)` form.

```py
import pydreamplet as dp

matrix = dp.Matrix2D.translate(10, 20).multiply(dp.Matrix2D.scale(2, 3))
point = matrix.apply(5, 6)
print(point)  # Vector(x=20.0, y=38.0)
```

Convenience constructors are available:

- `Matrix2D.identity()`
- `Matrix2D.translate(x, y=0)`
- `Matrix2D.scale(x, y=None)`
- `Matrix2D.scale_at(x, y, cx, cy)`
- `Matrix2D.rotate(angle)`
- `Matrix2D.skew_x(angle)`
- `Matrix2D.skew_y(angle)`

Use `multiply()` to compose two matrices and `apply(x, y)` to transform a point.

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

Use `to_matrix()` to convert a transform to a `Matrix2D`.

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

Use `to_matrix()` to compose all transforms into a single `Matrix2D` in SVG order.

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
