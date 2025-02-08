import math
from collections.abc import Callable


def linear_scale(
    domain: tuple[float, float], range_: tuple[float, float]
) -> Callable[[float], float]:
    """
    Linearly maps a value from the input domain to the output range.
    """
    d0, d1 = domain
    r0, r1 = range_

    def scale(value: float) -> float:
        return ((value - d0) / (d1 - d0)) * (r1 - r0) + r0

    return scale


def band_scale(
    domain: list[str], range_: tuple[float, float], padding: float = 0.1
) -> Callable[[str], float | None]:
    """
    Maps categorical values (strings) to evenly spaced positions in the range.
    The returned function also carries a `bandwidth` attribute that gives the computed band width.
    """
    r0, r1 = range_
    n = len(domain)
    if n == 0:
        raise ValueError("Domain must contain at least one value")
    # Compute the step: total range divided by number of bands plus gaps
    step = (r1 - r0) / (n + padding * (n - 1))
    # Each band takes (1 - padding) portion of the step.
    band_width = step * (1 - padding)

    def scale(value: str) -> float | None:
        try:
            index = domain.index(value)
            # Position is offset by index * step * (1 + padding)
            return r0 + index * step * (1 + padding)
        except ValueError:
            return None  # value not found in the domain

    # Attach a bandwidth method to the scale function.
    scale.bandwidth = lambda: band_width  # type: ignore
    return scale


def point_scale(
    domain: list[str], range_: tuple[float, float], padding: float = 0.5
) -> Callable[[str], float | None]:
    """
    Maps categorical values to points in the range, placing padding at both ends.
    """
    r0, r1 = range_
    n = len(domain)
    if n == 0:
        raise ValueError("Domain must contain at least one value")
    # Compute step based on (n - 1) intervals plus padding on each end.
    step = (r1 - r0) / (n - 1 + 2 * padding)

    def scale(value: str) -> float | None:
        try:
            index = domain.index(value)
            return r0 + step * (index + padding)
        except ValueError:
            return None

    return scale


def ordinal_scale(domain: list[str], range_: list) -> Callable[[str], object]:
    """
    Maps categorical values to a set of output values in a cyclic fashion.
    """
    if not range_:
        raise ValueError("Range must contain at least one value")
    mapping = {d: range_[i % len(range_)] for i, d in enumerate(domain)}

    def scale(value: str) -> object:
        return mapping.get(value)

    return scale


def square_scale(
    domain: tuple[float, float], range_: tuple[float, float]
) -> Callable[[float], float]:
    """
    Maps an input value (e.g. an area) to an output using a square-root transformation.

    This is useful when the visual representation (like the side length of a square)
    should be proportional to the square root of the area so that the actual area
    is proportional to the input value.

    The transformation is defined as:
        scale(value) = r0 + ((sqrt(value) - sqrt(d0)) / (sqrt(d1) - sqrt(d0))) * (r1 - r0)
    """
    d0, d1 = domain
    r0, r1 = range_
    if d0 < 0 or d1 < 0:
        raise ValueError("Domain values must be non-negative for square scale")
    sqrt_d0, sqrt_d1 = math.sqrt(d0), math.sqrt(d1)
    if sqrt_d1 == sqrt_d0:
        raise ValueError("Invalid domain: sqrt(d1) and sqrt(d0) cannot be equal")

    def scale(value: float) -> float:
        return r0 + ((math.sqrt(value) - sqrt_d0) / (sqrt_d1 - sqrt_d0)) * (r1 - r0)

    return scale


def circle_scale(
    domain: tuple[float, float], range_: tuple[float, float]
) -> Callable[[float], float]:
    """
    Maps an input value to the radius of a circle such that the circle's area is linearly
    proportional to the input value.

    If the input domain is (d0, d1) and the desired radius range is (r0, r1), then the area of the circle
    will vary from π·r0² to π·r1². The mapping is given by:

        radius(v) = sqrt( ((v - d0) / (d1 - d0)) * (r1² - r0²) + r0² )

    This way, if you use π·radius(v)² as the circle’s area, it will be proportional to v.
    """
    d0, d1 = domain
    r0, r1 = range_
    if d1 == d0:
        raise ValueError("Domain values must be distinct")

    def scale(value: float) -> float:
        # Linearly interpolate between r0^2 and r1^2, then take the square root.
        r_squared = ((value - d0) / (d1 - d0)) * (r1 * r1 - r0 * r0) + r0 * r0
        return math.sqrt(r_squared)

    return scale
