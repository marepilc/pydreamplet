---
title: Definitions
description: Reference for defs, gradients, stops, patterns, masks, clip paths, and filters.
navigation:
  title: Definitions
category: reference
---

# Definitions

SVG definitions store reusable paint, clipping, masking, filtering, and pattern
resources. pyDreamplet wraps the common definition elements and provides
`SVG.ensure_defs()` to create or retrieve a document-level `<defs>` container.

Definition classes inherit [`SvgElement`](/reference/svg-element), so they
support dynamic attributes, child operations, copying, and serialization.

## Import

```python
import pydreamplet as dp
```

## Defs

```python
dp.Defs(**kwargs)
svg.ensure_defs() -> dp.Defs
```

`Defs` represents `<defs>`. In most drawings, call `ensure_defs()` on the root
SVG instead of constructing `Defs` yourself.

```python
svg = dp.SVG(260, 160)
defs = svg.ensure_defs()
```

If the SVG already has a direct `<defs>` child, `ensure_defs()` returns it. If
not, it inserts a new one as the first child.

## Definition References

Gradient, pattern, mask, clip path, and filter wrappers inherit from
`SvgDefinition`, the shared base class for reusable SVG resources. Its public
surface is intentionally small: it adds the `url` property used when another
element references the resource.

```python
gradient = dp.LinearGradient(id="accent")

print(gradient.url)  # url(#accent)
```

Use `url` when assigning a resource to `fill`, `stroke`, `mask`, `clip_path`,
or `filter`. The older `id_ref` property remains available as an alias.

```python
rect.fill = gradient.url
```

## Stop

```python
dp.Stop(
    offset: AttributeValue,
    color: str | None = None,
    opacity: AttributeValue = None,
    **kwargs,
)
```

`Stop` represents a gradient `<stop>`. `color` maps to `stop-color` and
`opacity` maps to `stop-opacity`.

```python
stop = dp.Stop("50%", "#14b8a6", opacity=0.8)
```

## LinearGradient

```python
dp.LinearGradient(
    id: str | None = None,
    *,
    x1: AttributeValue = None,
    y1: AttributeValue = None,
    x2: AttributeValue = None,
    y2: AttributeValue = None,
    **kwargs,
)
```

`LinearGradient` represents `<linearGradient>`.

```python
gradient = dp.LinearGradient(
    id="accent",
    x1="0%",
    y1="0%",
    x2="100%",
    y2="0%",
)
gradient.add_stop("0%", "#14b8a6")
gradient.add_stop("100%", "#38bdf8")
```

### `add_stop`

```python
gradient.add_stop(offset: AttributeValue, color: str, opacity: AttributeValue = None, **kwargs) -> Self
```

Appends a `Stop` and returns the gradient.

```python
gradient.add_stop("50%", "#ffffff", opacity=0.35)
```

## RadialGradient

```python
dp.RadialGradient(
    id: str | None = None,
    *,
    cx: AttributeValue = None,
    cy: AttributeValue = None,
    r: AttributeValue = None,
    fx: AttributeValue = None,
    fy: AttributeValue = None,
    **kwargs,
)
```

`RadialGradient` represents `<radialGradient>`.

```python
glow = dp.RadialGradient(id="glow", cx="50%", cy="50%", r="60%")
glow.add_stop("0%", "#ffffff", opacity=0.9)
glow.add_stop("100%", "#14b8a6", opacity=0)
```

## Pattern

```python
dp.Pattern(id: str | None = None, **kwargs)
```

`Pattern` represents `<pattern>`.

```python
pattern = dp.Pattern(
    id="dots",
    width=12,
    height=12,
    patternUnits="userSpaceOnUse",
)
pattern.append(dp.Circle(cx=3, cy=3, r=2, fill="#14b8a6"))
```

## Mask

```python
dp.Mask(id: str | None = None, **kwargs)
```

`Mask` represents `<mask>`.

```python
mask = dp.Mask(id="fade")
mask.append(
    dp.Rect(x=0, y=0, width=260, height=160, fill="black"),
    dp.Circle(cx=130, cy=80, r=58, fill="white"),
)
```

Assign a mask with the `mask` attribute.

```python
shape.mask = mask.url
```

## ClipPath

```python
dp.ClipPath(id: str | None = None, **kwargs)
```

`ClipPath` represents `<clipPath>`.

```python
clip = dp.ClipPath(id="round-window")
clip.append(dp.Circle(cx=130, cy=80, r=60))
```

Assign a clip path with `clip_path`, which serializes to `clip-path`.

```python
image_group.clip_path = clip.url
```

## Use

```python
dp.Use(href: str | dp.SvgElement | None = None, **kwargs)
```

`Use` represents `<use>` and creates an instance of another SVG element. Pass a
referenced element, an ID, or a `#id` reference.

```python
heart = dp.Path(
    id="heart",
    d="M10,30 A20,20,0,0,1,50,30 A20,20,0,0,1,90,30 Q90,60,50,90 Q10,60,10,30 Z",
)

copy = dp.Use(heart, fill="red")
assert copy.href == "#heart"
```

Use `clip_path`, `mask`, `filter`, and paint attributes with normal pyDreamplet
attribute names.

```python
clip = dp.ClipPath(id="myClip").append(dp.Circle(cx=40, cy=35, r=35))

svg.ensure_defs().append(clip)
svg.append(
    heart,
    dp.Use(heart, clip_path=clip.url, fill="red"),
)
```

## Filter

```python
dp.Filter(id: str | None = None, **kwargs)
```

`Filter` represents `<filter>`. Use generic `SvgElement` for filter primitive
children that do not have specialized wrappers.

```python
shadow = dp.Filter(id="shadow", x="-20%", y="-20%", width="140%", height="140%")
shadow.append(
    dp.SvgElement(
        "feDropShadow",
        dx=0,
        dy=4,
        stdDeviation=3,
        flood_color="#000000",
        flood_opacity=0.25,
    )
)
```

Assign a filter with the `filter` attribute.

```python
card.filter = shadow.url
```

## Complete Example

```python
svg = dp.SVG(260, 160)
defs = svg.ensure_defs()

gradient = dp.LinearGradient(id="accent", x1="0%", y1="0%", x2="100%", y2="0%")
gradient.add_stop("0%", "#14b8a6")
gradient.add_stop("100%", "#38bdf8")

shadow = dp.Filter(id="shadow", x="-20%", y="-20%", width="140%", height="140%")
shadow.append(
    dp.SvgElement(
        "feDropShadow",
        dx=0,
        dy=4,
        stdDeviation=3,
        flood_color="#000000",
        flood_opacity=0.2,
    )
)

defs.append(gradient, shadow)

svg.append(
    dp.Rect(
        x=36,
        y=36,
        width=188,
        height=88,
        rx=14,
        fill=gradient.url,
        filter=shadow.url,
    )
)
```
