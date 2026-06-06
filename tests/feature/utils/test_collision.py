import pytest

from pydreamplet.core import BoundingBox
from pydreamplet.utils import (
    bboxes_overlap,
    place_labels_1d,
    resolve_collisions_1d,
)


def test_bboxes_overlap_treats_touching_edges_as_non_overlapping():
    left = BoundingBox(0, 0, 10, 10)
    right = BoundingBox(10, 0, 5, 5)

    assert bboxes_overlap(left, right) is False
    assert bboxes_overlap(left, right, padding=0.1) is True


def test_bboxes_overlap_detects_separated_and_overlapping_boxes():
    box = BoundingBox(0, 0, 10, 10)

    assert bboxes_overlap(box, BoundingBox(5, 5, 10, 10)) is True
    assert bboxes_overlap(box, BoundingBox(11, 0, 5, 5)) is False
    assert bboxes_overlap(box, BoundingBox(0, 11, 5, 5)) is False


def test_resolve_collisions_1d_preserves_order_and_spacing():
    result = resolve_collisions_1d([0, 1, 10], [4, 4, 4], gap=1)

    assert result == pytest.approx([0, 5, 10])


def test_resolve_collisions_1d_returns_positions_in_input_order():
    result = resolve_collisions_1d([5, 0, 1], [4, 4, 4], gap=1)

    assert result == pytest.approx([10, 0, 5])


def test_resolve_collisions_1d_respects_lower_and_upper_bounds():
    assert resolve_collisions_1d([0, 1, 2], [4, 4, 4], gap=1, bounds=(0, 20)) == (
        pytest.approx([2, 7, 12])
    )
    assert resolve_collisions_1d([18, 19, 20], [4, 4, 4], gap=1, bounds=(0, 20)) == (
        pytest.approx([8, 13, 18])
    )


def test_place_labels_1d_returns_extents():
    placements = place_labels_1d([0, 1], [4, 4], gap=1)

    assert [placement.anchor for placement in placements] == [0, 1]
    assert [placement.position for placement in placements] == pytest.approx([0, 5])
    assert placements[0].start == -2
    assert placements[0].end == 2
    assert placements[1].start == 3
    assert placements[1].end == 7


@pytest.mark.parametrize(
    ("factory", "match"),
    [
        (lambda: bboxes_overlap(BoundingBox(0, 0, 1, 1), BoundingBox(0, 0, 1, 1), -1), "padding"),
        (lambda: resolve_collisions_1d([0], [1, 2]), "same length"),
        (lambda: resolve_collisions_1d([0], [-1]), "non-negative"),
        (lambda: resolve_collisions_1d([0], [1], gap=-1), "gap"),
        (lambda: resolve_collisions_1d([0], [1], bounds=(10, 0)), "bounds"),
    ],
)
def test_collision_helpers_validate_invalid_input(factory, match):
    with pytest.raises(ValueError, match=match):
        factory()
