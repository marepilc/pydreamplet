---
icon: material/ruler
---

# Scales

Scales are functions that map from an input domain to an output range. They are useful for data visualization, allowing you to convert data values to visual properties like position, size, or color.

## Type Definitions

### `Real`

A type alias defined in `pydreamplet.core` representing numeric values:

```py
type Real = int | float
```

This type is used throughout the library for parameters that accept both integers and floating-point numbers.

### `NumericPair`

A type alias defined in `pydreamplet.scales` for representing numeric ranges:

```py
type NumericPair = tuple[Real, Real] | list[Real]
```

This type represents a pair of numeric values used for domains and ranges in scale functions. It can be either a tuple or a list containing two `Real` values.

## Scale Classes

- [**`LinearScale`**](linearscale.md) - Linear mapping between numeric domains
- [**`BandScale`**](bandscale.md) - Maps categories to evenly spaced bands
- [**`PointScale`**](pointscale.md) - Maps categories to discrete points
- [**`OrdinalScale`**](ordinalscale.md) - Maps categories to output values in cyclic fashion
- [**`ColorScale`**](colorscale.md) - Interpolates between colors based on numeric input
- [**`SquareScale`**](squarescale.md) - Square-root transformation for area-based scaling
- [**`CircleScale`**](circlescale.md) - Maps values to circle radii with area proportionality