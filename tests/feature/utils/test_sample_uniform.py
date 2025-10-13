import pytest

from pydreamplet.utils import sample_uniform


def test_first_precedence():
    # With "first" precedence, the first element is always included.
    my_list = list(range(10))
    # Expected: (0, 3, 6, 9)
    assert sample_uniform(my_list, n=4, precedence="first") == (0, 3, 6, 9)
    # Expected: (0, 4, 8)
    assert sample_uniform(my_list, n=3, precedence="first") == (0, 4, 8)


def test_last_precedence():
    # With "last" precedence, the last element is always included.
    my_list = list(range(10))
    # Expected: (1, 5, 9)
    assert sample_uniform(my_list, n=3, precedence="last") == (1, 5, 9)


def test_none_precedence():
    # With no precedence, indices are balanced and endpoints nudged inward.
    my_list = list(range(12))
    # Expected: (1, 3, 7, 10)
    assert sample_uniform(my_list, n=4, precedence=None) == (1, 3, 7, 10)


def test_single_item():
    # When n is 1, the function should return a single anchor index.
    my_list = list(range(10))
    assert sample_uniform(my_list, n=1, precedence="first") == (0,)
    assert sample_uniform(my_list, n=1, precedence="last") == (9,)
    # For precedence None, it should return the middle index.
    assert sample_uniform(my_list, n=1, precedence=None) == (5,)


def test_invalid_precedence():
    # An invalid precedence should raise a ValueError.
    my_list = list(range(10))
    with pytest.raises(ValueError):
        sample_uniform(my_list, n=3, precedence="invalid")  # type: ignore
