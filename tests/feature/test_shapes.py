import pytest

from pydreamplet.shapes import arc, cardinal_spline, cross, polygon, polyline, ring, star


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
        (lambda: cardinal_spline([0, 0, 1], tension=0), "even number"),
        (lambda: cardinal_spline([0, 0, 10, 10], closed=True), "at least 3"),
        (lambda: cardinal_spline([0, 0, 10, 10], tension=2), "between 0 and 1"),
    ],
)
def test_shape_helpers_validate_invalid_input(factory, match):
    with pytest.raises(ValueError, match=match):
        factory()
