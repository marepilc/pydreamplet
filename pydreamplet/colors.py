import colorsys
import json
import math
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

ColorInput = str | int | list[int | float] | tuple[int | float, ...]


def _format_alpha(alpha: float) -> str:
    alpha = constrain(alpha, 0, 1)
    return f"{alpha:g}"


def _rgb_channel(value: int | float) -> int:
    return int(constrain(value, 0, 255))


def _alpha_channel(value: int | float) -> float:
    return constrain(float(value), 0, 1)


def normalize_color(value: ColorInput) -> str:
    """
    Converts supported Python color values to SVG/CSS color strings.
    """
    if isinstance(value, int):
        channel = _rgb_channel(value)
        return rgb_to_hex((channel, channel, channel))

    if isinstance(value, (list, tuple)):
        if len(value) == 3:
            return rgb_to_hex(
                (
                    _rgb_channel(value[0]),
                    _rgb_channel(value[1]),
                    _rgb_channel(value[2]),
                )
            )
        if len(value) == 4:
            r = _rgb_channel(value[0])
            g = _rgb_channel(value[1])
            b = _rgb_channel(value[2])
            a = _alpha_channel(value[3])
            return f"rgba({r}, {g}, {b}, {_format_alpha(a)})"
        raise ValueError("Color sequences must contain 3 RGB or 4 RGBA values.")

    if isinstance(value, str):
        return value

    raise TypeError("Color values must be strings, numbers, RGB tuples, or RGBA tuples.")


def _parse_hex_color(value: str) -> tuple[int, int, int, float] | None:
    color = value.strip()
    rgx = re.compile(r"^#?([a-fA-F\d]{6}|[a-fA-F\d]{3})$")
    match = rgx.match(color)
    if match is None:
        return None

    hex_value = match.group(1)
    if len(hex_value) == 3:
        hex_value = "".join(ch * 2 for ch in hex_value)
    r = int(hex_value[0:2], 16)
    g = int(hex_value[2:4], 16)
    b = int(hex_value[4:6], 16)
    return r, g, b, 1


def _parse_rgb_color(value: str) -> tuple[int, int, int, float] | None:
    match = re.fullmatch(r"rgba?\((.+)\)", value.strip(), flags=re.IGNORECASE)
    if match is None:
        return None

    parts = [
        part.strip()
        for part in re.split(r"[,/ ]+", match.group(1).strip())
        if part.strip()
    ]
    if len(parts) not in (3, 4):
        return None

    try:
        r = _rgb_channel(float(parts[0].rstrip("%")))
        g = _rgb_channel(float(parts[1].rstrip("%")))
        b = _rgb_channel(float(parts[2].rstrip("%")))
        alpha = _alpha_channel(float(parts[3])) if len(parts) == 4 else 1
    except ValueError:
        return None
    return r, g, b, alpha


def _linear_to_srgb(channel: float) -> int:
    if channel <= 0.0031308:
        srgb = 12.92 * channel
    else:
        srgb = 1.055 * (channel ** (1 / 2.4)) - 0.055
    return _rgb_channel(math_round(srgb * 255))


def _parse_oklch_color(value: str) -> tuple[int, int, int, float] | None:
    match = re.fullmatch(r"oklch\((.+)\)", value.strip(), flags=re.IGNORECASE)
    if match is None:
        return None

    parts = [
        part.strip()
        for part in re.split(r"[,/ ]+", match.group(1).strip())
        if part.strip()
    ]
    if len(parts) not in (3, 4):
        return None

    try:
        lightness_text = parts[0]
        lightness = float(lightness_text.rstrip("%"))
        if lightness_text.endswith("%"):
            lightness /= 100

        chroma = float(parts[1])
        hue = float(parts[2].removesuffix("deg"))
        alpha = _alpha_channel(float(parts[3])) if len(parts) == 4 else 1
    except ValueError:
        return None

    a = chroma * math.cos(math.radians(hue))
    b = chroma * math.sin(math.radians(hue))
    l_ = lightness + 0.3963377774 * a + 0.2158037573 * b
    m_ = lightness - 0.1055613458 * a - 0.0638541728 * b
    s_ = lightness - 0.0894841775 * a - 1.2914855480 * b

    long_response = l_**3
    medium_response = m_**3
    short_response = s_**3

    red = (
        +4.0767416621 * long_response
        - 3.3077115913 * medium_response
        + 0.2309699292 * short_response
    )
    green = (
        -1.2684380046 * long_response
        + 2.6097574011 * medium_response
        - 0.3413193965 * short_response
    )
    blue = (
        -0.0041960863 * long_response
        - 0.7034186147 * medium_response
        + 1.7076147010 * short_response
    )

    return (
        _linear_to_srgb(red),
        _linear_to_srgb(green),
        _linear_to_srgb(blue),
        alpha,
    )


