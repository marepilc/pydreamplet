import re

import pytest

# Import the functions from your module.
# Adjust the import path as necessary.
from pydreamplet.colors import (
    blend,
    color2rgba,
    generate_colors,
    hex_to_rgb,
    hexStr,
    random_color,
    random_int,
    rgb_to_hex,
    str2rgb,
)


# === Tests for hexStr ===
def test_hexStr():
    assert hexStr(0) == "00"
    assert hexStr(255) == "ff"
    assert hexStr(16) == "10"


# === Tests for random_int ===
def test_random_int():
    for _ in range(100):
        value = random_int(5, 10)
        assert 5 <= value <= 10


# === Tests for str2rgb ===
def test_str2rgb_valid_6():
    result = str2rgb("#ff0000")
    assert result == {"r": 255, "g": 0, "b": 0}


def test_str2rgb_valid_3():
    result = str2rgb("#f00")
    assert result == {"r": 255, "g": 0, "b": 0}


def test_str2rgb_invalid():
    result = str2rgb("notacolor")
    assert result == {"r": 0, "g": 0, "b": 0}


# === Tests for hex_to_rgb ===
def test_hex_to_rgb_valid():
    assert hex_to_rgb("#ffffff") == (255, 255, 255)
    assert hex_to_rgb("#000000") == (0, 0, 0)


def test_hex_to_rgb_invalid():
    with pytest.raises(ValueError):
        hex_to_rgb("#fff")  # Invalid length; expecting 6 hex digits after '#'


# === Tests for rgb_to_hex ===
def test_rgb_to_hex():
    assert rgb_to_hex((255, 255, 255)) == "#ffffff"
    assert rgb_to_hex((0, 0, 0)) == "#000000"


# === Tests for color2rgba ===
def test_color2rgba_tuple():
    # Using a tuple of 3 numbers.
    result = color2rgba((255, 0, 0), alpha=0.5)
    assert result == "rgba(255, 0, 0, 0.5)"


def test_color2rgba_int():
    # Using an integer value (greyscale).
    result = color2rgba(128, alpha=0.75)
    assert result == "rgba(128, 128, 128, 0.75)"


def test_color2rgba_hex():
    # Using a hex string.
    result = color2rgba("#00ff00", alpha=0.3)
    assert result == "rgba(0, 255, 0, 0.3)"


# === Tests for blend ===
def test_blend_zero_proportion():
    # With proportion 0, should return the first color exactly.
    assert blend("#123456", "#abcdef", 0) == "#123456"


def test_blend_full_proportion():
    # With proportion 1, should return the second color exactly.
    assert blend("#123456", "#abcdef", 1) == "#abcdef"


def test_blend_half_proportion():
    # Blend black and white in equal parts.
    # Depending on rounding math_round, it might be "#7f7f7f" or "#808080".
    blended = blend("#000000", "#ffffff", 0.5)
    assert blended in ("#7f7f7f", "#808080")


def test_blend_invalid():
    # When one or both colors are invalid, should return "#000000".
    assert blend("invalid", "#abcdef", 0.5) == "#000000"


# === Tests for random_color ===
def test_random_color():
    color = random_color()
    assert isinstance(color, str)
    assert color.startswith("#")
    assert len(color) == 7
    # Check that each character (after '#') is a valid hex digit.
    hex_digits = "0123456789abcdefABCDEF"
    for ch in color[1:]:
        assert ch in hex_digits


# === Tests for generate_colors ===
def test_generate_colors_complementary():
    palette = generate_colors(base_color="#db45f9", n=10, harmony="complementary")
    assert len(palette) == 10
    for color in palette:
        assert re.match(r"^#[0-9a-fA-F]{6}$", color)


def test_generate_colors_compound():
    palette = generate_colors(base_color="#db45f9", n=10, harmony="compound")
    assert len(palette) == 10
    for color in palette:
        assert re.match(r"^#[0-9a-fA-F]{6}$", color)


def test_generate_colors_square():
    palette = generate_colors(base_color="#db45f9", n=10, harmony="square")
    assert len(palette) == 10
    for color in palette:
        assert re.match(r"^#[0-9a-fA-F]{6}$", color)


def test_generate_colors_invalid_harmony():
    with pytest.raises(ValueError):
        generate_colors(base_color="#db45f9", n=10, harmony="unknown")
