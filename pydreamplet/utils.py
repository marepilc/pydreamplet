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


def calculate_ticks(min_val, max_val, num_ticks=5):
    """
    Generate rounded ticks values between min_val and max_val.

    :param min_val: The minimum value.
    :param max_val: The maximum value.
    :param num_ticks: Desired number of gridlines (default 5).
    :return: List of rounded gridline values.
    """
    if min_val >= max_val:
        raise ValueError("min_val must be less than max_val")

    range_span = max_val - min_val
    step = round(range_span / num_ticks, -int(floor(log10(range_span / num_ticks))))

    start = ceil(min_val / step) * step
    end = floor(max_val / step) * step
    gridlines = list(range(int(start), int(end) + int(step), int(step)))

    return gridlines
