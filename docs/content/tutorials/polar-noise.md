---
title: Polar Noise
description: Build layered animated SVG waves from polar vectors, simplex noise, generated colors, filters, and path morphing.
navigation:
  title: Polar noise
category: tutorials
---

# Polar Noise

This tutorial builds a stack of animated organic shapes from points sampled
around a circle. Each point starts as a polar vector, then two-dimensional
simplex noise changes its radius. Several versions of every path are generated
and animated to create a continuous wave motion.

The final SVG has no background, so the same file can be displayed on both
light and dark pages.

## Imports and Canvas

`Vector.from_polar()` converts an angle in degrees into a unit vector.
`SimplexNoise2D` supplies repeatable radius offsets.

```python
import pydreamplet as dp
from pydreamplet.noise import SimplexNoise2D

theme = dp.Theme()
noise = SimplexNoise2D(seed=42)
svg = dp.SVG(1024, 1024)
```

Using a fixed seed keeps the generated artwork stable between runs. Changing
the seed creates a different family of contours while preserving the rest of
the composition.

## Add a Drop Shadow

SVG filters belong in a `<defs>` element. Here `feDropShadow` separates the
overlapping shapes without adding a background color.

```python
defs = svg.ensure_defs()
shadow = dp.Filter(
    id="drop-shadow",
    x="-20%",
    y="-20%",
    width="140%",
    height="140%",
)
shadow.append(
    dp.SvgElement(
        "feDropShadow",
        dx=0,
        dy=10,
        stdDeviation=8,
        flood_color="#000000",
        flood_opacity=0.65,
    )
)
defs.append(shadow)
```

The expanded filter bounds prevent the blurred shadow from being clipped near
the edge of a path.

## Center the Drawing

All generated coordinates are relative to `(0, 0)`. Translating one group to
the center keeps the point-generation code independent from the canvas size.

```python
margin = 64
group = dp.G(pos=(svg.w / 2, svg.h / 2))
svg.append(group)

shape_count = 8
min_radius = 20
max_radius = svg.w / 2 - margin
radius_step = (max_radius - min_radius) / (shape_count - 1)
palette = dp.generate_colors("#db45f9", n=shape_count)
```

The first shape uses the largest radius. Each following shape moves inward by
`radius_step`, producing nested layers.

## Generate One Noisy Contour

For every angle, create two unit vectors. `direction` determines the position
of the point. `noise_direction` determines where the noise field is sampled.

```python
line = dp.LineGenerator(curve="linear")
offset = dp.Vector(1, 1)

base_radius = max_radius
phase = 0
points: list[tuple[float, float]] = []

angle = 0.0
while angle < 360:
    direction = dp.Vector.from_polar(angle)
    noise_direction = dp.Vector.from_polar(angle + phase)
    radius = base_radius + noise.noise(
        noise_direction.x,
        noise_direction.y,
        frequency=1.5,
        amplitude=50,
    )
    points.append((direction * radius + offset).xy)
    angle += 5

path_data = f"{line(points)} Z"
```

Sampling noise along a unit circle makes the beginning and end of the contour
meet naturally. The small `offset` avoids sampling the exact same symmetric
coordinates around the noise origin.

An angle step of `5` provides enough detail for this composition while keeping
the animated SVG compact. Appending `Z` closes the contour, connecting the last
sampled point back to the first so the fill has a clean boundary.

## Build Animation Frames

SVG path morphing requires every value to contain a compatible sequence of
path commands. Each phase therefore uses the same angle loop and the same
number of points.

```python
wave_phases = (0, 90, 180, 270, 360)
wave_paths: list[str] = []

for phase in wave_phases:
    points = []
    angle = 0.0
    while angle < 360:
        direction = dp.Vector.from_polar(angle)
        noise_direction = dp.Vector.from_polar(angle + phase)
        radius = base_radius + noise.noise(
            noise_direction.x,
            noise_direction.y,
            frequency=1.5,
            amplitude=50,
        )
        points.append((direction * radius + offset).xy)
        angle += 5

    wave_paths.append(f"{line(points)} Z")
```

The final phase is `360`, which returns to the orientation used by phase `0`.
That gives the animation matching start and end states for a seamless loop.

## Layer and Animate the Shapes

Create one path for each palette color. The path starts with the first frame,
and an SVG `<animate>` element cycles its `d` attribute through all generated
frames.

```python
wave_duration = "7s"

for shape_index, color in enumerate(palette):
    base_radius = max_radius - shape_index * radius_step
    wave_paths = []

    for phase in wave_phases:
        points = []
        angle = 0.0
        while angle < 360:
            direction = dp.Vector.from_polar(angle)
            noise_direction = dp.Vector.from_polar(angle + phase)
            radius = base_radius + noise.noise(
                noise_direction.x,
                noise_direction.y,
                frequency=1.5,
                amplitude=50,
            )
            points.append((direction * radius + offset).xy)
            angle += 5

        wave_paths.append(f"{line(points)} Z")

    path = dp.Path(
        wave_paths[0],
        opacity=0.75,
        stroke=theme.ink,
        fill=color,
        filter="url(#drop-shadow)",
    )
    path.append(dp.Animate("d", values=wave_paths, dur=wave_duration))
    group.append(path)
```

The outer path is appended first and the smaller paths are appended afterward,
so every inner layer remains visible above the previous one.

## Complete Script

```python
import pydreamplet as dp
from pydreamplet.noise import SimplexNoise2D

theme = dp.Theme()
noise = SimplexNoise2D(seed=42)
svg = dp.SVG(1024, 1024)

defs = svg.ensure_defs()
shadow = dp.Filter(
    id="drop-shadow",
    x="-20%",
    y="-20%",
    width="140%",
    height="140%",
)
shadow.append(
    dp.SvgElement(
        "feDropShadow",
        dx=0,
        dy=10,
        stdDeviation=8,
        flood_color="#000000",
        flood_opacity=0.65,
    )
)
defs.append(shadow)

margin = 64
group = dp.G(pos=(svg.w / 2, svg.h / 2))
svg.append(group)

shape_count = 8
line = dp.LineGenerator(curve="linear")
offset = dp.Vector(1, 1)
palette = dp.generate_colors("#db45f9", n=shape_count)
min_radius = 20
max_radius = svg.w / 2 - margin
radius_step = (max_radius - min_radius) / (shape_count - 1)
wave_phases = (0, 90, 180, 270, 360)
wave_duration = "7s"

for shape_index, color in enumerate(palette):
    base_radius = max_radius - shape_index * radius_step
    wave_paths: list[str] = []

    for phase in wave_phases:
        points: list[tuple[float, float]] = []
        angle = 0.0
        while angle < 360:
            direction = dp.Vector.from_polar(angle)
            noise_direction = dp.Vector.from_polar(angle + phase)
            radius = base_radius + noise.noise(
                noise_direction.x,
                noise_direction.y,
                frequency=1.5,
                amplitude=50,
            )
            points.append((direction * radius + offset).xy)
            angle += 5

        wave_paths.append(f"{line(points)} Z")

    path = dp.Path(
        wave_paths[0],
        opacity=0.75,
        stroke=theme.ink,
        fill=color,
        filter="url(#drop-shadow)",
    )
    path.append(dp.Animate("d", values=wave_paths, dur=wave_duration))
    group.append(path)

svg.save("polar_noise.svg")
```

::svg-preview{src="/showcase/polar_noise.svg" alt="Layered animated polar contours shaped by two-dimensional simplex noise."}
::
