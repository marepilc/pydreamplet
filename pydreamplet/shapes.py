import math
from typing import Sequence, cast


_ANGLE_TOLERANCE = 1e-9


def _format_point(x: float, y: float) -> str:
    if math.isclose(x, 0, abs_tol=_ANGLE_TOLERANCE):
        x = 0
    if math.isclose(y, 0, abs_tol=_ANGLE_TOLERANCE):
        y = 0
    return f"{x:.2f},{y:.2f}"


def _validate_non_negative(value: float, name: str) -> None:
    if value < 0:
        raise ValueError(f"{name} must be non-negative")


def _validate_positive(value: float, name: str) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be positive")


def _arc_span(start_angle: float, end_angle: float) -> tuple[float, bool, int]:
    raw_delta = end_angle - start_angle
    sweep_flag = 1 if raw_delta >= 0 else 0
    if math.isclose(raw_delta, 0, abs_tol=_ANGLE_TOLERANCE):
        return 0, False, sweep_flag

    abs_delta = abs(raw_delta)
    normalized = abs_delta % 360
    if math.isclose(normalized, 360, abs_tol=_ANGLE_TOLERANCE):
        normalized = 0

    if math.isclose(normalized, 0, abs_tol=_ANGLE_TOLERANCE) and abs_delta >= 360:
        return 360 if raw_delta > 0 else -360, True, sweep_flag

    signed_delta = normalized if raw_delta > 0 else -normalized
    return signed_delta, False, sweep_flag


def star(
    x: float = 0,
    y: float = 0,
    n: int = 5,
    *,
    inner_radius: float,
    outer_radius: float,
    angle: float = 0,
) -> str:
    """
    Returns a d-string for a star with n points, inner_radius, outer_radius, and angle.

    The star is centered at (x, y) and consists of alternating outer and inner points.

    Parameters:
      x (float): x-coordinate of the center (default 0).
      y (float): y-coordinate of the center (default 5).
      n (int): Number of star points (default 5).
      inner_radius (float): Radius for the inner vertices.
      outer_radius (float): Radius for the outer vertices.
      angle (float): Rotation angle (in degrees) for the first outer vertex.

    Returns:
      str: A string suitable for the "d" attribute in an SVG path element.
    """
    if n < 2:
        raise ValueError("n must be at least 2")
    _validate_non_negative(inner_radius, "inner_radius")
    _validate_positive(outer_radius, "outer_radius")

    # Convert the angle offset from degrees to radians.
    angle_offset = math.radians(angle)

    points: list[str] = []
    # There are 2*n vertices: the angular step between each vertex is pi/n.
    step = math.pi / n
    for i in range(2 * n):
        # Choose the radius based on whether this is an outer or inner vertex.
        r = outer_radius if i % 2 == 0 else inner_radius
        # Compute the current angle.
        a = angle_offset + i * step
        # Calculate the (x, y) coordinates for the vertex.
        px = x + r * math.cos(a)
        py = y + r * math.sin(a)
        # Format the coordinate to two decimal places.
        points.append(_format_point(px, py))

    # Build the SVG path string: move to the first point, draw lines to the rest, then close the path.
    d_string = "M " + " L ".join(points) + " Z"
    return d_string


def polyline(x_coords: Sequence[float], y_coords: Sequence[float]) -> str:
    """
    Returns a d-string for a polyline connecting the points specified by x_coords and y_coords.

    The path will start at the first coordinate and then draw lines to each subsequent coordinate.

    Parameters:
      x_coords (list or tuple of float): A sequence of x coordinates.
      y_coords (list or tuple of float): A sequence of y coordinates.

    Returns:
      str: A string suitable for the "d" attribute in an SVG path element.

    Raises:
      ValueError: If the lengths of x_coords and y_coords do not match.
    """
    if len(x_coords) != len(y_coords):
        raise ValueError("x_coords and y_coords must have the same length")
    if not x_coords:
        raise ValueError("x_coords and y_coords must contain at least one point")

    # Create a list of formatted point strings (with two decimal places).
    points = [_format_point(x, y) for x, y in zip(x_coords, y_coords)]

    # Build the SVG path string: move to the first point, then draw lines to the rest.
    d_string = "M " + " L ".join(points)
    return d_string


