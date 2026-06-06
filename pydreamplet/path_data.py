import re
from dataclasses import dataclass
import math

from pydreamplet.math import Vector
from pydreamplet.types import Real

type PathToken = str | float

_COMMAND_RE = re.compile(r"[AaCcHhLlMmQqSsTtVvZz]")
_TOKEN_RE = re.compile(
    r"[AaCcHhLlMmQqSsTtVvZz]|[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?"
)

_ARG_COUNTS = {
    "M": 2,
    "L": 2,
    "H": 1,
    "V": 1,
    "C": 6,
    "S": 4,
    "Q": 4,
    "T": 2,
    "A": 7,
    "Z": 0,
}


def _format_number(value: Real) -> str:
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return f"{value:g}" if isinstance(value, float) else str(value)


@dataclass(frozen=True)
class PathCommand:
    command: str
    values: tuple[float, ...] = ()

    @property
    def is_relative(self) -> bool:
        return self.command.islower()

    @property
    def absolute_command(self) -> str:
        return self.command.upper()

    def to_string(self) -> str:
        if not self.values:
            return self.command
        args = " ".join(_format_number(value) for value in self.values)
        return f"{self.command}{args}"

    def __str__(self) -> str:
        return self.to_string()


@dataclass(frozen=True)
class PathSegment:
    command: str
    start: Vector
    end: Vector

    @property
    def length(self) -> float:
        return math.hypot(self.end.x - self.start.x, self.end.y - self.start.y)

    def point_at(self, distance: Real) -> Vector:
        if self.length == 0:
            return self.start
        t = max(0.0, min(1.0, float(distance) / self.length))
        return Vector(
            self.start.x + (self.end.x - self.start.x) * t,
            self.start.y + (self.end.y - self.start.y) * t,
        )

    @property
    def tangent(self) -> Vector:
        if self.length == 0:
            return Vector(0, 0)
        return Vector(
            (self.end.x - self.start.x) / self.length,
            (self.end.y - self.start.y) / self.length,
        )


class PathBuilder:
    def __init__(self):
        self._commands: list[tuple[str, tuple[Real, ...]]] = []

    def _append(self, command: str, *values: Real) -> "PathBuilder":
        self._commands.append((command, values))
        return self

    def move_to(self, x: Real, y: Real) -> "PathBuilder":
        return self._append("M", x, y)

    def move_by(self, dx: Real, dy: Real) -> "PathBuilder":
        return self._append("m", dx, dy)

    def line_to(self, x: Real, y: Real) -> "PathBuilder":
        return self._append("L", x, y)

    def line_by(self, dx: Real, dy: Real) -> "PathBuilder":
        return self._append("l", dx, dy)

    def horizontal_to(self, x: Real) -> "PathBuilder":
        return self._append("H", x)

    def horizontal_by(self, dx: Real) -> "PathBuilder":
        return self._append("h", dx)

    def vertical_to(self, y: Real) -> "PathBuilder":
        return self._append("V", y)

    def vertical_by(self, dy: Real) -> "PathBuilder":
        return self._append("v", dy)

    def curve_to(
        self,
        x1: Real,
        y1: Real,
        x2: Real,
        y2: Real,
        x: Real,
        y: Real,
    ) -> "PathBuilder":
        return self._append("C", x1, y1, x2, y2, x, y)

    def curve_by(
        self,
        dx1: Real,
        dy1: Real,
        dx2: Real,
        dy2: Real,
        dx: Real,
        dy: Real,
    ) -> "PathBuilder":
        return self._append("c", dx1, dy1, dx2, dy2, dx, dy)

    def smooth_curve_to(
        self,
        x2: Real,
        y2: Real,
        x: Real,
        y: Real,
    ) -> "PathBuilder":
        return self._append("S", x2, y2, x, y)

    def smooth_curve_by(
        self,
        dx2: Real,
        dy2: Real,
        dx: Real,
        dy: Real,
    ) -> "PathBuilder":
        return self._append("s", dx2, dy2, dx, dy)

    def quadratic_to(
        self,
        x1: Real,
        y1: Real,
        x: Real,
        y: Real,
    ) -> "PathBuilder":
        return self._append("Q", x1, y1, x, y)

    def quadratic_by(
        self,
        dx1: Real,
        dy1: Real,
        dx: Real,
        dy: Real,
    ) -> "PathBuilder":
        return self._append("q", dx1, dy1, dx, dy)

    def smooth_quadratic_to(self, x: Real, y: Real) -> "PathBuilder":
        return self._append("T", x, y)

    def smooth_quadratic_by(self, dx: Real, dy: Real) -> "PathBuilder":
        return self._append("t", dx, dy)

    def arc_to(
        self,
        rx: Real,
        ry: Real,
        x_axis_rotation: Real,
        large_arc: bool | int,
        sweep: bool | int,
        x: Real,
        y: Real,
    ) -> "PathBuilder":
        return self._append(
            "A",
            rx,
            ry,
            x_axis_rotation,
            int(large_arc),
            int(sweep),
            x,
            y,
        )

    def arc_by(
        self,
        rx: Real,
        ry: Real,
        x_axis_rotation: Real,
        large_arc: bool | int,
        sweep: bool | int,
        dx: Real,
        dy: Real,
    ) -> "PathBuilder":
        return self._append(
            "a",
            rx,
            ry,
            x_axis_rotation,
            int(large_arc),
            int(sweep),
            dx,
            dy,
        )

    def close(self) -> "PathBuilder":
        return self._append("Z")

    def to_string(self) -> str:
        parts: list[str] = []
        for command, values in self._commands:
            if values:
                args = " ".join(_format_number(value) for value in values)
                parts.append(f"{command}{args}")
            else:
                parts.append(command)
        return " ".join(parts)

    def __str__(self) -> str:
        return self.to_string()


