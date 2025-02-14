# `SimplexNoise3D`

The SimplexNoise3D class extends the simplex noise algorithm into three dimensions. It generates smooth noise values that are roughly in the range [-1, 1] when the amplitude is 1. These values are then mapped to the [0, 1] interval and scaled by the amplitude. This 3D noise is useful for volumetric effects, 3D procedural textures, or other applications requiring noise in three-dimensional space.

## <span class=class></span>`dreamplet.noise.SimplexNoise3D`

```py
SimplexNoise3D(seed: int = None)
```

<span class="param">**Parameters**</span>

- `seed` *(int, optional)*: An optional seed for noise generation. When provided, the noise sequence will be reproducible.

```py
simplex3d = SimplexNoise3D(seed=456)
value = simplex3d.noise(2.0, 3.5, 7.8, frequency=0.2, amplitude=1.0)
print(value)  # Outputs a noise value scaled to [0, 1]
```

### <span class="meth"></span>`noise`

```py
noise(
    self, x:
    float, y:
    float, z: float,
    frequency: float = 1,
    amplitude: float = 1
) -> float
```

Generates a noise value for the specified 3D coordinates.

<span class="param">**Parameters**</span>

- `x` *(float)*: The x-coordinate input.
- `y` *(float)*: The y-coordinate input.
- `z` *(float)*: The z-coordinate input.
- `frequency` *(float, optional)*: Scales the input coordinates to control the level of detail. Default is 1.
- `amplitude` *(float, optional)*: Scales the resulting noise value. Default is 1.

<span class="returns">**Returns**</span>

- *(float)*: The noise value, remapped from an approximate raw range of [-1, 1] to [0, 1] and then scaled by the amplitude.

**How it works**

1. **Input Scaling:** The (x, y, z) coordinates are scaled by the frequency.
2. **Skewing the Input Space:** The coordinates are skewed using a factor (derived from F3) to determine the simplex cell.
3. Simplex Cell Determination: The algorithm identifies the simplex cell (a tetrahedron in 3D) that contains the input point.
4. **Corner Contributions:** It calculates contributions from the four corners of the tetrahedron, applying an attenuation function based on the distance from the input point.
5. **Noise Aggregation:** The contributions are summed, scaled by a factor (32.0), and remapped from the raw noise range to the final [0, 1] range after applying the amplitude.
