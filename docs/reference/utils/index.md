# Helper functions

This module provides utility functions for various mathematical operations and unit conversions. It includes functions for rounding numbers using a round half up method, constraining values within a specified range, converting between degrees and radians, and generating rounded tick values for grid lines.

## <span class="func"></span>`math_round`

```py
math_round(x)
```

Rounds `x` to the nearest integer using the round half up method.

<span class="param">**Parameters**</span>

- `x` *(float)*: The number to round.

<span class="returns">**Returns**</span>

*(int)*: The rounded integer.

```py
print(math_round(3.4))  # Output: 3
print(math_round(3.6))  # Output: 4
```

## <span class="func"></span>`constrain`

```py
constrain(value, min_val, max_val)
```

Constrains the given `value` between `min_val` and `max_val`.

<span class="param">**Parameters**</span>

- `value` *(numeric)*: The value to be constrained.
- `min_val` *(numeric)*: The minimum allowed value.
- `max_val` *(numeric)*: The maximum allowed value.

<span class="returns">**Returns**</span>

*(numeric)*: The constrained value.

```py
print(constrain(10, 0, 5))  # Output: 5
print(constrain(-3, 0, 5))  # Output: 0
```

## <span class="func"></span>`radians`

```py
radians(degrees)
```

Converts an angle from degrees to radians.

<span class="param">**Parameters**</span>

- `degrees` *(float)*: Angle in degrees.
- 
<span class="returns">**Returns**</span>

*(float)*: Angle in radians.

```py
print(radians(180))  # Output: 3.141592653589793 (approximately)
```

## <span class="func"></span>`degrees`

```py
degrees(radians)
```

Converts an angle from radians to degrees.

<span class="param">**Parameters**</span>

- `radians` *(float)*: Angle in radians.

<span class="returns">**Returns**</span>

*(float)*: Angle in degrees.

```py
print(degrees(3.141592653589793))  # Output: 180.0
```

## <span class="func"></span>`calculate_ticks`

```py
calculate_ticks(min_val, max_val, num_ticks=5)
```

Generates a list of rounded tick values between `min_val` and `max_val`. The number of ticks is approximately equal to `num_ticks`.

<span class="param">**Parameters**</span>

- `min_val` *(float)*: The minimum value.
- `max_val` *(float)*: The maximum value.
- `num_ticks` *(int, optional)*: The desired number of tick values (default: 5).

<span class="returns">**Returns**</span>

*(list[int])*: A list of rounded tick values.

Raises `ValueError`: If min_val is not less than max_val.

```py
ticks = calculate_ticks(0, 100, num_ticks=5)
print(ticks)  # Example output: [0, 20, 40, 60, 80, 100]
```