def _tokenize_path_data(path_data: str) -> list[PathToken]:
    tokens: list[PathToken] = []
    for match in _TOKEN_RE.finditer(path_data):
        token = match.group(0)
        if _COMMAND_RE.fullmatch(token):
            tokens.append(token)
        else:
            tokens.append(float(token))
    return tokens


def _read_numbers(tokens: list[PathToken], index: int, count: int) -> list[float]:
    values: list[float] = []
    for offset in range(count):
        token_index = index + offset
        if token_index >= len(tokens):
            raise ValueError("Path 'd' attribute has incomplete command parameters.")
        token = tokens[token_index]
        if isinstance(token, str):
            raise ValueError("Path 'd' attribute has incomplete command parameters.")
        values.append(token)
    return values


def parse_path_data(path_data: str) -> list[PathCommand]:
    tokens = _tokenize_path_data(path_data)
    commands: list[PathCommand] = []
    index = 0
    command = ""

    while index < len(tokens):
        token = tokens[index]
        if isinstance(token, str):
            command = token
            index += 1
        elif not command:
            raise ValueError("Path 'd' attribute must start with a path command.")

        upper_command = command.upper()
        if upper_command not in _ARG_COUNTS:
            raise ValueError(f"Unsupported path command: {command!r}")

        if upper_command == "Z":
            commands.append(PathCommand(command, ()))
            command = ""
            continue

        arg_count = _ARG_COUNTS[upper_command]
        values = _read_numbers(tokens, index, arg_count)
        index += arg_count
        commands.append(PathCommand(command, tuple(values)))

        if upper_command == "M":
            command = "l" if command.islower() else "L"

    return commands


def _path_command_to_absolute(
    path_command: PathCommand,
    current: Vector,
    subpath_start: Vector,
) -> tuple[PathCommand, Vector, Vector]:
    command = path_command.command
    values = path_command.values
    upper_command = command.upper()
    is_relative = command.islower()

    if upper_command == "Z":
        return PathCommand("Z"), subpath_start, subpath_start

    if upper_command == "M":
        x, y = values
        point = Vector(current.x + x, current.y + y) if is_relative else Vector(x, y)
        return PathCommand("M", point.xy), point, point

    if upper_command == "H":
        x = values[0] + current.x if is_relative else values[0]
        point = Vector(x, current.y)
        return PathCommand("H", (point.x,)), point, subpath_start

    if upper_command == "V":
        y = values[0] + current.y if is_relative else values[0]
        point = Vector(current.x, y)
        return PathCommand("V", (point.y,)), point, subpath_start

    if not is_relative:
        endpoint_indices = {
            "L": (0, 1),
            "T": (0, 1),
            "S": (2, 3),
            "Q": (2, 3),
            "C": (4, 5),
            "A": (5, 6),
        }
        end_x_index, end_y_index = endpoint_indices[upper_command]
        return (
            PathCommand(upper_command, values),
            Vector(values[end_x_index], values[end_y_index]),
            subpath_start,
        )

    absolute_values = list(values)
    coordinate_indices = {
        "L": (0,),
        "T": (0,),
        "S": (0, 2),
        "Q": (0, 2),
        "C": (0, 2, 4),
        "A": (5,),
    }[upper_command]

    for point_index in coordinate_indices:
        absolute_values[point_index] += current.x
        absolute_values[point_index + 1] += current.y

    end_x_index = coordinate_indices[-1]
    endpoint = Vector(absolute_values[end_x_index], absolute_values[end_x_index + 1])
    return PathCommand(upper_command, tuple(absolute_values)), endpoint, subpath_start


