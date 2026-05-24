# `Path`

The `Path` class represents an SVG path element. It allows you to set the path data and provides computed properties based on the coordinates within the path.

!!! info

    This class inherits from [**`SvgElement`**](svgelement.md).

## <span class=class></span>`pydreamplet.core.Path`

<!--skip-->
<!--skip-->
```py
Path(d: str | PathBuilder = "", **kwargs)
```

Initializes a new path with an optional d attribute containing path commands.

<span class="param">**Parameters**</span>

- `d` *(str or PathBuilder, optional)*: The path data string or a path builder.
- `**kwargs`: Additional attributes for the path element.

<!--skip-->
```py
from pydreamplet import SVG, Path
from pydreamplet.shapes import star

svg = SVG(200, 200)
svg.append(
    Path(
        d=star(svg.w / 2, svg.h / 2, inner_radius=30, outer_radius=80, angle=-18),
        fill="#a00344",
    )
)
```

![Example](assets/path_example.svg){.img-light-dark-bg}

## <span class=class></span>`pydreamplet.path_data.PathBuilder`

<!--skip-->
```py
PathBuilder()
```

Builds SVG path data with chainable path commands. Absolute methods use the `_to` suffix; relative methods use the `_by` suffix.

```py
import pydreamplet as dp

path_data = (
    dp.PathBuilder()
    .move_to(10, 20)
    .line_to(110, 20)
    .line_to(110, 70)
    .close()
)

path = dp.Path(path_data, fill="none")
```

Supported methods:

- `move_to(x, y)`
- `move_by(dx, dy)`
- `line_to(x, y)`
- `line_by(dx, dy)`
- `horizontal_to(x)`
- `horizontal_by(dx)`
- `vertical_to(y)`
- `vertical_by(dy)`
- `curve_to(x1, y1, x2, y2, x, y)`
- `curve_by(dx1, dy1, dx2, dy2, dx, dy)`
- `smooth_curve_to(x2, y2, x, y)`
- `smooth_curve_by(dx2, dy2, dx, dy)`
- `quadratic_to(x1, y1, x, y)`
- `quadratic_by(dx1, dy1, dx, dy)`
- `smooth_quadratic_to(x, y)`
- `smooth_quadratic_by(dx, dy)`
- `arc_to(rx, ry, x_axis_rotation, large_arc, sweep, x, y)`
- `arc_by(rx, ry, x_axis_rotation, large_arc, sweep, dx, dy)`
- `close()`
- `to_string()`

## Path parsing and normalization

<!--skip-->
```py
parse_path_data(path_data: str) -> list[PathCommand]
normalize_path_commands(path_data: str) -> list[PathCommand]
normalize_path_data(path_data: str) -> str
iter_path_segments(path_data: str) -> list[PathSegment]
path_length(path_data: str) -> float
point_at_length(path_data: str, distance) -> Vector
tangent_at_length(path_data: str, distance) -> Vector
```

`parse_path_data()` parses an SVG path `d` string into structured `PathCommand` objects. It preserves relative commands and expands repeated coordinate groups into explicit commands.

`normalize_path_commands()` converts relative commands to absolute commands while preserving command types such as `H`, `V`, `C`, `Q`, and `A`.

`normalize_path_data()` returns the normalized commands as an SVG path string.

```py
import pydreamplet as dp

normalized = dp.normalize_path_data("M10 20 l100 0 v50 h-100 Z")
print(normalized)  # M10 20 L110 20 V70 H10 Z
```

The first measurement utilities support linear commands: `M`, `L`, `H`, `V`, and `Z`. Curves and arcs raise `ValueError` for now instead of returning an approximate result.

```py
import pydreamplet as dp

path = dp.Path("M0 0 L10 0 L10 10")
print(path.length)        # 20.0
print(path.point_at(15))  # Vector(x=10.0, y=5.0)
print(path.tangent_at(15))  # Vector(x=0.0, y=1.0)
```

`Path` exposes `length`, `point_at(distance)`, and `tangent_at(distance)` convenience APIs backed by the path measurement functions.

### <span class="prop"></span>`bbox`

Returns a `BoundingBox` for paths made from linear commands (`M`, `L`, `H`, `V`,
`Z`), Bezier commands (`C`, `S`, `Q`, `T`), and arc commands (`A`). Curve and arc
bounds are computed from geometric extrema, not just control points or endpoints.

```py
import pydreamplet as dp

path = dp.Path("M10 20 h100 v50 h-100 z")
print(path.bbox)  # BoundingBox(x=10.0, y=20.0, width=100.0, height=50.0)
```

### <span class="prop"></span>`d`

**Getter:** Returns the path data string.

**Setter:** Updates the path data.

<!--skip-->
<!--skip-->
```py
print(path.d)
path.d = "M0 0 L50 50"
```

### <span class="prop"></span>`w`

Returns the width of the path based on the extracted coordinates.

### <span class="prop"></span>`h`

Returns the height of the path based on the extracted coordinates.

### <span class="prop"></span>`center`

Returns the center point of the path as a [`Vector`](../math/vector.md).