def color_to_rgba(value: ColorInput) -> tuple[int, int, int, float]:
    """
    Converts supported Python and CSS color values to RGBA channels.
    """
    if isinstance(value, int):
        channel = _rgb_channel(value)
        return channel, channel, channel, 1

    if isinstance(value, (list, tuple)):
        if len(value) == 3:
            return (
                _rgb_channel(value[0]),
                _rgb_channel(value[1]),
                _rgb_channel(value[2]),
                1,
            )
        if len(value) == 4:
            return (
                _rgb_channel(value[0]),
                _rgb_channel(value[1]),
                _rgb_channel(value[2]),
                _alpha_channel(value[3]),
            )
        raise ValueError("Color sequences must contain 3 RGB or 4 RGBA values.")

    for parser in (_parse_hex_color, _parse_rgb_color, _parse_oklch_color):
        parsed = parser(value)
        if parsed is not None:
            return parsed

    raise ValueError(f"Unsupported color value: {value!r}")


class Color(MutableMapping[str, str]):
    """
    Theme color tokens with attribute and mapping-style access.
    """

    def __init__(self, **values: ColorInput):
        self._values = DEFAULT_COLORS | {
            key: normalize_color(value) for key, value in values.items()
        }

    def __getitem__(self, key: str) -> str:
        return self._values[key]

    def __setitem__(self, key: str, value: ColorInput) -> None:
        self._values[key] = normalize_color(value)

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

    def __setattr__(self, name: str, value: ColorInput) -> None:
        if name == "_values":
            super().__setattr__(name, value)
        else:
            self._values[name] = normalize_color(value)

    def to_dict(self) -> dict[str, str]:
        return dict(self._values)


class Theme:
    """
    Font settings and color tokens loaded from defaults or a theme JSON file.
    """

    _INTERNAL_ATTRIBUTES = {"font", "colors"}
    _FONT_ATTRIBUTES = {"font_family", "font_size", "font_weight", "line_height"}

    def __init__(self, path: str | Path | None = None):
        theme_values = self._load_theme(path)
        font_values = theme_values.get("font", {})
        color_values = theme_values.get("colors", {})

        self.font = DEFAULT_FONT | self._require_mapping(font_values, "font")
        self.colors = Color(**self._require_color_mapping(color_values, "colors"))

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
    def _require_color_mapping(value: Any, field: str) -> dict[str, ColorInput]:
        mapping = Theme._require_mapping(value, field)
        return {str(key): color for key, color in mapping.items()}

    @property
    def color(self) -> Color:
        return self.colors

    def __getattr__(self, name: str) -> str:
        try:
            return self.colors[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    def __setattr__(self, name: str, value: Any) -> None:
        if name in self._INTERNAL_ATTRIBUTES:
            super().__setattr__(name, value)
        elif name in self._FONT_ATTRIBUTES:
            super().__setattr__(name, value)
        else:
            self.colors[name] = value

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


def color2rgba(c: ColorInput, alpha: float = 1) -> str:
    """
    Converts an input color (which can be a list/tuple of three numbers,
    an integer, or a hex string) and an alpha value to an "rgba(r, g, b, a)" string.
    """
    try:
        r, g, b, parsed_alpha = color_to_rgba(c)
    except ValueError:
        r, g, b, parsed_alpha = 0, 0, 0, 1
    a = parsed_alpha if parsed_alpha < 1 else constrain(alpha, 0, 1)
    return f"rgba({r}, {g}, {b}, {_format_alpha(a)})"


def blend(color1: ColorInput, color2: ColorInput, proportion: float) -> str:
    """
    Blends two supported color values by the given proportion.
    proportion: 0 returns color1, 1 returns color2.
    Returns hex for opaque colors and rgba(...) when transparency is involved.
    """
    proportion = constrain(proportion, 0, 1)

    try:
        r1, g1, b1, a1 = color_to_rgba(color1)
        r2, g2, b2, a2 = color_to_rgba(color2)
    except ValueError:
        return "#000000"

    r = math_round((1 - proportion) * r1 + proportion * r2)
    g = math_round((1 - proportion) * g1 + proportion * g2)
    b = math_round((1 - proportion) * b1 + proportion * b2)
    a = (1 - proportion) * a1 + proportion * a2

    if a >= 1:
        return rgb_to_hex((r, g, b))
    return f"rgba({r}, {g}, {b}, {_format_alpha(a)})"


def blend_colors(color1: ColorInput, color2: ColorInput, proportion: float) -> str:
    """
    Alias for blend() with an explicit two-color name.
    """
    return blend(color1, color2, proportion)


def blend_color(color1: ColorInput, color2: ColorInput, proportion: float) -> str:
    """
    Backward-compatible singular alias for blend_colors().
    """
    return blend_colors(color1, color2, proportion)


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
