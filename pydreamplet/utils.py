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


def pie_angles(
    values: list[int | float], start_angle: int | float = 0
) -> list[tuple[float, float]]:
    """
    Calculate start and end angles for each pie slice.

    :param values: List of values for each slice.
    :param start_angle: Starting angle for the first slice.
    :return: List of tuples containing start and end angles for each slice.
    """
    total = sum(values)
    angles = []
    for value in values:
        end_angle = start_angle + (value / total) * 360
        angles.append((start_angle, end_angle))
        start_angle = end_angle
    return angles


def pure_linspace(start, stop, num):
    if num == 1:
        return [stop]
    step = (stop - start) / (num - 1)
    return [start + step * i for i in range(num)]


def sample_uniform(my_list, n, precedence="first"):
    L = len(my_list)
    if n <= 1:
        # if only one item is needed, return an anchor based on precedence.
        if precedence == "last":
            return (L - 1,)
        elif precedence is None:
            return (L // 2,)
        else:
            return (0,)

    # For "first" and "last" we use the idea of fixed endpoints.
    if precedence == "first":
        # always include the first item (index 0) and then use a constant step.
        step = (L - 1) // (n - 1)
        return tuple(0 + i * step for i in range(n))

    elif precedence == "last":
        # always include the last item and work backwards.
        step = (L - 1) // (n - 1)
        # compute indices in reverse then sort
        return tuple(sorted(L - 1 - i * step for i in range(n)))

    elif precedence is None:
        # When neither end is anchored, split the list into n buckets and choose
        # an index from each bucket. Compute the indices using pure Python.
        idx = [floor(x) for x in pure_linspace(0, L - 1, n)]
        # Adjust endpoints inward if possible.
        if idx[0] == 0 and L > n:
            idx[0] = 1
        if idx[-1] == L - 1 and L > n:
            idx[-1] = L - 2
        return tuple(idx)

    else:
        raise ValueError("precedence must be 'first', 'last', or None")
