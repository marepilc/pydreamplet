# `Vector`

The Vector class provides a simple implementation of a two-dimensional vector. It supports common operations such as addition, subtraction, scalar multiplication and division, normalization, and more. The class makes use of Python’s operator overloading to enable intuitive arithmetic with vectors, and it also offers properties for accessing and modifying the vector’s components, magnitude, and direction.

## <span class=class></span>`dreamplet.math.Vector`

```py
Vector(self, x: float, y: float)
```

Initializes a new 2D vector with the given x and y coordinates.

<span class="param">**Parameters**</span>

- `x` *(float)*: The x-coordinate.
- `y` *(float)*: The y-coordinate.

```py
v = Vector(3.0, 4.0)
print(v)  # Output: Vector(x=3.0, y=4.0)
```

### <span class="meth"></span>`set`

```py
set(self, x: float, y: float) -> None
```

Updates the x and y coordinates of the vector.

```py
v = Vector(1.0, 2.0)
v.set(5.0, 6.0)
print(v.xy)  # Output: (5.0, 6.0)

```

### <span class="meth"></span>`copy`

```py
copy(self) -> Vector
```

Returns a duplicate of the vector.

```py
v1 = Vector(2.0, 3.0)
v2 = v1.copy()
print(v1 == v2)  # Output: True
```

### <span class="meth"></span>`dot`

```py
dot(self, other: "Vector") -> float
```

Calculates the dot product of the current vector with another vector.

```py
v1 = Vector(1.0, 2.0)
v2 = Vector(3.0, 4.0)
result = v1.dot(v2)
print(result)  # Output: 11.0 (1*3 + 2*4)
```

### <span class="meth"></span>`normalize`

```py
normalize(self) -> Vector
```

Returns a new vector that is the normalized version of the current vector (i.e., with a magnitude of 1). Raises a ValueError if the vector is zero.

```py
v = Vector(3.0, 4.0)
normalized_v = v.normalize()
print(normalized_v.magnitude)  # Output: 1.0
```

### <span class="meth"></span>`limit`

```py
limit(self, limit_scalar: float) -> None
```

Limits the magnitude of the vector to `limit_scalar`. If the current magnitude exceeds the limit, the vector is scaled down to the specified maximum.

```py
v = Vector(10.0, 0.0)
v.limit(5.0)
print(v.magnitude)  # Output: 5.0
```

### <span class="prop"></span>`x` and `y`

Get or set the individual x and y components of the vector.

```py
v = Vector(1.0, 2.0)
print(v.x, v.y)  # Output: 1.0 2.0
v.x = 10.0
v.y = 20.0
print(v.xy)  # Output: (10.0, 20.0)
```

### <span class="prop"></span>`xy`

Returns a tuple containing the x and y coordinates of the vector.

```py
v = Vector(5.0, 6.0)
print(v.xy)  # Output: (5.0, 6.0)
```

### <span class="prop"></span>`direction`

**Getter:** Returns the angle (in radians) of the vector relative to the positive x-axis, calculated using `atan2`.

```py
v = Vector(1.0, 1.0)
print(v.direction)  # Output: ~0.785 (approximately pi/4)
```

**Setter:** Sets the vector’s direction (angle in radians) while preserving its magnitude.

```py
v = Vector(3.0, 4.0)
v.direction = math.pi / 2  # Set direction to 90 degrees
print(v)  # Output: Vector(x≈0.0, y=5.0)
```

### <span class="prop"></span>`magnitude`

**Getter:** Returns the length of the vector.

```py
v = Vector(3.0, 4.0)
print(v.magnitude)  # Output: 5.0
```

**Setter:** Sets the vector’s magnitude while preserving its direction.

```py
v = Vector(3.0, 4.0)
v.magnitude = 10.0
print(v.magnitude)  # Output: 10.0
```

## Operations

### Addition

```py
v1 = Vector(1.0, 2.0)
v2 = Vector(3.0, 4.0)
v3 = v1 + v2
print(v3)  # Output: Vector(x=4.0, y=6.0)
```

### Subtraction

```py
v1 = Vector(5.0, 7.0)
v2 = Vector(2.0, 3.0)
v3 = v1 - v2
print(v3)  # Output: Vector(x=3.0, y=4.0)
```

### Scalar Multiplication

```py
v = Vector(2.0, 3.0)
v_scaled = v * 3
print(v_scaled)  # Output: Vector(x=6.0, y=9.0)
```

### Scalar Division

```py
v = Vector(6.0, 9.0)
v_divided = v / 3
print(v_divided)  # Output: Vector(x=2.0, y=3.0)
```

### Comparison

```py
v1 = Vector(1.0, 2.0)
v2 = Vector(1.0, 2.0)
print(v1 == v2)  # Output: True
```