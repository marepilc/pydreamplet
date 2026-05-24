# pyDreamplet 2.0 Roadmap

This document tracks the current state of pyDreamplet and the work needed to make
version 2.0 a strong foundation for advanced infographics, data-driven SVG, and
creative coding with Python.

## Product Direction

pyDreamplet should remain a lightweight, expressive Python library for generating
SVG, but version 2.0 should move beyond being only a low-level SVG wrapper. The
goal is closer to "D3.js for Python" than to another plotting library: composable
primitives, data-to-visual mapping, shape/path generators, layouts, and precise
SVG control.

The target shape is a layered library:

- A stable SVG core for elements, attributes, transforms, serialization, and import.
- Geometry and path utilities for reliable curves, arcs, bounding boxes, and layouts.
- Shape, line, area, symbol, arc, and curve generators inspired by D3's composable model.
- Scales, colors, typography, and data utilities for visualization work.
- Axis, legend, annotation, and layout primitives rather than fixed chart components.
- Creative coding helpers for generative visuals, noise, grids, tiling, and animation.
- Optional ecosystem tooling for agentic coding, example generation, and MCP integration.
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
- [x] Typography measurement exists through HarfBuzz and fontTools.
- [x] Noise helpers exist, including 1D, 2D, and 3D simplex noise.
- [x] Marker helpers and predefined marker path constants exist.
- [x] Package includes bundled SVG resources.
- [x] `py.typed` is included for type-aware consumers.
- [x] Test suite exists and currently passes locally.
- [x] Documentation exists in MkDocs with tutorials, reference pages, blog posts, and SVG assets.
- [x] Documentation code blocks are tested by `tests/test_doc.py`.
- [x] GitHub Actions CI exists for tests and documentation deployment.

## Known Issues To Fix Before 2.0

- [x] Fix `pos` handling in `Circle`, `Ellipse`, and `Rect`.
  These constructors currently pass `pos` into `SvgElement` before converting it to
  `cx/cy` or `x/y`, which creates invalid SVG attributes such as
  `pos="Vector(x=1.0, y=2.0)"`.
- [x] Move IPython and ipykernel out of core runtime dependencies.
  Notebook display support should be optional and imported lazily.
- [x] Fix `mkdocs.yml` dark-mode typo: `mediia` should be `media`.
- [x] Replace broad `except Exception: pass` blocks with explicit parsing failures or
  documented fallback behavior.
- [x] Decide how strict unknown SVG attribute access should be.
  The current dynamic `__getattr__`/`__setattr__` model is convenient, but it makes
  typing and API discoverability harder.
- [x] Improve `SVG.from_file()` parsing.
  It currently assumes an integer `viewBox` and should support decimals, missing
  viewBox values, dimensions, and existing root attributes more robustly.
- [x] Replace or isolate the simplistic path coordinate parser used by `Path.w`,
  `Path.h`, and `Path.center`.
- [x] Improve text measurement accuracy.
  Typography measurement now uses HarfBuzz shaping with fontTools metrics instead
  of Pillow bounding boxes.
- [x] Add tests for malformed SVG input, path edge cases, and non-integer viewBox values.

## Packaging And Tooling

- [x] Split dependencies into clearer groups:
  - core runtime
  - notebook/Jupyter
  - docs
  - dev/test
- [x] Remove `ipykernel` from default install.
- [x] Decide whether HarfBuzz and fontTools should be optional under a
  `typography` extra.
  Text measurement is common enough for pyDreamplet that HarfBuzz and fontTools
  stay in the default runtime dependency set.
- [x] Revisit typography dependencies after choosing the more accurate text
  measurement backend.
- [x] Add a real `[mypy]` section to `mypy.ini`.
- [ ] Enable stricter type checking gradually, starting with stable public APIs:
  - [x] Keep `basedpyright pydreamplet` green in CI.
  - [ ] Enable stricter checks module by module for less dynamic modules first:
    `types.py`, `math.py`, `path_data.py`, `colors.py`, `scales.py`, and `utils.py`.
  - [x] Add typed helper APIs for common SVG attributes before tightening
    `core.py`.
  - [ ] Keep dynamic `SvgElement.__getattr__` / `__setattr__` as the documented
    escape hatch.
  - [ ] Tighten `core.py` only after typed constructors or helpers cover common
    public usage.
