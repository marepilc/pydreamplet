---
title: Animation
description: SVG animate elements, values, duration, and repeat count.
navigation:
  title: Animation
category: reference
---

# Animation

`Animate` creates an SVG `<animate>` element. Append it to a shape, text, path,
or group to animate one SVG attribute over time.

## Import

```python
import pydreamplet as dp
```

## Signature

```python
dp.Animate(attr: str, **kwargs)
```

The first argument is the SVG attribute name to animate. The constructor writes
that name to the generated `attributeName` attribute.

```python
svg = dp.SVG(360, 180)
svg.append(dp.Line(90, 90, 270, 90, stroke="currentColor", stroke_width=3, stroke_dasharray="8 8", opacity=0.35))

circle = dp.Circle(
    cx=90,
    cy=90,
    r=24,
    fill="currentColor",
    opacity=0.7,
    stroke="currentColor",
    stroke_width=4,
)

circle.append(
    dp.Animate("cx", values=[90, 270, 90], dur="3s"),
    dp.Animate("r", values=[24, 38, 24], dur="3s"),
    dp.Animate("opacity", values=[0.45, 1, 0.45], dur="3s"),
)

svg.append(circle)
```

::svg-preview{src="/showcase/ref_animation_animate.svg" alt="Animated SVG circle moving, growing, and changing opacity"}
::

## Constructor Parameters

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `attr` | `str` | required | SVG attribute name written to `attributeName`. |
| `repeatCount` | `int \| str` | `"indefinite"` | SVG repeat count. Use this exact camelCase keyword. |
| `values` | `list[Any]` | `None` | Keyframe values joined with semicolons. Non-list values are ignored. |
| `dur` | `str` | `"2s"` | SVG duration. |
| `**kwargs` | `Any` | none | Additional attributes for the `<animate>` element. |

`Animate` always sets:

| Attribute | Value |
| --- | --- |
| `attributeType` | `"XML"` |
| `attributeName` | the `attr` argument |
| `dur` | provided `dur`, or `"2s"` |
| `repeatCount` | provided `repeatCount`, or `"indefinite"` |

```python
anim = dp.Animate("opacity")

print(str(anim))
# <animate xmlns="http://www.w3.org/2000/svg" dur="2s" attributeType="XML" attributeName="opacity" repeatCount="indefinite" />
```

## Values

If `values` is a list, pyDreamplet stores the list on the instance and writes
the SVG `values` attribute by joining items with `;`.

```python
anim = dp.Animate("opacity", values=[0, 1, 0.5], dur="3s")

print(anim.values)
# [0, 1, 0.5]

print(anim.element.get("values"))
# 0;1;0.5
```

The current source annotates the getter as `list[str]`, while the setter accepts
`list[Any]`. At runtime, the original list values are preserved on the Python
object and converted to strings only for the SVG attribute.

Non-list constructor values are ignored.

```python
anim = dp.Animate("opacity", values="0;1;0")

print(anim.values)
# []

print(anim.has_attr("values"))
# False
```

## Properties

### `repeat_count`

```python
anim.repeat_count -> int | str
anim.repeat_count = value
```

Reads and writes the SVG `repeatCount` attribute.

```python
anim = dp.Animate("opacity")
anim.repeat_count = "5"

print(anim.element.get("repeatCount"))
# 5
```

### `values`

```python
anim.values -> list[str]
anim.values = value: list[Any]
```

Reads and writes the keyframe list. Setting it updates the SVG `values`
attribute.

```python
anim = dp.Animate("r")
anim.values = [8, 24, 8]

print(anim.element.get("values"))
# 8;24;8
```

## Attribute Names

Use SVG attribute names for `attr`, such as `"cx"`, `"r"`, `"fill"`,
`"opacity"`, or `"stroke-dashoffset"`.

For additional constructor keyword arguments, pyDreamplet applies the normal
`SvgElement` attribute-name normalization. That means `key_splines` becomes
`key-splines`.

SVG attributes that are not Python identifiers can be set after construction
with `attrs()`.

```python
anim = dp.Animate("opacity", values=[0, 1, 0], dur="2s")
anim.attrs({"calcMode": "spline", "keySplines": "0.4 0 0.2 1;0.4 0 0.2 1"})
```
