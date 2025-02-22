import math
import random
from typing import Optional


# ────────────────────────────────────────────────────────────
# Noise Value Generator (Random Walk)
# ────────────────────────────────────────────────────────────
class Noise:
    def __init__(self, min_val: float, max_val: float, noise_range: float):
        self._min = min_val
        self._max = max_val
        self.noise_range = noise_range
        self._value = random.uniform(min_val, max_val)

    @property
    def min(self) -> float:
        return self._min

    @min.setter
    def min(self, value: float):
        old_relative = self.noise_range
        if self._value < value:
            self._value = value
        self._min = value
        self._range = old_relative * (self._max - self._min)

    @property
    def max(self) -> float:
        return self._max

    @max.setter
    def max(self, value: float):
        old_relative = self.noise_range
        if self._value > value:
            self._value = value
        self._max = value
        self._range = old_relative * (self._max - self._min)

    @property
    def noise_range(self) -> float:
        return (
            self._range / (self._max - self._min) if (self._max - self._min) != 0 else 0
        )

    @noise_range.setter
    def noise_range(self, value: float):
        if 0 < value < 1:
            self._range = value * (self._max - self._min)

    @property
    def value(self) -> float:
        self._next_value()
        return self._value

    @value.setter
    def value(self, new_value: float):
        if self._min <= new_value <= self._max:
            self._value = new_value

    @property
    def int_value(self) -> int:
        self._next_value()
        return round(self._value)

    def _next_value(self):
        min0 = self._value - self._range / 2
        max0 = self._value + self._range / 2
        if min0 < self._min:
            min0 = self._min
            max0 = min0 + self._range
        elif max0 > self._max:
            max0 = self._max
            min0 = max0 - self._range
        self._value = random.uniform(min0, max0)


# ────────────────────────────────────────────────────────────
# Unified Noise Base Class
# Handles permutation generation, seeding, and helper functions.
# ────────────────────────────────────────────────────────────
class NoiseBase:
    def __init__(self, seed: Optional[int] = None):
        self.permutation = self._generate_permutation(seed)

    def _generate_permutation(self, seed: Optional[int] = None):
        p = list(range(256))
        # Choose a seeded random function if a seed is provided.
        rnd = self._seeded_random(seed) if seed is not None else random.random
        # Fisher-Yates shuffle
        for i in range(len(p) - 1, 0, -1):
            j = math.floor(rnd() * (i + 1))
            p[i], p[j] = p[j], p[i]
        # Duplicate the array to avoid overflow in permutation lookups.
        return p + p

    def _seeded_random(self, seed: int):
        def random_func():
            nonlocal seed
            seed = (seed * 16807) % 2147483647
            return (seed - 1) / 2147483646

        return random_func

    def _fade(self, t: float) -> float:
        # Fade function as defined by Ken Perlin.
        return t * t * t * (t * (t * 6 - 15) + 10)

    def _lerp(self, a: float, b: float, t: float) -> float:
        return a + t * (b - a)


# ────────────────────────────────────────────────────────────
# Simplex Noise 1D
# Produces values in roughly [-1, 1] (when amplitude is 1)
# ────────────────────────────────────────────────────────────
class SimplexNoise(NoiseBase):
    def __init__(self, seed: Optional[int] = None):
        super().__init__(seed)
        # For 1D, the gradient can be either 1 or -1.
        self.grad3 = [1, -1]

    def noise(self, x: float, frequency: float = 1, amplitude: float = 1) -> float:
        x *= frequency
        i0 = math.floor(x)
        i1 = i0 + 1
        x0 = x - i0
        x1 = x0 - 1.0

        t0 = 1.0 - x0 * x0
        t1 = 1.0 - x1 * x1

        n0 = 0.0
        n1 = 0.0

        if t0 > 0:
            t0 *= t0
            n0 = t0 * t0 * self._grad(self.permutation[i0 & 255], x0)
        if t1 > 0:
            t1 *= t1
            n1 = t1 * t1 * self._grad(self.permutation[i1 & 255], x1)

        # rawNoise is roughly in [-1, 1]
        raw_noise = 0.5 * (n0 + n1)
        # Map [-1, 1] -> [0, 1] then scale by amplitude
        return amplitude * ((raw_noise + 1) / 2)

    def _grad(self, hash_val: int, x: float) -> float:
        return self.grad3[hash_val & 1] * x