def cardinal_spline(
    points: Sequence[float] | Sequence[tuple[float, float]],
    tension: float = 0.0,
    closed: bool = False,
) -> str:
    """
    Generate an SVG path 'd' string for a cardinal spline
    through the given points, with adjustable 'tension'.

    This replicates the approach of D3’s 'cardinal' curve:
      - Each pair of adjacent points is joined by a cubic Bézier.
      - The two Bézier control points are computed based on 'tension'.
      - Tension=0 => classic cardinal; Tension=1 => straight lines.

    Parameters
    ----------
    points : list
        Either a flat list [x0, y0, x1, y1, ...] or a list of (x, y) pairs.
    tension : float
        A number in [0..1]. 0 => looser, 1 => no curvature.
    closed : bool
        Whether to close the spline (end connects back to start).

    Returns
    -------
    str
        An SVG path 'd' string, e.g. "M x0,y0 C c1x,c1y c2x,c2y x1,y1 ..."
    """
    # Normalize the input to a list of (float, float) pairs.
    xy: list[tuple[float, float]] = []
    if not points:
        return ""  # nothing to draw
    if not 0 <= tension <= 1:
        raise ValueError("tension must be between 0 and 1")

    first = points[0]
    if isinstance(first, (int, float)):
        if len(points) % 2 != 0:
            raise ValueError("flat points must contain an even number of values")
        # We're in the flat-list branch.
        flat_points = cast(Sequence[float], points)
        for i in range(0, len(flat_points), 2):
            xy.append((float(flat_points[i]), float(flat_points[i + 1])))
    elif isinstance(first, (tuple, list)) and len(first) == 2:
        # Input is already a list of (x, y) pairs.
        xy = [
            (float(x), float(y))
            for x, y in cast(Sequence[tuple[float, float]], points)
        ]
    else:
        raise ValueError(
            "points must be either flat [x0, y0, ...] or a list of (x, y) pairs"
        )

    n = len(xy)
    if n == 0:
        return ""
    if n == 1:
        # Single point: just move there.
        return f"M {xy[0][0]},{xy[0][1]}"
    if n == 2 and not closed:
        # Two points: draw a straight line.
        return f"M {xy[0][0]},{xy[0][1]} L {xy[1][0]},{xy[1][1]}"
    if closed and n < 3:
        raise ValueError("closed cardinal splines require at least 3 points")

    # k is the factor controlling the tangent lengths.
    # D3 uses k = (1 - tension) / 6 for its cardinal spline.
    k = (1 - tension) / 6

    d_parts: list[str] = []
    if closed:
        # CLOSED CARDINAL SPLINE
        d_parts.append(f"M {xy[0][0]},{xy[0][1]}")
        for i in range(n):
            p0 = xy[(i - 1) % n]  # previous
            p1 = xy[i % n]  # current
            p2 = xy[(i + 1) % n]  # next
            p3 = xy[(i + 2) % n]  # next-next

            # Compute control points.
            c1x = p1[0] + (p2[0] - p0[0]) * k
            c1y = p1[1] + (p2[1] - p0[1]) * k
            c2x = p2[0] - (p3[0] - p1[0]) * k
            c2y = p2[1] - (p3[1] - p1[1]) * k

            d_parts.append(f"C {c1x},{c1y} {c2x},{c2y} {p2[0]},{p2[1]}")
        d_parts.append("Z")
    else:
        # OPEN CARDINAL SPLINE
        # Create an extended list by duplicating the endpoints.
        e = [xy[0]] + xy + [xy[-1]]
        d_parts.append(f"M {e[1][0]},{e[1][1]}")
        for i in range(1, n):
            p0 = e[i - 1]
            p1 = e[i]
            p2 = e[i + 1]
            p3 = e[i + 2]

            c1x = p1[0] + (p2[0] - p0[0]) * k
            c1y = p1[1] + (p2[1] - p0[1]) * k
            c2x = p2[0] - (p3[0] - p1[0]) * k
            c2y = p2[1] - (p3[1] - p1[1]) * k

            d_parts.append(f"C {c1x},{c1y} {c2x},{c2y} {p2[0]},{p2[1]}")

    return " ".join(d_parts)


def polygon(x: float, y: float, radius: float, n: int, angle: float = 0) -> str:
    """
    Returns an SVG path d-string for a regular polygon with n sides,
    optionally rotated by a specified angle.

    The polygon is centered at (x, y) and inscribed in a circle with the
    given radius. The optional angle (in degrees) rotates the polygon around
    its center. By default, the first vertex is positioned at the top of the circle.

    Parameters:
      x (float): The x-coordinate of the polygon's center.
      y (float): The y-coordinate of the polygon's center.
      radius (float): The radius of the circle in which the polygon is inscribed.
      n (int): The number of sides (vertices) of the polygon.
      angle (float): The rotation angle in degrees (default is 0).

    Returns:
      str: A string suitable for the "d" attribute in an SVG <path> element.
    """
    if n < 3:
        raise ValueError("n must be at least 3")
    _validate_non_negative(radius, "radius")

    angle_offset = math.radians(angle)
    angle_step = 2 * math.pi / n
    points: list[str] = []
    for i in range(n):
        a = i * angle_step - math.pi / 2 + angle_offset
        sx = x + math.cos(a) * radius
        sy = y + math.sin(a) * radius
        points.append(_format_point(sx, sy))
    return "M " + " L ".join(points) + " Z"


