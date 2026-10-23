import pydreamplet as dp

from tools.runtime import (
    get_example_name,
    get_motive,
    get_motive_path,
    get_output_path,
)


def animate(attribute: str, values: str, duration: str) -> dp.SvgElement:
    """Create an indefinitely repeating SVG attribute animation."""
    return dp.SvgElement(
        "animate",
        attributeName=attribute,
        values=values,
        dur=duration,
        repeatCount="indefinite",
    )


def animate_transform(
    transform_type: str,
    values: str,
    duration: str,
) -> dp.SvgElement:
    """Create an additive SVG transform animation."""
    return dp.SvgElement(
        "animateTransform",
        attributeName="transform",
        type=transform_type,
        values=values,
        dur=duration,
        repeatCount="indefinite",
        additive="sum",
    )


def blur_filter(
    filter_id: str,
    deviation: float,
    *,
    bounds: tuple[str, str, str, str] | None = None,
) -> dp.Filter:
    """Create a reusable Gaussian blur filter."""
    blur = dp.Filter(id=filter_id)
    if bounds is not None:
        x, y, width, height = bounds
        blur.attrs({"x": x, "y": y, "width": width, "height": height})
    blur.append(
        dp.SvgElement(
            "feGaussianBlur",
            **{"in": "SourceGraphic", "stdDeviation": deviation},
        )
    )
    return blur


def distortion_filter(
    filter_id: str,
    *,
    frequency: str,
    octaves: int,
    seed: int,
    scale: int,
    blur: float,
    frequency_values: str,
    scale_values: str,
    frequency_duration: str,
    scale_duration: str,
    channels: tuple[str, str] = ("R", "G"),
    bounds: tuple[str, str, str, str] = ("-18%", "-18%", "136%", "136%"),
) -> dp.Filter:
    """Create an animated turbulence and displacement filter."""
    x, y, width, height = bounds
    noise_result = f"{filter_id}-noise"
    warped_result = f"{filter_id}-warped"

    turbulence = dp.SvgElement(
        "feTurbulence",
        type="fractalNoise",
        baseFrequency=frequency,
        numOctaves=octaves,
        seed=seed,
        result=noise_result,
    ).append(animate("baseFrequency", frequency_values, frequency_duration))

    displacement = dp.SvgElement(
        "feDisplacementMap",
        **{
            "in": "SourceGraphic",
            "in2": noise_result,
            "scale": scale,
            "xChannelSelector": channels[0],
            "yChannelSelector": channels[1],
            "result": warped_result,
        },
    ).append(animate("scale", scale_values, scale_duration))

    return (
        dp.Filter(id=filter_id)
        .attrs(
            {
                "x": x,
                "y": y,
                "width": width,
                "height": height,
                "color-interpolation-filters": "sRGB",
            }
        )
        .append(
            turbulence,
            displacement,
            dp.SvgElement(
                "feGaussianBlur",
                **{"in": warped_result, "stdDeviation": blur},
            ),
        )
    )


# Step 1: Load the selected motive and derive light/dark rendering parameters.
motive = get_motive()
theme = dp.Theme(get_motive_path(motive)) if motive else dp.Theme()
is_dark = motive == "dark"

svg = dp.SVG(1024, 1024)
defs = svg.ensure_defs()

main_group = dp.G(pos=(svg.w / 2, svg.h / 2))
svg.append(main_group)

bubble_radius = 480
bubble_light = theme.ink if is_dark else theme.white
bubble_shadow = theme.ink if is_dark else theme.slate
spectral_cyan = theme.cyan
spectral_violet = theme.violet
spectral_gold = theme.amber
spectral_green = theme.emerald
spectral_pink = theme.pink
spectral_red = theme.rose

base_light_opacity = 0.12 if is_dark else 0.28
base_edge_opacity = 0.16 if is_dark else 0.09
diffuse_strength = 0.28 if is_dark else 0.16

# Step 2: Clip all film colors and reflections to the circular soap bubble.
clip_path = dp.ClipPath("bubble").append(dp.Circle(pos=(0, 0), r=bubble_radius))

# Step 3: Build the translucent base film. Its off-center highlight makes the
# otherwise flat circle feel spherical.
bubble_base_gradient = dp.SvgElement(
    "radialGradient",
    id="bubble-base",
    cx="34%",
    cy="28%",
    r="72%",
).append(
    dp.SvgElement(
        "stop",
        offset="0%",
        stop_color=bubble_light,
        stop_opacity=base_light_opacity,
    ),
    dp.SvgElement(
        "stop",
        offset="42%",
        stop_color=theme.surface,
        stop_opacity=0.03,
    ),
    dp.SvgElement(
        "stop",
        offset="76%",
        stop_color=spectral_cyan,
        stop_opacity=0.10,
    ),
    dp.SvgElement(
        "stop",
        offset="100%",
        stop_color=bubble_shadow,
        stop_opacity=base_edge_opacity,
    ),
)

