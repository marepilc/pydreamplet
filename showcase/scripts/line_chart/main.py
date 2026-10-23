from datetime import date, timedelta

import pydreamplet as dp
from pydreamplet.markers import TICK_BOTTOM, Marker
from pydreamplet.noise import Noise
from pydreamplet.typography import TypographyMeasurer
from pydreamplet.utils import calculate_ticks, place_labels_1d, sample_uniform

from tools.runtime import (
    get_example_name,
    get_motive,
    get_motive_path,
    get_output_path,
)

motive = get_motive()
theme = dp.Theme(get_motive_path(motive)) if motive else dp.Theme()

svg = dp.SVG(800, 400, font_family=theme.font_family, font_size=theme.font_size)
margin = {"left": 50, "right": 105, "top": 18, "bottom": 50}
axis_layer = dp.G()
line_layer = dp.G()
label_layer = dp.G()
svg.append(axis_layer, line_layer, label_layer)

# the random data
products = ["bicycle", "apple", "ham", "spoon", "boat", "starship"]
data: dict[str, list[int]] = {}
for ix, product in enumerate(products):
    noise = Noise(0, 250, 0.1, seed=ix + 5)
    data[product] = [noise.int_value for _ in range(100)]

min_value = min(min(d) for d in data.values())
max_value = max(max(d) for d in data.values())

start_date = date(2025, 7, 1)
end_date = start_date + timedelta(days=99)
dates = [
    start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)
]

# scales
x_scale = dp.PointScale(dates, (margin["left"], svg.w - margin["right"]))
y_scale = dp.LinearScale(
    (min_value, max_value), (svg.h - margin["bottom"], margin["top"])
)

x_values: list[float] = []
for current_date in dates:
    x = x_scale.map(current_date)
    if x is None:
        raise ValueError(f"Date is outside the x-scale domain: {current_date}")
    x_values.append(x)

colors = dp.generate_colors(theme.teal, len(products))
last_points_y: list[float] = []

for ix, product in enumerate(products):
    points: list[float] = []
    for x, value in zip(x_values, data[product], strict=True):
        points.extend((x, y_scale.map(value)))
    line_layer.append(
        dp.Polyline(points, stroke=colors[ix], stroke_width=2, fill=theme.transparent)
    )
    last_points_y.append(points[-1])

# labels
measurer = TypographyMeasurer(
    font_family=theme.font_family,
    weight=theme.font_weight,
)
label_heights = [
    measurer.measure_text(product, font_size=theme.font_size)[1] for product in products
]
label_placements = place_labels_1d(
    last_points_y,
    label_heights,
    gap=4,
    bounds=(margin["top"], svg.h - margin["bottom"]),
)

line_end_x = x_values[-1]
label_x = line_end_x + 18
for product, color, placement in zip(
    products,
    colors,
    label_placements,
    strict=True,
):
    label_layer.append(
        dp.Text(
            product,
            x=label_x,
            y=placement.position,
            dominant_baseline="middle",
            fill=color,
            font_size=theme.font_size,
        ),
    )

# axis
axis_y = y_scale.output_range[0]
axis_layer.append(
    dp.Line(
        x1=margin["left"],
        y1=axis_y,
        x2=svg.w - margin["right"],
        y2=axis_y,
        stroke=theme.ink,
        stroke_width=1,
    )
)

tick_indices = sample_uniform(x_scale.domain, 5, None)
tick_points = []
for index in tick_indices:
    tick_points.extend([x_values[index], axis_y])

tick_path = dp.Polyline(tick_points, stroke="none", fill="none")
axis_layer.append(tick_path)

marker = Marker("bottom-tick", TICK_BOTTOM, 10, 10, fill=theme.ink)
defs = svg.ensure_defs()
defs.append(marker)
tick_path.marker_start = marker.url
tick_path.marker_mid = marker.url
tick_path.marker_end = marker.url

for index in tick_indices:
    axis_layer.append(
        dp.Text(
            dates[index].strftime("%d %b"),
            x=x_values[index],
            y=axis_y + 30,
            font_size=13,
            fill=theme.ink,
            text_anchor="middle",
        )
    )


# gridlines
for tick in calculate_ticks(min_value, max_value, 5):
    y = y_scale.map(tick)
    axis_layer.append(
        dp.Line(
            x1=margin["left"],
            y1=y,
            x2=svg.w - margin["right"],
            y2=y,
            stroke=theme.ink,
            opacity=0.18,
        )
    )
    axis_layer.append(
        dp.Text(
            str(tick),
            x=margin["left"] - 10,
            y=y + 4,
            font_size=13,
            fill=theme.ink,
            text_anchor="end",
        )
    )

filename_suffix = f"_{motive}" if motive else ""
svg.save(get_output_path(f"{get_example_name()}{filename_suffix}.svg"))
