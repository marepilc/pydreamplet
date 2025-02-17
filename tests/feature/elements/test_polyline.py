import pytest

import pydreamplet as dp


@pytest.fixture
def polyline():
    return dp.Polyline(points=[0, 0, 0, 10, 10, 10, 10, 0])


def test_polyline_create(polyline):
    assert polyline.points == [0, 0, 0, 10, 10, 10, 10, 0]


def test_polyline_points_setter(polyline):
    polyline.points = [0, 0, 0, 20, 20, 20, 20, 0]
    assert polyline.points == [0, 0, 0, 20, 20, 20, 20, 0]
    assert 'points="0,0 0,20 20,20 20,0"' in str(polyline)


def test_can_be_found_as_proper_type(polyline):
    svg = dp.SVG(300, 300)
    svg.append(polyline)
    pl = svg.find("polyline")
    assert isinstance(pl, dp.Polyline)
