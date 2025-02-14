# `Animate`

The `Animate` class represents an SVG animation element. It allows you to animate an attribute by specifying repeat count and a sequence of values.

!!! info

    This class inherites from [**`SvgElement`**](svgelement.md).

## <span class=class></span>`pydreamplet.core.Animate`

```py
Animate(attr: str, **kwargs)
```

Initializes a new animation for the specified attribute.

<span class="param">**Parameters**</span>

- `attr` *(str)*: The SVG attribute to animate.
- `**kwargs`: Additional attributes for the animate element.

```py
anim = Animate("fill", from_="red", to="blue")
```

### <span class="prop"></span>`repeat_count`

**Getter:** Returns the repeat count of the animation.

**Setter:** Updates the repeat count and the corresponding attribute.

```py
print(anim.repeat_count)
anim.repeat_count = "indefinite"
```

### <span class="prop"></span>`values`

**Getter:** Returns the list of animation values.

**Setter:** Sets the list of values and updates the values attribute.

```py
anim.values = ["red", "green", "blue"]
```