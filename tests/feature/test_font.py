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


def test_measure_text_accepts_explicit_font_path():
    """
    Test that explicit font paths do not require a system font lookup.
    """
    font_path = get_system_font_path("Arial", 400)
    assert font_path is not None, "Arial font should be found on the system."

    measurer = TypographyMeasurer(font_path=font_path)
    width, height = measurer.measure_text("AV", font_size=16)

    assert width > 0, "Width should be positive."
    assert height > 0, "Height should be positive."


def test_measure_text_multiline_height_scales_by_line_count():
    """
    Test that multiline text uses the shaped max line width and line metrics.
    """
    measurer = TypographyMeasurer()
    single_width, single_height = measurer.measure_text(
        "Test", font_family="Arial", weight=400, font_size=16
    )
    multiline_width, multiline_height = measurer.measure_text(
        "Test\nTest", font_family="Arial", weight=400, font_size=16
    )

    assert multiline_width == single_width
    assert multiline_height == single_height * 2
