# Type Definitions

This page documents the custom type definitions used throughout the pydreamplet library.

## Core Types

### `BoundingBox`

Defined in `pydreamplet.core`:

<!--skip-->
```py
BoundingBox(x: float, y: float, width: float, height: float)
```

Represents an axis-aligned bounding box. The `x` and `y` values are the top-left
corner. The class also exposes `left`, `top`, `right`, `bottom`, and `center`
properties.

```py
import pydreamplet as dp

rect = dp.Rect(pos=(10, 20), width=30, height=40)
box = rect.bbox
print(box.right)   # 40.0
print(box.center)  # Vector(x=25.0, y=40.0)
```

### `Real`

Defined in `pydreamplet.core`:

```py
type Real = int | float
```

The `Real` type represents numeric values that can be either integers or floating-point numbers. This type is used extensively throughout the library for coordinates, dimensions, angles, and other numeric parameters.

**Usage Examples:**

```py
from pydreamplet.core import Real

# These are all valid Real values
x: Real = 10      # integer
y: Real = 20.5    # float
angle: Real = 45  # integer for angle
```

**Used in:**
- Vector coordinates (`Vector(x: Real, y: Real)`)
- SVG element dimensions and positions
- Mathematical operations and transformations
- Scale domains and ranges

## Import Usage

The `Real` type can be imported and used in your own code:

```py
from pydreamplet.core import Real

def my_function(value: Real) -> Real:
    return value * 2
```

This provides consistent typing across your application when working with pydreamplet objects and functions.
