# pyDreamplet

**pyDreamplet** is a low-level library for SVG image generation — **perfect for creating beautiful data visualizations with Python**. Its intuitive API lets you build complex, scalable SVG graphics effortlessly, making it an ideal choice for projects ranging from simple charts to intricate visualizations.

## Features

- **Lightweight & Flexible:** Generate SVG images with minimal overhead.
- **Easy Integration:** Works seamlessly in Jupyter notebooks, scripts, or web applications.
- **Customizable:** Set any attribute on your SVG elements using simple keyword arguments.
- **No Heavy Dependencies:** Designed to work with just Python’s standard library (plus Pillow and IPython for additional features).

## Installation

Install pyDreamplet using your preferred package manager:

With poetry:

```schell
poetry add pydreamplet
```

With pip:

```schell
pip install pydreamplet
```

## Documentation

For complete documentation, tutorials, and API references, please visit [pyDreampled documentation](https://marepilc.github.io/pydreamplet/)

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