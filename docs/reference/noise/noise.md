# `Noise`

The Noise class provides a simple implementation of a noise value generator using a random walk approach. It generates a sequence of noise values that vary within a specified range, with each new value computed relative to the previous one. The variation is controlled by the noise_range parameter, which represents a fraction of the total range between the minimum and maximum values.

## <span class=class></span>`dreamplet.noise.Noise`

<!--skip-->
```py
Noise(min_val: float, max_val: float, noise_range: float)
```

<span class="param">**Parameters**</span>

- `min_val ` *(float)*: The lower bound for the noise value.
- `max_val ` *(float)*: The upper bound for the noise value.
- `noise_range` *(float)*: The fraction (between 0 and 1) of the total range used for generating random walk steps.

<!--skip-->
```py
noise_gen = Noise(0.0, 100.0, 0.1)
print(noise_gen.value)  # Outputs a new noise value within the specified bounds
```

### <span class="prop"></span>`min`

**Getter:** Returns the current minimum bound.

<!--skip-->
```py
current_min = noise_gen.min
```

**Setter:** Updates the minimum bound. If the current noise value is below the new minimum, it is adjusted to the new minimum. The effective noise range is recalculated accordingly.

<!--skip-->
```py
noise_gen.min = 10.0
```

### <span class="prop"></span>`max`

**Getter:** Returns the current maximum bound.

<!--skip-->
```py
current_max = noise_gen.max
```

**Setter:** Updates the maximum bound. If the current noise value exceeds the new maximum, it is adjusted to the new maximum. The effective noise range is recalculated accordingly.

<!--skip-->
```py
noise_gen.max = 90.0
```

### <span class="prop"></span>`noise_range`
**Getter:** Returns the current noise range as a fraction of the total range (max - min). If the total range is zero, it returns 0.

<!--skip-->
```py
current_noise_range = noise_gen.noise_range
```

**Setter:** Sets the noise range as a fraction (between 0 and 1) of the total range (max - min). Internally, it computes the absolute range used for generating the next value.

<!--skip-->
```py
noise_gen.noise_range = 0.2
```

### <span class="prop"></span>`value`

**Getter:** Returns the next noise value computed using a random walk algorithm. Each access generates a new value that varies randomly within a window defined by the current noise range and then updates the internal state.

<!--skip-->
```py
current_value = noise_gen.value
```

**Setter:** Directly sets the noise value if the provided value lies within the [min, max] bounds.

<!--skip-->
```py
noise_gen.value = 50.0
```

### <span class="prop"></span>`int_value`

**Getter:** Returns the next noise value as an integer, by rounding the computed float value. Like value, accessing this property updates the internal noise state.

<!--skip-->
```py
rounded_value = noise_gen.int_value
```

### <span class="meth"></span>`_next_value`

This internal method computes the next noise value. It defines a window centered around the current value with a width equal to the absolute noise range. If the computed window exceeds the [min, max] bounds, it adjusts the window to remain within limits before generating the new value using a uniform random distribution.

*Note: This method is used internally and is automatically invoked when accessing the value or int_value properties.*