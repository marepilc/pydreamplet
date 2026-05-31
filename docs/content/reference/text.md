---
title: Text
description: Text elements, multiline text, text paths, positions, and font-size behavior.
navigation:
  title: Text
category: reference
---

# Text

pyDreamplet provides `Text` for SVG `<text>` elements and `TextOnPath` for text
inside a nested `<textPath>`.

Both classes inherit the shared `SvgElement` attribute API, so SVG attributes
use Python-friendly names such as `font_size`, `font_weight`, `text_anchor`, and
`alignment_baseline`.

## Import

```python
import pydreamplet as dp
```

## Type Names

| Type | Meaning |
| --- | --- |
| `Real` | `int \| float` |
| `PointLike` | `Vector \| tuple[Real, Real] \| list[Real]` |

## Text

```python
dp.Text(
    initial_text: str = "",
    *,
    pos: PointLike | None = None,
    x: Real | None = None,
    y: Real | None = None,
    v_space: Real | None = None,
    **kwargs,
)
```

Creates an SVG `<text>` element.

| Parameter | Type | Description |
| --- | --- | --- |
| `initial_text` | `str` | Initial text content. |
| `pos` | `PointLike \| None` | Convenience position. Writes `x` and `y`. |
| `x` | `Real \| None` | SVG `x` attribute. |
| `y` | `Real \| None` | SVG `y` attribute. |
| `v_space` | `Real \| None` | Line spacing used when content contains newlines. |
| `**kwargs` | `Any` | Additional SVG attributes. |

`pos` is applied after `x` and `y`, so it wins if both are provided.

```python
text = dp.Text(
    "Hello",
    pos=(10, 20),
    font_size=12,
    font_weight=700,
    text_anchor="middle",
)

print(text.pos)
# Vector(x=10.0, y=20.0)

print(str(text))
# <text xmlns="http://www.w3.org/2000/svg" font-size="12" font-weight="700" text-anchor="middle" x="10.0" y="20.0">Hello</text>
```

## Properties

| Property | Type | Description |
| --- | --- | --- |
| `pos` | `Vector` | Reads and writes the `x` and `y` attributes. |
| `content` | `str` | Reads and writes text content. |
| `font_size` | `str \| int \| float` | Getter returns the numeric part as `float`; setter writes the SVG attribute. |

### Position

`pos` accepts a `Vector`, tuple, or list when setting.

```python
text = dp.Text("label")
text.pos = [30, 40]

print(text.x)    # 30.0
print(text.y)    # 40.0
print(text.pos)  # Vector(x=30.0, y=40.0)
```

Reading `pos` defaults missing coordinates to `0`.

```python
text = dp.Text("origin")

print(text.pos)
# Vector(x=0.0, y=0.0)
```

### Content

For single-line content, pyDreamplet stores the string directly on the `<text>`
element.

```python
text = dp.Text("Hello, World!", x=10, y=10, font_size=18)

print(text.content)
# Hello, World!
```

When assigned content contains newline characters, pyDreamplet replaces existing
child elements with `<tspan>` children.

```python
text = dp.Text("", x=10, y=10, font_size=20)
text.content = "Hello,\nWorld!"

print(str(text))
# <text xmlns="http://www.w3.org/2000/svg" font-size="20" x="10" y="10"><tspan x="10" y="10">Hello,</tspan><tspan x="10" dy="20.0">World!</tspan></text>
```

The first `<tspan>` receives the parent `x` and `y` attributes when present. Each
following `<tspan>` receives the parent `x` and a `dy` value.

If `v_space` is set, it is used as `dy`. Otherwise pyDreamplet uses the numeric
value of `font-size`; if that cannot be parsed, it falls back to `16`.

```python
svg = dp.SVG(320, 160)
svg.append(dp.Rect(x=0, y=0, width=320, height=160, fill="#f8fafc"))

text = dp.Text(
    "Hello,\nWorld!",
    x=34,
    y=58,
    font_size=32,
    v_space=40,
    fill="#1b313b",
    font_weight=700,
)

svg.append(text)
```

