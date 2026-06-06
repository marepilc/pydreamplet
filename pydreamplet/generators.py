import math
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any, Literal, TypeVar, cast

from pydreamplet.shapes import (
    basis_spline,
    cardinal_spline,
    catmull_rom_path,
    cross,
    linear_path,
    monotone_x_path,
    monotone_y_path,
    ring,
    star,
    step_path,
)
from pydreamplet.types import Real
from pydreamplet.utils import pie_angles

T = TypeVar("T")

type Accessor[T] = Callable[[T, int], Real]
type PointAccessor[T] = Callable[[T, int], tuple[Real, Real]]
type CurveName = Literal[
    "linear",
    "step",
    "basis",
    "cardinal",
    "catmull-rom",
    "monotone-x",
    "monotone-y",
]
type SymbolName = Literal["circle", "square", "diamond", "triangle", "cross", "star"]
type LinkCurve = Literal["linear", "horizontal", "vertical"]


def _format_point(x: float, y: float) -> str:
    if math.isclose(x, 0, abs_tol=1e-9):
        x = 0
    if math.isclose(y, 0, abs_tol=1e-9):
        y = 0
    return f"{x:.2f},{y:.2f}"


def _default_x(item: object, _index: int) -> Real:
    return cast(Sequence[Real], item)[0]


def _default_y(item: object, _index: int) -> Real:
    return cast(Sequence[Real], item)[1]


def _zero(_item: object, _index: int) -> Real:
    return 0


def _true(_item: object, _index: int) -> bool:
    return True


def _curve_path(
    points: Sequence[tuple[float, float]],
    curve: CurveName,
    *,
    closed: bool = False,
    tension: float = 0.0,
) -> str:
    if curve == "linear":
        return linear_path(points, closed=closed)
    if curve == "step":
        return step_path(points, closed=closed)
    if curve == "basis":
        return basis_spline(points, closed=closed)
    if curve == "cardinal":
        return cardinal_spline(points, tension=tension, closed=closed)
    if curve == "catmull-rom":
        return catmull_rom_path(points, closed=closed)
    if closed:
        raise ValueError(f"{curve!r} does not support closed paths")
    if curve == "monotone-x":
        return monotone_x_path(points)
    if curve == "monotone-y":
        return monotone_y_path(points)
    raise ValueError(f"unknown curve: {curve!r}")


def _segment_defined_points(
    data: Sequence[T],
    x: Accessor[T],
    y: Accessor[T],
    defined: Callable[[T, int], bool],
) -> list[list[tuple[float, float]]]:
    segments: list[list[tuple[float, float]]] = []
    current: list[tuple[float, float]] = []

    for index, item in enumerate(data):
        if not defined(item, index):
            if current:
                segments.append(current)
                current = []
            continue
        current.append((float(x(item, index)), float(y(item, index))))

    if current:
        segments.append(current)
    return segments


class LineGenerator[T]:
    """Generate SVG path data from a sequence of data points."""

    def __init__(
        self,
        *,
        x: Accessor[T] | None = None,
        y: Accessor[T] | None = None,
        defined: Callable[[T, int], bool] | None = None,
        curve: CurveName = "linear",
        tension: float = 0.0,
    ) -> None:
        self.x = x or _default_x
        self.y = y or _default_y
        self.defined = defined or _true
        self.curve: CurveName = curve
        self.tension = tension

    def __call__(self, data: Sequence[T]) -> str:
        paths = [
            _curve_path(segment, self.curve, tension=self.tension)
            for segment in _segment_defined_points(data, self.x, self.y, self.defined)
        ]
        return " ".join(path for path in paths if path)


class AreaGenerator[T]:
    """Generate a closed area path between two data-defined baselines."""

    def __init__(
        self,
        *,
        x0: Accessor[T] | None = None,
        x1: Accessor[T] | None = None,
        y0: Accessor[T] | None = None,
        y1: Accessor[T] | None = None,
        defined: Callable[[T, int], bool] | None = None,
        curve: CurveName = "linear",
        tension: float = 0.0,
    ) -> None:
        self.x0 = x0 or x1 or _default_x
        self.x1 = x1 or x0 or _default_x
        self.y0 = y0 or _zero
        self.y1 = y1 or _default_y
        self.defined = defined or _true
        self.curve: CurveName = curve
        self.tension = tension

    def __call__(self, data: Sequence[T]) -> str:
        paths: list[str] = []
        for index_points in self._segments(data):
            upper = [
                (float(self.x1(item, index)), float(self.y1(item, index)))
                for item, index in index_points
            ]
            lower = [
                (float(self.x0(item, index)), float(self.y0(item, index)))
                for item, index in reversed(index_points)
            ]
            paths.append(
                _curve_path([*upper, *lower], self.curve, closed=True, tension=self.tension)
            )
        return " ".join(path for path in paths if path)

    def _segments(self, data: Sequence[T]) -> list[list[tuple[T, int]]]:
        segments: list[list[tuple[T, int]]] = []
        current: list[tuple[T, int]] = []
        for index, item in enumerate(data):
            if not self.defined(item, index):
                if current:
                    segments.append(current)
                    current = []
                continue
            current.append((item, index))
        if current:
            segments.append(current)
        return segments


