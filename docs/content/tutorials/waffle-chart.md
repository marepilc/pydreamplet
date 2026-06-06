---
title: Waffle Chart
description: Build a proportional 10 by 10 waffle chart with SVG path cells.
navigation:
  title: Waffle chart
category: tutorials
---

# Waffle Chart

A waffle chart uses a fixed grid to show proportions. A 10 by 10 grid is a good
default because each cell represents one percent.

## Data and Layout

```python
import pydreamplet as dp

data = [130, 65, 108]
data.sort(reverse=True)

side = 300
side_count = 10
gutter = 5
total_cells = side_count**2
total = sum(data)
```

Convert each value to a number of cells.

```python
proportions = [round(value / total * total_cells) for value in data]
cell_side = (side - (side_count + 1) * gutter) / side_count
```

Build a list that maps each cell index to a group.

```python
cell_group_map = []
for group_index, count in enumerate(proportions):
    cell_group_map.extend([group_index] * count)

if len(cell_group_map) < total_cells:
    cell_group_map.extend([None] * (total_cells - len(cell_group_map)))
```

## Cell Paths

Drawing one path per group is more compact than appending 100 separate
rectangles.

```python
paths = {index: "" for index in range(len(data))}

for index in range(total_cells):
    column = index % side_count
    row = index // side_count

    x = gutter + column * (cell_side + gutter)
    y = gutter + row * (cell_side + gutter)

    group = cell_group_map[index]
    if group is not None:
        paths[group] += f"M {x} {y} h {cell_side} v {cell_side} h -{cell_side} Z "
```

## Draw the Chart

```python
svg = dp.SVG(side, side)
colors = ["#14b8a6", "#f59e0b", "#6366f1"]

for group_index, path_data in paths.items():
    if path_data:
        svg.append(dp.Path(d=path_data, fill=colors[group_index]))

svg.save("waffle-chart.svg")
```

::svg-preview{src="/showcase/tutorial_waffle_chart.svg" alt="Three-color 10 by 10 waffle chart."}
::

