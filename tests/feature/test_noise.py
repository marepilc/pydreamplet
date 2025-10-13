import math

from pydreamplet.noise import Noise, SimplexNoise, SimplexNoise2D, SimplexNoise3D

# ────────────────────────────────────────────────────────────
# Tests for the Noise (Random Walk) Class
# ────────────────────────────────────────────────────────────


def test_noise_value_in_range():
    # Create a Noise instance with bounds [0, 10] and a noise range of 0.5.
    n = Noise(0, 10, 0.5)
    # Test multiple readings to ensure they remain within the min/max bounds.
    for _ in range(10):
        val = n.value
        assert 0 <= val <= 10, f"Value {val} is out of range [0, 10]"


def test_noise_int_value():
    n = Noise(0, 10, 0.5)
    for _ in range(10):
        int_val = n.int_value
        # Check that int_value is indeed an integer and within range.
        assert isinstance(int_val, int), f"{int_val} is not an int"
        assert 0 <= int_val <= 10, f"Integer value {int_val} is out of range [0, 10]"


def test_setter_adjustments():
    n = Noise(0, 10, 0.5)
    # Set new minimum and maximum, then ensure that value adjusts if necessary.
    n.min = 5
    assert n.value >= 5, "Noise value did not adjust to the new minimum."
    n.max = 8
    assert n.value <= 8, "Noise value did not adjust to the new maximum."


# ────────────────────────────────────────────────────────────
# Tests for Simplex Noise 1D
# ────────────────────────────────────────────────────────────


def test_simplex_noise_1d_range():
    sn = SimplexNoise(seed=42)
    # Check that the noise function produces values within [0, 1] by default.
    for x in [0, 0.1, 0.5, 1.0, 2.0]:
        val = sn.noise(x)
        assert 0 <= val <= 1, f"1D noise value {val} at x={x} is not in [0, 1]"


def test_simplex_noise_1d_amplitude():
    sn = SimplexNoise(seed=42)
    amplitude = 2.5
    val = sn.noise(0.5, amplitude=amplitude)
    # The noise is scaled by amplitude so it should lie within [0, amplitude].
    assert (
        0 <= val <= amplitude
    ), f"1D noise value {val} with amplitude {amplitude} is out of range"


def test_deterministic_noise_1d():
    # Ensure that using the same seed produces identical noise outputs.
    sn1 = SimplexNoise(seed=123)
    sn2 = SimplexNoise(seed=123)
    val1 = sn1.noise(0.5)
    val2 = sn2.noise(0.5)
    assert math.isclose(
        val1, val2, rel_tol=1e-9
    ), "Deterministic 1D noise values do not match"


# ────────────────────────────────────────────────────────────
# Tests for Simplex Noise 2D
# ────────────────────────────────────────────────────────────


def test_simplex_noise_2d_range():
    sn2d = SimplexNoise2D(seed=42)
    for x, y in [(0, 0), (0.1, 0.2), (0.5, 0.5), (1, 1), (2, 3)]:
        val = sn2d.noise(x, y)
        assert 0 <= val <= 1, f"2D noise value {val} at ({x}, {y}) is not in [0, 1]"


def test_deterministic_noise_2d():
    sn1 = SimplexNoise2D(seed=123)
    sn2 = SimplexNoise2D(seed=123)
    val1 = sn1.noise(0.5, 0.5)
    val2 = sn2.noise(0.5, 0.5)
    assert math.isclose(
        val1, val2, rel_tol=1e-9
    ), "Deterministic 2D noise values do not match"


# ────────────────────────────────────────────────────────────
# Tests for Simplex Noise 3D
# ────────────────────────────────────────────────────────────


def test_simplex_noise_3d_range():
    sn3d = SimplexNoise3D(seed=42)
    for x, y, z in [(0, 0, 0), (0.1, 0.2, 0.3), (0.5, 0.5, 0.5), (1, 1, 1), (2, 3, 4)]:
        val = sn3d.noise(x, y, z)
        assert (
            0 <= val <= 1
        ), f"3D noise value {val} at ({x}, {y}, {z}) is not in [0, 1]"


def test_deterministic_noise_3d():
    sn1 = SimplexNoise3D(seed=123)
    sn2 = SimplexNoise3D(seed=123)
    val1 = sn1.noise(0.5, 0.5, 0.5)
    val2 = sn2.noise(0.5, 0.5, 0.5)
    assert math.isclose(
        val1, val2, rel_tol=1e-9
    ), "Deterministic 3D noise values do not match"
