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

<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Shape</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>ARROW</code></td>
      <td><svg width="48" height="32" viewBox="0 0 10 10" aria-label="ARROW marker shape"><path d="M2.499 5 L1.565 1.7 L8.435 5 L1.565 8.3 Z" fill="currentColor"/></svg></td>
    </tr>
    <tr>
      <td><code>ARROW_BASIC</code></td>
      <td><svg width="48" height="32" viewBox="0 0 10 10" aria-label="ARROW_BASIC marker shape"><path d="M0 1.91 10 5 0 8.09V1.91Z" fill="currentColor"/></svg></td>
    </tr>
    <tr>
      <td><code>ARROW_CONCAVE</code></td>
      <td><svg width="48" height="32" viewBox="0 0 10 10" aria-label="ARROW_CONCAVE marker shape"><path d="M0 8.09a22.48 22.48 0 0 0 0-6.18C2.862 3.396 6.241 4.382 10 5c-3.759.618-7.138 1.604-10 3.09Z" fill="currentColor"/></svg></td>
    </tr>
    <tr>
      <td><code>ARROW_CONVEX</code></td>
      <td><svg width="48" height="32" viewBox="0 0 10 10" aria-label="ARROW_CONVEX marker shape"><path d="M.505 5 0 1.91C1.453 1.908 6.391 2.989 10 5 6.391 7.011 1.453 8.092 0 8.09L.505 5Z" fill="currentColor"/></svg></td>
    </tr>
    <tr>
      <td><code>ARROW_SIMPLE</code></td>
      <td><svg width="48" height="32" viewBox="0 0 10 10" aria-label="ARROW_SIMPLE marker shape"><path d="M3.596 5 .768 2.172 2.182.757 6.424 5 2.182 9.243.768 7.828 3.596 5Z" fill="currentColor"/></svg></td>
    </tr>
    <tr>
      <td><code>CROSS</code></td>
      <td><svg width="48" height="32" viewBox="0 0 10 10" aria-label="CROSS marker shape"><path d="M1.667 3.333L3.333 1.667L5 3.333L6.667 1.667L8.333 3.333L6.667 5L8.333 6.667L6.667 8.333L5 6.667L3.333 8.333L1.667 6.667L3.333 5L1.667 3.333Z" fill="currentColor"/></svg></td>
    </tr>
    <tr>
      <td><code>DIAMOND</code></td>
      <td><svg width="48" height="32" viewBox="0 0 10 10" aria-label="DIAMOND marker shape"><path d="M5 1.91 8.09 5 5 8.09 1.91 5 5 1.91Z" fill="currentColor"/></svg></td>
    </tr>
    <tr>
      <td><code>DOT</code></td>
      <td><svg width="48" height="32" viewBox="0 0 10 10" aria-label="DOT marker shape"><path d="M 9.09 5 A 4.09 4.09 0 1 0 0.91 5 A 4.09 4.09 0 1 0 9.09 5 Z" fill="currentColor"/></svg></td>
    </tr>
    <tr>
      <td><code>SQUARE</code></td>
      <td><svg width="48" height="32" viewBox="0 0 10 10" aria-label="SQUARE marker shape"><path d="M1.91 1.91h6.18v6.18H1.91z" fill="currentColor"/></svg></td>
    </tr>
    <tr>
      <td><code>TICK_BOTTOM</code></td>
      <td><svg width="48" height="32" viewBox="0 0 10 10" aria-label="TICK_BOTTOM marker shape"><path d="M4 5h2v5H4z" fill="currentColor"/></svg></td>
    </tr>
    <tr>
      <td><code>TICK_HORIZONTAL</code></td>
      <td><svg width="48" height="32" viewBox="0 0 10 10" aria-label="TICK_HORIZONTAL marker shape"><path d="M2.5 4h5v2h-5z" fill="currentColor"/></svg></td>
    </tr>
    <tr>
      <td><code>TICK_LEFT</code></td>
      <td><svg width="48" height="32" viewBox="0 0 10 10" aria-label="TICK_LEFT marker shape"><path d="M0 4h5v2H0z" fill="currentColor"/></svg></td>
    </tr>
    <tr>
      <td><code>TICK_RIGHT</code></td>
      <td><svg width="48" height="32" viewBox="0 0 10 10" aria-label="TICK_RIGHT marker shape"><path d="M5 4h5v2H5z" fill="currentColor"/></svg></td>
    </tr>
    <tr>
      <td><code>TICK_TOP</code></td>
      <td><svg width="48" height="32" viewBox="0 0 10 10" aria-label="TICK_TOP marker shape"><path d="M4 0h2v5H4z" fill="currentColor"/></svg></td>
    </tr>
    <tr>
      <td><code>TICK_VERTICAL</code></td>
      <td><svg width="48" height="32" viewBox="0 0 10 10" aria-label="TICK_VERTICAL marker shape"><path d="M4 2.5h2v5H4z" fill="currentColor"/></svg></td>
    </tr>
  </tbody>
</table>

Use them as the `d` argument for `Marker`.

```python
from pydreamplet.markers import ARROW_CONCAVE, Marker

marker = Marker("concave-arrow", ARROW_CONCAVE, 10, 10, fill="#14b8a6")
```

`Marker` is registered for the `"marker"` tag with `SvgElement.register()`, so
marker elements found through `SvgElement.find()` are wrapped as `Marker`
instances when possible.
