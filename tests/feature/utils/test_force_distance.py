import pytest

from pydreamplet.utils import force_distance


def test_force_distance_example():
    """
    Tests force_distance with a typical input scenario where some labels must be adjusted.

    Input:
        [2, 6, 7, 8, 10, 16, 18] with distance=2.
    Expected output:
        [2, 5, 7, 9, 11, 16, 18]
    """
    input_values = [2, 6, 7, 8, 10, 16, 18]
    expected = [2, 5, 7, 9, 11, 16, 18]
    result = force_distance(input_values, distance=2)
    assert result == pytest.approx(expected)


def test_force_distance_already_spaced():
    """
    Tests force_distance when the input labels are already properly spaced.

    Input:
        [1, 3, 5, 7, 9] with distance=2.
    Expected output:
        [1, 3, 5, 7, 9]
    """
    input_values = [1, 3, 5, 7, 9]
    expected = [1, 3, 5, 7, 9]
    result = force_distance(input_values, distance=2)
    assert result == pytest.approx(expected)


def test_force_distance_single_value():
    """
    Tests force_distance with a single-element list.

    Input:
        [5] with any distance (using 2 here).
    Expected output:
        [5]
    """
    input_values = [5]
    expected = [5]
    result = force_distance(input_values, distance=2)
    assert result == pytest.approx(expected)


def test_force_distance_close_values():
    """
    Tests force_distance with values that are too close together,
    forcing an adjustment to satisfy the minimum distance.

    Input:
        [1, 1.1] with distance=2.

    The transformation sets:
        target[0] = 1, allowed interval for y[0] is [0, 2];
        target[1] = 1.1 - 2 = -0.9, allowed interval for y[1] is [-1.9, 0.1].
    Since 1 > -0.9, pooling forces both y values to their pooled average,
    which after clipping becomes approximately 0.05.
    Reconstructing x gives:
        x[0] = 0.05, x[1] = 0.05 + 2 = 2.05.

    Expected output:
        [0.05, 2.05]
    """
    input_values = [1, 1.1]
    expected = [0.05, 2.05]
    result = force_distance(input_values, distance=2)
    assert result == pytest.approx(expected, rel=1e-3)


def test_force_distance_unsorted():
    """
    Tests force_distance with an unsorted list to verify that the function
    correctly handles unsorted inputs by sorting internally and returning
    the results in the original order.

    Input:
         [16, 2, 18, 10, 7, 8, 6] with distance=2.
    Expected output:
         [16, 2, 18, 11, 7, 9, 5]
    """
    input_values = [16, 2, 18, 10, 7, 8, 6]
    expected = [16, 2, 18, 11, 7, 9, 5]
    result = force_distance(input_values, distance=2)
    assert result == pytest.approx(expected)
