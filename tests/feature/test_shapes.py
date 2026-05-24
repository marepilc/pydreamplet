import pytest
from typing import Any, cast

from pydreamplet.shapes import (
    arc,
    basis_spline,
    cardinal_spline,
    catmull_rom_path,
    cross,
    linear_path,
    monotone_x_path,
    monotone_y_path,
    polygon,
    polyline,
    ring,
    star,
    step_path,
)


def test_basic_shape_generators_return_expected_path_data():
    assert star(n=2, inner_radius=5, outer_radius=10) == (
        "M 10.00,0.00 L 0.00,5.00 L -10.00,0.00 L 0.00,-5.00 Z"
    )
    assert polygon(0, 0, 10, 4) == (
        "M 0.00,-10.00 L 10.00,0.00 L 0.00,10.00 L -10.00,0.00 Z"
    )
    assert cross(size=10, thickness=4) == (
        "M -2.00,5.00 L 2.00,5.00 L 2.00,2.00 L 5.00,2.00 "
        "L 5.00,-2.00 L 2.00,-2.00 L 2.00,-5.00 L -2.00,-5.00 "
        "L -2.00,-2.00 L -5.00,-2.00 L -5.00,2.00 L -2.00,2.00 Z"
    )
    assert polyline([0, 5, 10], [0, 10, 0]) == (
        "M 0.00,0.00 L 5.00,10.00 L 10.00,0.00"
    )


def test_linear_path_accepts_flat_and_pair_points():
    assert linear_path([0, 0, 10, 20, 30, 0]) == (
        "M 0.00,0.00 L 10.00,20.00 L 30.00,0.00"
    )
    assert linear_path([(0, 0), (10, 20), (30, 0)], closed=True) == (
        "M 0.00,0.00 L 10.00,20.00 L 30.00,0.00 Z"
    )


def test_step_path_modes():
    points = [(0, 0), (10, 20), (30, 0)]

    assert step_path(points) == (
        "M 0.00,0.00 L 5.00,0.00 L 5.00,20.00 L 10.00,20.00 "
        "L 20.00,20.00 L 20.00,0.00 L 30.00,0.00"
    )
    assert step_path(points, mode="before") == (
        "M 0.00,0.00 L 0.00,20.00 L 10.00,20.00 "
        "L 10.00,0.00 L 30.00,0.00"
    )
    assert step_path(points, mode="after", closed=True) == (
        "M 0.00,0.00 L 10.00,0.00 L 10.00,20.00 "
        "L 30.00,20.00 L 30.00,0.00 Z"
    )


def test_catmull_rom_path_generates_cubic_path():
    assert catmull_rom_path([(0, 0), (10, 20), (30, 0)]) == (
        "M 0.00,0.00 "
        "C 1.67,3.33 5.00,20.00 10.00,20.00 "
        "C 15.00,20.00 26.67,3.33 30.00,0.00"
    )


def test_catmull_rom_path_supports_closed_paths():
    assert catmull_rom_path([(0, 0), (10, 20), (30, 0)], closed=True) == (
        "M 0.00,0.00 "
        "C -3.33,3.33 5.00,20.00 10.00,20.00 "
        "C 15.00,20.00 31.67,3.33 30.00,0.00 "
        "C 28.33,-3.33 3.33,-3.33 0.00,0.00 Z"
    )


def test_basis_spline_generates_cubic_path():
    assert basis_spline([(0, 0), (10, 20), (30, 0), (40, 10)]) == (
        "M 0.00,0.00 "
        "C 3.33,6.67 6.67,13.33 11.67,13.33 "
        "C 16.67,13.33 23.33,6.67 28.33,5.00 "
        "C 33.33,3.33 36.67,6.67 40.00,10.00"
    )


def test_basis_spline_supports_closed_paths():
    assert basis_spline([(0, 0), (10, 20), (30, 0)], closed=True) == (
        "M 6.67,3.33 "
        "C 3.33,6.67 6.67,13.33 11.67,13.33 "
        "C 16.67,13.33 23.33,6.67 21.67,3.33 "
        "C 20.00,0.00 10.00,0.00 6.67,3.33 Z"
    )


def test_monotone_x_path_generates_limited_cubic_path():
    assert monotone_x_path([(0, 0), (10, 20), (30, 0)]) == (
        "M 0.00,0.00 "
        "C 3.33,6.67 6.67,20.00 10.00,20.00 "
        "C 16.67,20.00 23.33,6.67 30.00,0.00"
    )


