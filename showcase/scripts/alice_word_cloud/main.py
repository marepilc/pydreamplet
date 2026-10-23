import json
from collections.abc import Iterator
from math import cos, log, sin, sqrt, tau
import pydreamplet as dp
from pydreamplet.typography import TypographyMeasurer

from tools.runtime import (
    get_data_path,
    get_example_name,
    get_motive,
    get_motive_path,
    get_output_path,
)

# Step 1: Load the selected color motive and create a wide SVG canvas.
motive = get_motive()
theme = dp.Theme(get_motive_path(motive)) if motive else dp.Theme()

svg = dp.SVG(1200, 720)

# Step 2: Load the noun frequencies from this example's data directory.
script_name = get_example_name()
data_path = get_data_path("word_counts.json")
data = json.loads(data_path.read_text(encoding="utf-8"))
word_counts = [(str(word), int(count)) for word, count in data["words"]]

# Step 3: Configure text measurement with the same CSS font family and weight
# used by the SVG. Pydreamplet resolves the first available family.
font_weight = 700
measurer = TypographyMeasurer(
    dpi=72,
    font_family=theme.font_family,
    weight=font_weight,
)

# Step 4: Choose a vivid palette. Reusing motive colors keeps the cloud
# readable on both light and dark backgrounds.
palette = [
    theme.pink,
    theme.sky,
    theme.amber,
    theme.emerald,
    theme.violet,
    theme.rose,
    theme.orange,
    theme.cyan,
]

# Step 5: Reserve an elliptical region for the cloud and prepare a list of
# occupied rectangles. Every new word must fit inside the ellipse and avoid
# all rectangles already stored here.
center_x = svg.w / 2
center_y = svg.h / 2
cloud_radius_x = svg.w * 0.47
cloud_radius_y = svg.h * 0.45
placed_boxes: list[tuple[float, float, float, float]] = []
spatial_index: dict[tuple[int, int], list[int]] = {}
spatial_cell_size = 64


def box_cells(bounds: tuple[float, float, float, float]) -> Iterator[tuple[int, int]]:
    """Yield spatial-index cells touched by a bounding box."""
    left, top, right, bottom = bounds
    min_column = int(left // spatial_cell_size)
    max_column = int(right // spatial_cell_size)
    min_row = int(top // spatial_cell_size)
    max_row = int(bottom // spatial_cell_size)

    for column in range(min_column, max_column + 1):
        for row in range(min_row, max_row + 1):
            yield column, row


def register_box(bounds: tuple[float, float, float, float]) -> None:
    """Add an accepted bounding box to the spatial index."""
    box_index = len(placed_boxes)
    placed_boxes.append(bounds)
    for cell in box_cells(bounds):
        spatial_index.setdefault(cell, []).append(box_index)


def fits_cloud(bounds: tuple[float, float, float, float]) -> bool:
    """Return True when a word fits the cloud and does not overlap another."""
    left, top, right, bottom = bounds

    # Testing all four corners creates the rounded outline visible in classic
    # word-cloud layouts.
    corners = ((left, top), (right, top), (left, bottom), (right, bottom))
    if any(
        ((corner_x - center_x) / cloud_radius_x) ** 2
        + ((corner_y - center_y) / cloud_radius_y) ** 2
        > 1
        for corner_x, corner_y in corners
    ):
        return False

    nearby_box_indexes = {
        box_index
        for cell in box_cells(bounds)
        for box_index in spatial_index.get(cell, ())
    }
    return not any(
        left < other_right
        and right > other_left
        and top < other_bottom
        and bottom > other_top
        for other_left, other_top, other_right, other_bottom in (
            placed_boxes[box_index] for box_index in nearby_box_indexes
        )
    )


# Step 6: Convert counts to font sizes. A logarithmic scale prevents "Alice"
# from overwhelming all less frequent nouns while preserving their ranking.
max_count = word_counts[0][1]
min_count = word_counts[-1][1]
min_font_size = 12
max_font_size = 96


def create_candidate_positions(count: int = 7000) -> list[tuple[float, float]]:
    """Build an even phyllotaxis distribution, ordered center first."""
    positions = []
    aspect_ratio = cloud_radius_x / cloud_radius_y
    golden_turn = 0.381966

    for position_index in range(count):
        radius = cloud_radius_y * sqrt(position_index / (count - 1))
        angle = position_index * tau * golden_turn
        positions.append(
            (
                center_x + cos(angle) * radius * aspect_ratio,
                center_y + sin(angle) * radius,
            )
        )

    return positions


# A dense position map lets small labels discover gaps that a single spiral
# may pass between.
candidate_positions = create_candidate_positions()

# Step 7: Place the most frequent words first. Later smaller words fill the
# gaps left between them and make the final shape denser.
for word_index, (word, count) in enumerate(word_counts):
    normalized = (log(count) - log(min_count)) / (log(max_count) - log(min_count))
    font_size = min_font_size + normalized * (max_font_size - min_font_size)

    # Roughly one in five labels is vertical, matching the varied orientation
    # of a classic word cloud while leaving the largest words horizontal.
    rotation = 90 if word_index > 8 and word_index % 5 == 1 else 0

    # Step 8: Measure the actual shaped text instead of estimating its width
    # from the character count. This accounts for different glyph widths and
    # the font's real line metrics.
    for scale in (
        1,
        0.94,
        0.88,
        0.82,
        0.76,
        0.7,
        0.64,
        0.58,
        0.52,
        0.46,
        0.4,
        0.34,
        0.28,
    ):
        scaled_size = font_size * scale
        text_width, text_height = measurer.measure_text(
            word,
            font_size=scaled_size,
        )

        # Padding protects against browser rasterization differences and keeps
        # neighboring glyphs from visually touching.
        padding = max(1.0, scaled_size * 0.025)
        measured_width = text_width + padding * 2

        # TypographyMeasurer returns the full line height, including a font line
        # gap. Visible glyphs occupy less vertical space, so an optical factor
        # produces tighter packing while retaining measured font metrics.
        measured_height = text_height * 0.78 + padding * 2
        box_width = measured_height if rotation else measured_width
        box_height = measured_width if rotation else measured_height

        # Step 9: Test the dense position map from the center outwards. If no
        # position fits, retry with a slightly smaller rendering.
        for candidate_x, candidate_y in candidate_positions:
            candidate_box = (
                candidate_x - box_width / 2,
                candidate_y - box_height / 2,
                candidate_x + box_width / 2,
                candidate_y + box_height / 2,
            )

            if fits_cloud(candidate_box):
                register_box(candidate_box)

                # Step 10: Draw the word with exactly the same font properties
                # used by TypographyMeasurer.
                svg.append(
                    dp.Text(
                        word,
                        pos=(candidate_x, candidate_y),
                        fill=palette[word_index % len(palette)],
                        font_family=theme.font_family,
                        font_size=scaled_size,
                        font_weight=font_weight,
                        text_anchor="middle",
                        dominant_baseline="central",
                        transform=(f"rotate({rotation} {candidate_x} {candidate_y})"),
                    )
                )
                break
        else:
            continue
        break

# Step 11: Save the result in the standard showcase output directory. The
# motive suffix makes it possible to generate all color variants side by side.
filename_suffix = f"_{motive}" if motive else ""
svg.save(get_output_path(f"{script_name}{filename_suffix}.svg"))
