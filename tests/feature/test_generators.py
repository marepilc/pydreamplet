from typing import Literal, TypedDict

import pytest

from pydreamplet.generators import (
    ArcGenerator,
    AreaGenerator,
    LineGenerator,
    LinkGenerator,
    PieGenerator,
    PieSlice,
    RadialAreaGenerator,
    RadialLineGenerator,
    SymbolGenerator,
)


class XYDatum(TypedDict):
    x: int
    y: int


class SymbolDatum(TypedDict):
    symbol: Literal["triangle"]
    size: int


class LinkDatum(TypedDict):
    source: tuple[int, int]
    target: tuple[int, int]


def test_line_generator_uses_default_pair_accessors():
    generator = LineGenerator()

    assert generator([(0, 0), (10, 20), (30, 0)]) == (
        "M 0.00,0.00 L 10.00,20.00 L 30.00,0.00"
    )


def test_line_generator_splits_undefined_segments():
    generator = LineGenerator(defined=lambda item, _index: item is not None)

    assert generator([(0, 0), None, (10, 20), (30, 0)]) == (
        "M 0.00,0.00 M 10.00,20.00 L 30.00,0.00"
    )


def test_line_generator_supports_accessors_and_curves():
    data: list[XYDatum] = [{"x": 0, "y": 0}, {"x": 10, "y": 20}, {"x": 30, "y": 0}]
    generator = LineGenerator[XYDatum](
        x=lambda item, _index: item["x"],
        y=lambda item, _index: item["y"],
        curve="step",
    )

    assert generator(data) == (
        "M 0.00,0.00 L 5.00,0.00 L 5.00,20.00 L 10.00,20.00 "
        "L 20.00,20.00 L 20.00,0.00 L 30.00,0.00"
    )


def test_area_generator_closes_upper_and_lower_points():
    generator = AreaGenerator(y0=lambda _item, _index: 10)

    assert generator([(0, 0), (10, 20), (30, 0)]) == (
        "M 0.00,0.00 L 10.00,20.00 L 30.00,0.00 "
        "L 30.00,10.00 L 10.00,10.00 L 0.00,10.00 Z"
    )


def test_radial_line_generator_projects_degrees_to_cartesian_points():
    generator = RadialLineGenerator[tuple[int, int]](
        angle=lambda item, _index: item[0],
        radius=lambda item, _index: item[1],
    )

    assert generator([(0, 10), (90, 10), (180, 10)]) == (
        "M 10.00,0.00 L 0.00,10.00 L -10.00,0.00"
    )


def test_radial_area_generator_projects_inner_and_outer_radii():
    generator = RadialAreaGenerator[tuple[int, int]](
        angle=lambda item, _index: item[0],
        inner_radius=lambda _item, _index: 5,
        outer_radius=lambda item, _index: item[1],
    )

    assert generator([(0, 10), (90, 10)]) == (
        "M 10.00,0.00 L 0.00,10.00 L 0.00,5.00 L 5.00,0.00 Z"
    )


def test_pie_generator_returns_slice_metadata():
    slices = PieGenerator(start_angle=-90)([1, 2, 3])

    assert [(slice.start_angle, slice.end_angle) for slice in slices] == [
        (-90, -30),
        (-30, 90),
        (90, 270),
    ]
    assert slices[1].value == 2
    assert slices[1].index == 1
    assert slices[1].angle == 120
    assert slices[1].mid_angle == 30


def test_arc_generator_turns_pie_slices_into_ring_paths():
    slices = PieGenerator(start_angle=0, end_angle=90)([1])
    generator = ArcGenerator[PieSlice](
        inner_radius=lambda _item, _index: 5,
        outer_radius=lambda _item, _index: 10,
        start_angle=lambda item, _index: item.start_angle,
        end_angle=lambda item, _index: item.end_angle,
    )

    assert generator(slices[0]) == (
        "M 10.00,0.00 "
        "A 10.00 10.00 0 0 1 0.00,10.00 "
        "L 0.00,5.00 "
        "A 5.00 5.00 0 0 0 5.00,0.00 Z"
    )


def test_symbol_generator_returns_centered_symbol_paths():
    assert SymbolGenerator(symbol="square", size=100)() == (
        "M -5.00,-5.00 L 5.00,-5.00 L 5.00,5.00 L -5.00,5.00 Z"
    )
    item: SymbolDatum = {"symbol": "triangle", "size": 100}
    assert SymbolGenerator[SymbolDatum](
        symbol=lambda item, _index: item["symbol"],
        size=lambda item, _index: item["size"],
    )(item).startswith("M 0.00,-8.77")


def test_link_generator_supports_linear_and_orthogonal_cubic_links():
    item: LinkDatum = {"source": (0, 10), "target": (100, 50)}

    assert LinkGenerator[LinkDatum](
        source=lambda item, _index: item["source"],
        target=lambda item, _index: item["target"],
        curve="linear",
    )(item) == "M 0.00,10.00 L 100.00,50.00"

    assert LinkGenerator[LinkDatum](
        source=lambda item, _index: item["source"],
        target=lambda item, _index: item["target"],
    )(item) == "M 0.00,10.00 C 50.00,10.00 50.00,50.00 100.00,50.00"

    assert LinkGenerator[LinkDatum](
        source=lambda item, _index: item["source"],
        target=lambda item, _index: item["target"],
        curve="vertical",
    )(item) == "M 0.00,10.00 C 0.00,30.00 100.00,30.00 100.00,50.00"


@pytest.mark.parametrize(
    ("factory", "match"),
    [
        (lambda: PieGenerator()([0, 0]), "positive"),
        (lambda: PieGenerator()([1, -1]), "non-negative"),
        (lambda: SymbolGenerator(symbol="square", size=-1)(), "non-negative"),
        (
            lambda: LineGenerator[tuple[int, int]](curve="monotone-x")(
                [(0, 0), (0, 10), (10, 20)]
            ),
            "strictly",
        ),
    ],
)
def test_generators_validate_invalid_input(factory, match):
    with pytest.raises(ValueError, match=match):
        factory()
