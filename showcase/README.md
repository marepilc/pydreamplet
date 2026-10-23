# pydreamplet-showcase

A collection of SVG examples created with
[pydreamplet](https://github.com/marepilc/pydreamplet).

## Project Layout

```text
scripts/<example>/        Source files for a showcase
  main.py                 Showcase entry point
  *.py                    Optional local modules
  data/                   Data used by this showcase
tools/motives/            Light and dark color motives
tools/                    Shared CLI and runtime helpers
output/<script-name>/     Generated SVG files
```

## Requirements

- Python 3.14 or newer
- [uv](https://docs.astral.sh/uv/)

Install the project dependencies:

```shell
uv sync
```

## CLI

Run an example by passing its name to `dp`:

```shell
uv run dp polar_noise
```

The CLI resolves short names to `scripts/<example>/main.py`. Explicit
directories and entry-point paths work too:

```shell
uv run dp scripts/polar_noise
uv run dp scripts/polar_noise/main.py
```

The generated SVG is written to a directory named after the script:

```text
output/polar_noise/polar_noise.svg
```

Use `--motive` (or `-m`) to apply one of the predefined color motives:

```shell
uv run dp polar_noise --motive light
uv run dp polar_noise -m dark
```

When a motive is selected, the example scripts include it in the output
filename:

```text
output/polar_noise/polar_noise_light.svg
output/polar_noise/polar_noise_dark.svg
```

Available motives are `light` and `dark`. Their definitions are stored in
`tools/motives/`.

To display all CLI options:

```shell
uv run dp --help
```

Examples can also be run directly:

```shell
uv run python scripts/polar_noise/main.py
```

Direct execution uses the default pydreamplet theme and still writes the file
under `output/<script-name>/`.

## Adding an Example

1. Copy `scripts/template` to a descriptively named, lowercase snake-case
   directory:

   ```shell
   Copy-Item scripts/template scripts/my_example -Recurse
   ```

2. Add the artwork to `scripts/my_example/main.py` after the
   `# your art here` marker. Keep the runtime setup and output handling from
   the template:

   ```python
   import pydreamplet as dp

   from tools.runtime import (
       get_example_name,
       get_motive,
       get_motive_path,
       get_output_path,
   )

   motive = get_motive()
   theme = dp.Theme(get_motive_path(motive)) if motive else dp.Theme()

   svg = dp.SVG(1024, 1024)

   # Build the SVG here.

   filename_suffix = f"_{motive}" if motive else ""
   svg.save(get_output_path(f"{get_example_name()}{filename_suffix}.svg"))
   ```

3. Split larger examples into local modules when needed:

   ```text
   scripts/my_example/
     main.py
     components.py
     layout.py
     data/
       input.json
   ```

   The example directory is added to Python's import path by the CLI, so
   `main.py` can use straightforward local imports:

   ```python
   from components import build_legend
   from layout import create_layout
   ```

4. If the example needs input data, store it in its local `data` directory:

   ```text
   scripts/my_example/data/
   ```

   Resolve data files with the shared runtime helper:

   ```python
   from tools.runtime import get_data_path

   data_path = get_data_path("input.json")
   ```

5. Use colors from `theme` where practical so the example works with both
   predefined motives.

6. Generate and inspect all variants:

   ```shell
   uv run dp my_example
   uv run dp my_example -m light
   uv run dp my_example -m dark
   ```

7. Run the linter:

   ```shell
   uv run ruff check .
   ```

Generated files belong under `output/`, which is excluded from version
control. Keep example-specific source modules under `scripts/<example>/`,
example data under `scripts/<example>/data/`, and shared CLI/runtime behavior
under `tools/`.
