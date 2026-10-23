from math import cos, radians, sin
import pydreamplet as dp

from tools.runtime import (
    get_example_name,
    get_motive,
    get_motive_path,
    get_output_path,
)

motive = get_motive()
theme = dp.Theme(get_motive_path(motive)) if motive else dp.Theme()

svg = dp.SVG(1024, 1024)
margin = 24
min_radius = 10
circle_count = 32
max_radius = svg.w / 2 - margin
radius_step = (max_radius - min_radius) / (circle_count - 1)
colors = [
    dp.blend(theme.pink, theme.sky, i / circle_count) for i in range(circle_count)
]
g = dp.G(pos=(svg.w / 2, svg.h / 2))
svg.append(g)

angle_step = 360 / circle_count

for i in range(circle_count):
    angle = radians(i * angle_step)
    r = min_radius + i * radius_step
    final_cx = max_radius * cos(angle)
    final_cy = max_radius * sin(angle)

    circle = dp.Circle(
        pos=(final_cx, final_cy), r=min_radius, fill=theme.transparent, stroke=colors[i]
    )
    circle.append(dp.Animate("r", values=[min_radius, r, min_radius], dur="5s"))
    circle.append(dp.Animate("cx", values=[final_cx, 0, final_cx], dur="5s"))
    circle.append(dp.Animate("cy", values=[final_cy, 0, final_cy], dur="5s"))
    g.append(circle)

g.append(
    dp.AnimateTransform(
        "rotate",
        values=[0, 120, 240, 360],
        dur="10s",
        calcMode="linear",
        additive="sum",
    )
)

filename_suffix = f"_{motive}" if motive else ""
svg.save(get_output_path(f"{get_example_name()}{filename_suffix}.svg"))
