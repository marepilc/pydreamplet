---
title: Shape Helpers
description: Reference for path d-string helpers exported from pydreamplet.
navigation:
  title: Shape helpers
category: reference
---

# Shape Helpers

Shape helpers return SVG path `d` strings. Use them with [`Path`](/reference/paths)
or with data-driven generators.

These helpers are exported from top-level `pydreamplet`.

```python
import pydreamplet as dp
```

## Visual Example

```python
import pydreamplet as dp

svg = dp.SVG(420, 190)

svg.append(
    dp.Path(dp.star(58, 58, n=5, inner_radius=18, outer_radius=40, angle=-90), fill="#f83898"),
    dp.Path(dp.superellipse(155, 58, rx=48, ry=34, exponent=4, n=48), fill="#14b8a6"),
    dp.Path(dp.rounded_polygon([(245, 22), (320, 36), (306, 106), (232, 100)], radius=14), fill="#38bdf8"),
    dp.Path(dp.blob(372, 64, radius=38, variance=0.22, n=10, seed=5), fill="#95cf20"),
    dp.Path(dp.ring(96, 142, inner_radius=20, outer_radius=42, start_angle=-35, end_angle=250), fill="#f59e0b"),
    dp.Path(dp.cross(210, 142, size=74, thickness=22, angle=35), fill="#64748b"),
)
```

<img src="/showcase/ref_shape_helpers.svg" alt="Star, superellipse, rounded polygon, blob, ring, and cross paths." class="my-6 w-full rounded-md border border-neutral-200 bg-white dark:border-neutral-800" />

## Point Input

Curve and polygon helpers that accept `points` use `PointInput`:

```python
type PointInput = Sequence[float] | Sequence[Sequence[float]]
```

Both forms are valid:

```python
dp.linear_path([0, 0, 10, 20, 30, 0])
dp.linear_path([(0, 0), (10, 20), (30, 0)])
```

Flat point lists must contain an even number of values. Point-pair items must
contain exactly two coordinates.

## Basic Shapes

```python
star(
    x: float = 0,
    y: float = 0,
    n: int = 5,
    *,
    inner_radius: float,
    outer_radius: float,
    angle: float = 0,
) -> str
```

Creates an alternating inner/outer star. `n` must be at least `2`.
`inner_radius` must be non-negative and `outer_radius` must be positive.

```python
polygon(x: float, y: float, radius: float, n: int, angle: float = 0) -> str
```

Creates a regular polygon centered at `(x, y)`. `n` must be at least `3`.
`radius` must be non-negative.

```python
cross(
    x: float = 0,
    y: float = 0,
    *,
    size: float,
    thickness: float,
    angle: float = 0,
) -> str
```

Creates a 12-point cross. `size` and `thickness` must be positive.
`thickness` must be less than or equal to `size`.

```python
superellipse(
    x: float = 0,
    y: float = 0,
    *,
    rx: float,
    ry: float,
    exponent: float = 4,
    n: int = 64,
    angle: float = 0,
) -> str
```

Creates a closed superellipse. `exponent=2` is ellipse-like. Larger values
create squarer sides. `rx`, `ry`, and `exponent` must be positive. `n` must be
at least `4`.

## Organic and Rounded Shapes

```python
rounded_polygon(points: PointInput, *, radius: float) -> str
```

Creates a closed polygon with quadratic rounded corners. It requires at least
three points. `radius=0` falls back to `linear_path(points, closed=True)`.

```python
blob(
    x: float = 0,
    y: float = 0,
    *,
    radius: float,
    variance: float = 0.25,
    n: int = 12,
    seed: int = 0,
    smooth: bool = True,
) -> str
```

Creates a deterministic organic closed shape. `smooth=True` uses a closed
Catmull-Rom path. `smooth=False` uses straight segments.

## Line and Curve Paths

```python
polyline(x_coords: Sequence[float], y_coords: Sequence[float]) -> str
```

Creates an open line path from separate x and y sequences. Both sequences must
have the same non-zero length.

```python
linear_path(points: PointInput, closed: bool = False) -> str
```

Creates straight line segments. Empty input returns an empty string.

```python
step_path(
    points: PointInput,
    closed: bool = False,
    mode: Literal["before", "after", "mid"] = "mid",
) -> str
```

Creates stepped segments. `mode="before"` changes y before x, `mode="after"`
changes x before y, and `mode="mid"` changes y at the midpoint between adjacent
x values.

```python
cardinal_spline(points: PointInput, tension: float = 0.0, closed: bool = False) -> str
catmull_rom_path(points: PointInput, closed: bool = False) -> str
basis_spline(points: PointInput, closed: bool = False) -> str
monotone_x_path(points: PointInput) -> str
monotone_y_path(points: PointInput) -> str
```

Spline helpers return cubic Bezier path data. Closed Catmull-Rom, basis, and
cardinal paths require at least three points. `cardinal_spline()` requires
`0 <= tension <= 1`.

`monotone_x_path()` requires strictly monotonic x coordinates.
`monotone_y_path()` requires strictly monotonic y coordinates.

## Arcs and Rings

```python
arc(
    x: float = 0,
    y: float = 0,
    *,
    radius: float,
    start_angle: float = 0,
    end_angle: float = 360,
) -> str
```

Creates a circular arc. A zero span returns a move-only path. A full circle is
drawn as two 180-degree arc commands. `radius` must be positive.

```python
ring(
    x: float = 0,
    y: float = 0,
    *,
    inner_radius: float,
    outer_radius: float,
    start_angle: float = 0,
    end_angle: float = 360,
    without_inner: bool = False,
) -> str
```

Creates a donut or ring segment. A zero span returns an empty string.
`inner_radius` must be non-negative, `outer_radius` must be positive, and
`inner_radius <= outer_radius`.

For partial rings, `without_inner=True` omits the inner arc and closes the shape
with a chord.

## Example Output

```python
import pydreamplet as dp

assert dp.linear_path([(0, 0), (10, 20), (30, 0)]) == (
    "M 0.00,0.00 L 10.00,20.00 L 30.00,0.00"
)

assert dp.ring(inner_radius=5, outer_radius=10, start_angle=30, end_angle=30) == ""
```
