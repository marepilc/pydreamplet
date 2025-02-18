import pytest

from pydreamplet.utils import pie_angles


def test_equal_slices():
    """Test with equal slice values."""
    values = [1, 1, 1, 1]
    result = pie_angles(values)
    expected = [(0, 90), (90, 180), (180, 270), (270, 360)]
    assert result == expected


def test_different_slices():
    """Test with slices of different sizes."""
    values = [1, 2, 3]
    result = pie_angles(values)
    expected = [
        (0, 60),  # 1/6 of 360
        (60, 180),  # 2/6 of 360
        (180, 360),  # 3/6 of 360
    ]
    assert result == expected


def test_start_angle():
    """Test with a non-zero starting angle."""
    values = [1, 2, 3]
    start_angle = 90
    result = pie_angles(values, start_angle=start_angle)
    expected = [
        (90, 150),  # 1/6 of 360 added to start_angle 90: 90 + 60 = 150
        (150, 270),  # next slice: 150 + 120 = 270
        (270, 450),  # final slice: 270 + 180 = 450
    ]
    assert result == expected


def test_empty_values():
    """Test that an empty list returns an empty list."""
    values = []
    result = pie_angles(values)
    expected = []
    assert result == expected


def test_all_zero_values():
    """Test that a list of zeros raises a ZeroDivisionError."""
    # Since the sum of values is 0, the function will raise ZeroDivisionError.
    with pytest.raises(ZeroDivisionError):
        pie_angles([0, 0, 0])