def test_monotone_x_path_handles_flat_segments():
    assert monotone_x_path([(0, 0), (10, 0), (20, 10)]) == (
        "M 0.00,0.00 "
        "C 3.33,0.00 6.67,0.00 10.00,0.00 "
        "C 13.33,0.00 16.67,6.67 20.00,10.00"
    )


def test_monotone_y_path_generates_limited_cubic_path():
    assert monotone_y_path([(0, 0), (20, 10), (0, 30)]) == (
        "M 0.00,0.00 "
        "C 6.67,3.33 20.00,6.67 20.00,10.00 "
        "C 20.00,16.67 6.67,23.33 0.00,30.00"
    )


def test_empty_curve_helpers_return_empty_path():
    assert linear_path([]) == ""
    assert step_path([]) == ""
    assert catmull_rom_path([]) == ""
    assert basis_spline([]) == ""
    assert monotone_x_path([]) == ""
    assert monotone_y_path([]) == ""


def test_arc_distinguishes_zero_span_from_full_circle():
    assert arc(radius=10, start_angle=0, end_angle=0) == "M 10.00,0.00"

    full = arc(radius=10, start_angle=0, end_angle=360)

    assert full == (
        "M 10.00,0.00 "
        "A 10.00 10.00 0 0 1 -10.00,0.00 "
        "A 10.00 10.00 0 0 1 10.00,0.00"
    )


def test_arc_uses_sweep_and_large_arc_flags_from_angle_span():
    assert arc(radius=10, start_angle=0, end_angle=270) == (
        "M 10.00,0.00 A 10.00 10.00 0 1 1 0.00,-10.00"
    )
    assert arc(radius=10, start_angle=0, end_angle=-270) == (
        "M 10.00,0.00 A 10.00 10.00 0 1 0 0.00,10.00"
    )


def test_ring_without_inner_returns_closed_path():
    path_data = ring(
        inner_radius=5,
        outer_radius=10,
        start_angle=0,
        end_angle=90,
        without_inner=True,
    )

    assert path_data == (
        "M 5.00,0.00 "
        "L 10.00,0.00 "
        "A 10.00 10.00 0 0 1 0.00,10.00 "
        "L 0.00,5.00 Z"
    )


def test_ring_uses_reverse_sweep_for_inner_arc():
    assert ring(inner_radius=5, outer_radius=10, start_angle=0, end_angle=270) == (
        "M 10.00,0.00 "
        "A 10.00 10.00 0 1 1 0.00,-10.00 "
        "L 0.00,-5.00 "
        "A 5.00 5.00 0 1 0 5.00,0.00 Z"
    )
    assert ring(inner_radius=5, outer_radius=10, start_angle=0, end_angle=-270) == (
        "M 10.00,0.00 "
        "A 10.00 10.00 0 1 0 0.00,10.00 "
        "L 0.00,5.00 "
        "A 5.00 5.00 0 1 1 5.00,0.00 Z"
    )


def test_ring_zero_span_returns_empty_path():
    assert ring(inner_radius=5, outer_radius=10, start_angle=30, end_angle=30) == ""


@pytest.mark.parametrize(
    ("factory", "match"),
    [
        (lambda: star(n=1, inner_radius=5, outer_radius=10), "n must be at least 2"),
        (lambda: polyline([], []), "at least one point"),
        (lambda: polygon(0, 0, 10, 2), "n must be at least 3"),
        (lambda: cross(size=10, thickness=12), "less than or equal to size"),
        (lambda: arc(radius=0), "radius must be positive"),
        (lambda: ring(inner_radius=12, outer_radius=10), "inner_radius"),
        (lambda: linear_path([0, 0, 1]), "even number"),
        (lambda: step_path([(0, 0, 1)]), "exactly 2 coordinates"),
        (
            lambda: step_path([(0, 0), (1, 1)], mode=cast(Any, "bad")),
            "mode must be",
        ),
        (lambda: cardinal_spline([0, 0, 1], tension=0), "even number"),
        (lambda: cardinal_spline([0, 0, 10, 10], closed=True), "at least 3"),
        (lambda: cardinal_spline([0, 0, 10, 10], tension=2), "between 0 and 1"),
        (lambda: catmull_rom_path([0, 0, 10, 10], closed=True), "at least 3"),
        (lambda: basis_spline([0, 0, 10, 10], closed=True), "at least 3"),
        (lambda: monotone_x_path([(0, 0), (0, 10), (10, 20)]), "strictly"),
        (lambda: monotone_y_path([(0, 0), (10, 0), (20, 10)]), "strictly"),
    ],
)
def test_shape_helpers_validate_invalid_input(factory, match):
    with pytest.raises(ValueError, match=match):
        factory()
