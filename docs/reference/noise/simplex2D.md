# `SimplexNoise2D`

The SimplexNoise2D class is a two-dimensional noise generator based on the simplex noise algorithm. It produces smooth, continuous noise values that are roughly in the range [-1, 1] when the amplitude is 1. These values are then mapped to the [0, 1] interval and scaled by the provided amplitude. This class is useful for generating terrain, textures, or other procedural content in two dimensions.

## <span class=class></span>`dreamplet.noise.SimplexNoise2D`

```py
SimplexNoise2D(seed: int = None)
```

<span class="param">**Parameters**</span>

- `seed` *(int, optional)*: An optional seed for noise generation. When provided, the noise sequence will be reproducible.

```py
simplex2d = SimplexNoise2D(seed=123)
value = simplex2d.noise(10.5, 20.75, frequency=0.05, amplitude=1.0)
print(value)  # Outputs a noise value scaled to [0, 1]
```

### <span class="meth"></span>`noise`

```py
noise(
    self,
    x: float,
    y: float,
    frequency: float = 1,
    amplitude: float = 1,
) -> float
```

Generates a noise value for the specified 2D coordinates.

<span class="param">**Parameters**</span>

- `x` *(float)*: The x-coordinate input.
- `y` *(float)*: The y-coordinate input.
- `frequency` *(float, optional)*: Scales the input coordinates to control the level of detail. Default is 1.
- `amplitude` *(float, optional)*: Scales the resulting noise value. Default is 1.

<span class="returns">**Returns**</span>

- *(float)*: The noise value, mapped from a raw value in approximately [-1, 1] to a [0, 1] range, and then scaled by the amplitude.

**How it works**

1. **Input Scaling:** The coordinates (xin, yin) are multiplied by the frequency.
2. **Skewing and Unskewing:** The algorithm applies a skewing factor (using F2) to transform the input space into simplex space, then computes the unskewed distances.
3. **Corner Contributions:** It determines the simplex triangle for the input point and calculates contributions from each corner using an attenuation function.
4. **Noise Aggregation:** The contributions from the three corners are summed, scaled, and remapped from [-1, 1] to [0, 1] by the amplitude.

```py
noise_value = simplex2d.noise(5.0, 15.0, frequency=0.1, amplitude=0.8)
```