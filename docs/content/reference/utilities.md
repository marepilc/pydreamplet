---
title: Utilities
description: Numeric, angle, tick, pie, sampling, and collision helper utilities.
navigation:
  title: Utilities
category: reference
---

# Utilities

The `pydreamplet.utils` module contains small helpers used by colors, generators,
scales, charts, and label layout.

Utilities are imported from `pydreamplet.utils`.

```python
from pydreamplet.utils import calculate_ticks, place_labels_1d
```

## Visual Example

This example uses `place_labels_1d()` to resolve overlapping labels while keeping
each label close to its original anchor.

```python
import pydreamplet as dp
from pydreamplet.utils import place_labels_1d

anchors = [42, 55, 68, 128, 136, 206]
sizes = [36, 36, 36, 44, 44, 38]
placements = place_labels_1d(anchors, sizes, gap=4, bounds=(24, 276))

svg = dp.SVG(300, 150)
svg.append(dp.Line(24, 114, 276, 114, stroke="currentColor", opacity=0.3))

for anchor, placement in zip(anchors, placements):
    svg.append(
        dp.Line(anchor, 114, placement.position, 78, stroke="currentColor", opacity=0.35),
        dp.Circle(cx=anchor, cy=114, r=3, fill="#f83898"),
        dp.Rect(
            x=placement.start,
            y=60,
            width=placement.size,
            height=24,
            rx=4,
            fill="#14b8a6",
            opacity=0.24,
            stroke="#14b8a6",
            stroke_width=1.5,
        ),
        dp.Text(
            str(int(anchor)),
            x=placement.position,
            y=76,
            font_size=11,
            text_anchor="middle",
            fill="currentColor",
        ),
    )

svg.append(dp.Text("anchor positions", x=24, y=134, font_size=12, fill="currentColor"))
svg.append(dp.Text("resolved label positions", x=58, y=45, font_size=12, fill="currentColor"))
```

::svg-preview{src="/showcase/ref_utilities_labels.svg" alt="Overlapping anchor labels moved into non-overlapping positions."}
::

## Numeric Helpers

```python
math_round(x: Real) -> int
```

Rounds with half-up behavior by returning `int(x + 0.5)`.

```python
from pydreamplet.utils import math_round

assert math_round(3.4) == 3
assert math_round(3.6) == 4
```

```python
constrain(value: Real, min_val: Real, max_val: Real) -> Real
```

Clamps `value` into the inclusive range `[min_val, max_val]`.

```python
from pydreamplet.utils import constrain

assert constrain(10, 0, 5) == 5
assert constrain(-3, 0, 5) == 0
```

```python
radians(degrees: Real) -> Real
degrees(radians: Real) -> Real
```

Converts between degrees and radians.

```python
from pydreamplet.utils import degrees, radians

assert radians(180) == 3.141592653589793
assert degrees(3.141592653589793) == 180.0
```

## Ticks

```python
calculate_ticks(
    min_val: Real,
    max_val: Real,
    num_ticks: int = 5,
    below_max: bool = True,
) -> list[Real]
```

Returns rounded tick values using 1, 2, 5, or 10 times a power-of-ten step.
`min_val` must be less than `max_val`. When `below_max` is `True`, ticks above
the maximum are removed.

```python
from pydreamplet.utils import calculate_ticks

assert calculate_ticks(0, 42986, 5) == [0, 10000, 20000, 30000, 40000]
assert calculate_ticks(0, 1, 5) == [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
assert calculate_ticks(0, 42986, 3, below_max=False) == [0, 20000, 40000, 60000]
```

## Pie Angles

```python
pie_angles(
    values: Sequence[Real],
    start_angle: Real = 0,
    end_angle: Real | None = None,
) -> list[tuple[float, float]]
```

Splits an angular span proportionally by `values`. If `end_angle` is omitted,
the span is a full turn from `start_angle` to `start_angle + 360`.

```python
from pydreamplet.utils import pie_angles

assert pie_angles([1, 2, 3]) == [(0, 60), (60, 180), (180, 360)]
assert pie_angles([1, 2, 3], start_angle=90) == [(90, 150), (150, 270), (270, 450)]
assert pie_angles([]) == []
```

