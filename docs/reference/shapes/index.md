---
icon: material/shape-plus
---

# `d`-string generators

This module provides functions to generate SVG path `d`-strings for various geometric shapes. These functions return strings suitable for use in the "d" attribute of SVG path elements.

## <span class="func"></span>`star`

```py
star(
    x: float = 0,
    y: float = 0,
    n: int = 5,
    *, 
    inner_radius: float,
    outer_radius: float,
    angle: float = 0
) -> str
```

Returns a `d`-string for a star with `n` points. The star is centered at `(x, y)` and is constructed using alternating outer and inner vertices.

<span class="param">**Parameters**</span>

- `x` *(float, optional)*: x-coordinate of the center (default: 0).
- `y` *(float, optional)*: y-coordinate of the center (default: 0).
- `n` *(int, optional)*: Number of star points (default: 5).
- `inner_radius` *(float)*: Radius for the inner vertices.
- `outer_radius` *(float)*: Radius for the outer vertices.
- `angle` *(float, optional)*: Rotation angle in degrees for the first outer vertex (default: 0).

<span class="returns">**Returns**</span>

- *(str)*: A string suitable for the "d" attribute in an SVG path element.

```py
d_str = star(inner_radius=10, outer_radius=20)
print(d_str)
```

## <span class="func"></span>`polyline`

```py
polyline(
    x_coords: Sequence[float],
    y_coords: Sequence[float]
) -> str
```

Returns a `d`-string for a polyline connecting points specified by `x_coords` and `y_coords`.
Raises a `ValueError` if the lengths of `x_coords` and `y_coords` do not match.

<span class="param">**Parameters**</span>

- `x_coords` *(Sequence[float])*: A sequence of x coordinates.
- `y_coords` *(Sequence[float])*: A sequence of y coordinates.

<span class="returns">**Returns**</span>

*(str)*: A string suitable for the "d" attribute in an SVG path element.

```py
d_str = polyline([0, 50, 100], [0, 100, 0])
print(d_str)
```

## <span class="func"></span>`cardinal_spline`

```py
cardinal_spline(
    points: list[float] | list[tuple[float, float]],
    tension: float = 0.0,
    closed: bool = False,
) -> str
```

Generates an SVG path `d` string for a cardinal spline that smoothly interpolates through a set of points with adjustable tension. The spline is built from a series of cubic Bézier segments computed using the cardinal spline algorithm. A `tension` of `0.0` produces the classic smooth cardinal spline, while a `tension` of `1.0` yields straight-line segments. When `closed` is `True`, the spline wraps around so that the last point connects back to the first.

<span class="param">**Parameters**</span>

- `points` *(list[float] | list[tuple[float, float]])*: A sequence of points. This can be a flat list in the form `[x0, y0, x1, y1, …]` or a list of `(x, y)` tuples.
- `tension` *(float)*: A number between `0.0` and `1.0` that controls the curvature of the spline. Lower values yield a looser, more curved line; higher values produce a tighter, straighter line.
- `closed` *(bool)*: Whether the spline should be closed (i.e. the last point connects back to the first).

<span class="returns">**Returns**</span>

*(str)*: A string suitable for the `d` attribute of an SVG `<path>` element.

```py
d_str = cardinal_spline(
    [50, 50, 100, 100, 150, 50, 200, 100, 250, 50, 300, 100, 350, 50],
    tension=0.5,
    closed=False
)
print(d_str)
```

## <span class="func"></span>`polygon`

```py
polygon(
    x: float,
    y: float,
    radius: float,
    n: int,
    angle: float = 0,
) -> str
```

Returns a `d`-string for a regular polygon with `n` sides. The polygon is centered at `(x, y)` and is inscribed in a circle of the specified `radius`. An optional rotation `angle` (in degrees) is applied, rotating the polygon around its center. By default, the first vertex is positioned at the top of the circle (i.e. at -90°) and then rotated by the given `angle`.

<span class="param">**Parameters**</span>

