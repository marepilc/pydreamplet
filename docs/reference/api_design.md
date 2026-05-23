---
icon: material/api
---

# API design

This page defines the public API boundary and compatibility rules for
pyDreamplet 2.x. It is intended to keep the library flexible for SVG authoring
while making future additions easier to type, document, and maintain.

## Public API

The primary public API is the set of names exported from `pydreamplet`:

- `SVG`, `SvgElement`, `G`, and `Transformable` behavior exposed through element
  classes.
- Shape and SVG element classes such as `Circle`, `Ellipse`, `Rect`, `Line`,
  `Path`, `Polygon`, `Polyline`, `Text`, `TextOnPath`, and `Animate`.
- `Vector` for 2D coordinates and vector arithmetic.

Documented modules under `pydreamplet`, such as colors, markers, noise, scales,
shapes, typography, and utils, are also public when their functions or classes
are included in the reference documentation.

Names that start with `_`, private methods, implementation helpers, parser
internals, and undocumented modules are internal. They may change between minor
versions when needed to improve correctness or maintainability.

## Compatibility Rules

pyDreamplet 2.0 may break compatibility with 1.x when the change makes the API
clearer, more consistent, easier to type, or better aligned with SVG behavior.
Version 2.0 should favor a clean long-term foundation over preserving every 1.x
behavior.

After the 2.0 API is stable, pyDreamplet 2.x should follow these compatibility
rules:

- Public constructors, documented properties, and documented return types should
  remain backward compatible within the 2.x series.
- New optional parameters may be added to public functions and constructors when
  the default preserves existing behavior.
- Public behavior should not silently change when the change can reasonably
  break existing SVG output. Prefer a new helper, option, or documented migration
  path.
- Bug fixes may change output when the previous behavior was invalid SVG,
  malformed parsing, or inconsistent with the documented API.
- Internal helpers may change without a deprecation period.

When a breaking public change is necessary, it should be documented in the
changelog and migration notes before the stable 2.0 release. After 2.0, breaking
changes should normally wait for a future major release.

## Dynamic SVG Attributes

SVG has a large and evolving attribute surface. pyDreamplet keeps dynamic
attribute access as part of the public authoring model:

```py
rect = dp.Rect(width=100, height=50)
rect.fill = "tomato"
rect.stroke_width = 2
```

Attribute names use Python-friendly underscores and are serialized as SVG
hyphenated names. For example, `stroke_width` becomes `stroke-width`.

Dynamic attributes are convenient and remain the escape hatch for advanced or
less common SVG attributes. The tradeoff is that type checkers cannot discover
every possible SVG attribute from this model alone.

## Typed Helpers

Typed helpers and typed constructors should be added gradually for common
workflows. They should improve editor completion and type checking without
removing the dynamic attribute escape hatch.

Good candidates for typed helpers include:

- positioning and sizing,
- fill and stroke styling,
- text font settings,
- transforms,
- ids, classes, and metadata,
- `defs`, gradients, patterns, masks, clip paths, and filters.

The dynamic model should remain available even when typed helpers exist.

## Input Types

For coordinates and numeric geometry, pyDreamplet should move toward a consistent
input policy:

- `Vector` is the canonical 2D point type.
- `int` and `float` are accepted for scalar numeric values.
- Tuple or list point inputs may be accepted by convenience APIs when they reduce
  friction, but public behavior should be documented explicitly.

New APIs should avoid accepting broad untyped inputs unless they are deliberately
serving as SVG escape hatches.

## Module Boundaries

The library should evolve toward these layers:

- Core SVG elements and serialization.
- Geometry and path utilities.
- Scales, colors, typography, and data helpers.
- Composable generators for paths, shapes, axes, legends, annotations, and
  layouts.
- Examples and recipes built from lower-level primitives.

Complete charts should usually live as recipes or examples rather than becoming
the main public API surface.
