import os
import runpy
import sys
from enum import StrEnum
from pathlib import Path

import typer

app = typer.Typer(add_completion=False)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"


class Motive(StrEnum):
    LIGHT = "light"
    DARK = "dark"


def resolve_script(script: Path) -> Path:
    candidates: list[Path] = [script]
    if not script.is_absolute():
        candidates.append(SCRIPTS_DIR / script)

    expanded_candidates: list[Path] = []
    for candidate in candidates:
        expanded_candidates.append(candidate)
        if candidate.suffix == "":
            expanded_candidates.append(candidate.with_suffix(".py"))
            expanded_candidates.append(candidate / "main.py")

    for candidate in expanded_candidates:
        resolved = candidate.resolve()
        if resolved.is_file():
            return resolved

    raise typer.BadParameter(f"Script does not exist: {script}")


@app.command()
def main(
    script: Path = typer.Argument(
        ...,
        help="Showcase name, directory, or Python entry-point path.",
    ),
    motive: Motive | None = typer.Option(None, "--motive", "-m"),
) -> None:
    script = resolve_script(script)
    example_name = script.parent.name if script.name == "main.py" else script.stem

    os.environ["PYDREAMPLET_EXAMPLE_NAME"] = example_name
    os.environ["PYDREAMPLET_EXAMPLE_DIR"] = str(script.parent)
    if motive is None:
        os.environ.pop("PYDREAMPLET_MOTIVE", None)
    else:
        os.environ["PYDREAMPLET_MOTIVE"] = str(motive)

    sys.path.insert(0, str(script.parent))
    try:
        runpy.run_path(str(script), run_name="__main__")
    finally:
        sys.path.pop(0)