- `x` *(float)*: The x-coordinate of the polygon’s center.
- `y` *(float)*: The y-coordinate of the polygon’s center.
- `radius` *(float)*: The radius of the circle in which the polygon is inscribed.
- `n` *(int)*: The number of sides (vertices) of the polygon.
- `angle` *(float)*: The rotation angle in degrees to be applied to the polygon (default is 0).

<span class="returns">**Returns**</span>

*(str)*: A string suitable for the d attribute of an SVG `<path>` element.

```py
d_str = polygon(200, 200, 100, 6)
print(d_str)
```

## <span class="func"></span>`cross`

```py
cross(
    x: float = 0,
    y: float = 0,
    *,
    size: float,
    thickness: float,
    angle: float = 0
) -> str
```

Returns a `d`-string for a cross centered at `(x, y)` with a given `size`, `thickness`, and rotation `angle`.
The cross is formed by combining a vertical rectangle and a horizontal rectangle into a polygon with 12 vertices.

<span class="param">**Parameters**</span>

- `x` *(float, optional)*: x-coordinate of the center (default: 0).
- `y` *(float, optional)*: y-coordinate of the center (default: 0).
- `size` *(float)*: Total span (tip-to-tip) of the cross.
- `thickness` *(float)*: Thickness of the cross arms.
- `angle` *(float, optional)*: Rotation angle in degrees (default: 0).

<span class="returns">**Returns**</span>

*(str)*: A string suitable for the "d" attribute in an SVG path element.

```py
d_str = cross(size=50, thickness=10, angle=45)
print(d_str)
```

## <span class="func"></span>`arc`

```py
arc(
    x: float = 0,
    y: float = 0,
    *,
    radius: float,
    start_angle: float = 0,
    end_angle: float = 360
) -> str
```

Returns a `d`-string for an arc (a circular path) centered at `(x, y)` with the specified `radius`.
The arc spans from `start_angle` to `end_angle` (in degrees). If the arc represents a full circle, it is drawn using two 180° arc segments.

<span class="param">**Parameters**</span>

- `x` *(float, optional)*: x-coordinate of the center (default: 0).
- `y` *(float, optional)*: y-coordinate of the center (default: 0).
- `radius` *(float)*: Radius of the arc.
- ``start_angle`` *(float, optional)*: Starting angle in degrees (default: 0).
- end_angle *(float, optional)*: Ending angle in degrees (default: 360).

<span class="returns">**Returns**</span>

*(str)*: A string suitable for the "d" attribute in an SVG path element.

```py
d_str = arc(radius=30, start_angle=0, end_angle=180)
print(d_str)
```

## <span class="func"></span>`ring`

```py
ring(
    x: float = 0,
    y: float = 0,
    *,
    inner_radius: float,
    outer_radius: float,
    start_angle: float = 0,
    end_angle: float = 360,
    without_inner: bool = False
) -> str
```

Returns a `d`-string for a ring (donut or ring segment) centered at `(x, y)` with specified `inner_radius` and `outer_radius`.

For a full ring (360°), a complete donut is drawn.
For a partial ring:
If `without_inner` is `False`, a full ring segment is drawn (outer arc, radial line to inner arc, inner arc, and radial line back).
If `without_inner` is `True`, the inner arc is omitted and a single closed path is drawn.

<span class="param">**Parameters**</span>

- `x` *(float, optional)*: x-coordinate of the center (default: 0).
- `y` *(float, optional)*: y-coordinate of the center (default: 0).
- `inner_radius` *(float)*: Inner radius of the ring.
- `outer_radius` *(float)*: Outer radius of the ring.
- `start_angle` *(float, optional)*: Starting angle in degrees (default: 0).
- `end_angle` *(float, optional)*: Ending angle in degrees (default: 360).
- `without_inner` *(bool, optional)*: If True, omits the inner arc for partial rings (default: False).

<span class="returns">**Returns**</span>

*(str)*: A string suitable for the "d" attribute in an SVG path element.

```py
d_str = ring(inner_radius=20, outer_radius=40, start_angle=45, end_angle=315)
print(d_str)
```