def normalize_path_commands(path_data: str) -> list[PathCommand]:
    commands: list[PathCommand] = []
    current = Vector(0, 0)
    subpath_start = Vector(0, 0)

    for command in parse_path_data(path_data):
        absolute_command, current, subpath_start = _path_command_to_absolute(
            command, current, subpath_start
        )
        commands.append(absolute_command)

    return commands


def normalize_path_data(path_data: str) -> str:
    return " ".join(command.to_string() for command in normalize_path_commands(path_data))


def iter_path_segments(path_data: str) -> list[PathSegment]:
    segments: list[PathSegment] = []
    current = Vector(0, 0)
    subpath_start = Vector(0, 0)

    for path_command in normalize_path_commands(path_data):
        command = path_command.command
        values = path_command.values

        if command == "M":
            current = Vector(values[0], values[1])
            subpath_start = current
            continue

        if command == "Z":
            if current != subpath_start:
                segments.append(PathSegment("Z", current, subpath_start))
            current = subpath_start
            continue

        if command == "L":
            end = Vector(values[0], values[1])
        elif command == "H":
            end = Vector(values[0], current.y)
        elif command == "V":
            end = Vector(current.x, values[0])
        else:
            raise ValueError(
                f"Path measurement only supports linear commands, got {command!r}"
            )

        segments.append(PathSegment(command, current, end))
        current = end

    return segments


def path_length(path_data: str) -> float:
    return sum(segment.length for segment in iter_path_segments(path_data))


def point_at_length(path_data: str, distance: Real) -> Vector:
    remaining = max(0.0, float(distance))
    segments = iter_path_segments(path_data)
    if not segments:
        return Vector(0, 0)

    for segment in segments:
        if remaining <= segment.length:
            return segment.point_at(remaining)
        remaining -= segment.length

    return segments[-1].end


def tangent_at_length(path_data: str, distance: Real) -> Vector:
    remaining = max(0.0, float(distance))
    segments = iter_path_segments(path_data)
    if not segments:
        return Vector(0, 0)

    last_nonzero_tangent = Vector(0, 0)
    for segment in segments:
        if segment.length > 0:
            last_nonzero_tangent = segment.tangent
        if remaining <= segment.length:
            return segment.tangent
        remaining -= segment.length

    return last_nonzero_tangent


def extract_path_points(path_data: str) -> list[Vector]:
    """
    Extract explicit coordinate points from SVG path data.

    This is not a full geometric path evaluator. It parses command structure and
    returns points that are explicit coordinates in the path data: move/line
    endpoints, curve control/end points, horizontal/vertical line endpoints, and
    arc endpoints. Arc radii and flags are intentionally not treated as points.
    """
    points: list[Vector] = []

    for path_command in normalize_path_commands(path_data):
        command = path_command.command
        values = path_command.values

        if command == "Z":
            continue

        if command == "M":
            points.append(Vector(values[0], values[1]))
            continue

        if command == "H":
            previous_y = points[-1].y if points else 0
            points.append(Vector(values[0], previous_y))
            continue

        if command == "V":
            previous_x = points[-1].x if points else 0
            points.append(Vector(previous_x, values[0]))
            continue

        coordinate_indices = {
            "L": (0,),
            "T": (0,),
            "S": (0, 2),
            "Q": (0, 2),
            "C": (0, 2, 4),
            "A": (5,),
        }[command]

        for point_index in coordinate_indices:
            points.append(Vector(values[point_index], values[point_index + 1]))

    return points
