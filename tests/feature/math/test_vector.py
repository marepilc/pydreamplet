import math

import pytest

from pydreamplet.math import Vector


@pytest.fixture
def vector_3_4():
    """A vector with x=3, y=4 (magnitude=5)."""
    return Vector(3, 4)


@pytest.fixture
def vector_zero():
    """A zero vector."""
    return Vector(0, 0)


def test_initialization(vector_3_4):
    assert vector_3_4.x == 3
    assert vector_3_4.y == 4
    assert vector_3_4.xy == (3, 4)


def test_set_method(vector_3_4):
    v = vector_3_4.copy()
    v.set(7, 8)
    assert v.x == 7
    assert v.y == 8


def test_property_setters(vector_3_4):
    v = vector_3_4.copy()
    v.x = 10
    v.y = 20
    assert v.x == 10
    assert v.y == 20


def test_copy(vector_3_4):
    v_copy = vector_3_4.copy()
    # They should be equal but not the same object.
    assert v_copy == vector_3_4
    v_copy.x = 100
    assert vector_3_4.x == 3


# Test equality operator
def test_equality(vector_3_4):
    v = Vector(3, 4)
    assert vector_3_4 == v


# Test arithmetic operators
def test_addition(vector_3_4):
    result = vector_3_4 + Vector(1, 2)
    assert result == Vector(4, 6)


def test_inplace_addition(vector_3_4):
    v = vector_3_4.copy()
    v += Vector(1, 1)
    assert v == Vector(4, 5)


def test_subtraction(vector_3_4):
    result = vector_3_4 - Vector(1, 2)
    assert result == Vector(2, 2)


def test_inplace_subtraction(vector_3_4):
    v = vector_3_4.copy()
    v -= Vector(1, 1)
    assert v == Vector(2, 3)


def test_scalar_multiplication(vector_3_4):
    result = vector_3_4 * 2
    assert result == Vector(6, 8)


def test_rmul(vector_3_4):
    result = 3 * vector_3_4
    assert result == Vector(9, 12)


def test_inplace_multiplication(vector_3_4):
    v = vector_3_4.copy()
    v *= 3
    assert v == Vector(9, 12)


def test_scalar_division(vector_3_4):
    result = vector_3_4 / 2
    assert result == Vector(1.5, 2)


def test_inplace_division(vector_3_4):
    v = vector_3_4.copy()
    v /= 2
    assert v == Vector(1.5, 2)


# Test dot product
def test_dot_product(vector_3_4):
    dot = vector_3_4.dot(Vector(1, 2))
    expected = 3 * 1 + 4 * 2
    assert math.isclose(dot, expected)


# Test normalization
def test_normalize(vector_3_4):
    norm = vector_3_4.normalize()
    expected = Vector(3 / 5, 4 / 5)
    assert math.isclose(norm.x, expected.x)
    assert math.isclose(norm.y, expected.y)
    # Confirm the original vector is unchanged.
    assert vector_3_4 == Vector(3, 4)


def test_normalize_zero(vector_zero):
    with pytest.raises(ValueError):
        vector_zero.normalize()


# Test direction (angle) property
def test_direction_getter(vector_3_4):
    expected_angle = math.degrees(math.atan2(4, 3))
    assert math.isclose(vector_3_4.direction, expected_angle)


def test_direction_setter(vector_3_4):
    v = vector_3_4.copy()
    original_magnitude = v.magnitude
    # Set direction to 0 radians (pointing along the positive x-axis)
    v.direction = 0
    assert math.isclose(v.x, original_magnitude)
    assert math.isclose(v.y, 0)


# Test magnitude property
def test_magnitude_getter(vector_3_4):
    expected = 5  # sqrt(3^2 + 4^2)
    assert math.isclose(vector_3_4.magnitude, expected)


def test_magnitude_setter(vector_3_4):
    v = vector_3_4.copy()
    v.magnitude = 10
    expected_angle_deg = math.degrees(math.atan2(4, 3))
    expected_angle_rad = math.radians(expected_angle_deg)
    expected_x = math.cos(expected_angle_rad) * 10
    expected_y = math.sin(expected_angle_rad) * 10
    assert math.isclose(v.x, expected_x)
    assert math.isclose(v.y, expected_y)


# Test limit method
def test_limit_reduces_magnitude(vector_3_4):
    v = vector_3_4.copy()
    v.limit(3)
    assert math.isclose(v.magnitude, 3)


def test_limit_no_change_if_within_limit():
    v = Vector(1, 1)
    original = v.copy()
    v.limit(10)
    assert v == original


# Test __repr__ method
def test_repr(vector_3_4):
    expected = f"Vector(x={vector_3_4.x}, y={vector_3_4.y})"
    assert repr(vector_3_4) == expected


# Test error conditions for unsupported operand types
def test_invalid_addition(vector_3_4):
    with pytest.raises(TypeError):
        vector_3_4 + 5


def test_invalid_subtraction(vector_3_4):
    with pytest.raises(TypeError):
        vector_3_4 - "a"


def test_invalid_multiplication(vector_3_4):
    with pytest.raises(TypeError):
        vector_3_4 * "a"


def test_invalid_division(vector_3_4):
    with pytest.raises(TypeError):
        vector_3_4 / "a"