- [x] Add Ruff configuration to `pyproject.toml`.
- [x] Add Ruff lint checks to CI.
- [x] Add `uv run mypy pydreamplet` to CI.
- [x] Add package build verification to CI.
- [x] Add wheel install smoke test to CI.
- [x] Pin CI Python versions explicitly, for example `3.12` and latest stable.
- [x] Reduce default GitHub Actions permissions and grant `contents: write` only to
  the documentation deploy job.

## Core API Goals

- [x] Define a clear public/private API boundary.
- [x] Document backward compatibility rules for v2.x.
- [x] Decide whether dynamic SVG attributes remain the main API or become a lower-level escape hatch.
- [x] Add typed constructors for common elements while keeping flexible SVG attributes available.
- [x] Introduce a consistent `Point`/`Vector`/tuple input policy.
  First pass supports `Vector`, `(x, y)`, and `[x, y]` for common positioned
  elements and `set_position()`.
- [x] Add convenience methods for setting position, size, stroke, fill, class, id, and style.
- [x] Make copy, append, remove, find, and find_all behavior explicit and tested.
- [x] Add support for SVG `defs`, gradients, patterns, masks, clip paths, and filters.
- [x] Add a stronger transform model:
  - [x] parse transforms
  - [x] preserve transform order
  - [x] compose transforms
  - [x] support pivot/origin behavior consistently
- [x] Improve XML namespace handling and round-trip behavior.

## Geometry And Paths

- [x] Add a path builder API instead of requiring manual `d` strings.
- [x] Support SVG commands: `M`, `L`, `H`, `V`, `C`, `S`, `Q`, `T`, `A`, `Z`.
- [x] Support relative and absolute commands.
- [x] Add path normalization utilities.
- [x] Add path parsing as a first-class capability, separate from the `Path` element wrapper.
- [x] Add path measurement utilities:
  - [x] total length
  - [x] point at length
  - [x] tangent at length
  - [x] segment iteration
- [x] Add robust bounding boxes for lines, rectangles, circles, ellipses, polygons,
  polylines, and paths.
- [x] Add arc and ring helpers with tested sweep/large-arc behavior.
- [x] Add curve interpolation helpers for paths through points:
  - [x] linear
  - [x] step
  - [x] basis spline
  - [x] cardinal spline
  - [x] Catmull-Rom
  - [x] monotone X/Y
  - [x] closed curves
- [ ] Add generators that return SVG path data from data points:
  - line generator
  - area generator
  - radial line generator
  - radial area generator
  - arc generator
  - pie angle generator
  - symbol generator
  - link/edge generator
- [ ] Add shape generators for reusable geometric forms:
  - regular polygon
  - star
  - cross
  - superellipse
  - rounded polygon
  - blob/metaball-like organic shapes
- [ ] Add collision and label-placement utilities for infographic layouts.

## Data Visualization Primitives

- [ ] Treat complete charts as examples and recipes, not as the primary API.
- [ ] Avoid locking the library into fixed `BarChart`, `LineChart`, or similar classes
  unless they are optional recipes built on top of lower-level primitives.
- [ ] Introduce a D3-like generator layer for data-to-SVG conversion.
- [ ] Introduce Pythonic data binding helpers for turning sequences of data into SVG elements.
- [ ] Add selection/grouping helpers if they can stay simple and idiomatic in Python.
- [ ] Define layout primitives:
  - margin box
  - plotting frame
  - stack layout
  - pack layout
  - treemap layout
  - force layout
  - chord/ribbon layout
  - grid layout
  - radial layout
- [ ] Add axis generation as composable primitives using scales and tick helpers.
- [ ] Add legend generation as composable primitives.
- [ ] Add annotation helpers:
  - callouts
  - leader lines
  - brackets
  - ranges
  - highlighted regions
- [ ] Add map/geography primitives if they can be kept lightweight:
  - load bundled SVG maps
  - map regions by id
  - project points onto known SVG coordinate spaces
  - generate choropleth-like fills without becoming a full GIS package