def _radial_point(
    angle: Real,
    radius: Real,
    *,
    cx: Real = 0,
    cy: Real = 0,
) -> tuple[float, float]:
    radians = math.radians(float(angle))
    return (
        float(cx) + float(radius) * math.cos(radians),
        float(cy) + float(radius) * math.sin(radians),
    )


class RadialLineGenerator[T]:
    def __init__(
        self,
        *,
        angle: Accessor[T],
        radius: Accessor[T],
        cx: Real = 0,
        cy: Real = 0,
        defined: Callable[[T, int], bool] | None = None,
        curve: CurveName = "linear",
        tension: float = 0.0,
    ) -> None:
        self.angle = angle
        self.radius = radius
        self.cx = cx
        self.cy = cy
        self.defined = defined or _true
        self.curve: CurveName = curve
        self.tension = tension

    def __call__(self, data: Sequence[T]) -> str:
        def x(item: T, index: int) -> Real:
            return _radial_point(
                self.angle(item, index), self.radius(item, index), cx=self.cx, cy=self.cy
            )[0]

        def y(item: T, index: int) -> Real:
            return _radial_point(
                self.angle(item, index), self.radius(item, index), cx=self.cx, cy=self.cy
            )[1]

        return LineGenerator(
            x=x,
            y=y,
            defined=self.defined,
            curve=self.curve,
            tension=self.tension,
        )(data)


class RadialAreaGenerator[T]:
    def __init__(
        self,
        *,
        angle: Accessor[T],
        inner_radius: Accessor[T],
        outer_radius: Accessor[T],
        cx: Real = 0,
        cy: Real = 0,
        defined: Callable[[T, int], bool] | None = None,
        curve: CurveName = "linear",
        tension: float = 0.0,
    ) -> None:
        self.angle = angle
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.cx = cx
        self.cy = cy
        self.defined = defined or _true
        self.curve: CurveName = curve
        self.tension = tension

    def __call__(self, data: Sequence[T]) -> str:
        def outer_x(item: T, index: int) -> Real:
            return _radial_point(
                self.angle(item, index),
                self.outer_radius(item, index),
                cx=self.cx,
                cy=self.cy,
            )[0]

        def outer_y(item: T, index: int) -> Real:
            return _radial_point(
                self.angle(item, index),
                self.outer_radius(item, index),
                cx=self.cx,
                cy=self.cy,
            )[1]

        def inner_x(item: T, index: int) -> Real:
            return _radial_point(
                self.angle(item, index),
                self.inner_radius(item, index),
                cx=self.cx,
                cy=self.cy,
            )[0]

        def inner_y(item: T, index: int) -> Real:
            return _radial_point(
                self.angle(item, index),
                self.inner_radius(item, index),
                cx=self.cx,
                cy=self.cy,
            )[1]

        return AreaGenerator(
            x0=inner_x,
            x1=outer_x,
            y0=inner_y,
            y1=outer_y,
            defined=self.defined,
            curve=self.curve,
            tension=self.tension,
        )(data)


@dataclass(frozen=True)
class PieSlice:
    value: float
    index: int
    start_angle: float
    end_angle: float

    @property
    def angle(self) -> float:
        return self.end_angle - self.start_angle

    @property
    def mid_angle(self) -> float:
        return (self.start_angle + self.end_angle) / 2


class PieGenerator:
    def __init__(self, *, start_angle: Real = 0, end_angle: Real | None = None) -> None:
        self.start_angle = start_angle
        self.end_angle = end_angle

    def __call__(self, values: Sequence[Real]) -> list[PieSlice]:
        if any(value < 0 for value in values):
            raise ValueError("pie values must be non-negative")
        if sum(values) <= 0:
            raise ValueError("pie values must contain at least one positive value")

        return [
            PieSlice(float(value), index, start, end)
            for index, (value, (start, end)) in enumerate(
                zip(values, pie_angles(values, self.start_angle, self.end_angle))
            )
        ]


