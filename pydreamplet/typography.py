import os
import platform

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont


def get_system_font_path(
    font_family: str, weight: int = 400, weight_tolerance: int = 100
) -> str | None:
    """
    Search common system directories for a TrueType font file (.ttf) that matches the requested
    font_family and is within a specified tolerance of the desired weight.

    Args:
        font_family: The desired system font name (e.g. "Arial").
        weight: Numeric weight (e.g., 400 for regular, 700 for bold).
        weight_tolerance: Allowed difference between the desired weight and the font's actual weight.

    Returns:
        The full path to the matching TTF file, or None if no match is found.
    """
    system = platform.system()
    if system == "Windows":
        font_dirs = [os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts")]
    elif system == "Darwin":
        font_dirs = [
            "/System/Library/Fonts",
            "/Library/Fonts",
            os.path.expanduser("~/Library/Fonts"),
        ]
    else:
        # Assume Linux/Unix.
        font_dirs = ["/usr/share/fonts", os.path.expanduser("~/.fonts")]

    for font_dir in font_dirs:
        if not os.path.exists(font_dir):
            continue
        for root, dirs, files in os.walk(font_dir):
            for file in files:
                if file.lower().endswith(".ttf"):
                    file_path = os.path.join(root, file)
                    try:
                        font = TTFont(file_path)
                        # Check the 'name' table for the font family name (nameID 1).
                        family_matches = False
                        for record in font["name"].names:
                            if record.nameID == 1:
                                try:
                                    family_name = record.toUnicode()
                                except Exception:
                                    family_name = record.string.decode(
                                        "utf-8", errors="ignore"
                                    )
                                if font_family.lower() in family_name.lower():
                                    family_matches = True
                                    break
                        if not family_matches:
                            continue

                        # If the font has an OS/2 table, check its weight.
                        if "OS/2" in font:
                            os2_table = font["OS/2"]
                            font_weight = getattr(os2_table, "usWeightClass", 400)
                            if abs(font_weight - weight) <= weight_tolerance:
                                return file_path
                            # If the weight doesn't match, continue searching.
                        else:
                            # If no OS/2 table exists, return the first matching family.
                            return file_path
                    except Exception:
                        continue
    return None


class TypographyMeasurer:
    def __init__(self, dpi: float = 72.0):
        """
        Initialize with a given DPI (dots per inch). The default is 72 DPI,
        meaning 1 point equals 1 pixel. With higher DPI values, the point-to-pixel
        conversion increases accordingly.
        """
        self.dpi = dpi

    def measure_text(
        self, text: str, font_family: str, weight: int, font_size: float
    ) -> tuple[float, float]:
        """
        Measure the width and height of the given text rendered in the specified font.
        Supports multiline text if newline characters are present.

        Args:
            text: The text to measure.
            font_family: The system font name (e.g., "Arial").
            weight: Numeric weight (e.g., 400 for regular, 700 for bold).
            font_size: The desired font size in points.

        Returns:
            A tuple (width, height) in pixels.

        Raises:
            ValueError: If the specified font cannot be found.
        """
        from pydreamplet.typography import get_system_font_path  # adjust if needed

        font_path = get_system_font_path(font_family, weight)
        if font_path is None:
            raise ValueError(
                f"Font '{font_family}' with weight {weight} not found on the system."
            )

        # Convert point size to pixel size using DPI conversion.
        pixel_size = font_size * self.dpi / 72.0
        # ImageFont.truetype expects an integer, so we round the value.
        font = ImageFont.truetype(font_path, int(pixel_size))

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
