import math
import random
from dataclasses import dataclass
from typing import Literal

from pydreamplet.math import Vector
from pydreamplet.noise import SimplexNoise2D
from pydreamplet.types import NumericPair, Real

type HexOrientation = Literal["pointy", "flat"]


@dataclass(frozen=True)
class Tile:
    """A reusable tile footprint for creative layouts."""

    index: int
    row: int
    column: int
    center: Vector
    corners: tuple[Vector, ...]


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


def _validate_non_negative(name: str, value: float) -> None:
    if value < 0:
        raise ValueError(f"{name} must be non-negative")


def _clean_zero(value: float) -> float:
    return 0.0 if math.isclose(value, 0, abs_tol=1e-12) else value


def _clean_vector(x: float, y: float) -> Vector:
    return Vector(_clean_zero(x), _clean_zero(y))


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


def wave_points(
    count: int,
    width: Real,
    *,
    amplitude: Real,
    frequency: Real = 1,
    phase: Real = 0,
    origin: NumericPair = (0, 0),
) -> list[Vector]:
    """Return points along a sine wave."""
    _validate_count("count", count)

    origin_x, origin_y = _pair(origin)
    denominator = count - 1 if count > 1 else 1
    points: list[Vector] = []
    for index in range(count):
        x = float(width) * index / denominator
        angle = math.tau * float(frequency) * index / denominator + math.radians(
            float(phase)
        )
        y = math.sin(angle) * float(amplitude)
        points.append(_clean_vector(origin_x + x, origin_y + y))
    return points


def spiral_points(
    count: int,
    *,
    start_radius: Real = 0,
    end_radius: Real,
    turns: Real = 1,
    center: NumericPair = (0, 0),
    start_angle: Real = 0,
) -> list[Vector]:
    """Return points along an Archimedean spiral."""
    _validate_count("count", count)
    _validate_non_negative("start_radius", float(start_radius))
    _validate_non_negative("end_radius", float(end_radius))

    center_x, center_y = _pair(center)
    denominator = count - 1 if count > 1 else 1
    points: list[Vector] = []
    for index in range(count):
        t = index / denominator
        radius = float(start_radius) + (float(end_radius) - float(start_radius)) * t
        angle = math.radians(float(start_angle)) + math.tau * float(turns) * t
        points.append(
            _clean_vector(
                center_x + math.cos(angle) * radius,
                center_y + math.sin(angle) * radius,
            )
        )
    return points


def lissajous_points(
    count: int,
    *,
    x_radius: Real,
    y_radius: Real,
    a: Real = 3,
    b: Real = 2,
    delta: Real = 90,
    center: NumericPair = (0, 0),
    include_endpoint: bool = False,
) -> list[Vector]:
    """Return points along a Lissajous curve."""
    _validate_count("count", count)
    _validate_non_negative("x_radius", float(x_radius))
    _validate_non_negative("y_radius", float(y_radius))

    center_x, center_y = _pair(center)
    denominator = count - 1 if include_endpoint and count > 1 else count
    delta_radians = math.radians(float(delta))

    points: list[Vector] = []
    for index in range(count):
        t = math.tau * index / denominator
        points.append(
            _clean_vector(
                center_x + math.sin(float(a) * t + delta_radians) * float(x_radius),
                center_y + math.sin(float(b) * t) * float(y_radius),
            )
        )
    return points


