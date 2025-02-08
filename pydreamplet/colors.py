import random
import re

from pydreamplet.utils import constrain, math_round


def hexStr(n):
    """
    Converts an integer (0-255) to a two-digit hexadecimal string.
    """
    return format(n, "02x")


def randomInt(min_val, max_val):
    """Returns a random integer N such that min_val <= N <= max_val."""
    return random.randint(min_val, max_val)


def str2rgb(col):
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
            pass
    return rgb


def color2rgba(c, alpha=1):
    """
    Converts an input color (which can be a list/tuple of three numbers,
    an integer, or a hex string) and an alpha value to an "rgba(r, g, b, a)" string.
    """
    r = g = b = 0
    a = 1
    if isinstance(c, (list, tuple)):
        if len(c) == 3:
            r = constrain(c[0], 0, 255)
            g = constrain(c[1], 0, 255)
            b = constrain(c[2], 0, 255)
            a = constrain(alpha, 0, 1)
        else:
            r = g = b = 0
            a = 1
    elif isinstance(c, int):
        r = g = b = constrain(c, 0, 255)
        a = constrain(alpha, 0, 1)
    elif isinstance(c, str):
        rgb = str2rgb(c)
        r = rgb.get("r", 0)
        g = rgb.get("g", 0)
        b = rgb.get("b", 0)
        a = constrain(alpha, 0, 1)
    return f"rgba({r}, {g}, {b}, {a})"


def blend(color1, color2, proportion):
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
        except Exception:
            return "#000000"
    else:
        return "#000000"


def randomColor():
    """
    Generates a random hex color string.
    """
    r = hexStr(randomInt(0, 255))
    g = hexStr(randomInt(0, 255))
    b = hexStr(randomInt(0, 255))
    return "#" + r + g + b
