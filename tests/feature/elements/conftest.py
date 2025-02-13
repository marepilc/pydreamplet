import pytest

import pydreamplet as dp


@pytest.fixture
def svg_300():
    return dp.SVG(300, 300)


@pytest.fixture
def two_rectangles():
    rect1 = dp.Rect(x=0, y=0, width=10, height=10)
    rect2 = dp.Rect(x=50, y=50, width=20, height=30)
    return rect1, rect2
