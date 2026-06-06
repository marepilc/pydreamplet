---
title: Creative Helpers
description: Reference for point and tile helpers exported from pydreamplet.
navigation:
  title: Creative helpers
category: reference
---

# Creative Helpers

Creative helpers generate `Vector` points and `Tile` footprints for generative
layouts. These names are exported from top-level `pydreamplet`.

```python
import pydreamplet as dp
```

## Visual Example

```python
import pydreamplet as dp

svg = dp.SVG(360, 180)

for point in dp.phyllotaxis_points(90, spacing=6, center=(95, 90)):
    svg.append(dp.Circle(cx=point.x, cy=point.y, r=2.8, fill="currentColor"))

for tile in dp.hex_tiles(5, 3, 14, origin=(220, 42), gap=4):
    points = []
    for corner in tile.corners:
        points.extend(corner.xy)
    svg.append(dp.Polygon(points, fill="none", stroke="currentColor", stroke_width=2, opacity=0.65))
```

::svg-preview{src="/showcase/ref_creative_helpers.svg" alt="Phyllotaxis points next to a hex tile grid."}
::

## Tile

```python
@dataclass(frozen=True)
class Tile:
    index: int
    row: int
    column: int
    center: Vector
    corners: tuple[Vector, ...]
```

`square_tiles()` and `hex_tiles()` return immutable `Tile` records.

## Point Helpers

| Helper | Signature | Returns |
| --- | --- | --- |
| `grid_points` | `(columns, rows, width, height, *, origin=(0, 0), padding=0, jitter=0, seed=None)` | `list[Vector]` |
| `random_points` | `(count, width, height, *, origin=(0, 0), padding=0, seed=None)` | `list[Vector]` |
| `circle_points` | `(count, radius, *, center=(0, 0), start_angle=0, end_angle=360, include_endpoint=False, radius_jitter=0, seed=None)` | `list[Vector]` |
| `wave_points` | `(count, width, *, amplitude, frequency=1, phase=0, origin=(0, 0))` | `list[Vector]` |
| `spiral_points` | `(count, *, start_radius=0, end_radius, turns=1, center=(0, 0), start_angle=0)` | `list[Vector]` |
| `lissajous_points` | `(count, *, x_radius, y_radius, a=3, b=2, delta=90, center=(0, 0), include_endpoint=False)` | `list[Vector]` |
| `phyllotaxis_points` | `(count, *, spacing=1, angle=137.50776405, center=(0, 0), start_index=0)` | `list[Vector]` |
| `noise_points` | `(columns, rows, width, height, *, seed=None, frequency=1, amplitude=1, origin=(0, 0), padding=0)` | `list[tuple[Vector, float]]` |

`padding`, `jitter`, `origin`, and similar pair values accept either one number
or a two-number pair where the signature allows `Real | NumericPair`.

```python
points = dp.grid_points(3, 2, 20, 10)

assert [point.xy for point in points] == [
    (0.0, 0.0),
    (10.0, 0.0),
    (20.0, 0.0),
    (0.0, 10.0),
    (10.0, 10.0),
    (20.0, 10.0),
]
```

## Tile Helpers

| Helper | Signature | Returns |
| --- | --- | --- |
| `square_tiles` | `(columns, rows, width, height, *, origin=(0, 0), padding=0, gap=0)` | `list[Tile]` |
| `hex_tiles` | `(columns, rows, radius, *, origin=(0, 0), gap=0, orientation="pointy")` | `list[Tile]` |

`hex_tiles()` supports `orientation="pointy"` and `orientation="flat"`.

```python
tiles = dp.square_tiles(2, 2, 22, 12, gap=(2, 4))

assert tiles[0].center.xy == (5.0, 2.0)
assert [point.xy for point in tiles[0].corners] == [
    (0.0, 0.0),
    (10.0, 0.0),
    (10.0, 4.0),
    (0.0, 4.0),
]
```

## Validation

Count arguments must be positive. Radius and spacing values that define physical
sizes must be non-negative, except `hex_tiles()` radius, which must be positive.
Seeded helpers use deterministic local random generators.
