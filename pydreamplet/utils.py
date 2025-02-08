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