<img src="/showcase/ref_text_multiline.svg" alt="Multiline SVG text split into two tspan lines" class="mt-6 w-full rounded-lg border border-neutral-200 bg-white p-4 dark:border-neutral-800" />

Assigning new content removes any existing child elements before writing the new
content.

### Font Size

The `font_size` setter appends `px` only when the value does not contain any
letter.

```python
text = dp.Text("Label")

text.font_size = "12"
print(text.element.get("font-size"))  # 12px

text.font_size = "10.5pt"
print(text.element.get("font-size"))  # 10.5pt
```

The getter extracts the leading numeric part and returns it as a float. If the
attribute is missing or does not start with a number, it returns `16.0`.

```python
text = dp.Text("Label", font_size="18px")

print(text.font_size)
# 18.0
```

Constructor attributes are handled by the shared dynamic attribute API. Passing
`font_size=12` to the constructor writes `font-size="12"` directly; the `px`
defaulting behavior only happens when assigning through the `font_size`
property.

## TextOnPath

```python
dp.TextOnPath(
    initial_text: str = "",
    path_id: str = "",
    text_path_args: dict[str, object] | None = None,
    **kwargs,
)
```

Creates a `<text>` element with a nested `<textPath>`.

| Parameter | Type | Description |
| --- | --- | --- |
| `initial_text` | `str` | Initial text content inside `<textPath>`. |
| `path_id` | `str` | Referenced path id. `#` is added when omitted. |
| `text_path_args` | `dict[str, object] \| None` | Attributes applied to the nested `<textPath>`. |
| `**kwargs` | `Any` | Attributes applied to the outer `<text>` element. |

```python
svg = dp.SVG(360, 180)
svg.append(dp.Rect(x=0, y=0, width=360, height=180, fill="#f8fafc"))

path = dp.Path(
    id="curve",
    d="M40 120 C95 30 265 30 320 120",
    fill="none",
    stroke="#0f766e",
    stroke_width=3,
)

label = dp.TextOnPath(
    "Text follows the curve",
    path_id="curve",
    text_path_args={
        "startOffset": "50%",
        "text_anchor": "middle",
    },
    fill="#be185d",
    font_size=24,
    font_weight=700,
)

svg.append(path).append(label)
```

<img src="/showcase/ref_text_on_path.svg" alt="Text rendered along a curved SVG path" class="mt-6 w-full rounded-lg border border-neutral-200 bg-white p-4 dark:border-neutral-800" />

If `path_id` already starts with `#`, it is used unchanged.

```python
label = dp.TextOnPath("around", path_id="#curve")

print(label.text_path.href)
# #curve
```

`text_path_args` can set or override any nested textPath attribute. When
`path_id` is provided, its generated `href` is only used if `text_path_args` does
not already contain `href`.

Use exact SVG attribute casing for attributes that require it, such as
`startOffset`. Python-friendly underscore names are still normalized, so
`text_anchor` becomes `text-anchor`.

```python
label = dp.TextOnPath(
    "around",
    path_id="curve",
    text_path_args={"href": "#other-curve"},
)

print(label.text_path.href)
# #other-curve
```

## TextOnPath Properties

| Property | Type | Description |
| --- | --- | --- |
| `text_path` | `SvgElement` | Wrapper around the nested `<textPath>` element. |
| `content` | `str` | Reads and writes nested `<textPath>` text. |
| `font_size` | `str \| int \| float` | Same behavior as `Text.font_size`, applied to the outer `<text>`. |

```python
label = dp.TextOnPath("old", path_id="curve")
label.content = "new"

print(label.content)
# new

label.font_size = "15em"
print(label.element.get("font-size"))  # 15em
print(label.font_size)                 # 15.0
```

## Common Attributes

Use standard SVG text attributes through keyword arguments or `attrs()`.

```python
title = dp.Text(
    "pyDreamplet",
    x=120,
    y=48,
    fill="currentColor",
    font_family="Inter, sans-serif",
    font_size=32,
    font_weight=700,
    text_anchor="middle",
    alignment_baseline="middle",
)
```

These names are converted to SVG attributes such as `font-family`,
`font-size`, `text-anchor`, and `alignment-baseline`.
