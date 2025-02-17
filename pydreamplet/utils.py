from math import ceil, floor, log10
from math import pi as PI


def math_round(x):
    """
    Rounds x to the nearest integer using round half up.
    """
    return int(x + 0.5)


def constrain(value, min_val, max_val):
    """Constrain value between min_val and max_val."""
    return max(min_val, min(value, max_val))


def radians(degrees):
    """Convert degrees to radians."""
    return degrees * PI / 180


def degrees(radians):
    """Convert radians to degrees."""
    return radians * 180 / PI


def calculate_ticks(min_val, max_val, num_ticks=5, below_max=False):
    """
    Generate rounded tick values between min_val and max_val.

    :param min_val: The minimum value.
    :param max_val: The maximum value.
    :param num_ticks: Desired number of gridlines (default 5).
    :return: List of rounded gridline values.
    """
    if min_val >= max_val:
        raise ValueError("min_val must be less than max_val")

    range_span = max_val - min_val
    raw_step = range_span / num_ticks

    # Get order of magnitude
    magnitude = 10 ** floor(log10(raw_step))

    # Choose the best "nice" step (1, 2, or 5 times a power of ten)
    for factor in [1, 2, 5, 10]:
        step = factor * magnitude
        if range_span / step <= num_ticks:
            break

    # Compute start and end ticks
    start = ceil(min_val / step) * step
    end = ceil(max_val / step) * step  # Use ceil to ensure coverage

    ticks = list(range(int(start), int(end) + int(step), int(step)))
    if below_max:
        ticks = [tick for tick in ticks if tick <= max_val]

    return ticks
