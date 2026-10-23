import pydreamplet as dp
from pydreamplet.noise import SimplexNoise2D

from tools.runtime import (
    get_example_name,
    get_motive,
    get_motive_path,
    get_output_path,
)

motive = get_motive()
theme = dp.Theme(get_motive_path(motive)) if motive else dp.Theme()

noise = SimplexNoise2D()
svg = dp.SVG(1024, 1024)
defs = svg.ensure_defs()
shadow = dp.Filter(
    id="drop-shadow",
    x="-20%",
    y="-20%",
    width="140%",
    height="140%",
)
shadow.append(
    dp.SvgElement(
        "feDropShadow",
        dx=0,
        dy=10,
        stdDeviation=8,
        flood_color="#000000",
        flood_opacity=0.65,
    )
)
defs.append(shadow)

margin = 64
g = dp.G(pos=(svg.w / 2, svg.h / 2))
svg.append(g)

shapes_count = 8
line = dp.LineGenerator(curve="basis")
offset = dp.Vector(1, 1)
palette = dp.generate_colors("#db45f9", n=shapes_count)
min_radius = 20
max_radius = svg.w / 2 - margin
radius_step = (max_radius - min_radius) / (shapes_count - 1)
wave_phases = (0, 90, 180, 270, 360)
wave_duration = "7s"

for shape_index, color in enumerate(palette):
    base_radius = max_radius - shape_index * radius_step
    wave_paths: list[str] = []
    for phase in wave_phases:
        points: list[tuple[float, float]] = []
        angle = 0
        while angle < 360:
            direction = dp.Vector.from_polar(angle)
            noise_direction = dp.Vector.from_polar(angle + phase)
            radius = base_radius + noise.noise(
                noise_direction.x,
                noise_direction.y,
                frequency=1.5,
                amplitude=50,
            )
            points.append((direction * radius + offset).xy)
            angle += 5
        wave_paths.append(f"{line(points)} Z")

    path = dp.Path(
        wave_paths[0],
        opacity=0.75,
        stroke=theme.ink,
        fill=color,
        filter="url(#drop-shadow)",
    )
    path.append(
        dp.Animate(
            "d",
            values=wave_paths,
            dur=wave_duration,
        )
    )
    g.append(path)

filename_suffix = f"_{motive}" if motive else ""
svg.save(get_output_path(f"{get_example_name()}{filename_suffix}.svg"))
