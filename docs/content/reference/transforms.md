---
title: Transforms
description: Group transforms, transform parsing, and affine matrices.
navigation:
  title: Transforms
category: reference
---

# Transforms

pyDreamplet exposes two layers for SVG transforms:

- `G` gives drawing code a convenient `pos`, `angle`, `scale`, `pivot`, and
  `order` API.
- `Transform`, `TransformList`, and `Matrix2D` model SVG transform functions and
  affine matrices directly.

Use `G` for normal drawing composition. Use the lower-level classes when you
need to parse, inspect, compose, or apply transforms numerically.

## Import

```python
import pydreamplet as dp
```

## Type Names

| Type | Meaning |
| --- | --- |
| `Real` | `int \| float` |
| `PointLike` | `Vector \| tuple[Real, Real] \| list[Real]` |

## Groups

```python
dp.G(
    pos: PointLike | None = None,
    scale: dp.Vector | None = None,
    angle: float = 0,
    pivot: PointLike | None = None,
    order: str = "trs",
    **kwargs,
)
```

`G` creates an SVG `<g>` element and can transform all of its children together.
The constructor also accepts normal SVG attributes through `**kwargs`.

```python
svg = dp.SVG(360, 180)
svg.append(dp.Rect(x=0, y=0, width=360, height=180, fill="#f8fafc"))

group = dp.G(pos=(180, 90), angle=25, scale=dp.Vector(1.25, 1.25))
group.append(dp.Rect(x=-45, y=-28, width=90, height=56, rx=8, fill="#14b8a6", opacity=0.82))
group.append(dp.Line(-70, 0, 70, 0, stroke="#1b313b", stroke_width=2, opacity=0.45))
group.append(dp.Text("G", x=0, y=6, fill="#111827", font_size=28, font_weight=800, text_anchor="middle"))

svg.append(group)

print(group.transform)
# translate(180 90) rotate(25) scale(1.25 1.25)
```

<img src="/showcase/ref_transforms_group.svg" alt="SVG group translated, rotated, and scaled" class="mt-6 w-full rounded-lg border border-neutral-200 bg-white p-4 dark:border-neutral-800" />

### Group Properties

| Property | Type | Description |
| --- | --- | --- |
| `pos` | `Vector` | Translation. Set with a `Vector`, tuple, or list. |
| `angle` | `float` | Rotation angle in degrees. |
| `scale` | `Vector` | Scale factors for x and y. Set with a `Vector`. |
| `pivot` | `Vector` | Pivot used by rotation and scale. Set with a `Vector`, tuple, or list. |
| `order` | `str` | Transform order. Default is `"trs"`. |

`order` is read one character at a time:

| Character | Operation |
| --- | --- |
| `t` | translate |
| `r` | rotate |
| `s` | scale |

```python
group = dp.G(pos=(20, 20), angle=45, scale=dp.Vector(2, 2))
print(group.transform)
# translate(20 20) rotate(45) scale(2 2)

group.order = "rts"
print(group.transform)
# rotate(45) translate(20 20) scale(2 2)
```

The implementation does not validate that `order` contains only `t`, `r`, and
`s`. Unknown characters are ignored because they do not map to a transform.

### Pivot

`pivot` applies to rotation and scale.

```python
group = dp.G(pivot=(10, 20), angle=30, scale=dp.Vector(2, 3))

print(group.transform)
# rotate(30,10,20) translate(10 20) scale(2 3) translate(-10 -20)
```

For scale, the pivot is emitted as translate-scale-translate. That means a
pivoted scale contributes three transform functions to the final `transform`
attribute.

### Parsing Existing Transforms

Setting `transform` through `attrs()` parses supported SVG transform functions
and updates the convenience properties.

```python
group = dp.G()
group.attrs({"transform": "translate(10, 12) scale(2)"})

print(group.pos)    # Vector(x=10.0, y=12.0)
print(group.scale)  # Vector(x=2.0, y=2.0)
```

Malformed numeric values raise `ValueError`.

```python
try:
    dp.G().attrs({"transform": "translate(foo 12)"})
except ValueError:
    print("invalid transform")
```

Extra supported transform functions, such as `skewX()` and `matrix()`, are
preserved when the group is updated.

```python
group = dp.G()
group.attrs({"transform": "translate(10 12) skewX(20) rotate(30)"})

group.pos = dp.Vector(20, 24)

print(group.transform)
# translate(20 24) skewX(20) rotate(30)
```

## Transform

```python
dp.Transform(name: str, *values: Real)
```

`Transform` represents one SVG transform function. It validates the supported
function names and argument counts.

| Factory | Output |
| --- | --- |
| `Transform.translate(x, y=0)` | `translate(x y)` |
| `Transform.scale(x, y=None)` | `scale(x y)`; when `y` is `None`, `y` equals `x` |
| `Transform.rotate(angle, cx=None, cy=None)` | `rotate(angle)` or `rotate(angle,cx,cy)` |
| `Transform.skew_x(angle)` | `skewX(angle)` |
| `Transform.skew_y(angle)` | `skewY(angle)` |
| `Transform.matrix(a, b, c, d, e, f)` | `matrix(a b c d e f)` |

