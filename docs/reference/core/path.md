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

Builds SVG path data with chainable absolute path commands.

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
- `line_to(x, y)`
- `horizontal_to(x)`
- `vertical_to(y)`
- `curve_to(x1, y1, x2, y2, x, y)`
- `smooth_curve_to(x2, y2, x, y)`
- `quadratic_to(x1, y1, x, y)`
- `smooth_quadratic_to(x, y)`
- `arc_to(rx, ry, x_axis_rotation, large_arc, sweep, x, y)`
- `close()`
- `to_string()`

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
