import math
import random

from pydreamplet.math import Vector
from pydreamplet.noise import SimplexNoise2D
from pydreamplet.types import NumericPair, Real


def _pair(value: Real | NumericPair) -> tuple[float, float]:
    if isinstance(value, int | float):
        size = float(value)
        return size, size
    if len(value) != 2:
        raise ValueError("expected a number or a pair of two numbers")
    return float(value[0]), float(value[1])


def _validate_count(name: str, value: int) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be positive")


def _clean_zero(value: float) -> float:
    return 0.0 if math.isclose(value, 0, abs_tol=1e-12) else value


def grid_points(
    columns: int,
    rows: int,
    width: Real,
    height: Real,
    *,
    origin: NumericPair = (0, 0),
    padding: Real | NumericPair = 0,
    jitter: Real | NumericPair = 0,
    seed: int | None = None,
) -> list[Vector]:
    """Return regularly spaced points across a rectangular area."""
    _validate_count("columns", columns)
    _validate_count("rows", rows)

    origin_x, origin_y = _pair(origin)
    padding_x, padding_y = _pair(padding)
    jitter_x, jitter_y = _pair(jitter)
    inner_width = float(width) - padding_x * 2
    inner_height = float(height) - padding_y * 2
    if inner_width < 0 or inner_height < 0:
        raise ValueError("padding cannot exceed width or height")

    rng = random.Random(seed)
    x_step = inner_width / (columns - 1) if columns > 1 else 0
    y_step = inner_height / (rows - 1) if rows > 1 else 0

    points: list[Vector] = []
    for row in range(rows):
        for column in range(columns):
            x = origin_x + padding_x + column * x_step
            y = origin_y + padding_y + row * y_step
            if jitter_x:
                x += rng.uniform(-jitter_x, jitter_x)
            if jitter_y:
                y += rng.uniform(-jitter_y, jitter_y)
            points.append(Vector(x, y))
    return points


def random_points(
    count: int,
    width: Real,
    height: Real,
    *,
    origin: NumericPair = (0, 0),
    padding: Real | NumericPair = 0,
    seed: int | None = None,
) -> list[Vector]:
    """Return uniformly distributed points inside a rectangular area."""
    _validate_count("count", count)

    origin_x, origin_y = _pair(origin)
    padding_x, padding_y = _pair(padding)
    min_x = origin_x + padding_x
    max_x = origin_x + float(width) - padding_x
    min_y = origin_y + padding_y
    max_y = origin_y + float(height) - padding_y
    if min_x > max_x or min_y > max_y:
        raise ValueError("padding cannot exceed width or height")

    rng = random.Random(seed)
    return [
        Vector(rng.uniform(min_x, max_x), rng.uniform(min_y, max_y))
        for _ in range(count)
    ]


def circle_points(
    count: int,
    radius: Real,
    *,
    center: NumericPair = (0, 0),
    start_angle: Real = 0,
    end_angle: Real = 360,
    include_endpoint: bool = False,
    radius_jitter: Real = 0,
    seed: int | None = None,
) -> list[Vector]:
    """Return points distributed around a circular or arc-shaped path."""
    _validate_count("count", count)
    if radius < 0:
        raise ValueError("radius must be non-negative")
    if radius_jitter < 0:
        raise ValueError("radius_jitter must be non-negative")

    center_x, center_y = _pair(center)
    rng = random.Random(seed)
    denominator = count - 1 if include_endpoint and count > 1 else count
    angle_span = float(end_angle) - float(start_angle)

    points: list[Vector] = []
    for index in range(count):
        angle = math.radians(float(start_angle) + angle_span * index / denominator)
        point_radius = float(radius)
        if radius_jitter:
            point_radius += rng.uniform(-float(radius_jitter), float(radius_jitter))
        x = center_x + math.cos(angle) * point_radius
        y = center_y + math.sin(angle) * point_radius
        points.append(
            Vector(
                _clean_zero(x),
                _clean_zero(y),
            )
        )
    return points


def noise_points(
    columns: int,
    rows: int,
    width: Real,
    height: Real,
    *,
    seed: int | None = None,
    frequency: Real = 1,
    amplitude: Real = 1,
    origin: NumericPair = (0, 0),
    padding: Real | NumericPair = 0,
) -> list[tuple[Vector, float]]:
    """Return grid points paired with deterministic 2D simplex noise values."""
    noise = SimplexNoise2D(seed=seed)
    points = grid_points(columns, rows, width, height, origin=origin, padding=padding)
    return [
        (
            point,
            noise.noise(
                point.x,
                point.y,
                frequency=float(frequency),
                amplitude=float(amplitude),
            ),
        )
        for point in points
    ]
