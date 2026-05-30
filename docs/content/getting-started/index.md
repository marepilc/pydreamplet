---
title: Getting started
description: Install pyDreamplet and create your first SVG.
navigation:
  title: Getting started
category: guide
---

# Getting Started

This section covers the first workflow: install pyDreamplet, create an SVG
canvas, draw a shape, and save the result.

## Installation

Install the core package with `uv`:

```shell
uv add pydreamplet
```

Or with `pip`:

```shell
pip install pydreamplet
```

For notebook display support, install the optional notebook extra:

```shell
uv add "pydreamplet[notebook]"
```

```shell
pip install "pydreamplet[notebook]"
```

## Your First SVG

Create a canvas, append a shape, then save the SVG file:

```python
import pydreamplet as dp

svg = dp.SVG(300, 300)

circle = dp.Circle(
    cx=150,
    cy=150,
    r=90,
    fill="#14b8a6",
    stroke="#0f172a",
    stroke_width=4,
)

svg.append(circle)
svg.save("example.svg")
```

In a notebook, use `display()` to render the result inline:

```python
svg.display()
```

## Core Ideas

pyDreamplet mirrors the structure of SVG. You create elements, configure their
attributes, append them to a parent, and export the result.

- `SVG` is the root canvas.
- Shape classes such as `Circle`, `Rect`, `Line`, `Path`, and `Text` map to SVG
  elements.
- `G` groups elements and lets you move or transform them together.
- Scales and generators help turn data into visual geometry.

## Next

The next chunk should cover the basic drawing workflow in more detail: canvas
size, coordinates, common shapes, styling, display, and saving.
