# Changelog

All notable changes for pyDreamplet 2.x are tracked here while the `version-2`
branch is in progress.

## 2.1.4

### Fixed

- `resolve_collisions_1d()` no longer shifts unrelated labels when resolving
  overflow at the upper bound. Boundary corrections now propagate only through
  the adjacent collision chain.

## 2.1.3

### Changed

- `TypographyMeasurer` now accepts default `font_family` and `weight` values,
  resolves CSS font fallback lists, maps generic font families to system fonts,
  and avoids italic or oblique variants when measuring regular text.

## 2.1.2

### Fixed

- `ColorScale` now accepts supported CSS color strings such as `oklch(...)`,
  allowing it to work directly with `Theme` color tokens.

## 2.1.0

### Added

- Added `Theme` and `Color` for reusable font settings and color tokens.
- Added `blend_colors()` as the explicit two-color blending helper. The shorter
  `blend()` name remains available for compatibility.
- Added `AnimateTransform` for SVG `<animateTransform>` transform animations.

### Changed

- `Color` tokens now accept CSS color strings, grayscale integers, RGB tuples,
  and RGBA tuples while normalizing Python color values to SVG/CSS strings.
- `Theme` now exposes color tokens directly, so `theme.amber` and
  `theme.colors.amber` are equivalent.
- Default named theme colors now use Tailwind CSS 4.3 shade `500`; `surface`
  uses `zinc-100` and `ink` uses `zinc-800`.
- Color blending now accepts hex, grayscale integers, RGB/RGBA tuples,
  `rgb(...)`, `rgba(...)`, and `oklch(...)` inputs.

## 2.0.0

### Breaking Changes

- `TypographyMeasurer.measure_text()` now requires `font_family`, `weight`, and
  `font_size` to be passed as keyword arguments after `text`.
- Notebook display dependencies are no longer installed by default. Install the
  `notebook` extra to use `SVG.display()` in environments that do not already
  provide IPython.
- `arc()` now treats `start_angle == end_angle` as a zero-length arc instead of
  a full circle.
- `ring()` now treats `start_angle == end_angle` as an empty path instead of a
  full ring.
- `arc()` and `ring()` now preserve clockwise/counter-clockwise direction based
  on the sign of `end_angle - start_angle`.
- Shape helpers now validate degenerate inputs and may raise `ValueError` where
  previous versions emitted invalid or surprising path data.
- Text measurement now uses HarfBuzz/fontTools instead of Pillow, so measured
  dimensions may differ.

### Fixed

- Fixed `pos` handling in `Circle`, `Ellipse`, and `Rect` constructors.
  Passing `pos=Vector(...)` now maps to `cx`/`cy` or `x`/`y` before SVG
  attributes are created, so serialized output no longer includes invalid
  `pos="Vector(...)"` attributes.
- Fixed `Noise` validation so invalid bounds and `noise_range` values fail
  explicitly, while zero and full-range noise windows are handled correctly.
- Fixed seeded noise permutation generation for `seed=0`.
- Brought one-dimensional simplex noise closer to the classic simplex gradient
  formulation and restored a useful `[0, amplitude]` output range.

### Changed

- Added `url` properties to reusable SVG definitions and markers for clearer
  `url(#id)` references. The older `id_ref` properties remain as aliases.
- Added `Use` for SVG `<use>` elements, including `SvgElement` references and
  automatic `#id` normalization.
- Added a first-pass `pydreamplet.generators` module for D3-like data-to-path
  generation, including line, area, radial line, radial area, arc, pie, symbol,
  and link generators.
- Added reusable shape helpers for superellipses, rounded polygons, and
  deterministic organic blob paths.
- Added collision and label-placement helpers for infographic layouts, including
  bounding-box overlap checks and one-dimensional label spacing.
- Moved notebook display dependencies out of the core runtime dependency set.
  `ipython` and `ipykernel` are now available through the optional `notebook`
  extra instead of being installed by default.
