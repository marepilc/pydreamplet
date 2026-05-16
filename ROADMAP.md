# pyDreamplet 2.0 Roadmap

This document tracks the current state of pyDreamplet and the work needed to make
version 2.0 a strong foundation for advanced infographics, charts, and creative
coding with Python.

## Product Direction

pyDreamplet should remain a lightweight, expressive Python library for generating
SVG, but version 2.0 should move beyond being only a low-level SVG wrapper.

The target shape is a layered library:

- A stable SVG core for elements, attributes, transforms, serialization, and import.
- Geometry and path utilities for reliable curves, arcs, bounding boxes, and layout.
- Scales, colors, typography, and data utilities for visualization work.
- Higher-level marks and chart components for common infographic patterns.
- Creative coding helpers for generative visuals, noise, grids, tiling, and animation.
- Documentation centered on rich examples, not only API reference pages.

## Current Foundation

- [x] Python package exists as `pydreamplet`.
- [x] Package exposes a small public API through `pydreamplet.__init__`.
- [x] Core SVG elements are implemented: `SVG`, `SvgElement`, `G`, `Circle`, `Ellipse`,
  `Rect`, `Line`, `Path`, `Polygon`, `Polyline`, `Text`, `TextOnPath`, `Animate`.
- [x] Basic transform support exists through `Transformable` and `G`.
- [x] SVG serialization, pretty printing, saving, and loading from file exist.
- [x] Shape helper functions exist for stars, polygons, arcs, rings, crosses, splines,
  and polylines.
- [x] Scale helpers exist: linear, band, point, ordinal, color, square, and circle scales.
- [x] Color helpers exist for conversion, blending, random colors, and palette generation.
- [x] Typography measurement exists through Pillow and fontTools.
- [x] Noise helpers exist, including 1D, 2D, and 3D simplex noise.
- [x] Marker helpers and predefined marker path constants exist.
- [x] Package includes bundled SVG resources.
- [x] `py.typed` is included for type-aware consumers.
- [x] Test suite exists and currently passes locally.
- [x] Documentation exists in MkDocs with tutorials, reference pages, blog posts, and SVG assets.
- [x] Documentation code blocks are tested by `tests/test_doc.py`.
- [x] GitHub Actions CI exists for tests and documentation deployment.

## Known Issues To Fix Before 2.0

- [ ] Fix `pos` handling in `Circle`, `Ellipse`, and `Rect`.
  These constructors currently pass `pos` into `SvgElement` before converting it to
  `cx/cy` or `x/y`, which creates invalid SVG attributes such as
  `pos="Vector(x=1.0, y=2.0)"`.
- [ ] Move IPython and ipykernel out of core runtime dependencies.
  Notebook display support should be optional and imported lazily.
- [ ] Fix `mkdocs.yml` dark-mode typo: `mediia` should be `media`.
- [ ] Replace broad `except Exception: pass` blocks with explicit parsing failures or
  documented fallback behavior.
- [ ] Decide how strict unknown SVG attribute access should be.
  The current dynamic `__getattr__`/`__setattr__` model is convenient, but it makes
  typing and API discoverability harder.
- [ ] Improve `SVG.from_file()` parsing.
  It currently assumes an integer `viewBox` and should support decimals, missing
  viewBox values, dimensions, and existing root attributes more robustly.
- [ ] Replace or isolate the simplistic path coordinate parser used by `Path.w`,
  `Path.h`, and `Path.center`.
- [ ] Add tests for malformed SVG input, path edge cases, and non-integer viewBox values.

## Packaging And Tooling

- [ ] Split dependencies into clearer groups:
  - core runtime
  - notebook/Jupyter
  - docs
  - dev/test
- [ ] Remove `ipykernel` from default install.
- [ ] Consider whether Pillow and fontTools should be optional under a `typography`
  extra if text measurement is not required by the core package.
- [ ] Add a real `[mypy]` section to `mypy.ini`.
- [ ] Enable stricter type checking gradually, starting with core public APIs.
- [ ] Add Ruff configuration to `pyproject.toml`.
- [ ] Add formatting/lint checks to CI.
- [ ] Add `uv run mypy pydreamplet` to CI.
- [ ] Add package build verification to CI.
- [ ] Add wheel install smoke test to CI.
- [ ] Pin CI Python versions explicitly, for example `3.12` and latest stable.
- [ ] Reduce default GitHub Actions permissions and grant `contents: write` only to
  the documentation deploy job.

## Core API Goals

- [ ] Define a clear public/private API boundary.
- [ ] Document backward compatibility rules for v2.x.
- [ ] Decide whether dynamic SVG attributes remain the main API or become a lower-level escape hatch.
- [ ] Add typed constructors for common elements while keeping flexible SVG attributes available.
- [ ] Introduce a consistent `Point`/`Vector`/tuple input policy.
- [ ] Add convenience methods for setting position, size, stroke, fill, class, id, and style.
- [ ] Make copy, append, remove, find, and find_all behavior explicit and tested.
- [ ] Add support for SVG `defs`, gradients, patterns, masks, clip paths, and filters.
- [ ] Add a stronger transform model:
  - parse transforms
  - preserve transform order
  - compose transforms
  - support pivot/origin behavior consistently
- [ ] Improve XML namespace handling and round-trip behavior.

## Geometry And Paths

- [ ] Add a path builder API instead of requiring manual `d` strings.
- [ ] Support SVG commands: `M`, `L`, `H`, `V`, `C`, `S`, `Q`, `T`, `A`, `Z`.
- [ ] Support relative and absolute commands.
- [ ] Add path normalization utilities.
- [ ] Add robust bounding boxes for lines, rectangles, circles, ellipses, polygons,
  polylines, and paths.
