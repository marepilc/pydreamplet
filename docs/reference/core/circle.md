# `Circle`

The `Circle` class represents an SVG circle element. It supports setting the center position and radius, and provides computed properties such as diameter and area.

!!! info

    This class inherits from [**`SvgElement`**](svgelement.md).

### <span class=class></span>`pydreamplet.core.Circle`

```py
Circle(**kwargs)
```

Initializes a new circle. If pos is provided in kwargs, it sets the circle's center coordinates.

<span class="param">**Parameters**</span>

- `**kwargs`: Attributes for the circle, including pos (a [`Vector`](../math/vector.md)) and other SVG properties (e.g., r for radius).

```py
from pydreamplet import SVG, Circle

svg = SVG(200, 200)
svg.append(Circle(cx=100, cy=100, r=50, fill="#a00344"))
```

<figure class="light-dark-bg" markdown="span">
  ![Result](assets/circle_example.svg)
  <figcaption>Result</figcaption>
</figure>

### <span class="prop"></span>`pos`

**Getter:** Returns the center of the circle as a [`Vector`](../math/vector.md).

**Setter:** Updates the center coordinates.

```py
print(circle.pos)
circle.pos = Vector(60, 60)
```

### <span class="prop"></span>`radius`
**Getter:** Returns the radius of the circle.

**Setter:** Updates the radius.

```py
print(circle.radius)
circle.radius = 30
```

### <span class="prop"></span>`center`

Alias for pos, returning the circle's center.

### <span class="prop"></span>`diameter`

Returns the circle's diameter (2 × radius).

### <span class="prop"></span>`area`

Returns the area of the circle, computed as $\pi \times (\text{radius})^2$.