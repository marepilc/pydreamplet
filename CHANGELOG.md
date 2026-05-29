# Changelog

All notable changes for pyDreamplet 2.0 are tracked here while the `version-2`
branch is in progress.

## Unreleased

### Fixed

- Fixed `pos` handling in `Circle`, `Ellipse`, and `Rect` constructors.
  Passing `pos=Vector(...)` now maps to `cx`/`cy` or `x`/`y` before SVG
  attributes are created, so serialized output no longer includes invalid
  `pos="Vector(...)"` attributes.

### Changed

- Added a first-pass `pydreamplet.generators` module for D3-like data-to-path
  generation, including line, area, radial line, radial area, arc, pie, symbol,
  and link generators.
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
- Reduced default GitHub Actions permissions and limited `contents: write` to
  the documentation deploy job.
- Added an API design document defining the public/private boundary,
  compatibility rules, dynamic SVG attribute policy, typed helper direction, and
  intended module layers for v2.x.
- Clarified that v2.0 may intentionally break v1.x compatibility when the change
  improves the long-term API.

### Tests

- Added feature tests for the new generator layer, including accessor-based
  line/area generation, undefined data gaps, radial projection, pie slice
  metadata, arc paths, symbols, and link curves.
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
