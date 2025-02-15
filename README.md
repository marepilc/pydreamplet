# pyDreamplet

low level library for SVG image generation. Perfect for data visualization with Python.

## Installation

With poetry:

```schell
poetry add pydreamplet

With pip:

```schell
pip install pydreamplet
```

## Documentation

[https://marepilc.github.io/pydreamplet/](https://marepilc.github.io/pydreamplet/)

## Usage example


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