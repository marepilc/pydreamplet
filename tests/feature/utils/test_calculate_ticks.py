from pydreamplet.utils import calculate_ticks


def test_ticks_are_properly_rounded():
    ticks = calculate_ticks(0, 42986, 5)
    assert ticks == [0, 10000, 20000, 30000, 40000]
    ticks = calculate_ticks(0, 87654, 5, below_max=False)
    assert ticks == [0, 20000, 40000, 60000, 80000, 100000]
    ticks = calculate_ticks(0, 157000, 5, below_max=False)
    assert ticks == [0, 50000, 100000, 150000, 200000]


def test_below_max_ticks():
    ticks = calculate_ticks(0, 42986, 5, below_max=True)
    assert ticks == [0, 10000, 20000, 30000, 40000]


def test_num_ticks_works():
    ticks = calculate_ticks(0, 42986, 3)
    assert ticks == [0, 20000, 40000]
    ticks = calculate_ticks(0, 42986, 3, below_max=False)
    assert ticks == [0, 20000, 40000, 60000]


def test_decimal_ranges():
    """Test calculate_ticks with decimal ranges (0 to 1)."""
    # Basic decimal range
    ticks = calculate_ticks(0, 1, 5)
    expected = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    assert ticks == expected
    
    # Partial decimal range
    ticks = calculate_ticks(0.1, 0.9, 5)
    expected = [0.2, 0.4, 0.6, 0.8]
    assert ticks == expected
    
    # Small decimal range
    ticks = calculate_ticks(0, 0.5, 5)
    expected = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
    assert ticks == expected
    
    # Negative decimal range
    ticks = calculate_ticks(-0.5, 0.5, 5)
    expected = [-0.4, -0.2, 0.0, 0.2, 0.4]
    assert ticks == expected
    
    # Very small decimal range
    ticks = calculate_ticks(0.001, 0.009, 5)
    expected = [0.002, 0.004, 0.006, 0.008]
    assert ticks == expected
