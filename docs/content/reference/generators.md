---
title: Path Generators
description: Reference for data-driven path generators exported from pydreamplet.
navigation:
  title: Path generators
category: reference
---

# Path Generators

Path generators convert data into SVG path `d` strings. Generator classes and
factory functions are exported from top-level `pydreamplet`.

```python
import pydreamplet as dp
```

## Visual Example

```python
import pydreamplet as dp

line = dp.LineGenerator(curve="catmull-rom")
area = dp.AreaGenerator(y0=lambda _item, _index: 150, curve="linear")
symbol = dp.SymbolGenerator(symbol=lambda item, _index: item["symbol"], size=180)

points = [(24, 130), (82, 54), (148, 96), (214, 34), (290, 88)]
symbols = [
    {"x": 52, "y": 146, "symbol": "circle"},
    {"x": 116, "y": 146, "symbol": "diamond"},
    {"x": 180, "y": 146, "symbol": "triangle"},
    {"x": 244, "y": 146, "symbol": "star"},
]

svg = dp.SVG(330, 180)
svg.append(dp.Path(area(points), fill="currentColor", opacity=0.16))
svg.append(dp.Path(line(points), fill="none", stroke="currentColor", stroke_width=4))

for item in symbols:
    svg.append(
        dp.Path(
            symbol(item),
            fill="currentColor",
            transform=f"translate({item['x']} {item['y']})",
        )
    )
```

::svg-preview{src="/showcase/ref_path_generators.svg" alt="Area, line, and symbol paths generated from data."}
::

## Curves

Line and area generators support these curve names:

| Curve | Notes |
| --- | --- |
| `"linear"` | Straight segments. |
| `"step"` | Horizontal-vertical step path. |
| `"basis"` | Smooth basis spline. |
| `"cardinal"` | Cardinal spline with `tension`. |
| `"catmull-rom"` | Catmull-Rom spline. |
| `"monotone-x"` | Monotone cubic interpolation in x. Open paths only. |
| `"monotone-y"` | Monotone cubic interpolation in y. Open paths only. |

## LineGenerator

```python
LineGenerator(
    *,
    x: Accessor[T] | None = None,
    y: Accessor[T] | None = None,
    defined: Callable[[T, int], bool] | None = None,
    curve: CurveName = "linear",
    tension: float = 0.0,
)
```

Default accessors read `item[0]` and `item[1]`. Undefined items split the path
into separate segments.

```python
generator = dp.LineGenerator()

assert generator([(0, 0), (10, 20), (30, 0)]) == (
    "M 0.00,0.00 L 10.00,20.00 L 30.00,0.00"
)
```

The factory function `dp.line_generator(**kwargs)` returns `LineGenerator`.

## AreaGenerator

```python
AreaGenerator(
    *,
    x0: Accessor[T] | None = None,
    x1: Accessor[T] | None = None,
    y0: Accessor[T] | None = None,
    y1: Accessor[T] | None = None,
    defined: Callable[[T, int], bool] | None = None,
    curve: CurveName = "linear",
    tension: float = 0.0,
)
```

Builds a closed path from upper points and lower points.

```python
area = dp.AreaGenerator(y0=lambda _item, _index: 10)

assert area([(0, 0), (10, 20), (30, 0)]).endswith("Z")
```

The factory function `dp.area_generator(**kwargs)` returns `AreaGenerator`.

## Radial Generators

```python
RadialLineGenerator(
    *,
    angle: Accessor[T],
    radius: Accessor[T],
    cx: Real = 0,
    cy: Real = 0,
    defined: Callable[[T, int], bool] | None = None,
    curve: CurveName = "linear",
    tension: float = 0.0,
)
```

```python
RadialAreaGenerator(
    *,
    angle: Accessor[T],
    inner_radius: Accessor[T],
    outer_radius: Accessor[T],
    cx: Real = 0,
    cy: Real = 0,
    defined: Callable[[T, int], bool] | None = None,
    curve: CurveName = "linear",
    tension: float = 0.0,
)
```

Angles are degrees. The factories are `dp.radial_line_generator()` and
`dp.radial_area_generator()`.

## PieGenerator and PieSlice

```python
PieGenerator(*, start_angle: Real = 0, end_angle: Real | None = None)
```

Calling a `PieGenerator` returns `list[PieSlice]`.

```python
@dataclass(frozen=True)
class PieSlice:
    value: float
    index: int
    start_angle: float
    end_angle: float
```

`PieSlice.angle` returns `end_angle - start_angle`. `PieSlice.mid_angle`
returns the midpoint angle.

```python
slices = dp.PieGenerator(start_angle=-90)([1, 2, 3])

assert slices[1].angle == 120
assert slices[1].mid_angle == 30
```

Values must be non-negative and include at least one positive value. The factory
function is `dp.pie_generator()`.

## ArcGenerator

```python
ArcGenerator(
    *,
    inner_radius: Accessor[T],
    outer_radius: Accessor[T],
    start_angle: Accessor[T],
    end_angle: Accessor[T],
    cx: Real = 0,
    cy: Real = 0,
)
```

Converts a datum, often a `PieSlice`, into a ring-sector path string.

```python
arc = dp.ArcGenerator(
    inner_radius=lambda _item, _index: 20,
    outer_radius=lambda _item, _index: 48,
    start_angle=lambda item, _index: item.start_angle,
    end_angle=lambda item, _index: item.end_angle,
)
```

The factory function is `dp.arc_generator()`.

## SymbolGenerator

```python
SymbolGenerator(
    *,
    symbol: Callable[[T, int], SymbolName] | SymbolName = "circle",
    size: Accessor[T] | Real = 64,
)
```

Supported symbols are `"circle"`, `"square"`, `"diamond"`, `"triangle"`,
`"cross"`, and `"star"`. `size` is interpreted as area-like input.

The factory function is `dp.symbol_generator()`.

## LinkGenerator

```python
LinkGenerator(
    *,
    source: PointAccessor[T],
    target: PointAccessor[T],
    curve: LinkCurve = "horizontal",
)
```

Supported link curves are `"linear"`, `"horizontal"`, and `"vertical"`.

```python
link = dp.LinkGenerator(
    source=lambda item, _index: item["source"],
    target=lambda item, _index: item["target"],
)

d = link({"source": (0, 10), "target": (100, 50)})
```

The factory function is `dp.link_generator()`.