def cross(
    x: float = 0, y: float = 0, *, size: float, thickness: float, angle: float = 0
) -> str:
    """
    Returns a d-string for a cross centered at (x, y) with a given size, thickness, and angle.

    The cross is constructed as the union of a vertical rectangle (of width = thickness and height = size)
    and a horizontal rectangle (of width = size and height = thickness). The resulting polygon has 12 vertices.

    Parameters:
      x (float): x-coordinate of the center (default 0).
      y (float): y-coordinate of the center (default 0).
      size (float): Total span of the cross (tip-to-tip).
      thickness (float): Thickness of the cross arms.
      angle (float): Rotation angle (in degrees) for the cross.

    Returns:
      str: A string suitable for the "d" attribute in an SVG path element.
    """
    _validate_positive(size, "size")
    _validate_positive(thickness, "thickness")
    if thickness > size:
        raise ValueError("thickness must be less than or equal to size")

    # Calculate half dimensions
    h = size / 2  # half-size: distance from center to tip
    t = thickness / 2  # half-thickness

    # Define the vertices of the cross polygon (without rotation and centered at (0,0)).
    # The points are defined in order to trace the outer boundary:
    # Starting from the left side of the top arm and moving clockwise.
    points = [
        (-t, h),  # top left of vertical bar
        (t, h),  # top right of vertical bar
        (t, t),  # inner top right (junction of vertical and horizontal)
        (h, t),  # right end of horizontal bar (top)
        (h, -t),  # right end of horizontal bar (bottom)
        (t, -t),  # inner bottom right (junction)
        (t, -h),  # bottom right of vertical bar
        (-t, -h),  # bottom left of vertical bar
        (-t, -t),  # inner bottom left (junction)
        (-h, -t),  # left end of horizontal bar (bottom)
        (-h, t),  # left end of horizontal bar (top)
        (-t, t),  # inner top left (junction)
    ]

    # Convert the rotation angle from degrees to radians.
    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    rotated_points: list[tuple[float, float]] = []
    for px, py in points:
        # Rotate the point by the given angle.
        rx = px * cos_a - py * sin_a
        ry = px * sin_a + py * cos_a
        # Translate to the desired center (x, y).
        rotated_points.append((rx + x, ry + y))

    # Construct the SVG path d-string: move to the first point, then draw lines to each subsequent point, and close the path.
    d_string = (
        "M " + " L ".join(_format_point(rx, ry) for rx, ry in rotated_points) + " Z"
    )
    return d_string


def arc(
    x: float = 0,
    y: float = 0,
    *,
    radius: float,
    start_angle: float = 0,
    end_angle: float = 360,
) -> str:
    """
    Returns a d-string for an arc (a circular path) centered at (x, y) with a given radius.
    The arc spans from start_angle to end_angle (in degrees). If the arc is a full circle,
    it is drawn using two arc segments.

    Parameters:
      x (float): x-coordinate of the center (default 0).
      y (float): y-coordinate of the center (default 0).
      radius (float): Radius of the arc.
      start_angle (float): Starting angle in degrees (default 0).
      end_angle (float): Ending angle in degrees (default 360).

    Returns:
      str: A string suitable for the "d" attribute in an SVG path element.
    """
    _validate_positive(radius, "radius")

    start_rad = math.radians(start_angle)
    end_rad = math.radians(end_angle)
    delta_deg, is_full_circle, sweep_flag = _arc_span(start_angle, end_angle)

    # Helper function to compute a point on the circle.
    def point(angle_rad: float) -> tuple[float, float]:
        return (x + radius * math.cos(angle_rad), y + radius * math.sin(angle_rad))

    start_point = point(start_rad)
    end_point = point(end_rad)

    if math.isclose(delta_deg, 0, abs_tol=_ANGLE_TOLERANCE):
        return f"M {_format_point(start_point[0], start_point[1])}"

    if is_full_circle:
        # For a full circle, we need to split the arc into two 180° segments.
        direction = 1 if sweep_flag == 1 else -1
        mid_point = point(start_rad + direction * math.pi)
        # Each arc segment is exactly 180° so the large_arc_flag is 0.
        d = (
            f"M {_format_point(start_point[0], start_point[1])} "
            f"A {radius:.2f} {radius:.2f} 0 0 {sweep_flag} {_format_point(mid_point[0], mid_point[1])} "
            f"A {radius:.2f} {radius:.2f} 0 0 {sweep_flag} {_format_point(start_point[0], start_point[1])}"
        )
    else:
        # For a partial arc, set the large_arc_flag based on the angular span.
        large_arc_flag = 1 if abs(delta_deg) > 180 else 0
        d = (
            f"M {_format_point(start_point[0], start_point[1])} "
            f"A {radius:.2f} {radius:.2f} 0 {large_arc_flag} {sweep_flag} {_format_point(end_point[0], end_point[1])}"
        )

    return d