# Step 4: Define blur and animated distortion filters. Different frequencies
# produce broad liquid blobs, fine interference lines, and an unstable rim.
blur = blur_filter("blur", 10)
blur_2 = blur_filter("blur-2", 20)
rim_blur = blur_filter("rim-blur", 5)
silk_blur = blur_filter("silk-blur", 12)
fine_blur = blur_filter("fine-blur", 2.5)
light_spot_blur = blur_filter(
    "light-spot-blur",
    14,
    bounds=("-160%", "-160%", "420%", "420%"),
)
reflection_blur = blur_filter(
    "reflection-blur",
    17,
    bounds=("-35%", "-35%", "170%", "170%"),
)

film_distort = distortion_filter(
    "film-distort",
    frequency="0.012 0.028",
    octaves=3,
    seed=8,
    scale=28,
    blur=11,
    frequency_values="0.012 0.028;0.018 0.018;0.010 0.034;0.012 0.028",
    scale_values="22;34;26;30;22",
    frequency_duration="18s",
    scale_duration="14s",
)
edge_distort = distortion_filter(
    "edge-distort",
    frequency="0.008 0.020",
    octaves=2,
    seed=21,
    scale=16,
    blur=8,
    frequency_values="0.008 0.020;0.012 0.016;0.006 0.024;0.008 0.020",
    scale_values="12;20;15;18;12",
    frequency_duration="22s",
    scale_duration="16s",
    bounds=("-15%", "-15%", "130%", "130%"),
)
blob_distort = distortion_filter(
    "blob-distort",
    frequency="0.009 0.022",
    octaves=4,
    seed=34,
    scale=38,
    blur=18,
    frequency_values=("0.009 0.022;0.014 0.018;0.007 0.028;0.011 0.020;0.009 0.022"),
    scale_values="28;46;34;40;28",
    frequency_duration="26s",
    scale_duration="19s",
    channels=("R", "B"),
    bounds=("-22%", "-22%", "144%", "144%"),
)

# Step 5: Add diffuse lighting for the dark motive. The animated point light
# moves slowly across the surface and changes the perceived curvature.
bubble_lighting = (
    dp.Filter(id="bubble-lighting")
    .attrs(
        {
            "x": "-20%",
            "y": "-20%",
            "width": "140%",
            "height": "140%",
            "color-interpolation-filters": "sRGB",
        }
    )
    .append(
        dp.SvgElement(
            "feGaussianBlur",
            **{"in": "SourceAlpha", "stdDeviation": 42, "result": "soft-alpha"},
        ),
        dp.SvgElement(
            "feDiffuseLighting",
            **{
                "in": "soft-alpha",
                "surfaceScale": 26,
                "diffuseConstant": 0.55,
                "lighting-color": bubble_light,
                "result": "diffuse-light",
            },
        ).append(
            dp.SvgElement("fePointLight", x=-190, y=-245, z=320).append(
                animate("x", "-205;-170;-188;-220;-205", "12s"),
                animate("y", "-260;-228;-238;-276;-260", "15s"),
                animate("z", "300;380;330;360;300", "18s"),
            )
        ),
        dp.SvgElement(
            "feComposite",
            **{
                "in": "diffuse-light",
                "in2": "SourceGraphic",
                "operator": "arithmetic",
                "k1": 0,
                "k2": 1,
                "k3": diffuse_strength,
                "k4": 0,
                "result": "lit-bubble",
            },
        ),
        dp.SvgElement(
            "feComposite",
            **{"in": "lit-bubble", "in2": "SourceAlpha", "operator": "in"},
        ),
    )
)

# Step 6: Create the base, moving highlights, colored inner rims, and the soft
# outer edge. These definitions are later instantiated with <use>.
bubble_background = dp.Circle(
    pos=(0, 0),
    r=bubble_radius,
    fill="url(#bubble-base)",
    id="bubble-bg",
)
if is_dark:
    bubble_background.attrs({"filter": bubble_lighting.url})

