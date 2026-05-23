import re

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


def extract_path_points(path_data: str) -> list[Vector]:
    """
    Extract explicit coordinate points from SVG path data.

    This is not a full geometric path evaluator. It parses command structure and
    returns points that are explicit coordinates in the path data: move/line
    endpoints, curve control/end points, horizontal/vertical line endpoints, and
    arc endpoints. Arc radii and flags are intentionally not treated as points.
    """
    tokens = _tokenize_path_data(path_data)
    points: list[Vector] = []
    index = 0
    command = ""
    current = Vector(0, 0)
    subpath_start = Vector(0, 0)

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
            current = subpath_start
            command = ""
            continue

        arg_count = _ARG_COUNTS[upper_command]
        values = _read_numbers(tokens, index, arg_count)
        index += arg_count

        is_relative = command.islower()

        if upper_command == "M":
            x, y = values
            current = (
                Vector(current.x + x, current.y + y)
                if is_relative
                else Vector(x, y)
            )
            subpath_start = current
            points.append(current)
            command = "l" if is_relative else "L"
            continue

        if upper_command == "H":
            x = values[0]
            current = (
                Vector(current.x + x, current.y)
                if is_relative
                else Vector(x, current.y)
            )
            points.append(current)
            continue

        if upper_command == "V":
            y = values[0]
            current = (
                Vector(current.x, current.y + y)
                if is_relative
                else Vector(current.x, y)
            )
            points.append(current)
            continue

        coordinate_indices = {
            "L": (0,),
            "T": (0,),
            "S": (0, 2),
            "Q": (0, 2),
            "C": (0, 2, 4),
            "A": (5,),
        }[upper_command]

        command_points: list[Vector] = []
        for point_index in coordinate_indices:
            x = values[point_index]
            y = values[point_index + 1]
            command_points.append(
                Vector(current.x + x, current.y + y) if is_relative else Vector(x, y)
            )

        points.extend(command_points)
        current = command_points[-1]

    return points
