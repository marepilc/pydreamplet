import pytest

import pydreamplet as dp


@pytest.fixture
def polygon():
    return dp.Polygon(points=[0, 0, 0, 10, 10, 10, 10, 0])


def test_polygon_create(polygon):
    assert polygon.points == [0, 0, 0, 10, 10, 10, 10, 0]


def test_polygon_points_setter(polygon):
    polygon.points = [0, 0, 0, 20, 20, 20, 20, 0]
    assert polygon.points == [0, 0, 0, 20, 20, 20, 20, 0]
    assert 'points="0,0 0,20 20,20 20,0"' in str(polygon)


def test_can_be_found_as_proper_type(polygon):
    svg = dp.SVG(300, 300)
    svg.append(polygon)
    pl = svg.find("polygon")
    assert isinstance(pl, dp.Polygon)
