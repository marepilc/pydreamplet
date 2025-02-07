from pathlib import Path

from pydreamplet.typography import TypographyMeasurer, get_system_font_path


def test_get_system_font_path_found():
    """
    Test that a common system font (e.g., 'Arial') can be found.
    Note: This test assumes that 'Arial' is installed on your system.
    """
    font_path = get_system_font_path("Arial", 400)
    # The function should return a valid file path if the font is found.
    assert font_path is not None, "Arial font should be found on the system."
    assert Path(font_path).exists(), f"Font path does not exist: {font_path}"


def test_get_system_font_path_not_found():
    """
    Test that a non-existent font returns None.
    """
    font_path = get_system_font_path("ThisFontDoesNotExist", 400)
    assert font_path is None, "Non-existent font should return None."


def test_measure_text_returns_positive_dimensions():
    """
    Test that the text measurement returns positive width and height.
    """
    measurer = TypographyMeasurer()
    width, height = measurer.measure_text(
        "Test", font_family="Arial", weight=400, font_size=16
    )
    assert width > 0, "Width should be positive."
    assert height > 0, "Height should be positive."
