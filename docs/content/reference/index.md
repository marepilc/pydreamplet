---
title: Reference
description: API reference for pyDreamplet primitives, helpers, and SVG output.
---

# Reference

This section collects focused API notes for pyDreamplet primitives and output helpers.

Start here when you already know the basic drawing flow and need exact constructor shapes, properties, or output behavior.

## Core

- [SVG](/reference/svg) - root document, viewBox, dimensions, saving, and loading.
- [SvgElement](/reference/svg-element) - shared attribute, child, search, copy, and serialization API.

## Drawing Elements

- [Shapes](/reference/shapes) - `Circle`, `Ellipse`, `Rect`, `Line`, `Polygon`, and `Polyline`.
- [Paths](/reference/paths) - `Path`, `PathBuilder`, parsing, normalization, linear measurement, and bounding boxes.
- [Transforms](/reference/transforms) - `G`, `Transform`, `TransformList`, and `Matrix2D`.
- [Text](/reference/text) - `Text`, multiline `tspan` output, `TextOnPath`, and font-size behavior.
- [Animation](/reference/animation) - `Animate`, keyframe values, duration, and repeat count.
- [Definitions](/reference/definitions) - `Defs`, gradients, stops, patterns, masks, clip paths, and filters.
- [Scales](/reference/scales) - numeric, categorical, color, square-root, and circle-area scales.
- [Creative helpers](/reference/creative) - top-level point and tile layout helpers.
- [Path generators](/reference/generators) - data-driven line, area, radial, pie, arc, symbol, and link path generators.
- [Shape helpers](/reference/shape-helpers) - path `d` string helpers for stars, curves, rings, and organic shapes.
- [Vector](/reference/vector) - 2D coordinates, arithmetic, magnitude, direction, normalization, and limiting.
- [Colors](/reference/colors) - top-level color conversion, blending, random color, and palette helpers.
- [Typography](/reference/typography) - system font lookup and HarfBuzz/fontTools text measurement.
- [Noise](/reference/noise) - bounded random-walk values and deterministic simplex noise.
- [Utilities](/reference/utilities) - numeric, angle, tick, pie, sampling, and collision helpers.
- [Markers](/reference/markers) - SVG marker elements and predefined arrow, tick, and symbol path constants.

## Planned next

- Audit remaining reference coverage
