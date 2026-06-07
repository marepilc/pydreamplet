import colorsys
import json
import random
import re
from collections.abc import Iterator, MutableMapping
from pathlib import Path
from typing import Any

from pydreamplet.utils import constrain, math_round


DEFAULT_COLORS: dict[str, str] = {
    "inherit": "inherit",
    "current": "currentColor",
    "transparent": "transparent",
    "black": "#000000",
    "white": "#ffffff",
    "slate": "#314158",
    "gray": "#364153",
    "zinc": "#3f3f46",
    "neutral": "#404040",
    "stone": "#44403b",
    "red": "#c10007",
    "orange": "#ca3500",
    "amber": "#bb4d00",
    "yellow": "#a65f00",
    "lime": "#497d00",
    "green": "#008236",
    "emerald": "#007a55",
    "teal": "#00786f",
    "cyan": "#007595",
    "sky": "#0069a8",
    "blue": "#1447e6",
    "indigo": "#432dd7",
    "violet": "#6e11b0",
    "purple": "#8200db",
    "fuchsia": "#c800de",
    "pink": "#c6005c",
    "rose": "#c70036",
    "ink": "#18181b",
    "surface": "#e4e4e7",
}

DEFAULT_FONT: dict[str, str | int | float] = {
    "fontFamily": "sans-serif",
    "fontSize": 14,
    "fontWeight": 400,
    "lineHeight": 1.5,
}