def ring(
    x: float = 0,
    y: float = 0,
    *,
    inner_radius: float,
    outer_radius: float,
    start_angle: float = 0,
    end_angle: float = 360,
    without_inner: bool = False,
) -> str:
    """
    Returns an SVG path string for a ring (donut or ring segment) centered at (x, y)
    with the given inner and outer radii.

    For a full ring (360°) a complete donut is drawn (ignoring without_inner).

    For a partial ring (angle != 360°):
      - If without_inner is False, a full ring segment is drawn (outer arc,
        radial line from outer_end to inner_end, inner arc, and radial line back).
      - If without_inner is True, the inner arc is omitted. Instead a single closed path is drawn:
          1. Move to inner_start.
          2. Draw a radial line from inner_start to outer_start.
          3. Draw the outer arc from outer_start to outer_end.
          4. Draw a radial line from outer_end to inner_end.
          5. Close the path (which draws a chord from inner_end back to inner_start).
    """
    _validate_non_negative(inner_radius, "inner_radius")
    _validate_positive(outer_radius, "outer_radius")
    if inner_radius > outer_radius:
        raise ValueError("inner_radius must be less than or equal to outer_radius")

    start_rad = math.radians(start_angle)
    end_rad = math.radians(end_angle)
    delta_deg, is_full_circle, sweep_flag = _arc_span(start_angle, end_angle)
    inner_sweep_flag = 0 if sweep_flag == 1 else 1

    def point(r: float, angle: float) -> tuple[float, float]:
        return (x + r * math.cos(angle), y + r * math.sin(angle))

    outer_start = point(outer_radius, start_rad)
    outer_end = point(outer_radius, end_rad)
    inner_start = point(inner_radius, start_rad)
    inner_end = point(inner_radius, end_rad)

    if math.isclose(delta_deg, 0, abs_tol=_ANGLE_TOLERANCE):
        return ""

    if is_full_circle:
        direction = 1 if sweep_flag == 1 else -1
        mid_outer = point(outer_radius, start_rad + direction * math.pi)
        mid_inner = point(inner_radius, start_rad + direction * math.pi)
        d = (
            f"M {_format_point(outer_start[0], outer_start[1])} "
            f"A {outer_radius:.2f} {outer_radius:.2f} 0 0 {sweep_flag} {_format_point(mid_outer[0], mid_outer[1])} "
            f"A {outer_radius:.2f} {outer_radius:.2f} 0 0 {sweep_flag} {_format_point(outer_start[0], outer_start[1])} "
            f"M {_format_point(inner_end[0], inner_end[1])} "
            f"A {inner_radius:.2f} {inner_radius:.2f} 0 0 {inner_sweep_flag} {_format_point(mid_inner[0], mid_inner[1])} "
            f"A {inner_radius:.2f} {inner_radius:.2f} 0 0 {inner_sweep_flag} {_format_point(inner_start[0], inner_start[1])} Z"
        )
        return d

    large_arc_flag = 1 if abs(delta_deg) > 180 else 0

    if without_inner:
        d = (
            f"M {_format_point(inner_start[0], inner_start[1])} "
            f"L {_format_point(outer_start[0], outer_start[1])} "
            f"A {outer_radius:.2f} {outer_radius:.2f} 0 {large_arc_flag} {sweep_flag} {_format_point(outer_end[0], outer_end[1])} "
            f"L {_format_point(inner_end[0], inner_end[1])} Z"
        )
    else:
        d = (
            f"M {_format_point(outer_start[0], outer_start[1])} "
            f"A {outer_radius:.2f} {outer_radius:.2f} 0 {large_arc_flag} {sweep_flag} {_format_point(outer_end[0], outer_end[1])} "
            f"L {_format_point(inner_end[0], inner_end[1])} "
            f"A {inner_radius:.2f} {inner_radius:.2f} 0 {large_arc_flag} {inner_sweep_flag} {_format_point(inner_start[0], inner_start[1])} Z"
        )
    return d
