import random

import pydreamplet as dp
from data_reader import COMPANY_FILES, get_combo_chart_data
from pydreamplet.markers import TICK_BOTTOM, Marker
from pydreamplet.utils import calculate_ticks

from tools.runtime import (
    get_example_dir,
    get_example_name,
    get_motive,
    get_motive_path,
    get_output_path,
)

motive = get_motive()
theme = dp.Theme(get_motive_path(motive)) if motive else dp.Theme()


def icon_label(
    filename: str,
    label: str,
    color: str,
    pos: tuple[float, float],
    text_x: float,
    text_anchor: str = "start",
) -> dp.G:
    icon = dp.SVG.from_file(str(get_example_dir() / "assets" / filename))
    icon.find("path", id="background").fill = dp.tone(theme.surface, 0.1)
    icon.find("path", id="background-strips").fill = dp.tone(theme.surface, 0.15)
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


svg = dp.SVG(
    1024,
    680,
    font_family=theme.font_family,
    font_size=theme.font_size,
)

margin = {"left": 88, "right": 88, "top": 112, "bottom": 72}

symbol = random.choice(list(COMPANY_FILES.keys()))
company_name = COMPANY_FILES[symbol].removesuffix(".csv").title()
data = get_combo_chart_data(symbol)

max_revenue = max(item.revenue for item in data.annual_revenue)

# header
svg.append(
    dp.Text(
        company_name,
        pos=(svg.w / 2, margin["top"] / 2),
        text_anchor="middle",
        font_size=32,
        fill=theme.ink,
        font_weight=600,
    )
)

# total revenue
defs = svg.ensure_defs()
revenue_years = [d.fiscal_year for d in data.annual_revenue]
revenue_values = [d.revenue for d in data.annual_revenue]
x_revenue_scale = dp.BandScale(revenue_years, (margin["left"], svg.w - margin["right"]))
y_revenue_scale = dp.LinearScale(
    (0, max_revenue), (svg.h - margin["bottom"], margin["top"])
)
revenue_layer_mask = dp.G(id="revenue-layer")
revenue_clip_path = dp.ClipPath(id="revenue-clip")
for year, revenue in zip(revenue_years, revenue_values):
    x = x_revenue_scale.map(year)
    y = y_revenue_scale.map(revenue)
    height = svg.h - y - margin["bottom"]
    revenue_layer_mask.append(
        dp.Rect(pos=(x, y), width=x_revenue_scale.bandwidth, height=height)
    )
    revenue_clip_path.append(
        dp.Rect(pos=(x, y), width=x_revenue_scale.bandwidth, height=height)
    )
defs.append(revenue_layer_mask)
defs.append(revenue_clip_path)
area_gradient = dp.LinearGradient(
    id="area-gradient",
    x1=0,
    y1=margin["top"],
    x2=0,
    y2=svg.h - margin["bottom"],
)
area_gradient.attrs({"gradientUnits": "userSpaceOnUse"})
area_gradient.add_stop("0%", theme.lime, 1)
area_gradient.add_stop("100%", theme.lime, 0.25)
defs.append(area_gradient)

# actual columns
revenue_layer = dp.G().append(dp.Use(revenue_layer_mask, fill=theme.blue))

# stock line
stock_months = [d.date.toordinal() for d in data.monthly_prices]
stock_values = [d.close for d in data.monthly_prices]

stock_x_scale = dp.PointScale(stock_months, (margin["left"], svg.w - margin["right"]))
stock_y_scale = dp.LinearScale(
    (0, max(stock_values)), (svg.h - margin["bottom"], margin["top"])
)
stock_layer = dp.G()
line_generator = dp.LineGenerator(curve="basis")
stock_points = [
    (stock_x_scale.map(month), stock_y_scale.map(value))
    for month, value in zip(stock_months, stock_values, strict=True)
]
area_generator = dp.AreaGenerator(
    y0=lambda _point, _index: svg.h - margin["bottom"],
    curve="basis",
)
area_path = area_generator(stock_points)
path = line_generator(stock_points)

stock_layer.append(
    dp.Path(
        d=area_path,
        fill="url(#area-gradient)",
        stroke=theme.transparent,
        clip_path="url(#revenue-clip)",
    ),
    dp.Path(
        d=path,
        fill=theme.transparent,
        stroke=dp.tone(theme.green, -0.5),
        stroke_width=3,
    ),
)

# axes
axis_layer = dp.G()
axis_y = svg.h - margin["bottom"]
axis_layer.append(
    dp.Line(
        x1=margin["left"],
        y1=axis_y,
        x2=svg.w - margin["right"],
        y2=axis_y,
        stroke=theme.ink,
    )
)

year_x_values = [
    x_revenue_scale.map(year) + x_revenue_scale.bandwidth / 2 for year in revenue_years
]
tick_path = dp.Polyline(
    [coordinate for x in year_x_values for coordinate in (x, axis_y)],
    stroke="none",
    fill="none",
)
axis_layer.append(tick_path)

marker = Marker("bottom-tick", TICK_BOTTOM, 10, 10, fill=theme.ink)
defs.append(marker)
tick_path.marker_start = marker.url
tick_path.marker_mid = marker.url
tick_path.marker_end = marker.url

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

for tick in calculate_ticks(0, max_revenue, 5):
    y = y_revenue_scale.map(tick)
    axis_layer.append(
        dp.Line(
            x1=margin["left"],
            y1=y,
            x2=svg.w - margin["right"],
            y2=y,
            stroke=theme.ink,
            opacity=0.15,
        ),
        dp.Text(
            f"${tick / 1_000_000_000:.0f}B",
            x=margin["left"] - 10,
            y=y,
            text_anchor="end",
            dominant_baseline="middle",
            font_size=12,
            fill=theme.blue,
        ),
    )

for tick in calculate_ticks(0, max(stock_values), 5):
    y = stock_y_scale.map(tick)
    axis_layer.append(
        dp.Text(
            f"${tick:.0f}",
            x=svg.w - margin["right"] + 10,
            y=y,
            dominant_baseline="middle",
            font_size=12,
            fill=theme.green,
        )
    )

svg.append(axis_layer, revenue_layer, stock_layer)

svg.append(
    icon_label("revenue.svg", "Total Revenue", theme.blue, (30, 40), 70),
    icon_label(
        "stock_price.svg",
        "Stock Price",
        theme.green,
        (svg.w - 90, 40),
        -10,
        "end",
    ),
)

filename_suffix = f"_{motive}" if motive else ""
svg.save(get_output_path(f"{get_example_name()}{filename_suffix}.svg"))
