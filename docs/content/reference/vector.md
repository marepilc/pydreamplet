---
title: Vector
description: Reference for the 2D Vector type exported from pydreamplet.
navigation:
  title: Vector
category: reference
---

# Vector

`Vector` is pyDreamplet's small 2D coordinate type. It is used by geometry
helpers, bounding boxes, positions, and creative layout functions.

`Vector` is exported from top-level `pydreamplet`.

```python
import pydreamplet as dp
```

## Visual Example

```python
import pydreamplet as dp

origin = dp.Vector(56, 124)
direction = dp.Vector(108, -72)
tip = origin + direction
unit = direction.normalize()
normal = dp.Vector(-unit.y, unit.x)
arrow_base = tip - unit * 12

svg = dp.SVG(260, 170)
svg.append(
    dp.Line(origin.x, origin.y, tip.x, origin.y, stroke="#64748b", stroke_width=1, stroke_dasharray="4 5", opacity=0.75),
    dp.Line(origin.x, origin.y, tip.x, tip.y, stroke="#14b8a6", stroke_width=3, stroke_linecap="round"),
    dp.Path(
        dp.linear_path(
            [tip.xy, (arrow_base + normal * 5).xy, (arrow_base - normal * 5).xy],
            closed=True,
        ),
        fill="#14b8a6",
    ),
    dp.Circle(cx=origin.x, cy=origin.y, r=4, fill="#14b8a6"),
    dp.Circle(cx=tip.x, cy=tip.y, r=4, fill="#14b8a6"),
    dp.Text("origin", x=28, y=143, font_size=12, fill="currentColor"),
    dp.Text("tip", x=172, y=48, font_size=12, fill="currentColor"),
    dp.Text(f"length {direction.magnitude:.1f}", x=154, y=106, font_size=12, fill="currentColor"),
    dp.Text(f"unit {unit.x:.2f}, {unit.y:.2f}", x=154, y=124, font_size=12, fill="currentColor"),
)
```

::svg-preview{src="/showcase/ref_vector.svg" alt="A vector from an origin point to a tip with length and normalized direction labels."}
::

## Constructor

```python
Vector(x: Real, y: Real)
```

Coordinates are stored as floats.

```python
v = dp.Vector(3, 4)

assert v.x == 3
assert v.y == 4
assert v.xy == (3, 4)
```

## Polar Coordinates

```python
Vector.from_polar(angle: Real, radius: Real = 1) -> Vector
```

Creates a vector from an angle in degrees and an optional radius. Angles follow
the SVG coordinate system: `0` points right, `90` points down, `180` points
left, and `270` points up.

```python
right = dp.Vector.from_polar(0, 10)
down = dp.Vector.from_polar(90, 10)
unit = dp.Vector.from_polar(45)

assert right == dp.Vector(10, 0)
assert round(down.x, 6) == 0
assert round(down.y, 6) == 10
assert round(unit.magnitude, 6) == 1
```

## Properties

| Property | Type | Notes |
| --- | --- | --- |
| `x` | `float` | Get or set the x coordinate. |
| `y` | `float` | Get or set the y coordinate. |
| `xy` | `tuple[float, float]` | Read-only tuple of `(x, y)`. |
| `direction` | `float` | Angle in degrees from `atan2(y, x)`. Setting it preserves magnitude. |
| `magnitude` | `float` | Vector length. Setting it preserves direction. |

```python
v = dp.Vector(3, 4)

assert v.magnitude == 5

v.direction = 0
assert round(v.x, 6) == 5
assert round(v.y, 6) == 0
```

## Methods

```python
set(x: Real, y: Real) -> None
copy() -> Vector
dot(other: Vector) -> float
normalize() -> Vector
limit(limit_scalar: Real) -> None
```

`normalize()` returns a new vector and does not modify the original. It raises
`ValueError` for a zero vector.

`limit()` mutates the vector only when its current magnitude is larger than the
limit.

```python
v = dp.Vector(3, 4)
unit = v.normalize()

assert round(unit.magnitude, 6) == 1
assert v == dp.Vector(3, 4)

v.limit(3)
assert round(v.magnitude, 6) == 3
```

## Operators

Vector addition and subtraction require another `Vector`. Scalar multiplication
and division accept real numbers.

```python
assert dp.Vector(3, 4) + dp.Vector(1, 2) == dp.Vector(4, 6)
assert dp.Vector(3, 4) - dp.Vector(1, 2) == dp.Vector(2, 2)
assert dp.Vector(3, 4) * 2 == dp.Vector(6, 8)
assert 3 * dp.Vector(3, 4) == dp.Vector(9, 12)
assert dp.Vector(3, 4) / 2 == dp.Vector(1.5, 2)
```

In-place variants mutate the original vector:

```python
v = dp.Vector(3, 4)
v += dp.Vector(1, 1)
v *= 2

assert v == dp.Vector(8, 10)
```

Unsupported vector addition and subtraction raise `TypeError`.
