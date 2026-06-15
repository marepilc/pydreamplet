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
    # With no precedence, both endpoints are included and every gap is equal.
    my_list = list(range(12))
    assert sample_uniform(my_list, n=4) == (0, 11)

    my_list = list(range(11))
    assert sample_uniform(my_list, n=4) == (0, 5, 10)


def test_none_precedence_treats_n_as_maximum():
    my_list = list(range(4))
    assert sample_uniform(my_list, n=10) == (0, 1, 2, 3)


def test_single_item():
    # When n is 1, the function should return a single anchor index.
    my_list = list(range(10))
    assert sample_uniform(my_list, n=1, precedence="first") == (0,)
    assert sample_uniform(my_list, n=1, precedence="last") == (9,)
    assert sample_uniform(my_list, n=1) == (0,)


def test_empty_input_or_non_positive_limit():
    assert sample_uniform([], n=4) == ()
    assert sample_uniform(list(range(10)), n=0) == ()
    assert sample_uniform(list(range(10)), n=-1) == ()


def test_invalid_precedence():
    # An invalid precedence should raise a ValueError.
    my_list = list(range(10))
    with pytest.raises(ValueError):
        sample_uniform(my_list, n=3, precedence="invalid")  # type: ignore
