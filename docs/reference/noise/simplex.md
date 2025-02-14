# `SimplexNoise`

The SimplexNoise class is a one-dimensional noise generator that builds on the functionality provided by the NoiseBase class. It implements the simplex noise algorithm to produce smooth noise values that are roughly in the range [-1, 1] when the amplitude is set to 1. These values are then mapped to the [0, 1] range and scaled by the provided amplitude.

### <span class=class></span>`dreamplet.noise.SimplexNoise`

```py
SimplexNoise(seed: int = None)
```

<span class="param">**Parameters**</span>

- `seed` *(int, optional)*: An optional seed for noise generation. Providing a seed ensures that the noise sequence is reproducible.

```py
simplex = SimplexNoise(seed=42)
print(simplex.noise(0.5))
```

### <span class="meth"></span>`noise`

```py
noise(self, x: float, frequency: float = 1, amplitude: float = 1) -> float
```

Generates a noise value for a given coordinate using the simplex noise algorithm.

<span class="param">**Parameters**</span>

- `x` *(floaf)*: The input coordinate at which to compute the noise.
- `frequency` *(float, optional)*: Scales the input coordinate. Default value is 1.
- `amplitude` *(float, optional)*: Scales the resulting noise value. Default value is 1.

<span class="returns">**Returns**</span>

- *(floaf)*: The noise value computed at the given coordinate, mapped from the raw range of approximately [-1, 1] to [0, 1] and then scaled by the amplitude.

**How it works**

1. **Input Scaling:** The input coordinate x is multiplied by frequency to control the noise detail.
2. **Lattice Points:** The function determines the integer coordinates surrounding x (i.e., i0 and i1) and calculates the distances (x0 and x1).
3. **Weight Calculation:** Two weights (t0 and t1) are computed using a quadratic attenuation function.
4. **Gradient Contributions:** For each lattice point, if the corresponding weight is positive, it is squared and used to calculate a contribution via the internal _grad method.
5. **Noise Aggregation:** The contributions are combined into a raw noise value, which is roughly in the range [-1, 1].
6. **Mapping and Scaling:** The raw noise value is mapped to the [0, 1] range and then scaled by the provided amplitude.