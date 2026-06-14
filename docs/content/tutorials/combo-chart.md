---
title: Revenue and Stock Price Combo Chart
description: Build a dual-axis SVG chart with annual revenue bars, a monthly stock price curve, gradients, clipping, custom ticks, and embedded icons.
navigation:
  title: Revenue and stock price
category: tutorials
---

# Revenue and Stock Price Combo Chart

This tutorial builds a dual-axis combination chart with Python and
pyDreamplet. Annual revenue is shown as blue columns, while monthly stock
prices form a smooth green line. The translucent area below the line is visible
only inside the columns.

The visual treatment was inspired by one of the charts published by Visual
Capitalist.

::svg-preview{src="/showcase/combo_chart_light.svg" dark-src="/showcase/combo_chart_dark.svg" alt="Apple annual revenue columns combined with a monthly stock price line from 2014 through 2025."}
::

## What You Will Learn

By the end of the tutorial, you will know how to:

- read two time series with different frequencies from one CSV file,
- use a `BandScale` for annual columns and a `PointScale` for monthly values,
- plot two measures with independent vertical scales,
- reuse geometry with SVG `<defs>` and `<use>`,
- clip an area chart to the shape of the revenue columns,
- create ticks, grid lines, labels, gradients, and embedded SVG icons,
- generate light and dark versions from the same drawing code.

## Project Setup

This tutorial requires Python 3.12 or newer and pyDreamplet:

```bash
pip install pydreamplet
```

Create the following directory structure:

```text
combo-chart/
├── assets/
│   ├── revenue.svg
│   └── stock_price.svg
├── data/
│   └── apple.csv
├── data_reader.py
└── main.py
```