- [ ] Add color palettes designed for categorical and sequential data.
- [ ] Add accessibility helpers for titles, descriptions, roles, and readable SVG metadata.
- [ ] Add examples that show real infographic workflows built from primitives.

## Creative Coding Layer

- [ ] Expand noise utilities with deterministic seeding examples.
- [ ] Add generative grid helpers.
- [ ] Add tiling and pattern helpers.
- [ ] Add point cloud and distribution generators.
- [ ] Add parametric curve helpers.
- [ ] Add polar/radial helper functions.
- [ ] Add particle/flow field examples.
- [ ] Add animation examples based on native SVG animation.
- [ ] Add reusable creative presets that remain editable as plain SVG.

## Agentic Coding And MCP Ecosystem

- [ ] Treat agentic tooling as a separate ecosystem layer, not as part of the core runtime.
- [ ] Create a Codex/agent skill for generating pyDreamplet examples from short creative briefs.
- [ ] Create an agent skill for converting sketches or chart descriptions into pyDreamplet code.
- [ ] Create an agent skill for debugging generated SVG output and suggesting simplifications.
- [ ] Consider an MCP server exposing:
  - component and API reference
  - runnable example search
  - SVG asset search
  - path/shape generator documentation
  - project templates
- [ ] Keep MCP and agent skills versioned alongside documentation, so agents use the correct API.
- [ ] Use the MCP server or skills to support documentation authoring and example generation.

## Documentation

- [x] MkDocs documentation exists.
- [x] Getting started guide exists.
- [x] API reference pages exist.
- [x] Blog examples exist.
- [x] Documentation uses generated SVG assets.
- [x] Documentation code blocks are tested.
- [ ] Fix spelling and wording issues in current docs and README.
- [ ] Add a v2.0 concept page explaining the D3-like layered architecture.
- [ ] Add a gallery of examples as a primary documentation entry point.
- [ ] Add a page for design principles and API philosophy.
- [ ] Add a "Generators" documentation section for paths, curves, shapes, symbols, and layouts.
- [ ] Add a "Recipes" section for full infographic examples built from primitives.
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
- [ ] Add tests for path, shape, curve, and layout generators.
- [ ] Add tests for generated full-example recipes where useful.
- [ ] Add tests for serialization round-trips.
- [ ] Add tests for deterministic creative coding outputs with seeds.
- [ ] Add CI matrix for supported Python versions.

## Release Readiness For 2.0

- [ ] Define the v2.0 public API.
- [ ] Decide what v1.x APIs are deprecated, removed, or kept.
- [ ] Add deprecation warnings where needed before final 2.0 release.
- [ ] Publish migration guide.
- [ ] Build complete example gallery.
- [ ] Ensure docs cover installation, quick start, generators, layouts, infographics,
  creative coding, API reference, and migration.
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

- [x] Write the public API design document.
- [x] Decide module boundaries.
- [x] Define compatibility rules.
- [ ] Design the generator, layout, scale, axis, legend, and annotation layers.
- [ ] Create one complete vertical slice, such as a polished custom infographic built
  from primitives rather than a fixed chart class.

### Milestone 3: Build D3-Like Visualization Primitives

- [ ] Implement path and shape generators.
- [ ] Implement curve interpolation through points.
- [ ] Implement axes, legends, labels, annotations, and layout helpers.
- [ ] Implement recipes that demonstrate how to compose primitives into full visuals.
- [ ] Add real-world infographic examples.
- [ ] Add SVG snapshots for examples.

### Milestone 4: Documentation And Agent Tooling

- [ ] Prepare current docs for migration.
- [ ] Build the Nuxt Content documentation site.
- [ ] Port current pages and assets.
- [ ] Add custom example/gallery components.
- [ ] Add generator and recipe documentation.
- [ ] Decide whether to ship agent skills or an MCP server as a separate package/repo.
- [ ] Deploy the new docs site.

### Milestone 5: 2.0 Release

- [ ] Finish migration guide.
- [ ] Run full test, typecheck, build, and docs validation.
- [ ] Publish release candidate.
- [ ] Collect feedback.
- [ ] Publish stable 2.0.
