from itertools import groupby
from math import asin, ceil

import pydreamplet as dp
from data_reader import Segmentation, get_data
from pydreamplet.typography import TypographyMeasurer
from pydreamplet.utils import degrees

from tools.runtime import (
    get_example_name,
    get_motive,
    get_motive_path,
    get_output_path,
)

motive = get_motive()
theme = dp.Theme(get_motive_path(motive)) if motive else dp.Theme()

svg = dp.SVG(1500, 1500, font_family=theme.font_family, font_size=theme.font_size + 4)
main_group = dp.G(pos=(svg.w / 2, svg.h / 2))
category_arcs_group = dp.G(pos=(svg.w / 2, svg.h / 2))
svg.append(main_group, category_arcs_group)

suppliers = get_data()

# Calculate of the min and max values
qn_range: tuple[int, int] = (
    min(s.qn for s in suppliers),
    ceil(max(s.qn for s in suppliers) / 10) * 10,  # round max_qn to the nearest 10
)
ppm_range: tuple[int, int] = (
    min(s.ppm for s in suppliers),
    max(s.ppm for s in suppliers),
)
qty_range: tuple[int, int] = (
    min(s.qty for s in suppliers),
    max(s.qty for s in suppliers),
)
spend_range: tuple[int, int] = (
    min(s.spend for s in suppliers),
    max(s.spend for s in suppliers),
)

cat_data: list[dict[str, float | str]] = []
step = 340 / (len(suppliers) - 1)
angle = -80

for category, group in groupby(suppliers, key=lambda x: x.category):
    count = len(list(group))
    end_angle = angle + step * (count - 1)
    cat_data.append(
        {"category": category, "start_angle": angle, "end_angle": end_angle}
    )
    angle = end_angle + step

measurer = TypographyMeasurer(font_family=theme.font_family, weight=400)
qty_scale = dp.CircleScale(qty_range, (2, 16))
spend_scale = dp.CircleScale(spend_range, (2, 16))
qn_scale = dp.LinearScale(qn_range, (300, 30))
ppm_scale = dp.ColorScale(ppm_range, (theme.surface, theme.red))
segmentation_color = theme.amber
phase_out_color = theme.red
circle_color = theme.sky
dimmed_ink = theme.gray

main_group.append(
    dp.Text("QN", pos=(0, 6), text_anchor="middle", font_weight=600, fill=theme.ink)
)
for i in range(10):
    radius = qn_scale.map(i * 10)
    x_offset = 15
    alpha = degrees(asin(x_offset / radius))

    start_angle = -90 + alpha
    end_angle = 270 - alpha
    circle = dp.Path(
        dp.arc(0, 0, radius=radius, start_angle=start_angle, end_angle=end_angle)
    )
    circle.fill = "none"
    circle.stroke = theme.ink
    main_group.append(
        circle,
        dp.Text(
            str(i * 10),
            pos=(0, 4 - radius),
            text_anchor="middle",
            fill=theme.ink,
        ),
    )

defs = svg.ensure_defs()
for category_index, cat in enumerate(cat_data):
    arc_element = dp.Path(
        dp.ring(
            0,
            0,
            inner_radius=710,
            outer_radius=720,
            start_angle=float(cat["start_angle"]),
            end_angle=float(cat["end_angle"]),
            without_inner=True,
        ),
        fill=theme.transparent,
        stroke=theme.ink,
        stroke_width=2,
    )
    text_arc = dp.Path(
        dp.arc(
            0,
            0,
            radius=730,
            start_angle=float(cat["start_angle"]),
            end_angle=float(cat["end_angle"]),
        ),
        id=f"category_{category_index}",
    )
    defs.append(text_arc)

    text = dp.TextOnPath(
        str(cat["category"]),
        path_id=f"#category_{category_index}",
        text_path_args={"startOffset": "50%"},
    )
    text.font_size = "24"
    text.font_weight = "600"
    text.fill = theme.ink
    text.text_anchor = "middle"
    category_arcs_group.append(arc_element, text)

