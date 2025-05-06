from math import ceil, floor, log10
from math import pi as PI
from typing import Any, TypedDict


class Pool(TypedDict):
    sum: float
    count: int
    low: float
    high: float
    value: float


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


def calculate_ticks(
    min_val: int | float, max_val: int | float, num_ticks=5, below_max=True
):
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

    # Initialize step before the loop
    step = magnitude  # Default value

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
    values: list[int | float],
    start_angle: int | float = 0,
    end_angle: int | float | None = None,
) -> list[tuple[float, float]]:
    """
    Calculate start and end angles for each pie slice.

    :param values: List of values for each slice.
    :param start_angle: Starting angle for the first slice.
    :param end_angle: Ending angle for the last slice (if None, will be start_angle + 360).
    :return: List of tuples containing start and end angles for each slice.
    """
    # If end_angle is not specified, make it start_angle + 360 for a full circle
    if end_angle is None:
        end_angle = start_angle + 360

    total = sum(values)
    angles = []
    angle_span = end_angle - start_angle
    current_angle = start_angle

    for value in values:
        slice_angle = (value / total) * angle_span
        end_slice = current_angle + slice_angle
        angles.append((current_angle, end_slice))
        current_angle = end_slice

    return angles


def pure_linspace(start: int | float, stop: int | float, num: int) -> list[int | float]:
    if num == 1:
        return [stop]
    step = (stop - start) / (num - 1)
    return [start + step * i for i in range(num)]


def sample_uniform(input_list: list[Any], n: int, precedence="first"):
    L = len(input_list)
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


def create_pool(
    sum_val: float, count: int, low_val: float, high_val: float, value_val: float
) -> Pool:
    return {
        "sum": sum_val,
        "count": count,
        "low": low_val,
        "high": high_val,
        "value": value_val,
    }


def force_distance(values: list[float], distance: float) -> list[float]:
    """
    Given an unsorted list of numeric values and a band size,
    adjust the positions so that each label (with width=band) centered
    at the new position [x - band/2, x + band/2] does not overlap its neighbors.

    Each label i must lie within [v[i] - band/2, v[i] + band/2].
    The function finds positions x[i] with the constraint:
         x[i+1] - x[i] >= band,
    while keeping x[i] as close as possible to the original v[i].

    The algorithm works by rewriting x[i] = y[i] + i*band, so that the
    non-overlap condition becomes y[i+1] >= y[i]. Then for each i the allowed
    y values are:
         [v[i] - band/2 - i*band,  v[i] + band/2 - i*band].
    A pooling algorithm is used to adjust the targets:
         target[i] = v[i] - i*band.

    The input list is unsorted; it is sorted internally before computing,
    and then the result is returned in the original order.
    """
    # Create array of pairs (original_index, value) and sort by value
    indexed_values = list(enumerate(values))
    sorted_pairs = sorted(indexed_values, key=lambda x: x[1])
    sorted_values = [v for _, v in sorted_pairs]
    n = len(sorted_values)
    half = distance / 2.0

    # Compute target values and allowed intervals for the "y" variables.
    target = [v - i * distance for i, v in enumerate(sorted_values)]
    lower = [v - half - i * distance for i, v in enumerate(sorted_values)]
    upper = [v + half - i * distance for i, v in enumerate(sorted_values)]

    # Create pools of indices that must share the same y value.
    pools: list[Pool] = []
    for i in range(n):
        pool: Pool = {
            "sum": target[i],
            "count": 1,
            "low": lower[i],
            "high": upper[i],
            "value": target[i],
        }
        while pools and pools[-1]["value"] > pool["value"]:
            prev = pools.pop()
            merged_low = max(prev["low"], pool["low"])
            merged_high = min(prev["high"], pool["high"])
            merged_sum = prev["sum"] + pool["sum"]
            merged_count = prev["count"] + pool["count"]
            new_value = merged_sum / merged_count
            # Clip the new pooled value to the merged allowed interval.
            new_value = max(merged_low, min(merged_high, new_value))
            pool = {
                "sum": merged_sum,
                "count": merged_count,
                "low": merged_low,
                "high": merged_high,
                "value": new_value,
            }
        pools.append(pool)

    # Expand the pools into a full list of y values.
    y: list[float] = []
    for pool in pools:
        # Mypy now knows pool["count"] is an int.
        y.extend([pool["value"]] * pool["count"])

    # Compute the final x positions for the sorted order.
    x_sorted = [y_val + i * distance for i, y_val in enumerate(y)]

    # Map the computed positions back to the original order.
    result = [0.0] * n
    for sorted_index, (orig_index, _) in enumerate(sorted_pairs):
        result[orig_index] = x_sorted[sorted_index]
    return result
