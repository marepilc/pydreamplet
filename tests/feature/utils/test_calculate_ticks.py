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
