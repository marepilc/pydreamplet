# Type Definitions

This page documents the custom type definitions used throughout the pydreamplet library.

## Core Types

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