class ArcGenerator[T]:
    def __init__(
        self,
        *,
        inner_radius: Accessor[T],
        outer_radius: Accessor[T],
        start_angle: Accessor[T],
        end_angle: Accessor[T],
        cx: Real = 0,
        cy: Real = 0,
    ) -> None:
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.cx = cx
        self.cy = cy

    def __call__(self, item: T, index: int = 0) -> str:
        return ring(
            float(self.cx),
            float(self.cy),
            inner_radius=float(self.inner_radius(item, index)),
            outer_radius=float(self.outer_radius(item, index)),
            start_angle=float(self.start_angle(item, index)),
            end_angle=float(self.end_angle(item, index)),
        )


class SymbolGenerator[T]:
    def __init__(
        self,
        *,
        symbol: Callable[[T, int], SymbolName] | SymbolName = "circle",
        size: Accessor[T] | Real = 64,
    ) -> None:
        self.symbol = symbol
        self.size = size

    def __call__(self, item: T | None = None, index: int = 0) -> str:
        datum = cast(T, item)
        symbol = self.symbol(datum, index) if callable(self.symbol) else self.symbol
        size = float(self.size(datum, index)) if callable(self.size) else float(self.size)
        if size < 0:
            raise ValueError("symbol size must be non-negative")

        if symbol == "circle":
            radius = math.sqrt(size / math.pi)
            return ring(inner_radius=0, outer_radius=radius, start_angle=0, end_angle=360)
        if symbol == "square":
            side = math.sqrt(size)
            half = side / 2
            points = [(-half, -half), (half, -half), (half, half), (-half, half)]
            return linear_path(points, closed=True)
        if symbol == "diamond":
            y = math.sqrt(size / 2)
            x = size / (2 * y) if y else 0
            return linear_path([(0, -y), (x, 0), (0, y), (-x, 0)], closed=True)
        if symbol == "triangle":
            side = math.sqrt((4 * size) / math.sqrt(3)) if size else 0
            height = side * math.sqrt(3) / 2
            return linear_path(
                [(0, -height * 2 / 3), (side / 2, height / 3), (-side / 2, height / 3)],
                closed=True,
            )
        if symbol == "cross":
            return cross(size=math.sqrt(size) * 1.5, thickness=math.sqrt(size) / 2)
        if symbol == "star":
            outer = math.sqrt(size / math.pi) * 1.5
            return star(n=5, inner_radius=outer * 0.45, outer_radius=outer, angle=-90)
        raise ValueError(f"unknown symbol: {symbol!r}")


class LinkGenerator[T]:
    def __init__(
        self,
        *,
        source: PointAccessor[T],
        target: PointAccessor[T],
        curve: LinkCurve = "horizontal",
    ) -> None:
        self.source = source
        self.target = target
        self.curve = curve

    def __call__(self, item: T, index: int = 0) -> str:
        x0, y0 = (float(value) for value in self.source(item, index))
        x1, y1 = (float(value) for value in self.target(item, index))
        if self.curve == "linear":
            return linear_path([(x0, y0), (x1, y1)])
        if self.curve == "horizontal":
            mid_x = (x0 + x1) / 2
            return (
                f"M {_format_point(x0, y0)} "
                f"C {_format_point(mid_x, y0)} {_format_point(mid_x, y1)} "
                f"{_format_point(x1, y1)}"
            )
        if self.curve == "vertical":
            mid_y = (y0 + y1) / 2
            return (
                f"M {_format_point(x0, y0)} "
                f"C {_format_point(x0, mid_y)} {_format_point(x1, mid_y)} "
                f"{_format_point(x1, y1)}"
            )
        raise ValueError(f"unknown link curve: {self.curve!r}")


def line_generator(**kwargs: Any) -> LineGenerator[Any]:
    return LineGenerator(**kwargs)


def area_generator(**kwargs: Any) -> AreaGenerator[Any]:
    return AreaGenerator(**kwargs)


def radial_line_generator(**kwargs: Any) -> RadialLineGenerator[Any]:
    return RadialLineGenerator(**kwargs)


def radial_area_generator(**kwargs: Any) -> RadialAreaGenerator[Any]:
    return RadialAreaGenerator(**kwargs)


def pie_generator(**kwargs: Any) -> PieGenerator:
    return PieGenerator(**kwargs)


def arc_generator(**kwargs: Any) -> ArcGenerator[Any]:
    return ArcGenerator(**kwargs)


def symbol_generator(**kwargs: Any) -> SymbolGenerator[Any]:
    return SymbolGenerator(**kwargs)


def link_generator(**kwargs: Any) -> LinkGenerator[Any]:
    return LinkGenerator(**kwargs)