The complete data and icon files are available in the
[combo chart showcase directory](https://github.com/marepilc/pydreamplet-showcase/tree/master/scripts/combo_chart).

The CSV combines monthly closing prices with annual revenue records:

```csv
date,monthly_close,fiscal_year,annual_revenue
2014-01-31,12.094000,,
2014-02-28,16.320667,,
2014-12-31,14.827333,2014,3198356000
```

Most rows contain only a monthly price. The row that closes a fiscal year also
contains its year and annual revenue. Keeping the values in one file makes the
example easy to distribute, while the reader still separates them into two
clean series.

> The bundled CSV is suitable for reproducing this example. For a production
> chart, document the source, adjustment method, reporting currency, and update
> date of your financial data.

## Read and Structure the Data

Create `data_reader.py`. Small frozen dataclasses give every value a clear name
and prevent accidental changes after loading.

```python
import csv
from dataclasses import dataclass
from datetime import date
from pathlib import Path


@dataclass(frozen=True, slots=True)
class StockDataPoint:
    date: date
    close: float


@dataclass(frozen=True, slots=True)
class AnnualRevenue:
    fiscal_year: int
    period_end: date
    revenue: int


@dataclass(frozen=True, slots=True)
class ComboChartData:
    monthly_prices: list[StockDataPoint]
    annual_revenue: list[AnnualRevenue]


def read_combo_chart_data(csv_path: Path) -> ComboChartData:
    monthly_prices: list[StockDataPoint] = []
    annual_revenue: list[AnnualRevenue] = []

    with csv_path.open(newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            row_date = date.fromisoformat(row["date"])

            if row["monthly_close"]:
                monthly_prices.append(
                    StockDataPoint(
                        date=row_date,
                        close=float(row["monthly_close"]),
                    )
                )

            if row["annual_revenue"]:
                annual_revenue.append(
                    AnnualRevenue(
                        fiscal_year=int(row["fiscal_year"]),
                        period_end=row_date,
                        revenue=int(row["annual_revenue"]),
                    )
                )

    if not monthly_prices or not annual_revenue:
        raise ValueError("The CSV must contain price and revenue data")

    return ComboChartData(
        monthly_prices=monthly_prices,
        annual_revenue=annual_revenue,
    )
```

The two `if` statements are independent because one CSV row may contain both a
monthly price and an annual revenue value.

## Create the Canvas

Start `main.py` with the imports, file paths, theme, and canvas:

```python
from pathlib import Path

import pydreamplet as dp
from pydreamplet.markers import TICK_BOTTOM, Marker
from pydreamplet.utils import calculate_ticks

from data_reader import read_combo_chart_data


BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "data" / "apple.csv"
OUTPUT_PATH = BASE_DIR / "apple_combo_chart.svg"

theme = dp.Theme()
data = read_combo_chart_data(DATA_PATH)

svg = dp.SVG(
    1024,
    680,
    font_family=theme.font_family,
    font_size=theme.font_size,
)

margin = {"left": 88, "right": 88, "top": 112, "bottom": 72}
plot_left = margin["left"]
plot_right = svg.w - margin["right"]
plot_top = margin["top"]
plot_bottom = svg.h - margin["bottom"]
```

The larger top margin leaves room for the title and legend-like icon labels.
The left and right margins reserve space for two independent vertical axes.

## Add the Title

The chart title is centered in the header area rather than inside the plotting
rectangle:

```python
svg.append(
    dp.Text(
        "Apple",
        pos=(svg.w / 2, margin["top"] / 2),
        text_anchor="middle",
        font_size=32,
        fill=theme.ink,
        font_weight=600,
    )
)
```

## Build the Revenue Scales

Revenue has one value per fiscal year. A `BandScale` assigns each year a
horizontal band and exposes the computed column width through `bandwidth`.
A `LinearScale` maps revenue from zero to the tallest column.

```python
revenue_years = [item.fiscal_year for item in data.annual_revenue]
revenue_values = [item.revenue for item in data.annual_revenue]
max_revenue = max(revenue_values)

x_revenue_scale = dp.BandScale(
    revenue_years,
    (plot_left, plot_right),
)
y_revenue_scale = dp.LinearScale(
    (0, max_revenue),
    (plot_bottom, plot_top),
)
```

The vertical output range is reversed. In SVG, `y=0` is at the top, so larger
data values must map to smaller screen coordinates.

## Define the Columns Once

The same column geometry serves two purposes:

1. it draws the blue revenue columns,
2. it becomes a clipping path for the green area.

Create both definitions in one loop:

```python
defs = svg.ensure_defs()

revenue_shape = dp.G(id="revenue-shape")
revenue_clip = dp.ClipPath(id="revenue-clip")

for year, revenue in zip(revenue_years, revenue_values, strict=True):
    x = x_revenue_scale.map(year)
    y = y_revenue_scale.map(revenue)
    height = plot_bottom - y

    column = dp.Rect(
        pos=(x, y),
        width=x_revenue_scale.bandwidth,
        height=height,
    )
    revenue_shape.append(column)

    revenue_clip.append(
        dp.Rect(
            pos=(x, y),
            width=x_revenue_scale.bandwidth,
            height=height,
        )
    )

defs.append(revenue_shape, revenue_clip)
```

An SVG element cannot have two parents, which is why the clipping path receives
its own rectangles instead of reusing the same Python objects.

The visible columns can now reference the group with `<use>`:

```python
revenue_layer = dp.G().append(
    dp.Use(revenue_shape, fill=theme.blue)
)
```

This keeps the generated SVG easier to inspect and makes the relationship
between the visible bars and clipping geometry explicit.

## Add the Area Gradient

The stock area fades vertically from opaque green to a lighter transparent
green:

```python
area_gradient = dp.LinearGradient(
    id="area-gradient",
    x1=0,
    y1=plot_top,
    x2=0,
    y2=plot_bottom,
)
area_gradient.attrs({"gradientUnits": "userSpaceOnUse"})
area_gradient.add_stop("0%", theme.lime, 1)
area_gradient.add_stop("100%", theme.lime, 0.25)
defs.append(area_gradient)
```

`gradientUnits="userSpaceOnUse"` makes the gradient follow the chart's
coordinate system. Without it, SVG would calculate the gradient relative to
the bounding box of each painted shape.

## Draw the Stock Price Series

Monthly prices need a denser horizontal scale. Converting dates to ordinal
integers gives `PointScale` simple, ordered domain values:

```python
stock_months = [item.date.toordinal() for item in data.monthly_prices]
stock_values = [item.close for item in data.monthly_prices]

stock_x_scale = dp.PointScale(
    stock_months,
    (plot_left, plot_right),
)
stock_y_scale = dp.LinearScale(
    (0, max(stock_values)),
    (plot_bottom, plot_top),
)
```

The revenue and stock series intentionally use different vertical scales.
Their units and magnitudes are unrelated: revenue is measured in billions of
dollars, while the share price is measured in dollars per share.

Build the monthly points:

```python
stock_points: list[tuple[float, float]] = []

for month, value in zip(stock_months, stock_values, strict=True):
    x = stock_x_scale.map(month)
    assert x is not None
    stock_points.append((x, stock_y_scale.map(value)))
```

`PointScale.map()` returns `None` for a value outside its domain. Every month in
this loop came from that domain, so the assertion documents a valid invariant
and helps static type checkers.

Generate a smooth line and a matching area:

```python
line_generator = dp.LineGenerator(curve="basis")
area_generator = dp.AreaGenerator(
    y0=lambda _point, _index: plot_bottom,
    curve="basis",
)

line_path = line_generator(stock_points)
area_path = area_generator(stock_points)

stock_layer = dp.G().append(
    dp.Path(
        d=area_path,
        fill="url(#area-gradient)",
        stroke=theme.transparent,
        clip_path="url(#revenue-clip)",
    ),
    dp.Path(
        d=line_path,
        fill=theme.transparent,
        stroke=dp.tone(theme.green, -0.5),
        stroke_width=3,
    ),
)
```

The area exists across the whole plotting region, but
`clip_path="url(#revenue-clip)"` reveals it only where it overlaps a revenue
column. The line is not clipped, so it remains readable between columns.

## Draw the Horizontal Axis

Create a separate group for axes and grid lines:

```python
axis_layer = dp.G()
axis_y = plot_bottom

axis_layer.append(
    dp.Line(
        x1=plot_left,
        y1=axis_y,
        x2=plot_right,
        y2=axis_y,
        stroke=theme.ink,
    )
)
```

Place one tick at the center of each revenue band:

```python
year_x_values = [
    x_revenue_scale.map(year) + x_revenue_scale.bandwidth / 2
    for year in revenue_years
]

tick_points = [
    coordinate
    for x in year_x_values
    for coordinate in (x, axis_y)
]

tick_path = dp.Polyline(
    tick_points,
    stroke="none",
    fill="none",
)
axis_layer.append(tick_path)

bottom_tick = Marker(
    "bottom-tick",
    TICK_BOTTOM,
    10,
    10,
    fill=theme.ink,
)
defs.append(bottom_tick)

tick_path.marker_start = bottom_tick.url
tick_path.marker_mid = bottom_tick.url
tick_path.marker_end = bottom_tick.url
```

A marker avoids drawing a separate short line for every tick. The invisible
polyline supplies the positions, and SVG repeats the marker at every point.

Add the year labels:

```python
for year, x in zip(revenue_years, year_x_values, strict=True):
    axis_layer.append(
        dp.Text(
            str(year),
            x=x,
            y=axis_y + 30,
            text_anchor="middle",
            font_size=12,
            fill=theme.ink,
        )
    )
```

## Add the Revenue Axis and Grid

The left axis uses blue labels to connect it visually to the revenue columns:

```python
for tick in calculate_ticks(0, max_revenue, 5):
    y = y_revenue_scale.map(tick)
    axis_layer.append(
        dp.Line(
            x1=plot_left,
            y1=y,
            x2=plot_right,
            y2=y,
            stroke=theme.ink,
            opacity=0.15,
        ),
        dp.Text(
            f"${tick / 1_000_000_000:.0f}B",
            x=plot_left - 10,
            y=y,
            text_anchor="end",
            dominant_baseline="middle",
            font_size=12,
            fill=theme.blue,
        ),
    )
```

`calculate_ticks()` chooses readable values across the requested range. Dividing
by one billion keeps labels such as `$20B` compact.

## Add the Stock Price Axis

The right axis uses the stock scale and green labels. It does not need another
set of grid lines because those would imply that the two vertical scales share
the same intervals.

```python
for tick in calculate_ticks(0, max(stock_values), 5):
    y = stock_y_scale.map(tick)
    axis_layer.append(
        dp.Text(
            f"${tick:.0f}",
            x=plot_right + 10,
            y=y,
            dominant_baseline="middle",
            font_size=12,
            fill=theme.green,
        )
    )
```

Color is doing useful work here: blue belongs to revenue, green belongs to
stock price. This is especially important in a dual-axis chart, where readers
must quickly identify which scale belongs to which series.

## Add the Icon Labels

The two small illustrations are ordinary SVG files loaded into the main SVG.
The helper recolors selected paths so the icons follow the active theme:

```python
def icon_label(
    filename: str,
    label: str,
    color: str,
    pos: tuple[float, float],
    text_x: float,
    text_anchor: str = "start",
) -> dp.G:
    icon = dp.SVG.from_file(str(BASE_DIR / "assets" / filename))

    # Nested SVG elements need explicit dimensions. Without them, browsers use
    # the SVG default of 300 by 150 pixels.
    icon.attrs({"width": 60, "height": 40})

    icon.find("path", id="background").fill = dp.tone(theme.surface, 0.1)
    icon.find("path", id="background-strips").fill = dp.tone(
        theme.surface,
        0.15,
    )
    icon.find("path", id="frame").fill = color
    icon.find("path", id="chart").fill = color

    return dp.G(pos=pos).append(
        icon,
        dp.Text(
            label,
            x=text_x,
            y=30,
            fill=color,
            font_size=22,
            text_anchor=text_anchor,
        ),
    )
```

Explicit `width` and `height` are essential for nested `<svg>` elements. A
`viewBox` controls the internal coordinate system, but it does not by itself
set the element's rendered size.

## Assemble and Save the Chart

Append the layers in visual order:

```python
svg.append(
    axis_layer,
    revenue_layer,
    stock_layer,
)

svg.append(
    icon_label(
        "revenue.svg",
        "Total Revenue",
        theme.blue,
        (30, 40),
        70,
    ),
    icon_label(
        "stock_price.svg",
        "Stock Price",
        theme.green,
        (svg.w - 90, 40),
        -10,
        "end",
    ),
)

svg.save(str(OUTPUT_PATH))
```

The axes are appended first, the columns second, and the stock layer last. This
keeps the stock line visible above the columns while the subtle grid remains in
the background.

Run the script:

```bash
python main.py
```

The generated file is `apple_combo_chart.svg`.

## Generate a Dark Version

The showcase uses pyDreamplet theme files to generate light and dark variants.
The drawing code does not need to change; only the theme does:

```python
theme = dp.Theme("path/to/dark-theme.json")
```

All important colors come from `theme`, including the canvas text, series
colors, icon fills, and grid lines. Keeping literal colors out of the drawing
logic makes theme variants predictable.

## Why This Chart Works

Combination charts can become confusing quickly. This design stays readable
because it follows a few constraints:

- each measure has a distinct mark: columns for revenue and a line for price,
- each vertical axis uses the same color as its series,
- only the revenue scale produces grid lines,
- annual and monthly data use independent horizontal scales over the same plot,
- the clipped gradient connects the two series without hiding the columns,
- the title and series labels sit outside the data region.

The chart compares patterns, not equivalent quantities. A rise in both series
does not prove that revenue caused a stock-price movement. The dual axes help
fit two histories into one graphic, but they should not be used to imply a
mathematical relationship.

## Next Steps

The complete showcase version supports Apple, Amazon, Microsoft, Nvidia, and
Tesla. To extend this tutorial:

1. add another CSV file with the same columns,
2. pass its path to `read_combo_chart_data()`,
3. change the title and output filename,
4. keep the symbol explicit when reproducible output matters.

You can also replace the local CSV reader with an API or database query. Keep
the `ComboChartData` structure unchanged and the drawing code will not need to
know where the values came from.

The complete source is available in the
[pyDreamplet showcase repository](https://github.com/marepilc/pydreamplet-showcase/tree/master/scripts/combo_chart).
