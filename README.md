# pyDreamplet

**pyDreamplet is a typed Python library for creating SVG graphics, data
visualizations, charts, maps, and generative art.** It provides a flexible,
low-level API for building and manipulating scalable vector graphics directly
from Python.

Use pyDreamplet for custom data visualization, creative coding, report
graphics, diagrams, and other projects where you need precise control over the
generated SVG. It works in Python scripts, Jupyter notebooks, and web
applications, and the resulting files remain resolution-independent and easy
to style or edit.

## Features

- **Programmatic SVG generation:** Create, compose, query, and manipulate SVG
  elements with a Pythonic API.
- **Data visualization tools:** Use numeric, categorical, color, square, and
  circle scales alongside helpers for ticks, labels, and chart geometry.
- **Paths and shapes:** Generate lines, curves, splines, arcs, stars, polygons,
  and other reusable SVG path data.
- **Maps and creative coding:** Build geographic visualizations, generative
  art, grids, waves, spirals, noise-based layouts, and animations.
- **Typography support:** Measure text accurately using installed OpenType and
  TrueType fonts.
- **Typed and lightweight:** Benefit from inline type information, a compact
  dependency set, and optional Jupyter notebook display support.

## Installation

Install pyDreamplet using your preferred package manager:

With uv:

```shell
uv add pydreamplet
```

For notebook display support with `svg.display()`:

```shell
uv add pydreamplet --extra notebook
```

With pip:

```shell
pip install pydreamplet
```

For notebook display support with `svg.display()`:

```shell
pip install "pydreamplet[notebook]"
```

## Documentation

For complete documentation, tutorials, and API references, please visit [pyDreamplet documentation](https://py.dreamplet.com/)

## Examples

### Multidimensional Visualization of Supplier Quality Performance

This example showcases a sophisticated, multidimensional SVG visualization that displays supplier quality performance metrics. In this visualization, data dimensions such as defect occurrences, defect quantity, and spend are combined to provide an insightful overview of supplier performance. The visualization uses color, shape, and layout to encode multiple measures, allowing users to quickly identify strengths and weaknesses across suppliers.

![supplier quality performance](https://raw.githubusercontent.com/marepilc/pydreamplet/794fa89bf4d11f270c9f08dbd9ab20b50444203c/docs/assets/readme/readme_demo_01.svg)

### Creative Coding

This example uses pyDreamplet to create an engaging animated visualization featuring a series of circles. The animation leverages dynamic properties like stroke color and radius, which are mapped using linear and color scales. Each circle’s position and size are animated over time, creating a pulsating, rotating effect that results in a visually striking pattern.

![creative coding](https://raw.githubusercontent.com/marepilc/pydreamplet/794fa89bf4d11f270c9f08dbd9ab20b50444203c/docs/getting_started/assets/getting_started_img_02.svg)

## Usage example

Here's a quick example of how to create a waffle chart using pyDreamplet:

```python
import pydreamplet as dp
from pydreamplet.colors import random_color

data = [130, 65, 108]


def waffle_chart(data, side=300, rows=10, cols=10, gutter=5, colors=["blue"]):
    sorted_data = sorted(data, reverse=True)
    while len(colors) < len(sorted_data):
        colors.append(random_color())

    svg = dp.SVG(side, side)

    total_cells = rows * cols
    total = sum(data)
    proportions = [int(round(d / total * total_cells, 0)) for d in sorted_data]
    print("Proportions:", proportions)

    cell_side = (side - (cols + 1) * gutter) / cols

    cell_group_map = []
    for group_index, count in enumerate(proportions):
        cell_group_map.extend([group_index] * count)

    if len(cell_group_map) < total_cells:
        cell_group_map.extend([None] * (total_cells - len(cell_group_map)))

    paths = {i: "" for i in range(len(sorted_data))}

    for i in range(total_cells):
        col = i % cols
        row = i // cols

        x = gutter + col * (cell_side + gutter)
        y = gutter + row * (cell_side + gutter)

        group = cell_group_map[i]
        if group is not None:
            paths[group] += f"M {x} {y} h {cell_side} v {cell_side} h -{cell_side} Z "

    for group_index, d_str in paths.items():
        if d_str:
            path = dp.Path(d=d_str, fill=colors[group_index])
            svg.append(path)

    return svg


svg = waffle_chart(data)
svg.display()  # in jupyter notebook
svg.save("waffle_chart.svg")
```

![waffle chart](https://raw.githubusercontent.com/marepilc/pydreamplet/794fa89bf4d11f270c9f08dbd9ab20b50444203c/docs/blog/posts/assets/waffle_chart/waffle_chart.svg)
## Contributing

I welcome contributions from the community! Whether you have ideas for new features, bug fixes, or improvements to the documentation, your **input is invaluable**.

- **Open an Issue:** Found a bug or have a suggestion? Open an issue on GitHub.
- **Submit a Pull Request:** Improve the code or documentation? I’d love to review your PR.
- **Join the Discussion:** Get involved in discussions and help shape the future of **pyDreamplet**.

## License

This project is licensed under the MIT License.