# ────────────────────────────────────────────────────────────
# Simplex Noise 2D
# Produces values in roughly [-1, 1] (when amplitude is 1)
# ────────────────────────────────────────────────────────────
class SimplexNoise2D(NoiseBase):
    def __init__(self, seed: Optional[int] = None):
        super().__init__(seed)
        self.grad3 = [
            [1, 1],
            [-1, 1],
            [1, -1],
            [-1, -1],
            [1, 0],
            [-1, 0],
            [0, 1],
            [0, -1],
            [1, 1],
            [-1, 1],
            [1, -1],
            [-1, -1],  # Duplicated to have 12 entries.
        ]
        self.F2 = 0.5 * (math.sqrt(3.0) - 1.0)
        self.G2 = (3.0 - math.sqrt(3.0)) / 6.0

    def noise(
        self, x: float, y: float, frequency: float = 1, amplitude: float = 1
    ) -> float:
        x *= frequency
        y *= frequency

        s = (x + y) * self.F2
        i = math.floor(x + s)
        j = math.floor(y + s)

        t = (i + j) * self.G2
        X0 = i - t
        Y0 = j - t
        x0 = x - X0
        y0 = y - Y0

        if x0 > y0:
            i1, j1 = 1, 0
        else:
            i1, j1 = 0, 1

        x1 = x0 - i1 + self.G2
        y1 = y0 - j1 + self.G2
        x2 = x0 - 1.0 + 2.0 * self.G2
        y2 = y0 - 1.0 + 2.0 * self.G2

        ii = int(i) & 255
        jj = int(j) & 255

        gi0 = self.permutation[ii + self.permutation[jj]] % 12
        gi1 = self.permutation[ii + i1 + self.permutation[jj + j1]] % 12
        gi2 = self.permutation[ii + 1 + self.permutation[jj + 1]] % 12

        t0 = 0.5 - x0 * x0 - y0 * y0
        if t0 < 0:
            n0 = 0.0
        else:
            t0 *= t0
            n0 = t0 * t0 * self._dot(self.grad3[gi0], x0, y0)

        t1 = 0.5 - x1 * x1 - y1 * y1
        if t1 < 0:
            n1 = 0.0
        else:
            t1 *= t1
            n1 = t1 * t1 * self._dot(self.grad3[gi1], x1, y1)

        t2 = 0.5 - x2 * x2 - y2 * y2
        if t2 < 0:
            n2 = 0.0
        else:
            t2 *= t2
            n2 = t2 * t2 * self._dot(self.grad3[gi2], x2, y2)

        raw_noise = 70.0 * (n0 + n1 + n2)
        return amplitude * ((raw_noise + 1) / 2)

    def _dot(self, g: list, x: float, y: float) -> float:
        return g[0] * x + g[1] * y