A list whose sum is zero raises `ZeroDivisionError`.

## Sampling

```python
sample_uniform(
    input_list: list[Any],
    n: int,
    precedence: Literal["first", "last"] | None = None,
) -> tuple[int, ...]
```

Returns evenly spaced indices. By default, the first and last indices are
included, and `n` is the maximum number of indices returned. If `n` is greater
than the input length, every index is returned. With `n=1`, the default mode
returns the first index.

`precedence="first"` and `"last"` retain the anchored sampling behavior.

```python
from pydreamplet.utils import sample_uniform

items = list(range(10))

assert sample_uniform(items, n=4) == (0, 3, 6, 9)
assert sample_uniform(items, n=20) == tuple(range(10))
assert sample_uniform(items, n=4, precedence="first") == (0, 3, 6, 9)
assert sample_uniform(items, n=3, precedence="last") == (1, 5, 9)
```

Invalid precedence values raise `ValueError`.

## Label Layout

```python
force_distance(values: Sequence[Real], distance: Real) -> list[Real]
```

Adjusts unsorted numeric positions so adjacent sorted positions are at least
`distance` apart, then returns results in the original input order.

```python
from pydreamplet.utils import force_distance

positions = force_distance([2, 6, 7, 8, 10, 16, 18], distance=2)
assert positions == [2, 5, 7, 9, 11, 16, 18]
```

```python
resolve_collisions_1d(
    anchors: Sequence[Real],
    sizes: Sequence[Real],
    *,
    gap: Real = 0,
    bounds: tuple[Real, Real] | None = None,
) -> list[float]
```

Resolves centered 1D items so their extents do not overlap. `anchors` and
`sizes` must have the same length. `gap` and every size must be non-negative.
When `bounds` are provided, each item's full extent is kept inside the range.
If the last item exceeds the upper bound, the backward pass moves only its
adjacent collision chain. Earlier, non-colliding items are not shifted as a
group.

```python
from pydreamplet.utils import resolve_collisions_1d

assert resolve_collisions_1d([0, 1, 10], [4, 4, 4], gap=1) == [0, 5, 10]
assert resolve_collisions_1d([5, 0, 1], [4, 4, 4], gap=1) == [10, 0, 5]
```

For bounded layouts, labels outside the affected collision chain retain their
positions:

```python
positions = resolve_collisions_1d(
    [139.82, 92.97, 291.10, 331.26, 340.63, 221.48],
    [19.11] * 6,
    gap=4,
    bounds=(18, 350),
)

assert [round(position, 3) for position in positions] == [
    139.82,
    92.97,
    291.1,
    317.335,
    340.445,
    221.48,
]
```

```python
place_labels_1d(
    anchors: Sequence[Real],
    sizes: Sequence[Real],
    *,
    gap: Real = 0,
    bounds: tuple[Real, Real] | None = None,
) -> list[LabelPlacement]
```

Wraps `resolve_collisions_1d()` and returns `LabelPlacement` records.

```python
from pydreamplet.utils import place_labels_1d

placements = place_labels_1d([0, 1], [4, 4], gap=1)

assert [placement.position for placement in placements] == [0, 5]
assert placements[0].start == -2
assert placements[0].end == 2
```

`LabelPlacement` is a frozen dataclass with `anchor`, `position`, and `size`
fields plus computed `start` and `end` properties.

## Bounding Boxes

```python
bboxes_overlap(a: BoundingBox, b: BoundingBox, padding: Real = 0) -> bool
```

Returns `True` when two `BoundingBox` objects overlap. Touching edges are not
considered overlapping. Positive `padding` expands both boxes before testing.

```python
from pydreamplet import BoundingBox
from pydreamplet.utils import bboxes_overlap

left = BoundingBox(0, 0, 10, 10)
right = BoundingBox(10, 0, 5, 5)

assert bboxes_overlap(left, right) is False
assert bboxes_overlap(left, right, padding=0.1) is True
```

Negative padding raises `ValueError`.