- Made `SVG.display()` import IPython lazily, so importing `pydreamplet` does
  not require notebook dependencies.
- Fixed the MkDocs Material dark-mode palette configuration typo, changing
  `mediia` to `media`.
- Replaced broad silent exception handling in transform, typography, and color
  parsing with explicit parsing errors or documented fallback behavior.
- Added basedpyright configuration for the current dynamic SVG API surface.
- Decided to keep dynamic SVG attribute access for v2.0, with typed helpers and
  documentation planned as the path to better discoverability.
- Improved `SVG.from_file()` parsing to preserve root attributes, support
  decimal `viewBox` values, and derive a missing `viewBox` from dimensions.
- Isolated path data coordinate extraction into a dedicated helper used by
  `Path.w`, `Path.h`, and `Path.center`.
- Centralized shared numeric type aliases in `pydreamplet.types`.
- Replaced Pillow-based text measurement with HarfBuzz shaping and fontTools
  metrics, and removed Pillow from core runtime dependencies.
- Made `TypographyMeasurer.measure_text()` accept `Text` and `TextOnPath`
  elements directly, reading content and font attributes from the element.
- Updated installation documentation to show `uv` first and `pip` second,
  including notebook extra installation examples.
- Added a base `[mypy]` section and configured mypy to ignore missing
  `uharfbuzz` stubs.
- Split local dependency groups for development and documentation tooling.
- Kept HarfBuzz and fontTools as default runtime dependencies because text
  measurement is a common pyDreamplet workflow.
- Added Ruff configuration and expanded CI to run pytest, basedpyright, mypy,
  Ruff, documentation build, package build, and wheel install smoke checks on
  pinned Python versions.
- Added Python 3.14 to the CI test matrix for the v2.0 release line.
- Reduced default GitHub Actions permissions and limited `contents: write` to
  the documentation deploy job.
- Added an API design document defining the public/private boundary,
  compatibility rules, dynamic SVG attribute policy, typed helper direction, and
  intended module layers for v2.x.
- Clarified that v2.0 may intentionally break v1.x compatibility when the change
  improves the long-term API.
- Expanded the top-level `pydreamplet` import surface for commonly used public
  APIs while keeping specialized modules available for focused imports.
- Migrated the documentation to a Nuxt Content/Nuxt UI site with a home page,
  getting started guides, searchable reference pages, tutorials, SVG previews,
  generated assets, dark/light theme support, and top-level navigation.
- Ported the legacy layered SVG art tutorial and blog examples into the new
  Tutorials section, updating code for the current API.
- Added visual examples across the reference section so API pages show what the
  documented code produces.

### Tests

- Added feature tests for the new generator layer, including accessor-based
  line/area generation, undefined data gaps, radial projection, pie slice
  metadata, arc paths, symbols, and link curves.
- Added feature tests for superellipse, rounded polygon, and blob path
  generation.
- Added feature tests for collision detection and one-dimensional label
  placement helpers.
- Added regression tests for `pos` constructor serialization on `Circle`,
  `Ellipse`, and `Rect`.
- Added regression tests proving package import does not require IPython and
  that `SVG.display()` reports missing notebook dependencies clearly.
- Added regression tests for malformed and unsupported group transform parsing.
- Added regression tests for path bounds with relative commands, horizontal and
  vertical lines, curves, arcs, and repeated move coordinates.
- Added typography tests for explicit font paths and multiline measurements.
- Added typography coverage for measuring a `Text` element directly.
- Added regression tests for malformed SVG files, invalid and non-integer
  `viewBox` values, decimal dimensions, and path data edge cases.
- Added public API import tests for the expanded top-level import surface.
- Added noise regression tests for `noise_range`, invalid bounds, seeded
  permutation generation, and simplex output behavior.
- Added current documentation code-block tests that parse Nuxt Content examples
  and execute portable guide/tutorial snippets against the public API.
- Cleaned up test typing so basedpyright can validate both `pydreamplet` and the
  test suite as part of the release checks.
