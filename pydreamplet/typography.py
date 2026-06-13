import os
import platform
import re
from pathlib import Path
from typing import Any, Protocol, overload, cast

from fontTools.ttLib import TTFont, TTLibError
import uharfbuzz as _hb

from pydreamplet.types import Real

hb = cast(Any, _hb)
FontSize = Real | str
_GENERIC_FONT_FAMILIES: dict[str, dict[str, tuple[str, ...]]] = {
    "Windows": {
        "sans-serif": ("Arial",),
        "serif": ("Times New Roman",),
        "monospace": ("Consolas", "Courier New"),
    },
    "Darwin": {
        "sans-serif": ("Helvetica", "Arial"),
        "serif": ("Times", "Times New Roman"),
        "monospace": ("Menlo", "Courier"),
    },
    "Linux": {
        "sans-serif": ("DejaVu Sans", "Liberation Sans"),
        "serif": ("DejaVu Serif", "Liberation Serif"),
        "monospace": ("DejaVu Sans Mono", "Liberation Mono"),
    },
}


class TextElementLike(Protocol):
    @property
    def content(self) -> str: ...


def _font_family_candidates(font_family: str) -> list[str]:
    system_families = _GENERIC_FONT_FAMILIES.get(
        platform.system(), _GENERIC_FONT_FAMILIES["Linux"]
    )
    candidates: list[str] = []
    for family in font_family.split(","):
        family = family.strip().strip("'\"")
        if not family:
            continue
        replacements = system_families.get(family.lower(), (family,))
        for replacement in replacements:
            if replacement not in candidates:
                candidates.append(replacement)
    return candidates


def _font_record_values(font: TTFont, name_ids: set[int]) -> list[str]:
    values: list[str] = []
    for record in font["name"].names:  # type: ignore[index]
        if record.nameID not in name_ids:
            continue
        try:
            value = record.toUnicode().strip()
        except UnicodeError:
            value = record.string.decode("utf-8", errors="ignore").strip()
        if value:
            values.append(value)
    return values


def _normalize_font_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def get_system_font_path(
    font_family: str, weight: int = 400, weight_tolerance: int = 100
) -> str | None:
    """
    Search common system directories for a TrueType or OpenType font file (.ttf/.otf)
    that matches the requested font_family and is within a specified tolerance of
    the desired weight.

    Args:
        font_family: A system font name or CSS fallback list
            (e.g. "Inter, Arial, sans-serif").
        weight: Numeric weight (e.g., 400 for regular, 700 for bold).
        weight_tolerance: Allowed difference between the desired weight and the
            font's actual weight.

    Returns:
        The full path to the matching font file, or None if no match is found.
    """
    candidates = _font_family_candidates(font_family)
    if not candidates:
        return None

    normalized_candidates = [_normalize_font_name(name) for name in candidates]
    system = platform.system()
    font_dirs = []

    if system == "Windows":
        # System-wide fonts directory.
        system_fonts = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts")
        font_dirs.append(system_fonts)
        # User-specific fonts directory.
        local_fonts = os.path.join(
            os.environ.get("LOCALAPPDATA", ""), "Microsoft", "Windows", "Fonts"
        )
        if local_fonts and os.path.exists(local_fonts):
            font_dirs.append(local_fonts)
    elif system == "Darwin":
        font_dirs = [
            "/System/Library/Fonts",
            "/Library/Fonts",
            os.path.expanduser("~/Library/Fonts"),
        ]
    else:
        # Assume Linux/Unix.
        font_dirs = [
            "/usr/share/fonts",
            os.path.expanduser("~/.fonts"),
            "/usr/local/share/fonts",
        ]

        # In WSL, also check Windows font directories
        if os.path.exists("/mnt/c/Windows/Fonts"):
            font_dirs.extend(
                [
                    "/mnt/c/Windows/Fonts",
                    "/mnt/c/Users/"
                    + os.environ.get("USER", "")
                    + "/AppData/Local/Microsoft/Windows/Fonts",
                ]
            )

    # Consider both TTF and OTF files.
    extensions = (".ttf", ".otf")

    matches: list[tuple[int, int, str]] = []
    for font_dir in font_dirs:
        if not os.path.exists(font_dir):
            continue
        for root, _, files in os.walk(font_dir):
            for file in files:
                if not file.lower().endswith(extensions):
                    continue

                file_path = os.path.join(root, file)
                try:
                    font = TTFont(file_path)
                except (OSError, TTLibError):
                    continue

                family_names = _font_record_values(font, {1, 16})
                normalized_names = {
                    _normalize_font_name(name) for name in family_names
                }
                try:
                    family_index = next(
                        index
                        for index, candidate in enumerate(normalized_candidates)
                        if candidate in normalized_names
                    )
                except StopIteration:
                    continue

                style_names = _font_record_values(font, {2, 17})
                style_description = " ".join(style_names + [Path(file_path).stem])
                if "italic" in style_description.lower() or "oblique" in (
                    style_description.lower()
                ):
                    continue

                font_weight = 400
                if "OS/2" in font:
                    os2_table = font["OS/2"]
                    font_weight = getattr(os2_table, "usWeightClass", 400)
                weight_difference = abs(font_weight - weight)
                if weight_difference <= weight_tolerance:
                    matches.append((family_index, weight_difference, file_path))

    if not matches:
        return None
    return min(matches)[2]