```python
transforms = [
    dp.Transform.translate(10, 20),
    dp.Transform.rotate(45, 5, 6),
    dp.Transform.scale(2, 3),
    dp.Transform.skew_x(15),
    dp.Transform.matrix(1, 0, 0, 1, 10, 20),
]

print([str(transform) for transform in transforms])
# ['translate(10 20)', 'rotate(45,5,6)', 'scale(2 3)', 'skewX(15)', 'matrix(1 0 0 1 10 20)']
```

`rotate()` requires either no pivot values or both pivot values.

```python
try:
    dp.Transform.rotate(45, 10)
except ValueError:
    print("rotate pivot requires both cx and cy")
```

### `to_matrix`

```python
transform.to_matrix() -> dp.Matrix2D
```

Converts a single transform function to an affine matrix.

```python
matrix = dp.Transform.rotate(90, 10, 20).to_matrix()

print(matrix.as_tuple())
# (0.0, 1.0, -1.0, 0.0, 30.0, 10.0)
```

## TransformList

```python
dp.TransformList(transforms: list[dp.Transform] | None = None)
```

`TransformList` stores transform functions in order.

### `parse`

```python
dp.TransformList.parse(value: str) -> dp.TransformList
```

Parses a transform attribute string. Commas and spaces are both accepted between
numbers.

```python
transform_list = dp.TransformList.parse(
    "translate(10, 20) skewX(15) rotate(45, 5, 6) scale(2)"
)

print([transform.name for transform in transform_list.transforms])
# ['translate', 'skewX', 'rotate', 'scale']

print(str(transform_list))
# translate(10 20) skewX(15) rotate(45,5,6) scale(2)
```

Unsupported function names raise `ValueError`.

```python
try:
    dp.TransformList.parse("perspective(1)")
except ValueError:
    print("unsupported transform")
```

### Methods

```python
transform_list.append(transform: dp.Transform) -> dp.TransformList
transform_list.first(name: str) -> dp.Transform | None
transform_list.replace_first(name: str, transform: dp.Transform | None) -> None
transform_list.to_matrix() -> dp.Matrix2D
```

`append()` mutates the list and returns the same `TransformList`.

`first()` returns the first transform with the requested function name.

`replace_first()` replaces the first matching transform. Passing `None` removes
the first matching transform. If there is no existing transform and the new
transform is not `None`, it is appended.

`to_matrix()` composes the transforms in list order.

```python
transform_list = dp.TransformList.parse("translate(10 20) rotate(90) scale(2)")
matrix = transform_list.to_matrix()

print(matrix.apply(1, 0))
# Vector(x=10.0, y=22.0)
```

## Matrix2D

```python
dp.Matrix2D(
    a: Real = 1,
    b: Real = 0,
    c: Real = 0,
    d: Real = 1,
    e: Real = 0,
    f: Real = 0,
)
```

`Matrix2D` stores the six values used by SVG's `matrix(a b c d e f)` transform.
Values are stored as floats.

| Factory | Description |
| --- | --- |
| `Matrix2D.identity()` | Identity matrix. |
| `Matrix2D.translate(x, y=0)` | Translation matrix. |
| `Matrix2D.scale(x, y=None)` | Scale matrix. |
| `Matrix2D.scale_at(x, y, cx, cy)` | Scale around a pivot. |
| `Matrix2D.rotate(angle)` | Rotation matrix in degrees. |
| `Matrix2D.skew_x(angle)` | Skew-X matrix in degrees. |
| `Matrix2D.skew_y(angle)` | Skew-Y matrix in degrees. |

```python
matrix = dp.Matrix2D.translate(10, 20).multiply(dp.Matrix2D.scale(2, 3))

print(matrix.as_tuple())
# (2.0, 0.0, 0.0, 3.0, 10.0, 20.0)

print(matrix.apply(5, 6))
# Vector(x=20.0, y=38.0)

print(str(matrix))
# matrix(2 0 0 3 10 20)
```

### Methods

```python
matrix.multiply(other: dp.Matrix2D) -> dp.Matrix2D
matrix.apply(x: Real, y: Real) -> dp.Vector
matrix.as_tuple() -> tuple[float, float, float, float, float, float]
```

`multiply()` returns a new matrix and leaves both inputs unchanged.

`apply()` transforms one point and returns a `Vector`.

`as_tuple()` returns `(a, b, c, d, e, f)`.

```python
matrix = dp.Matrix2D.scale_at(2, 3, 10, 20)

print(matrix.as_tuple())
# (2.0, 0.0, 0.0, 3.0, -10.0, -40.0)

print(matrix.apply(10, 20))
# Vector(x=10.0, y=20.0)
```