# Create one rotated group per supplier. Keeping this outside the category loop
# prevents labels and chart marks from being drawn repeatedly.
supplier_groups: list[dp.G] = []
supplier_angles: list[float] = []
angle = -80
for _supplier in suppliers:
    supplier_group = dp.G(angle=angle)
    supplier_groups.append(supplier_group)
    supplier_angles.append(angle)
    main_group.append(supplier_group)
    angle += step

# Draw each supplier's QN mark once.
for supplier, supplier_group in zip(suppliers, supplier_groups, strict=True):
    qn = qn_scale.map(supplier.qn)
    supplier_group.append(
        dp.Path(
            dp.ring(
                0,
                0,
                inner_radius=qn,
                outer_radius=300,
                start_angle=-1.3,
                end_angle=1.3,
            ),
            fill=theme.cyan,
        )
    )

# Mark strategic, preferred, and phase-out suppliers next to the QN chart.
for supplier, supplier_group in zip(suppliers, supplier_groups, strict=True):
    if supplier.segmentation in (Segmentation.STRATEGIC, Segmentation.PREFERRED):
        supplier_group.append(
            dp.Path(
                dp.star(318, 0, inner_radius=5, outer_radius=8),
                fill=(
                    segmentation_color
                    if supplier.segmentation == Segmentation.STRATEGIC
                    else "none"
                ),
                stroke=segmentation_color,
                stroke_width=1,
            )
        )
    elif supplier.segmentation == Segmentation.PHASE_OUT:
        supplier_group.append(
            dp.Path(
                dp.cross(318, 0, size=12, thickness=4, angle=45),
                fill=phase_out_color,
                stroke=phase_out_color,
                stroke_width=1,
            )
        )

# Draw each supplier name in a readable orientation. Labels on the left half
# are flipped locally so they remain upright after the group rotation.
label_x = 330
label_font_size = 18
line_end_x = 600
for supplier, supplier_group, supplier_angle in zip(
    suppliers, supplier_groups, supplier_angles, strict=True
):
    is_left_half = 90 < supplier_angle % 360 < 270
    text_width = measurer.measure_text(
        supplier.name,
        font_size=label_font_size,
    )[0]
    text_transform = {"transform": f"rotate(180 {label_x} 0)"} if is_left_half else {}

    supplier_group.append(
        dp.Text(
            supplier.name,
            x=label_x,
            y=0,
            text_anchor="end" if is_left_half else "start",
            dominant_baseline="middle",
            font_family=theme.font_family,
            font_size=label_font_size,
            fill=theme.ink,
            **text_transform,
        ),
        dp.Line(
            x1=label_x + text_width + 10,
            y1=0,
            x2=line_end_x,
            y2=0,
            stroke=theme.ink,
            stroke_width=1,
            stroke_dasharray="5, 5",
        ),
    )

# Encode supplied quantity and spend as outline and filled circles.
for supplier, supplier_group in zip(suppliers, supplier_groups, strict=True):
    supplier_group.append(
        dp.Circle(
            cx=620,
            cy=0,
            r=qty_scale.map(supplier.qty),
            fill="none",
            stroke=circle_color,
            stroke_width=1,
        ),
        dp.Circle(
            cx=660,
            cy=0,
            r=spend_scale.map(supplier.spend),
            fill=circle_color,
            stroke=circle_color,
            stroke_width=1,
        ),
    )

# Encode PPM as a colored ring immediately inside the category arcs.
for supplier, supplier_group in zip(suppliers, supplier_groups, strict=True):
    supplier_group.append(
        dp.Path(
            dp.ring(
                0,
                0,
                inner_radius=690,
                outer_radius=705,
                start_angle=-1.3,
                end_angle=1.3,
            ),
            fill=ppm_scale.map(supplier.ppm),
            stroke=dimmed_ink,
            stroke_width=1,
        )
    )

# Add a title outside the radial chart.
svg.append(
    dp.Text(
        "Supplier\nQuality\nPerformance",
        x=10,
        y=10,
        font_family=theme.font_family,
        font_size=36,
        font_weight=700,
        text_anchor="start",
        dominant_baseline="hanging",
        v_space=44,
        stroke="none",
        fill=theme.ink,
    )
)

# Quantity and spend legend.
metrics_legend = dp.G(pos=(1280, 40))
svg.append(metrics_legend)
metrics_legend.append(dp.Text("Qty.", x=0, y=0, font_size=32, fill=theme.ink))

