import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def get_example_dir() -> Path:
    example_dir = os.environ.get("PYDREAMPLET_EXAMPLE_DIR")
    if example_dir is not None:
        return Path(example_dir)

    return Path(sys.argv[0]).resolve().parent


def get_example_name() -> str:
    example_name = os.environ.get("PYDREAMPLET_EXAMPLE_NAME")
    if example_name is not None:
        return example_name

    script_path = Path(sys.argv[0])
    return script_path.parent.name if script_path.stem == "main" else script_path.stem


def get_motive() -> str | None:
    return os.environ.get("PYDREAMPLET_MOTIVE")


def get_motive_path(motive: str) -> str:
    return str(PROJECT_ROOT / "tools" / "motives" / f"{motive}.json")


def get_data_path(filename: str) -> Path:
    return get_example_dir() / "data" / filename


def get_output_path(filename: str) -> str:
    output_dir = PROJECT_ROOT / "output" / get_example_name()
    output_dir.mkdir(parents=True, exist_ok=True)
    return str(output_dir / filename)