def phyllotaxis_points(
    count: int,
    *,
    spacing: Real = 1,
    angle: Real = 137.50776405,
    center: NumericPair = (0, 0),
    start_index: int = 0,
) -> list[Vector]:
    """Return points arranged with a sunflower-like phyllotaxis spiral."""
    _validate_count("count", count)
    if spacing < 0:
        raise ValueError("spacing must be non-negative")
    if start_index < 0:
        raise ValueError("start_index must be non-negative")

    center_x, center_y = _pair(center)
    points: list[Vector] = []
    for offset in range(count):
        index = start_index + offset
        radius = float(spacing) * math.sqrt(index)
        theta = math.radians(float(angle) * index)
        points.append(
            _clean_vector(
                center_x + math.cos(theta) * radius,
                center_y + math.sin(theta) * radius,
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


def square_tiles(
    columns: int,
    rows: int,
    width: Real,
    height: Real,
    *,
    origin: NumericPair = (0, 0),
    padding: Real | NumericPair = 0,
    gap: Real | NumericPair = 0,
) -> list[Tile]:
    """Return rectangular tile footprints fitted inside a rectangular area."""
    _validate_count("columns", columns)
    _validate_count("rows", rows)

    origin_x, origin_y = _pair(origin)
    padding_x, padding_y = _pair(padding)
    gap_x, gap_y = _pair(gap)
    _validate_non_negative("gap", gap_x)
    _validate_non_negative("gap", gap_y)

    inner_width = float(width) - padding_x * 2
    inner_height = float(height) - padding_y * 2
    if inner_width < 0 or inner_height < 0:
        raise ValueError("padding cannot exceed width or height")

    tile_width = (inner_width - gap_x * (columns - 1)) / columns
    tile_height = (inner_height - gap_y * (rows - 1)) / rows
    if tile_width < 0 or tile_height < 0:
        raise ValueError("gap cannot exceed available width or height")

    tiles: list[Tile] = []
    for row in range(rows):
        for column in range(columns):
            index = row * columns + column
            x0 = origin_x + padding_x + column * (tile_width + gap_x)
            y0 = origin_y + padding_y + row * (tile_height + gap_y)
            x1 = x0 + tile_width
            y1 = y0 + tile_height
            tiles.append(
                Tile(
                    index=index,
                    row=row,
                    column=column,
                    center=_clean_vector((x0 + x1) / 2, (y0 + y1) / 2),
                    corners=(
                        _clean_vector(x0, y0),
                        _clean_vector(x1, y0),
                        _clean_vector(x1, y1),
                        _clean_vector(x0, y1),
                    ),
                )
            )
    return tiles


def hex_tiles(
    columns: int,
    rows: int,
    radius: Real,
    *,
    origin: NumericPair = (0, 0),
    gap: Real | NumericPair = 0,
    orientation: HexOrientation = "pointy",
) -> list[Tile]:
    """Return regular hexagon tile footprints in an offset grid."""
    _validate_count("columns", columns)
    _validate_count("rows", rows)
    if radius <= 0:
        raise ValueError("radius must be positive")

    origin_x, origin_y = _pair(origin)
    gap_x, gap_y = _pair(gap)
    _validate_non_negative("gap", gap_x)
    _validate_non_negative("gap", gap_y)

    radius_float = float(radius)
    if orientation == "pointy":
        angle_offset = -90.0
        x_step = math.sqrt(3) * radius_float + gap_x
        y_step = 1.5 * radius_float + gap_y
    elif orientation == "flat":
        angle_offset = 0.0
        x_step = 1.5 * radius_float + gap_x
        y_step = math.sqrt(3) * radius_float + gap_y
    else:
        raise ValueError("orientation must be 'pointy' or 'flat'")

    tiles: list[Tile] = []
    for row in range(rows):
        for column in range(columns):
            index = row * columns + column
            if orientation == "pointy":
                center_x = origin_x + column * x_step + (row % 2) * x_step / 2
                center_y = origin_y + row * y_step
            else:
                center_x = origin_x + column * x_step
                center_y = origin_y + row * y_step + (column % 2) * y_step / 2

            corners = tuple(
                _clean_vector(
                    center_x + math.cos(math.radians(angle_offset + 60 * i))
                    * radius_float,
                    center_y + math.sin(math.radians(angle_offset + 60 * i))
                    * radius_float,
                )
                for i in range(6)
            )
            tiles.append(
                Tile(
                    index=index,
                    row=row,
                    column=column,
                    center=_clean_vector(center_x, center_y),
                    corners=corners,
                )
            )
    return tiles
