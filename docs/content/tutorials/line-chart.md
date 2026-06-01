---
title: Line Chart
description: Build a multi-series line chart with pyDreamplet scales, noise, markers, and labels.
navigation:
  title: Line chart
category: tutorials
---

# Line Chart

This tutorial creates a multi-series line chart from generated data. It uses
`Noise` for smooth fake values, scales for positioning, markers for ticks, and
utility functions for label and tick placement.

The data setup uses optional packages:

```bash
pip install polars pendulum
```

## Imports

```python
import pendulum
import polars as pl
import pydreamplet as dp

from pydreamplet.colors import generate_colors
from pydreamplet.markers import Marker, TICK_BOTTOM
from pydreamplet.noise import Noise
from pydreamplet.scales import LinearScale, PointScale
from pydreamplet.utils import calculate_ticks, force_distance, sample_uniform
```

## Generate Data

```python
products = ["bicycle", "apple", "ham", "spoon", "boat", "starship"]

data = {}
for index, product in enumerate(products):
    noise = Noise(0, 250, 0.1, seed=index + 1)
    data[product] = [noise.int_value for _ in range(100)]

start_date = pendulum.date(2024, 7, 1)
end_date = start_date.add(days=99)

df = pl.DataFrame(data).with_columns(
    date=pl.date_range(start_date, end_date, interval="1d", eager=True)
).select(["date", *products])
```

## Canvas and Scales

`PointScale.map()` returns `float | None` because a requested domain value may
be missing. Here every date comes from the scale domain, so the assertion is
both valid and useful for type checkers.

```python
svg = dp.SVG(800, 400)
defs = svg.ensure_defs()
axis_layer = dp.G()
svg.append(axis_layer)

margin = {"left": 50, "right": 105, "top": 18, "bottom": 50}
dates = df["date"].to_list()

min_value = df.select(products).min_horizontal().min()
max_value = df.select(products).max_horizontal().max()

scale_x = PointScale(dates, (margin["left"], svg.w - margin["right"]))
scale_y = LinearScale((min_value, max_value), (svg.h - margin["bottom"], margin["top"]))

x_values = []
for date in dates:
    x = scale_x.map(date)
    assert x is not None
    x_values.append(x)
```

## Draw the Series

```python
colors = generate_colors("#cc340c", len(products))
last_points_y = []

for i, product in enumerate(products):
    points = []
    for j, value in enumerate(df[product].to_list()):
        points.extend([x_values[j], scale_y.map(value)])

    svg.append(
        dp.Polyline(
            points,
            stroke=colors[i],
            stroke_width=2,
            fill="none",
        )
    )
    last_points_y.append(points[-1])
```

::svg-preview{src="/showcase/tutorial_line_chart_lines.svg" alt="Multi-series line chart before axes and labels are added."}
::

## Labels and Axes

Use `force_distance()` to spread labels near the final data points. Use
`sample_uniform()` to pick a small number of date ticks from the full domain.

```python
label_y_positions = force_distance(last_points_y, 16)

for i, product in enumerate(products):
    svg.append(
        dp.Text(
            product,
            x=x_values[-1] + 8,
            y=label_y_positions[i] + 5,
            font_size=14,
            fill=colors[i],
        )
    )

axis_y = scale_y.output_range[0]
axis_layer.append(
    dp.Line(
        x1=margin["left"],
        y1=axis_y,
        x2=svg.w - margin["right"],
        y2=axis_y,
        stroke="currentColor",
        stroke_width=1,
    )
)

tick_indices = sample_uniform(scale_x.domain, 5, None)
tick_points = []
for index in tick_indices:
    tick_points.extend([x_values[index], axis_y])

tick_path = dp.Polyline(tick_points, stroke="none", fill="none")
axis_layer.append(tick_path)

marker = Marker("bottom-tick", TICK_BOTTOM, 10, 10, fill="currentColor")
defs.append(marker)
tick_path.marker_start = marker.id_ref
tick_path.marker_mid = marker.id_ref
tick_path.marker_end = marker.id_ref

for index in tick_indices:
    tick_date = pendulum.instance(dates[index])
    axis_layer.append(
        dp.Text(
            tick_date.format("D MMM 'YY"),
            x=x_values[index],
            y=axis_y + 30,
            font_size=13,
            fill="currentColor",
            text_anchor="middle",
        )
    )
```

## Grid Lines

```python
for tick in calculate_ticks(min_value, max_value, 5):
    y = scale_y.map(tick)
    axis_layer.append(
        dp.Line(
            x1=margin["left"],
            y1=y,
            x2=svg.w - margin["right"],
            y2=y,
            stroke="currentColor",
            opacity=0.18,
        )
    )
    axis_layer.append(
        dp.Text(
            str(tick),
            x=margin["left"] - 10,
            y=y + 4,
            font_size=13,
            fill="currentColor",
            text_anchor="end",
        )
    )

svg.save("line-chart.svg")
```

::svg-preview{src="/showcase/tutorial_line_chart_final.svg" alt="Final line chart with axes, labels, ticks, and grid lines."}
::