small_qty_radius = qty_scale.map(5_000)
large_qty_radius = qty_scale.map(300_000)
metrics_legend.append(
    dp.Circle(
        cx=small_qty_radius,
        cy=40,
        r=small_qty_radius,
        fill="none",
        stroke=circle_color,
        stroke_width=1,
    ),
    dp.Text(
        "5K",
        x=small_qty_radius * 2 + 10,
        y=45,
        font_size=24,
        fill=theme.ink,
    ),
    dp.Circle(
        cx=80,
        cy=40,
        r=large_qty_radius,
        fill="none",
        stroke=circle_color,
        stroke_width=1,
    ),
    dp.Text(
        "300K",
        x=80 + large_qty_radius + 10,
        y=45,
        font_size=24,
        fill=theme.ink,
    ),
    dp.Text("Spend", x=0, y=90, font_size=32, fill=theme.ink),
)

small_spend_radius = spend_scale.map(100_000)
large_spend_radius = spend_scale.map(1_000_000)
metrics_legend.append(
    dp.Circle(
        cx=small_spend_radius,
        cy=130,
        r=small_spend_radius,
        fill=circle_color,
        stroke=circle_color,
        stroke_width=1,
    ),
    dp.Text(
        "$100K",
        x=small_spend_radius * 2 + 10,
        y=135,
        font_size=24,
        fill=theme.ink,
    ),
    dp.Circle(
        cx=120,
        cy=130,
        r=large_spend_radius,
        fill=circle_color,
        stroke=circle_color,
        stroke_width=1,
    ),
    dp.Text(
        "$1M",
        x=120 + large_spend_radius + 10,
        y=135,
        font_size=24,
        fill=theme.ink,
    ),
)

# Segmentation legend.
segmentation_legend = dp.G(pos=(10, 1380))
svg.append(segmentation_legend)
segmentation_legend.append(
    dp.Text("Segmentation", x=0, y=0, font_size=32, fill=theme.ink),
    dp.Path(
        dp.star(8, 40, inner_radius=5, outer_radius=8, angle=342),
        fill=segmentation_color,
        stroke=segmentation_color,
        stroke_width=1,
    ),
    dp.Text("strategic", x=25, y=45, font_size=24, fill=theme.ink),
    dp.Path(
        dp.star(8, 70, inner_radius=5, outer_radius=8, angle=342),
        fill="none",
        stroke=segmentation_color,
        stroke_width=1,
    ),
    dp.Text("preferred", x=25, y=75, font_size=24, fill=theme.ink),
    dp.Path(
        dp.cross(8, 100, size=12, thickness=4, angle=45),
        fill=phase_out_color,
        stroke=phase_out_color,
        stroke_width=1,
    ),
    dp.Text("phase-out", x=25, y=105, font_size=24, fill=theme.ink),
)

# PPM gradient legend.
ppm_gradient = dp.SvgElement("linearGradient", id="ppm-gradient")
ppm_gradient.append(
    dp.SvgElement(
        "stop",
        offset="0%",
        style=f"stop-color:{ppm_scale.map(ppm_range[0])};stop-opacity:1",
    ),
    dp.SvgElement(
        "stop",
        offset="100%",
        style=f"stop-color:{ppm_scale.map(ppm_range[1])};stop-opacity:1",
    ),
)
defs.append(ppm_gradient)

ppm_legend = dp.G(pos=(1150, 1440))
svg.append(ppm_legend)
ppm_legend.append(
    dp.Text("PPM", x=0, y=0, font_size=32, fill=theme.ink),
    dp.Text(
        f"{ppm_range[0]:,}",
        x=0,
        y=35,
        font_size=24,
        fill=theme.ink,
    ),
    dp.Rect(
        x=30,
        y=20,
        width=200,
        height=20,
        fill="url(#ppm-gradient)",
        stroke=dimmed_ink,
        stroke_width=1,
    ),
    dp.Text(
        f"{ppm_range[1]:,}",
        x=245,
        y=35,
        font_size=24,
        fill=theme.ink,
    ),
)

filename_suffix = f"_{motive}" if motive else ""
svg.save(get_output_path(f"{get_example_name()}{filename_suffix}.svg"))
