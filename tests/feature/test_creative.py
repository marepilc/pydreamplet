import math

import pytest

from pydreamplet.creative import (
    circle_points,
    grid_points,
    hex_tiles,
    noise_points,
    random_points,
    square_tiles,
)


def test_grid_points_fill_rectangular_area_by_rows():
    assert [point.xy for point in grid_points(3, 2, 20, 10)] == [
        (0.0, 0.0),
        (10.0, 0.0),
        (20.0, 0.0),
        (0.0, 10.0),
        (10.0, 10.0),
        (20.0, 10.0),
    ]


def test_grid_points_support_origin_padding_and_single_axis_counts():
    assert [point.xy for point in grid_points(1, 3, 20, 20, origin=(5, 10), padding=5)] == [
        (10.0, 15.0),
        (10.0, 20.0),
        (10.0, 25.0),
    ]


def test_grid_points_jitter_is_deterministic_with_seed():
    first = grid_points(2, 2, 10, 10, jitter=1, seed=4)
    second = grid_points(2, 2, 10, 10, jitter=1, seed=4)

    assert [point.xy for point in first] == [point.xy for point in second]
    assert first[0].xy == pytest.approx((-0.527903820525131, -0.7936679315385684))


def test_random_points_are_deterministic_with_seed():
    points = random_points(3, 10, 5, seed=3)

    assert [point.xy for point in points] == pytest.approx(
        [
            (2.3796462709189137, 2.721146126479759),
            (3.6995516654807927, 3.019600192980972),
            (6.25720304108054, 0.32764429619906554),
        ]
    )


def test_circle_points_distribute_points_around_radius():
    points = circle_points(4, 10)

    assert [point.xy for point in points] == pytest.approx(
        [
            (10.0, 0.0),
            (0.0, 10.0),
            (-10.0, 0.0),
            (0.0, -10.0),
        ],
        abs=1e-12,
    )


def test_circle_points_can_include_arc_endpoint():
    points = circle_points(3, 10, start_angle=0, end_angle=180, include_endpoint=True)

    assert [point.xy for point in points] == pytest.approx(
        [(10.0, 0.0), (0.0, 10.0), (-10.0, 0.0)],
        abs=1e-12,
    )


def test_circle_points_radius_jitter_is_deterministic():
    first = circle_points(3, 10, radius_jitter=2, seed=7)
    second = circle_points(3, 10, radius_jitter=2, seed=7)

    assert [point.xy for point in first] == [point.xy for point in second]
    assert not math.isclose(first[0].x, 10)


def test_noise_points_pair_grid_points_with_simplex_values():
    values = noise_points(2, 2, 10, 10, seed=5, frequency=0.1)

    assert [point.xy for point, _value in values] == [
        (0.0, 0.0),
        (10.0, 0.0),
        (0.0, 10.0),
        (10.0, 10.0),
    ]
    assert [value for _point, value in values] == pytest.approx(
        [0.5, 0.5371459619387864, 0.6732551823336207, 0.4938600705783195]
    )


def test_square_tiles_fit_rectangular_area_with_gap():
    tiles = square_tiles(2, 2, 22, 12, gap=(2, 4))

    assert [(tile.index, tile.row, tile.column) for tile in tiles] == [
        (0, 0, 0),
        (1, 0, 1),
        (2, 1, 0),
        (3, 1, 1),
    ]
    assert [tile.center.xy for tile in tiles] == [
        (5.0, 2.0),
        (17.0, 2.0),
        (5.0, 10.0),
        (17.0, 10.0),
    ]
    assert [point.xy for point in tiles[0].corners] == [
        (0.0, 0.0),
        (10.0, 0.0),
        (10.0, 4.0),
        (0.0, 4.0),
    ]


def test_square_tiles_support_origin_and_padding():
    tiles = square_tiles(1, 1, 20, 10, origin=(5, 7), padding=(2, 1))

    assert tiles[0].center.xy == (15.0, 12.0)
    assert [point.xy for point in tiles[0].corners] == [
        (7.0, 8.0),
        (23.0, 8.0),
        (23.0, 16.0),
        (7.0, 16.0),
    ]


def test_hex_tiles_generate_pointy_offset_grid():
    tiles = hex_tiles(2, 2, 10)

    assert [(tile.index, tile.row, tile.column) for tile in tiles] == [
        (0, 0, 0),
        (1, 0, 1),
        (2, 1, 0),
        (3, 1, 1),
    ]
    assert [tile.center.xy for tile in tiles] == pytest.approx(
        [
            (0.0, 0.0),
            (17.32050807568877, 0.0),
            (8.660254037844386, 15.0),
            (25.980762113533157, 15.0),
        ]
    )
    expected_corners = [
        (0.0, -10.0),
        (8.660254037844387, -5.0),
        (8.660254037844387, 5.0),
        (0.0, 10.0),
        (-8.660254037844387, 5.0),
        (-8.660254037844387, -5.0),
    ]
    for point, expected in zip(tiles[0].corners, expected_corners, strict=True):
        assert point.xy == pytest.approx(expected)


def test_hex_tiles_generate_flat_offset_grid():
    tiles = hex_tiles(2, 2, 10, orientation="flat")

    assert [tile.center.xy for tile in tiles] == pytest.approx(
        [
            (0.0, 0.0),
            (15.0, 8.660254037844386),
            (0.0, 17.32050807568877),
            (15.0, 25.980762113533157),
        ]
    )
    expected_corners = [
        (10.0, 0.0),
        (5.0, 8.660254037844386),
        (-5.0, 8.660254037844387),
        (-10.0, 0.0),
        (-5.0, -8.660254037844386),
        (5.0, -8.660254037844386),
    ]
    for point, expected in zip(tiles[0].corners, expected_corners, strict=True):
        assert point.xy == pytest.approx(expected)


@pytest.mark.parametrize(
    "factory",
    [
        lambda: grid_points(0, 1, 10, 10),
        lambda: grid_points(1, 0, 10, 10),
        lambda: random_points(0, 10, 10),
        lambda: circle_points(0, 10),
        lambda: circle_points(1, -1),
        lambda: circle_points(1, 10, radius_jitter=-1),
        lambda: square_tiles(0, 1, 10, 10),
        lambda: square_tiles(1, 0, 10, 10),
        lambda: square_tiles(2, 1, 10, 10, gap=20),
        lambda: hex_tiles(0, 1, 10),
        lambda: hex_tiles(1, 1, 0),
        lambda: hex_tiles(1, 1, 10, gap=-1),
        lambda: hex_tiles(1, 1, 10, orientation="diagonal"),  # type: ignore[arg-type]
    ],
)
def test_creative_helpers_validate_invalid_input(factory):
    with pytest.raises(ValueError):
        factory()
