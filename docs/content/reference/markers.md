---
title: Markers
description: SVG marker definitions and predefined marker path constants.
navigation:
  title: Markers
category: reference
---

# Markers

The `pydreamplet.markers` module provides `Marker`, a reusable SVG `<marker>`
wrapper, plus predefined path data constants for arrows, ticks, and simple
symbols.

Markers are imported from `pydreamplet.markers`.

```python
from pydreamplet.markers import ARROW_BASIC, Marker
```

## Visual Example

Create markers inside `Defs`, then reference them from a line or path with
`marker_start`, `marker_mid`, or `marker_end`.

```python
import pydreamplet as dp
from pydreamplet.markers import ARROW_BASIC, DOT, Marker

svg = dp.SVG(300, 130)

defs = dp.Defs()
arrow = Marker("arrow-head", ARROW_BASIC, 10, 10, fill="#14b8a6", orient="auto")
dot = Marker("dot-start", DOT, 8, 8, fill="#f83898")
defs.append(arrow, dot)
svg.append(defs)

line = dp.Line(
    38,
    76,
    252,
    76,
    stroke="currentColor",
    stroke_width=3,
    stroke_linecap="round",
)
line.marker_start = dot.id_ref
line.marker_end = arrow.id_ref

svg.append(
    line,
    dp.Text("marker_start", x=38, y=48, font_size=12, text_anchor="middle", fill="currentColor"),
    dp.Text("marker_end", x=252, y=48, font_size=12, text_anchor="middle", fill="currentColor"),
    dp.Text("Marker(...).id_ref", x=92, y=108, font_size=12, fill="currentColor"),
)
```

::svg-preview{src="/showcase/ref_markers_line.svg" alt="A line with a dot marker at the start and an arrow marker at the end."}
::

## Marker

```python
Marker(
    id: str,
    d: str,
    width: Real,
    height: Real,
    **kwargs: Any,
)
```

`Marker` creates a `<marker>` element with `id`, `markerWidth`,
`markerHeight`, `viewBox="0 0 10 10"`, `refX`, `refY`, and `orient` attributes.
It also creates one nested `Path` whose `d` is the supplied marker shape.

Supported `kwargs` include:

- `refX`, default `"5"`
- `refY`, default `"5"`
- `orient`, default `"0"`
- `fill`, default `"#000000"` for the nested marker path
- `stroke`, default `"none"` for the nested marker path
- `stroke-width`, default `"1"` for the nested marker path

Because `stroke-width` is not a valid Python keyword, pass it with dictionary
expansion when constructing a marker.

```python
marker = Marker(
    "outlined-arrow",
    ARROW_BASIC,
    10,
    10,
    fill="none",
    stroke="currentColor",
    **{"stroke-width": "1.5"},
)
```

## Properties

```python
marker.d -> str
marker.d = ARROW_CONVEX
```

Gets or replaces the nested marker path data.

```python
marker.fill -> str | None
marker.fill = "#14b8a6"
```

Gets or sets the nested path fill.

```python
marker.stroke -> str | None
marker.stroke = "currentColor"
```

Gets or sets the nested path stroke.

```python
marker.stroke_width -> Real | None
marker.stroke_width = "2"
```

Gets or sets the nested path stroke width. The getter returns the parsed numeric
value from the underlying `Path`.

```python
marker.id_ref -> str
```

Returns `url(#<id>)`, suitable for assigning to `marker_start`, `marker_mid`, or
`marker_end`.

```python
marker = Marker("arrow", ARROW_BASIC, 10, 10)

assert marker.id_ref == "url(#arrow)"
```

## Predefined Paths

The module exports these path data constants:

- `ARROW`
- `ARROW_BASIC`
- `ARROW_CONCAVE`
- `ARROW_CONVEX`
- `ARROW_SIMPLE`
- `CROSS`
- `DIAMOND`
- `DOT`
- `SQUARE`
- `TICK_BOTTOM`
- `TICK_HORIZONTAL`
- `TICK_LEFT`
- `TICK_RIGHT`
- `TICK_TOP`
- `TICK_VERTICAL`

Use them as the `d` argument for `Marker`.

```python
from pydreamplet.markers import ARROW_CONCAVE, Marker

marker = Marker("concave-arrow", ARROW_CONCAVE, 10, 10, fill="#14b8a6")
```

`Marker` is registered for the `"marker"` tag with `SvgElement.register()`, so
marker elements found through `SvgElement.find()` are wrapped as `Marker`
instances when possible.
