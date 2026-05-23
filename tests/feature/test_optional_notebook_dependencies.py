import builtins
import importlib
import sys
from collections.abc import Callable
from types import ModuleType
from typing import Any

import pytest


def without_ipython(original_import: Callable[..., ModuleType]) -> Callable[..., ModuleType]:
    def import_hook(name: str, *args: Any, **kwargs: Any) -> ModuleType:
        if name == "IPython" or name.startswith("IPython."):
            raise ModuleNotFoundError("No module named 'IPython'")
        return original_import(name, *args, **kwargs)

    return import_hook


def test_package_import_does_not_require_ipython(monkeypatch):
    for name in list(sys.modules):
        if name == "pydreamplet" or name.startswith("pydreamplet."):
            sys.modules.pop(name)

    monkeypatch.setattr(builtins, "__import__", without_ipython(builtins.__import__))

    pydreamplet = importlib.import_module("pydreamplet")

    assert pydreamplet.SVG(10, 10).w == 10


def test_svg_display_reports_missing_notebook_dependencies(monkeypatch):
    import pydreamplet as dp

    monkeypatch.setattr(builtins, "__import__", without_ipython(builtins.__import__))

    with pytest.raises(RuntimeError, match=r"pydreamplet\[notebook\]"):
        dp.SVG(10, 10).display()