# ────────────────────────────────────────────────────────────
# Simplex Noise 3D
# Produces values in roughly [-1, 1] (when amplitude is 1)
# ────────────────────────────────────────────────────────────
class SimplexNoise3D(NoiseBase):
    def __init__(self, seed: Optional[int] = None):
        super().__init__(seed)
        self.grad3 = [
            [1, 1, 0],
            [-1, 1, 0],
            [1, -1, 0],
            [-1, -1, 0],
            [1, 0, 1],
            [-1, 0, 1],
            [1, 0, -1],
            [-1, 0, -1],
            [0, 1, 1],
            [0, -1, 1],
            [0, 1, -1],
            [0, -1, -1],
        ]
        self.F3 = 1.0 / 3.0
        self.G3 = 1.0 / 6.0

    def noise(
        self, x: float, y: float, z: float, frequency: float = 1, amplitude: float = 1
    ) -> float:
        x *= frequency
        y *= frequency
        z *= frequency

        s = (x + y + z) * self.F3
        i = math.floor(x + s)
        j = math.floor(y + s)
        k = math.floor(z + s)

        t = (i + j + k) * self.G3
        X0 = i - t
        Y0 = j - t
        Z0 = k - t
        x0 = x - X0
        y0 = y - Y0
        z0 = z - Z0

        # Determine simplex corner ordering.
        if x0 >= y0:
            if y0 >= z0:
                i1, j1, k1 = 1, 0, 0
                i2, j2, k2 = 1, 1, 0
            elif x0 >= z0:
                i1, j1, k1 = 1, 0, 0
                i2, j2, k2 = 1, 0, 1
            else:
                i1, j1, k1 = 0, 0, 1
                i2, j2, k2 = 1, 0, 1
        else:
            if y0 < z0:
                i1, j1, k1 = 0, 0, 1
                i2, j2, k2 = 0, 1, 1
            elif x0 < z0:
                i1, j1, k1 = 0, 1, 0
                i2, j2, k2 = 0, 1, 1
            else:
                i1, j1, k1 = 0, 1, 0
                i2, j2, k2 = 1, 1, 0

        x1 = x0 - i1 + self.G3
        y1 = y0 - j1 + self.G3
        z1 = z0 - k1 + self.G3
        x2 = x0 - i2 + 2.0 * self.G3
        y2 = y0 - j2 + 2.0 * self.G3
        z2 = z0 - k2 + 2.0 * self.G3
        x3 = x0 - 1.0 + 3.0 * self.G3
        y3 = y0 - 1.0 + 3.0 * self.G3
        z3 = z0 - 1.0 + 3.0 * self.G3

        ii = int(i) & 255
        jj = int(j) & 255
        kk = int(k) & 255

        gi0 = self.permutation[ii + self.permutation[jj + self.permutation[kk]]] % 12
        gi1 = (
            self.permutation[
                ii + i1 + self.permutation[jj + j1 + self.permutation[kk + k1]]
            ]
            % 12
        )
        gi2 = (
            self.permutation[
                ii + i2 + self.permutation[jj + j2 + self.permutation[kk + k2]]
            ]
            % 12
        )
        gi3 = (
            self.permutation[
                ii + 1 + self.permutation[jj + 1 + self.permutation[kk + 1]]
            ]
            % 12
        )

        t0 = 0.5 - x0 * x0 - y0 * y0 - z0 * z0
        if t0 < 0:
            n0 = 0.0
        else:
            t0 *= t0
            n0 = t0 * t0 * self._dot(self.grad3[gi0], x0, y0, z0)

        t1 = 0.5 - x1 * x1 - y1 * y1 - z1 * z1
        if t1 < 0:
            n1 = 0.0
        else:
            t1 *= t1
            n1 = t1 * t1 * self._dot(self.grad3[gi1], x1, y1, z1)

        t2 = 0.5 - x2 * x2 - y2 * y2 - z2 * z2
        if t2 < 0:
            n2 = 0.0
        else:
            t2 *= t2
            n2 = t2 * t2 * self._dot(self.grad3[gi2], x2, y2, z2)

        t3 = 0.5 - x3 * x3 - y3 * y3 - z3 * z3
        if t3 < 0:
            n3 = 0.0
        else:
            t3 *= t3
            n3 = t3 * t3 * self._dot(self.grad3[gi3], x3, y3, z3)

        raw_noise = 32.0 * (n0 + n1 + n2 + n3)
        return amplitude * ((raw_noise + 1) / 2)

    def _dot(self, g: list, x: float, y: float, z: float) -> float:
        return g[0] * x + g[1] * y + g[2] * z