bubble_light_spot = (
    dp.Circle(
        pos=(-190, -245),
        r=34,
        fill=bubble_light,
        id="bubble-light-spot",
        filter=light_spot_blur.url,
    )
    .attrs({"opacity": 0.42 if is_dark else 0.24})
    .append(
        animate("cx", "-190;-174;-202;-212;-190", "12s"),
        animate("cy", "-245;-224;-236;-268;-245", "15s"),
        animate(
            "opacity",
            "0.34;0.50;0.40;0.46;0.34" if is_dark else "0.16;0.32;0.22;0.28;0.16",
            "9s",
        ),
    )
)
small_light_spot = (
    dp.Circle(
        pos=(-148, -292),
        r=12,
        fill=theme.white,
        id="small-light-spot",
        filter=fine_blur.url,
    )
    .attrs({"opacity": 0.52 if is_dark else 0.34})
    .append(
        animate("cx", "-148;-134;-152;-164;-148", "10s"),
        animate("cy", "-292;-278;-300;-306;-292", "13s"),
    )
)
inner_cyan_rim = dp.Circle(
    pos=(0, 0),
    r=bubble_radius - 18,
    fill="none",
    id="inner-cyan-rim",
    stroke=spectral_cyan,
    stroke_width=8,
    filter=rim_blur.url,
).attrs({"opacity": 0.22 if is_dark else 0.34})
inner_magenta_rim = dp.Circle(
    pos=(0, 0),
    r=bubble_radius - 46,
    fill="none",
    id="inner-magenta-rim",
    stroke=spectral_violet,
    stroke_width=5,
    filter=silk_blur.url,
).attrs({"opacity": 0.14 if is_dark else 0.24})
outer_rim = dp.Circle(
    pos=(0, 0),
    r=bubble_radius,
    fill="none",
    id="outer-rim",
    stroke=theme.ink if is_dark else theme.white,
    stroke_width=26,
    filter=blur.url,
).attrs({"opacity": 0.38 if is_dark else 0.55})

# Step 7: Layer broad spectral film regions. Animated displacement makes their
# boundaries flow without changing the circular silhouette.
cyan_arc = (
    dp.Path(
        (
            "M -420 -250 C -340 -365, -180 -428, -20 -416 "
            "C 88 -408, 184 -382, 292 -352 "
            "C 236 -318, 118 -308, 8 -320 "
            "C -152 -338, -286 -294, -382 -184 Z"
        ),
        fill=spectral_cyan,
        id="cyan-film-arc",
        filter=blob_distort.url,
    )
    .attrs({"opacity": 0.20})
    .append(
        animate("opacity", "0.16;0.23;0.18;0.21;0.16", "20s"),
        animate_transform("translate", "0 0;18 -6;-10 12;0 0", "24s"),
    )
)
violet_arc = (
    dp.Path(
        (
            "M -424 -206 C -476 -68, -468 94, -418 226 "
            "C -382 322, -324 394, -252 438 "
            "C -288 344, -330 258, -348 158 "
            "C -370 34, -356 -88, -300 -180 "
            "C -344 -184, -388 -194, -424 -206 Z"
        ),
        fill=spectral_violet,
        id="violet-film-arc",
        filter=blob_distort.url,
    )
    .attrs({"opacity": 0.18})
    .append(
        animate("opacity", "0.13;0.22;0.16;0.20;0.13", "24s"),
        animate_transform("rotate", "0 0 0;2.5 0 0;-1.5 0 0;0 0 0", "30s"),
    )
)
gold_arc = (
    dp.Path(
        (
            "M -270 -20 C -196 -126, -72 -188, 76 -188 "
            "C 188 -188, 292 -158, 344 -104 "
            "C 244 -116, 154 -106, 52 -72 "
            "C -64 -34, -154 -12, -232 34 Z"
        ),
        fill=spectral_gold,
        id="gold-film-arc",
        filter=blob_distort.url,
    )
    .attrs({"opacity": 0.16})
    .append(
        animate("opacity", "0.11;0.19;0.14;0.17;0.11", "17s"),
        animate_transform("translate", "0 0;-12 10;16 -4;0 0", "21s"),
    )
)
green_arc = (
    dp.Path(
        (
            "M 116 -154 C 214 -118, 284 -30, 306 82 "
            "C 326 184, 288 284, 214 346 "
            "C 230 250, 222 166, 184 76 "
            "C 154 6, 112 -56, 70 -118 Z"
        ),
        fill=spectral_green,
        id="green-film-arc",
        filter=blob_distort.url,
    )
    .attrs({"opacity": 0.13})
    .append(
        animate("opacity", "0.09;0.16;0.11;0.14;0.09", "22s"),
        animate_transform("rotate", "0 0 0;-2 0 0;1.2 0 0;0 0 0", "27s"),
    )
)
pink_arc = (
    dp.Path(
        (
            "M -190 178 C -92 280, 72 304, 204 244 "
            "C 266 216, 304 188, 346 152 "
            "C 270 268, 154 328, 10 318 "
            "C -86 312, -164 274, -222 212 Z"
        ),
        fill=spectral_pink,
        id="pink-film-arc",
        filter=blob_distort.url,
    )
    .attrs({"opacity": 0.19})
    .append(
        animate("opacity", "0.13;0.23;0.16;0.20;0.13", "15s"),
        animate_transform("translate", "0 0;12 10;-14 -6;0 0", "18s"),
    )
)
lower_rose = (
    dp.Path(
        (
            "M -92 280 C 8 328, 156 324, 250 258 "
            "C 202 354, 84 412, -42 396 "
            "C -120 386, -186 348, -230 292 Z"
        ),
        fill=spectral_red,
        id="lower-rose-film",
        filter=film_distort.url,
    )
    .attrs({"opacity": 0.13})
    .append(animate_transform("translate", "0 0;8 -14;-18 8;0 0", "23s"))
)