- [ ] Add arc and ring helpers with tested sweep/large-arc behavior.
- [ ] Add curve interpolation helpers suitable for line charts and creative coding.
- [ ] Add collision and label-placement utilities for infographic layouts.

## Data Visualization Layer

- [ ] Introduce a `marks` layer for reusable visual primitives:
  - bar
  - line
  - area
  - scatter point
  - label
  - axis
  - grid
  - legend
  - annotation
- [ ] Introduce chart-level helpers for common use cases:
  - line chart
  - bar chart
  - scatter plot
  - waffle chart
  - pie/donut chart
  - radial chart
  - map-based visualization
- [ ] Define a chart layout model with margins, plotting area, titles, captions, and legends.
- [ ] Add axis generation using scales and tick helpers.
- [ ] Add color palettes designed for categorical and sequential data.
- [ ] Add accessibility helpers for titles, descriptions, roles, and readable SVG metadata.
- [ ] Add examples that show real infographic workflows, not only primitive drawing.

## Creative Coding Layer

- [ ] Expand noise utilities with deterministic seeding examples.
- [ ] Add generative grid helpers.
- [ ] Add tiling and pattern helpers.
- [ ] Add particle/flow field examples.
- [ ] Add animation examples based on native SVG animation.
- [ ] Add reusable creative presets that remain editable as plain SVG.

## Documentation

- [x] MkDocs documentation exists.
- [x] Getting started guide exists.
- [x] API reference pages exist.
- [x] Blog examples exist.
- [x] Documentation uses generated SVG assets.
- [x] Documentation code blocks are tested.
- [ ] Fix spelling and wording issues in current docs and README.
- [ ] Add a v2.0 concept page explaining the layered architecture.
- [ ] Add a gallery of examples as a primary documentation entry point.
- [ ] Add a page for design principles and API philosophy.
- [ ] Add migration notes from v1.x to v2.0.
- [ ] Add more complete reference documentation for each public class and function.
- [ ] Add visual regression or snapshot strategy for generated SVG examples.
- [ ] Ensure every major feature has a runnable example.

## Nuxt Content Documentation Migration

- [ ] Keep the existing MkDocs site until the Nuxt Content site reaches feature parity.
- [ ] Inventory all current Markdown pages and assets.
- [ ] Add frontmatter to documentation pages:
  - `title`
  - `description`
  - `navigation`
  - `category`
  - `version`
- [ ] Move reusable static assets into a Nuxt-compatible structure.
- [ ] Convert MkDocs-specific Markdown syntax to Nuxt Content/MDC equivalents.
- [ ] Build custom documentation components:
  - example preview
  - code/result split view
  - SVG preview
  - API signature block
  - parameter table
  - gallery item
- [ ] Decide whether API reference pages are handwritten, generated, or hybrid.
- [ ] Add search.
- [ ] Add versioned documentation support.
- [ ] Add deployment pipeline for the Nuxt documentation site.
- [ ] Preserve existing documentation URLs where possible, or add redirects.

## Testing Strategy

- [x] Unit and feature tests exist.
- [x] Documentation code blocks are tested.
- [x] Current local test result: `161 passed`.
- [ ] Add stricter tests around public API contracts.
- [ ] Add tests for optional dependencies being absent.
- [ ] Add tests for package import speed and minimal import behavior.
- [ ] Add SVG snapshot tests for complex generated examples.
- [ ] Add tests for generated chart components.
- [ ] Add tests for serialization round-trips.
- [ ] Add tests for deterministic creative coding outputs with seeds.
- [ ] Add CI matrix for supported Python versions.

## Release Readiness For 2.0

- [ ] Define the v2.0 public API.
- [ ] Decide what v1.x APIs are deprecated, removed, or kept.
- [ ] Add deprecation warnings where needed before final 2.0 release.
- [ ] Publish migration guide.
- [ ] Build complete example gallery.
- [ ] Ensure docs cover installation, quick start, charts, infographics, creative coding,
  API reference, and migration.
- [ ] Verify package metadata on PyPI.
- [ ] Verify source distribution and wheel contents.
- [ ] Verify fresh install in a clean environment.
- [ ] Tag release candidate.
- [ ] Test release candidate against documentation examples.
- [ ] Publish v2.0.

## Suggested Milestones

### Milestone 1: Stabilize The Existing Library

- [ ] Fix constructor bugs and small documentation configuration issues.
- [ ] Clean dependency groups.
- [ ] Strengthen CI.
- [ ] Improve mypy and linting configuration.
- [ ] Add missing tests around the current public API.

### Milestone 2: Define The v2.0 Architecture

- [ ] Write the public API design document.
- [ ] Decide module boundaries.
- [ ] Define compatibility rules.
- [ ] Design the chart and mark layer.
- [ ] Create one complete vertical slice, such as a production-quality line chart.

### Milestone 3: Build High-Level Visualization Features

- [ ] Implement marks.
- [ ] Implement axes, legends, labels, and layout helpers.
- [ ] Implement core chart helpers.
- [ ] Add real-world infographic examples.
- [ ] Add SVG snapshots for examples.

### Milestone 4: Documentation Platform

- [ ] Prepare current docs for migration.
- [ ] Build the Nuxt Content documentation site.
- [ ] Port current pages and assets.
- [ ] Add custom example/gallery components.
- [ ] Deploy the new docs site.

### Milestone 5: 2.0 Release

- [ ] Finish migration guide.
- [ ] Run full test, typecheck, build, and docs validation.
- [ ] Publish release candidate.
- [ ] Collect feedback.
- [ ] Publish stable 2.0.

