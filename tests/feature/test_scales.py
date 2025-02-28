import math

import pytest

from pydreamplet.scales import (
    BandScale,
    CircleScale,
    ColorScale,
    LinearScale,
    OrdinalScale,
    PointScale,
    SquareScale,
)


# ----- LinearScale Tests -----
def test_linear_scale_map_and_invert():
    # Create a linear scale with domain (0, 10) and output_range (0, 100)
    scale = LinearScale((0, 10), (0, 100))
    # Test mapping: 5 should map to 50
    assert scale.map(5) == 50
    # Test mapping boundaries
    assert scale.map(0) == 0
    assert scale.map(10) == 100
    # Test invert: 50 should invert to 5
    assert scale.invert(50) == 5
    # Test invert boundaries
    assert scale.invert(0) == 0
    assert scale.invert(100) == 10


def test_linear_scale_setters():
    scale = LinearScale((0, 5), (0, 50))
    # Change domain and output range and test mapping
    scale.domain = (10, 20)
    scale.output_range = (100, 200)
    assert math.isclose(scale.map(15), 150)
    assert math.isclose(scale.invert(150), 15)


# ----- BandScale Tests -----
def test_band_scale_map():
    # Setup: three categories, output range 0 to 300, padding 0.1
    domain = ["a", "b", "c"]
    scale = BandScale(domain, (0, 300), padding=0.1)
    # Calculate expected values based on the scale formula:
    # total_padding = (n - 1)*padding + 2*outer_padding = (2*0.1 + 2*0.1) = 0.4
    # band_width = 300 / (3 + 0.4) = approx 88.2353
    # step = band_width * (1 + padding) = 88.2353 * 1.1 ≈ 97.0588
    # First band start: 0 + band_width*outer_padding = 88.2353 * 0.1 ≈ 8.8235
    pos_a = scale.map("a")
    pos_b = scale.map("b")
    pos_c = scale.map("c")

    expected_start = scale.bandwidth * scale.outer_padding
    assert math.isclose(pos_a, expected_start, rel_tol=1e-4)
    # The difference between consecutive bands should equal the step size.
    assert math.isclose(pos_b - pos_a, scale.step, rel_tol=1e-4)
    assert math.isclose(pos_c - pos_b, scale.step, rel_tol=1e-4)


def test_band_scale_unknown_value():
    scale = BandScale(["a", "b"], (0, 100))
    with pytest.raises(ValueError):
        scale.map("c")


def test_band_scale_duplicate_domain():
    # Expect a ValueError when duplicate values are present in the domain.
    with pytest.raises(ValueError):
        BandScale(["a", "b", "a"], (0, 100), padding=0.1)


# ----- PointScale Tests -----
def test_point_scale_map_and_unknown():
    domain = ["a", "b", "c"]
    # With padding 0.5, step = (100-0)/( (3 - 1) + 2*0.5 ) = 100/3 ≈ 33.3333
    scale = PointScale(domain, (0, 100), padding=0.5)
    # Expected positions:
    # "a": 0 + step*(0 + 0.5) ≈ 16.67
    # "b": 0 + step*(1 + 0.5) ≈ 50.0
    # "c": 0 + step*(2 + 0.5) ≈ 83.33
    step = (100) / (2 + 1)  # 100/3
    assert math.isclose(scale.map("a"), step * 0.5, rel_tol=1e-4)
    assert math.isclose(scale.map("b"), step * 1.5, rel_tol=1e-4)
    assert math.isclose(scale.map("c"), step * 2.5, rel_tol=1e-4)
    # Test unknown value returns None
    assert scale.map("d") is None


def test_point_scale_duplicate_domain():
    # Expect a ValueError when duplicate values are present in the domain.
    with pytest.raises(ValueError):
        PointScale(["a", "a", "b"], (0, 100), padding=0.5)


# ----- OrdinalScale Tests -----
def test_ordinal_scale_map():
    # Given two colors, the mapping should cycle over the domain.
    domain = ["a", "b", "c", "d"]
    output_range = ["red", "green"]
    scale = OrdinalScale(domain, output_range)
    expected_mapping = {
        "a": "red",  # 0 % 2 == 0
        "b": "green",  # 1 % 2 == 1
        "c": "red",  # 2 % 2 == 0
        "d": "green",  # 3 % 2 == 1
    }
    for key, expected in expected_mapping.items():
        assert scale.map(key) == expected


def test_ordinal_scale_duplicate_domain():
    # Expect a ValueError when duplicate values are present in the domain.
    with pytest.raises(ValueError):
        OrdinalScale(["a", "b", "a"], ["red", "blue"])


# ----- ColorScale Tests -----
def test_color_scale_map_and_clamping():
    # Create a color scale from black to white.
    scale = ColorScale((0, 100), ("#000000", "#ffffff"))
    # For value 0, expect black
    assert scale.map(0) == "#000000"
    # For value 100, expect white
    assert scale.map(100) == "#ffffff"
    # For value 50, expect a mid-gray. Since int(127.5) truncates to 127,
    # expected hex is '#7f7f7f' (0x7f == 127)
    assert scale.map(50) == "#7f7f7f"
    # Test clamping: values outside the domain are clamped
    assert scale.map(-20) == "#000000"
    assert scale.map(150) == "#ffffff"


def test_color_scale_invalid_domain():
    # Domain with equal min and max should raise an error.
    with pytest.raises(ValueError):
        ColorScale((5, 5), ("#000000", "#ffffff"))


def test_color_scale_invalid_output_range():
    # Output range must have exactly two colors.
    with pytest.raises(ValueError):
        ColorScale((0, 100), ("#000000",))


# ----- SquareScale Tests -----
def test_square_scale_map():
    # For a square scale with domain (0, 100) and output_range (0, 10),
    # the mapping should produce sqrt-based scaling.
    scale = SquareScale((0, 100), (0, 10))
    # For value 0, result should be 0.
    assert math.isclose(scale.map(0), 0, rel_tol=1e-4)
    # For value 100, result should be 10.
    assert math.isclose(scale.map(100), 10, rel_tol=1e-4)
    # For value 25, sqrt(25)=5 so mapping should yield 5.
    assert math.isclose(scale.map(25), 5, rel_tol=1e-4)


def test_square_scale_invalid_domain():
    # Domain values must be non-negative.
    with pytest.raises(ValueError):
        SquareScale((-1, 100), (0, 10))
    # Also, if the square roots of domain endpoints are equal, error.
    with pytest.raises(ValueError):
        SquareScale((25, 25), (0, 10))


# ----- CircleScale Tests -----
def test_circle_scale_map():
    # With domain (0, 100) and output_range (5, 10), the radius is computed so that
    # the area is proportional to the input value.
    scale = CircleScale((0, 100), (5, 10))
    # For value 0, radius should be 5.
    assert math.isclose(scale.map(0), 5, rel_tol=1e-4)
    # For value 100, radius should be 10.
    assert math.isclose(scale.map(100), 10, rel_tol=1e-4)
    # For value 50, compute expected radius:
    # r_squared = ((50/100) * (10^2 - 5^2)) + 5^2 = (0.5 * (100 - 25)) + 25 = (0.5 * 75) + 25 = 37.5 + 25 = 62.5
    # Expected radius = sqrt(62.5)
    expected_radius = math.sqrt(62.5)
    assert math.isclose(scale.map(50), expected_radius, rel_tol=1e-4)


def test_circle_scale_invalid_domain():
    # Domain values must be distinct.
    with pytest.raises(ValueError):
        CircleScale((50, 50), (5, 10))