# Step 8: Add fine edge color, red interference, and soft reflected shapes.
fine_blue_edge = dp.Path(
    (
        "M -470 -320 C -366 -456, -188 -520, 18 -514 "
        "C 206 -508, 362 -448, 458 -342 "
        "C 326 -398, 176 -416, 18 -404 "
        "C -178 -390, -330 -334, -438 -230 Z"
    ),
    fill=theme.teal,
    id="fine-blue-edge",
    filter=edge_distort.url,
).attrs({"opacity": 0.16})
red_top_glow = dp.Path(
    "M -78 -506 C 88 -532, 252 -510, 374 -438 C 442 -398, 484 -344, 510 -274",
    fill="none",
    id="red-top-glow",
    stroke=spectral_red,
    stroke_width=48 if is_dark else 44,
    filter=edge_distort.url,
).attrs(
    {
        "opacity": 0.16 if is_dark else 0.11,
        "stroke-linecap": "round",
    }
)
red_arc = dp.Path(
    "M -92 -474 C 90 -516, 290 -454, 404 -294",
    fill="none",
    id="red-ring",
    stroke=spectral_red,
    stroke_width=18 if is_dark else 16,
    filter=blur_2.url,
).attrs(
    {
        "opacity": 0.24 if is_dark else 0.16,
        "stroke-linecap": "round",
    }
)
reflection_smear = (
    dp.Path(
        (
            "M -266 -232 C -238 -268, -184 -284, -130 -258 "
            "C -172 -250, -214 -228, -250 -194 "
            "C -276 -170, -294 -194, -266 -232 Z"
        ),
        fill=theme.white,
        id="reflection-smear",
        filter=reflection_blur.url,
    )
    .attrs({"opacity": 0.07 if is_dark else 0.12})
    .append(
        animate(
            "opacity",
            "0.03;0.11;0.06;0.09;0.03" if is_dark else "0.06;0.18;0.10;0.14;0.06",
            "8s",
        ),
        animate_transform("translate", "0 0;7 -5;-6 4;0 0", "17s"),
    )
)

# Step 9: Register all definitions before referencing them with <use>.
defs.append(
    clip_path,
    bubble_base_gradient,
    blur,
    blur_2,
    rim_blur,
    silk_blur,
    fine_blur,
    light_spot_blur,
    reflection_blur,
    film_distort,
    edge_distort,
    blob_distort,
    bubble_lighting,
    bubble_background,
    bubble_light_spot,
    small_light_spot,
    inner_cyan_rim,
    inner_magenta_rim,
    outer_rim,
    cyan_arc,
    violet_arc,
    gold_arc,
    green_arc,
    pink_arc,
    lower_rose,
    fine_blue_edge,
    red_top_glow,
    red_arc,
    reflection_smear,
)

# Step 10: Compose the bubble from back to front. Every film layer is clipped
# to the bubble, while the moving highlights and rims stay above the colors.
for definition in (
    bubble_background,
    cyan_arc,
    violet_arc,
    gold_arc,
    green_arc,
    pink_arc,
    lower_rose,
    fine_blue_edge,
    red_top_glow,
    reflection_smear,
    bubble_light_spot,
    small_light_spot,
    inner_cyan_rim,
    inner_magenta_rim,
    outer_rim,
    red_arc,
):
    main_group.append(dp.Use(definition, clip_path=clip_path.url))

# Step 11: Save a separate default, light, or dark variant.
filename_suffix = f"_{motive}" if motive else ""
svg.save(get_output_path(f"{get_example_name()}{filename_suffix}.svg"))