class TypographyMeasurer:
    def __init__(
        self,
        dpi: float = 72.0,
        font_path: str | None = None,
        *,
        font_family: str | None = None,
        weight: int = 400,
    ):
        """
        Initialize with a given DPI (dots per inch). The default is 72 DPI,
        meaning 1 point equals 1 pixel. With higher DPI values, the point-to-pixel
        conversion increases accordingly.

        If a font_path is provided, it will be used. Otherwise font_family and
        weight provide defaults for system font lookup during measurement.
        """
        self.dpi = dpi
        self.font_path = font_path
        self.font_family = font_family
        self.weight = weight
        self._resolved_font_paths: dict[tuple[str, int], str] = {}
        self._font_data_cache: dict[str, bytes] = {}
        self._ttfont_cache: dict[str, TTFont] = {}

    def _resolve_font_path(
        self, font_family: str | None, weight: int | None
    ) -> str:
        if self.font_path:
            return self.font_path

        font_family = font_family or self.font_family
        weight = weight if weight is not None else self.weight
        if font_family is None:
            raise ValueError(
                "A font path was not provided and font_family is required to "
                "search for a font."
            )

        cache_key = (font_family, weight)
        if cache_key not in self._resolved_font_paths:
            resolved_path = get_system_font_path(font_family, weight)
            if resolved_path is not None:
                self._resolved_font_paths[cache_key] = resolved_path
        if cache_key not in self._resolved_font_paths:
            raise ValueError(
                f"Font '{font_family}' with weight {weight} not found on the system."
            )
        return self._resolved_font_paths[cache_key]

    def _get_font_data(self, font_path: str) -> bytes:
        if font_path not in self._font_data_cache:
            self._font_data_cache[font_path] = Path(font_path).read_bytes()
        return self._font_data_cache[font_path]

    def _get_ttfont(self, font_path: str) -> TTFont:
        if font_path not in self._ttfont_cache:
            self._ttfont_cache[font_path] = TTFont(font_path)
        return self._ttfont_cache[font_path]

    def _font_scale(self, font_path: str, font_size: Real) -> tuple[float, float]:
        ttfont = self._get_ttfont(font_path)
        head_table = cast(Any, ttfont["head"])
        units_per_em = head_table.unitsPerEm
        pixel_size = float(font_size) * self.dpi / 72.0
        return pixel_size, pixel_size / units_per_em

    def _line_height(self, font_path: str, font_size: Real) -> float:
        ttfont = self._get_ttfont(font_path)
        pixel_size, scale = self._font_scale(font_path, font_size)

        if "OS/2" in ttfont:
            os2_table = ttfont["OS/2"]
            ascender = getattr(os2_table, "sTypoAscender", 0)
            descender = getattr(os2_table, "sTypoDescender", 0)
            line_gap = getattr(os2_table, "sTypoLineGap", 0)
            if ascender or descender or line_gap:
                return float((ascender - descender + line_gap) * scale)

        if "hhea" in ttfont:
            hhea_table = cast(Any, ttfont["hhea"])
            return float(
                (hhea_table.ascent - hhea_table.descent + hhea_table.lineGap) * scale
            )

        return pixel_size

    def _measure_line_width(self, text: str, font_path: str, font_size: Real) -> float:
        font_data = self._get_font_data(font_path)
        face = hb.Face(font_data)
        font = hb.Font(face)
        font.scale = (face.upem, face.upem)

        buffer = hb.Buffer()
        buffer.add_str(text)
        buffer.guess_segment_properties()
        hb.shape(font, buffer)

        _, scale = self._font_scale(font_path, font_size)
        advance = sum(position.x_advance for position in buffer.glyph_positions)
        return float(advance * scale)

    @staticmethod
    def _coerce_font_size(value: object, default: Real = 12.0) -> Real:
        if value is None:
            return default
        if isinstance(value, (int, float)):
            return value
        if isinstance(value, str):
            match = re.match(r"\s*([0-9]+(?:\.[0-9]+)?)", value)
            if match:
                return float(match.group(1))
        raise ValueError(f"font_size must be numeric, got {value!r}")

    @staticmethod
    def _coerce_weight(value: object) -> int | None:
        if value is None:
            return None
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            return int(value)
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized == "normal":
                return 400
            if normalized == "bold":
                return 700
            try:
                return int(normalized)
            except ValueError as exc:
                raise ValueError(f"font weight must be numeric, got {value!r}") from exc
        raise ValueError(f"font weight must be numeric, got {value!r}")

    def _text_measurement_args(
        self,
        text: str | object,
        font_family: str | None,
        weight: int | None,
        font_size: FontSize | None,
    ) -> tuple[str, str | None, int | None, Real]:
        if isinstance(text, str):
            return text, font_family, weight, self._coerce_font_size(font_size)

        content = getattr(text, "content", None)
        if not isinstance(content, str):
            raise TypeError("measure_text() expects a string or a text element.")

        if font_family is None:
            font_family_value = getattr(text, "font_family", None)
            if font_family_value is not None:
                font_family = str(font_family_value)

        if weight is None:
            weight = self._coerce_weight(getattr(text, "font_weight", None))
            if weight is None and font_family is not None:
                weight = 400

        if font_size is None:
            font_size = self._coerce_font_size(getattr(text, "font_size", None))

        return content, font_family, weight, self._coerce_font_size(font_size)

    @overload
    def measure_text(
        self,
        text: str,
        *,
        font_family: str | None = None,
        weight: int | None = None,
        font_size: FontSize | None = None,
    ) -> tuple[float, float]: ...

    @overload
    def measure_text(
        self,
        text: TextElementLike,
        *,
        font_family: str | None = None,
        weight: int | None = None,
        font_size: FontSize | None = None,
    ) -> tuple[float, float]: ...

    def measure_text(
        self,
        text: str | object,
        *,
        font_family: str | None = None,
        weight: int | None = None,
        font_size: FontSize | None = None,
    ) -> tuple[float, float]:
        """
        Measure the width and height of the given text rendered in the specified font.
        Supports multiline text if newline characters are present.
        Uses HarfBuzz for OpenType shaping and fontTools for font metrics.

        Args:
            text: The string or text element to measure.
            font_family: The system font name (e.g., "Arial"). Optional if
                self.font_path is provided.
            weight: Numeric weight (e.g., 400 for regular, 700 for bold).
                Optional if self.font_path is provided.
            font_size: The desired font size in points. If omitted for a text
                element, its font_size is used.

        Returns:
            A tuple (width, height) in pixels.

        Raises:
            ValueError: If the specified font cannot be found and font_family or
                weight are missing.
        """
        text, font_family, weight, font_size = self._text_measurement_args(
            text, font_family, weight, font_size
        )
        font_path = self._resolve_font_path(font_family, weight)
        lines = text.split("\n") or [""]
        width = max(
            (self._measure_line_width(line, font_path, font_size) for line in lines),
            default=0.0,
        )
        height = self._line_height(font_path, font_size) * len(lines)

        return (float(width), float(height))