class Color(MutableMapping[str, str]):
    """
    Theme color tokens with attribute and mapping-style access.
    """

    def __init__(self, **values: str):
        self._values = DEFAULT_COLORS | values

    def __getitem__(self, key: str) -> str:
        return self._values[key]

    def __setitem__(self, key: str, value: str) -> None:
        self._values[key] = value

    def __delitem__(self, key: str) -> None:
        del self._values[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._values)

    def __len__(self) -> int:
        return len(self._values)

    def __getattr__(self, name: str) -> str:
        try:
            return self._values[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    def __setattr__(self, name: str, value: str) -> None:
        if name == "_values":
            super().__setattr__(name, value)
        else:
            self._values[name] = value

    def to_dict(self) -> dict[str, str]:
        return dict(self._values)


class Theme:
    """
    Font settings and color tokens loaded from defaults or a theme JSON file.
    """

    def __init__(self, path: str | Path | None = None):
        theme_values = self._load_theme(path)
        font_values = theme_values.get("font", {})
        color_values = theme_values.get("colors", {})

        self.font = DEFAULT_FONT | self._require_mapping(font_values, "font")
        self.colors = Color(**self._require_str_mapping(color_values, "colors"))

    @staticmethod
    def _load_theme(path: str | Path | None) -> dict[str, Any]:
        if path is None:
            return {}

        theme_path = Path(path)
        theme_values = json.loads(theme_path.read_text(encoding="utf-8"))
        if not isinstance(theme_values, dict):
            raise ValueError("Theme JSON must contain an object.")
        return theme_values

    @staticmethod
    def _require_mapping(value: Any, field: str) -> dict[str, Any]:
        if not isinstance(value, dict):
            raise ValueError(f"Theme field '{field}' must contain an object.")
        return value

    @staticmethod
    def _require_str_mapping(value: Any, field: str) -> dict[str, str]:
        mapping = Theme._require_mapping(value, field)
        return {str(key): str(color) for key, color in mapping.items()}

    @property
    def font_family(self) -> str:
        return str(self.font["fontFamily"])

    @font_family.setter
    def font_family(self, value: str) -> None:
        self.font["fontFamily"] = value

    @property
    def font_size(self) -> int | float:
        value = self.font["fontSize"]
        if not isinstance(value, (int, float)):
            raise TypeError("fontSize must be a number.")
        return value

    @font_size.setter
    def font_size(self, value: int | float) -> None:
        self.font["fontSize"] = value

    @property
    def font_weight(self) -> int:
        value = self.font["fontWeight"]
        if not isinstance(value, int):
            raise TypeError("fontWeight must be an integer.")
        return value

    @font_weight.setter
    def font_weight(self, value: int) -> None:
        self.font["fontWeight"] = value

    @property
    def line_height(self) -> int | float:
        value = self.font["lineHeight"]
        if not isinstance(value, (int, float)):
            raise TypeError("lineHeight must be a number.")
        return value

    @line_height.setter
    def line_height(self, value: int | float) -> None:
        self.font["lineHeight"] = value

    def to_dict(self) -> dict[str, object]:
        return {
            "font": dict(self.font),
            "colors": self.colors.to_dict(),
        }


def hexStr(n: int) -> str:
    """
    Converts an integer (0-255) to a two-digit hexadecimal string.
    """
    return format(n, "02x")


def random_int(min_val: int, max_val: int) -> int:
    """Returns a random integer N such that min_val <= N <= max_val."""
    return random.randint(min_val, max_val)


def str2rgb(col: str) -> dict[str, int]:
    """
    Converts a hex color string to an RGB dictionary.
    Accepts strings in the format "#RRGGBB" or "#RGB".
    If the input doesn't match, returns {'r': 0, 'g': 0, 'b': 0}.
    """
    rgb = {"r": 0, "g": 0, "b": 0}
    # Regex matches a string starting with one or more '#' and then either 6 or 3 hex digits.
    rgx = re.compile(r"^#+([a-fA-F\d]{6}|[a-fA-F\d]{3})$")
    if rgx.match(col):
        # Expand shorthand (e.g. "#abc" -> "#aabbcc")
        if len(col) == 4:
            col = "#" + col[1] * 2 + col[2] * 2 + col[3] * 2
        try:
            rgb["r"] = int(col[1:3], 16)
            rgb["g"] = int(col[3:5], 16)
            rgb["b"] = int(col[5:7], 16)
        except ValueError:
            # In case of conversion error, keep default (0,0,0)
            return rgb
    return rgb


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """
    Convert a hex color string (e.g., "#ff0000") to an (R, G, B) tuple.
    """
    hex_color = hex_color.lstrip("#")
    if len(hex_color) != 6:
        raise ValueError("Hex color must be in the format RRGGBB")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return (r, g, b)


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    """
    Convert an (R, G, B) tuple to a hex color string.
    """
    r, g, b = rgb
    return f"#{r:02x}{g:02x}{b:02x}"


def color2rgba(
    c: str | int | list[int] | tuple[int, int, int], alpha: float = 1
) -> str:
    """
    Converts an input color (which can be a list/tuple of three numbers,
    an integer, or a hex string) and an alpha value to an "rgba(r, g, b, a)" string.
    """
    r = g = b = 0
    a: float = 1
    if isinstance(c, (list, tuple)):
        if len(c) == 3:
            r = int(constrain(c[0], 0, 255))
            g = int(constrain(c[1], 0, 255))
            b = int(constrain(c[2], 0, 255))
            a = constrain(alpha, 0, 1)
        else:
            r = g = b = 0
            a = 1
    elif isinstance(c, int):
        r = g = b = int(constrain(c, 0, 255))
        a = constrain(alpha, 0, 1)
    else:
        rgb = str2rgb(c)
        r = int(rgb.get("r", 0))
        g = int(rgb.get("g", 0))
        b = int(rgb.get("b", 0))
        a = constrain(alpha, 0, 1)
    return f"rgba({r}, {g}, {b}, {a})"


def blend(color1: str, color2: str, proportion: float) -> str:
    """
    Blends two hex color strings by the given proportion.
    proportion: 0 returns color1, 1 returns color2.
    Returns the blended color as a hex string.
    """
    proportion = constrain(proportion, 0, 1)
    # Ensure the colors start with '#'
    c1 = color1 if color1.startswith("#") else "#" + color1
    c2 = color2 if color2.startswith("#") else "#" + color2

    # Regex to test for valid hex color (3 or 6 hex digits)
    rgx = re.compile(r"^#+([a-fA-F\d]{6}|[a-fA-F\d]{3})$")
    if rgx.match(c1) and rgx.match(c2):
        # Remove leading '#' and expand shorthand if necessary.
        col1 = c1[1:]
        col2 = c2[1:]
        if len(col1) == 3:
            col1 = "".join([ch * 2 for ch in col1])
        if len(col2) == 3:
            col2 = "".join([ch * 2 for ch in col2])
        try:
            r1 = int(col1[0:2], 16)
            r2 = int(col2[0:2], 16)
            r = math_round((1 - proportion) * r1 + proportion * r2)
            g1 = int(col1[2:4], 16)
            g2 = int(col2[2:4], 16)
            g = math_round((1 - proportion) * g1 + proportion * g2)
            b1 = int(col1[4:6], 16)
            b2 = int(col2[4:6], 16)
            b = math_round((1 - proportion) * b1 + proportion * b2)
            return "#" + hexStr(r) + hexStr(g) + hexStr(b)
        except ValueError:
            return "#000000"
    else:
        return "#000000"


def random_color():
    """
    Generates a random hex color string.
    """
    r = hexStr(random_int(0, 255))
    g = hexStr(random_int(0, 255))
    b = hexStr(random_int(0, 255))
    return "#" + r + g + b


def generate_colors(base_color: str, n: int = 10) -> list[str]:
    """
    Generates a list of `n` colors equally distributed on the color wheel.

    The function uses the lightness and saturation of the provided base color,
    then rotates the hue in equal increments to generate a balanced palette.

    Parameters:
        n (int): Number of colors to generate.
        base_color (str): A hex color string (e.g., "#db45f9") used to determine
            the saturation and lightness for the palette. The hues of the generated
            colors are evenly spaced starting from the hue of the base color.

    Returns:
        list[str]: A list of hex color strings.

    Example:
        >>> palette = generate_equal_colors(n=5, base_color="#db45f9")
        >>> print(palette)
        ['#db45f9', '#c4f95d', '#6cf95d', '#5d9ef9', '#9d5df9']
    """
    # Convert the base color to an RGB tuple (0-255)
    r, g, b = hex_to_rgb(base_color)
    # Normalize RGB to 0-1 for colorsys functions.
    r_norm, g_norm, b_norm = r / 255.0, g / 255.0, b / 255.0
    # Convert RGB to HLS (Hue, Lightness, Saturation)
    base_hue, light, sat = colorsys.rgb_to_hls(r_norm, g_norm, b_norm)

    palette: list[str] = []
    for i in range(n):
        # Evenly space hues on the color wheel.
        new_hue = (base_hue + i / n) % 1.0
        # Convert HLS back to RGB (normalized values)
        r_new, g_new, b_new = colorsys.hls_to_rgb(new_hue, light, sat)
        # Scale back to 0-255 and convert to a hex color string.
        rgb_int = (
            math_round(r_new * 255),
            math_round(g_new * 255),
            math_round(b_new * 255),
        )
        palette.append(rgb_to_hex(rgb_int))
    return palette
