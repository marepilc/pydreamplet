import os
import platform

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont


def get_system_font_path(
    font_family: str, weight: int = 400, weight_tolerance: int = 100
) -> str | None:
    """
    Search common system directories for a TrueType or OpenType font file (.ttf/.otf)
    that matches the requested font_family and is within a specified tolerance of the desired weight.

    Args:
        font_family: The desired system font name (e.g. "Arial").
        weight: Numeric weight (e.g., 400 for regular, 700 for bold).
        weight_tolerance: Allowed difference between the desired weight and the font's actual weight.

    Returns:
        The full path to the matching font file, or None if no match is found.
    """
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

    # Consider both TTF and OTF files.
    extensions = (".ttf", ".otf")

    for font_dir in font_dirs:
        if not os.path.exists(font_dir):
            continue
        for root, dirs, files in os.walk(font_dir):
            for file in files:
                if not file.lower().endswith(extensions):
                    continue

                file_path = os.path.join(root, file)
                try:
                    font = TTFont(file_path)
                except Exception:
                    continue

                # Loop over all name records for a looser match.
                family_matches = False
                for record in font["name"].names:
                    try:
                        record_value = record.toUnicode().strip()
                    except Exception:
                        record_value = record.string.decode(
                            "utf-8", errors="ignore"
                        ).strip()
                    if font_family.lower() in record_value.lower():
                        family_matches = True
                        break
                if not family_matches:
                    continue

                # If the OS/2 table exists, check the weight.
                if "OS/2" in font:
                    os2_table = font["OS/2"]
                    font_weight = getattr(os2_table, "usWeightClass", 400)
                    if abs(font_weight - weight) <= weight_tolerance:
                        return file_path
                    else:
                        continue  # Weight doesn't match, keep searching.
                else:
                    # If no OS/2 table exists, return the first matching family.
                    return file_path
    return None


class TypographyMeasurer:
    def __init__(self, dpi: float = 72.0, font_path: str | None = None):
        """
        Initialize with a given DPI (dots per inch). The default is 72 DPI,
        meaning 1 point equals 1 pixel. With higher DPI values, the point-to-pixel
        conversion increases accordingly.

        If a font_path is provided, it will be used; otherwise the system is searched.
        """
        self.dpi = dpi
        self.font_path = font_path

    def measure_text(
        self,
        text: str,
        font_family: str | None = None,
        weight: int | None = None,
        font_size: float = 12.0,
    ) -> tuple[float, float]:
        """
        Measure the width and height of the given text rendered in the specified font.
        Supports multiline text if newline characters are present.

        Args:
            text: The text to measure.
            font_family: The system font name (e.g., "Arial"). Optional if self.font_path is provided.
            weight: Numeric weight (e.g., 400 for regular, 700 for bold). Optional if self.font_path is provided.
            font_size: The desired font size in points.

        Returns:
            A tuple (width, height) in pixels.

        Raises:
            ValueError: If the specified font cannot be found and font_family or weight are missing.
        """
        # If no font_path is already set, require font_family and weight.
        if not self.font_path:
            if font_family is None or weight is None:
                raise ValueError(
                    "A font path was not provided and font_family and weight are required to search for a font."
                )
            self.font_path = get_system_font_path(font_family, weight)
        if self.font_path is None:
            raise ValueError(
                f"Font '{font_family}' with weight {weight} not found on the system."
            )

        # Convert point size to pixel size using DPI conversion.
        pixel_size = font_size * self.dpi / 72.0
        # ImageFont.truetype expects an integer size.
        font = ImageFont.truetype(self.font_path, int(pixel_size))

        # Create a dummy image for measurement.
        dummy_img = Image.new("RGB", (1000, 1000))
        draw = ImageDraw.Draw(dummy_img)

        # Use multiline_textbbox if there are newline characters.
        if "\n" in text:
            bbox = draw.multiline_textbbox((0, 0), text, font=font)
        else:
            bbox = draw.textbbox((0, 0), text, font=font)

        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        return float(width), float(height)
