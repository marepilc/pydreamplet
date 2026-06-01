---
title: Noise
description: Random-walk and deterministic simplex noise utilities.
navigation:
  title: Noise
category: reference
---

# Noise

The `pydreamplet.noise` module provides a bounded random-walk generator and
deterministic simplex noise in one, two, and three dimensions.

Noise classes are imported from `pydreamplet.noise`.

```python
from pydreamplet.noise import Noise, SimplexNoise, SimplexNoise2D, SimplexNoise3D
```

`NoiseBase` is the shared base class for the simplex implementations. It owns
seeded permutation generation and helper math; user code normally instantiates
`SimplexNoise`, `SimplexNoise2D`, or `SimplexNoise3D` instead.

## Visual Example

This example samples `SimplexNoise2D` over a small grid. Each noise value drives
the radius and opacity of one circle.

```python
import pydreamplet as dp
from pydreamplet.noise import SimplexNoise2D

noise = SimplexNoise2D(seed=12)
svg = dp.SVG(300, 160)

for row in range(5):
    for column in range(9):
        value = noise.noise(column * 0.28, row * 0.28, frequency=1.2)
        svg.append(
            dp.Circle(
                cx=34 + column * 28,
                cy=34 + row * 22,
                r=3 + value * 8,
                fill="#14b8a6",
                opacity=0.22 + value * 0.68,
            )
        )

svg.append(
    dp.Text("SimplexNoise2D(seed=12)", x=34, y=145, font_size=12, fill="currentColor")
)
```

::svg-preview{src="/showcase/ref_noise_simplex.svg" alt="Grid of circles sized and faded by two-dimensional simplex noise."}
::

## Noise

```python
Noise(
    min_val: float,
    max_val: float,
    noise_range: float,
    *,
    seed: int | None = None,
)
```

`Noise` produces a bounded random walk. Each read of `value` or `int_value`
advances the generator by choosing a new value inside a moving window. The
`noise_range` argument is a fraction of `max_val - min_val`; values must be in
the inclusive range `[0, 1]`.

```python
from pydreamplet.noise import Noise

walk = Noise(0.0, 100.0, 0.12, seed=4)
values = [walk.value for _ in range(6)]
```

The bounds and current value are mutable:

```python
walk.min = 20.0
walk.max = 80.0
walk.value = 50.0

print(walk.noise_range)
print(walk.int_value)
```

Setting `value` outside the current `[min, max]` range is ignored. Changing
`min` or `max` clamps the current value only when it falls outside the new
bound. Invalid bounds and invalid `noise_range` values raise `ValueError`.

## SimplexNoise

```python
SimplexNoise(seed: int | None = None)
```

`SimplexNoise` samples one-dimensional simplex noise.

```python
noise = SimplexNoise(seed=42)
value = noise.noise(0.5, frequency=2.0, amplitude=1.5)
```

```python
noise(x: float, frequency: float = 1, amplitude: float = 1) -> float
```

The returned value is mapped into `[0, amplitude]`.

## SimplexNoise2D

```python
SimplexNoise2D(seed: int | None = None)
```

`SimplexNoise2D` samples two-dimensional simplex noise and is useful for grids,
fields, and procedural textures.

```python
noise = SimplexNoise2D(seed=42)
value = noise.noise(0.25, 0.75, frequency=1.8)
```

```python
noise(x: float, y: float, frequency: float = 1, amplitude: float = 1) -> float
```

The same seed and coordinates produce the same value.

## SimplexNoise3D

```python
SimplexNoise3D(seed: int | None = None)
```

`SimplexNoise3D` samples three-dimensional simplex noise. The third coordinate
can represent depth, time, or another generated axis.

```python
noise = SimplexNoise3D(seed=42)
frame_value = noise.noise(0.25, 0.75, 0.1, frequency=1.8)
```

```python
noise(
    x: float,
    y: float,
    z: float,
    frequency: float = 1,
    amplitude: float = 1,
) -> float
```

The returned value is mapped into `[0, amplitude]`.
