# `Text`

The `Text` class represents an SVG text element. It supports setting the position and content, and for multiline text, it automatically splits the content into <tspan> elements.

!!! info

    This class inherits from [**`SvgElement`**](svgelement.md).

## <span class=class></span>`pydreamplet.core.Text`

```py
Text(initial_text: str = "", **kwargs)
```

Initializes a new text element with optional initial content. If pos is provided, it sets the text position.

<span class="param">**Parameters**</span>

- `initial_text` _(str, optional)_: The initial text content.
- `**kwargs`: Additional attributes for the text element. Common keyword arguments include:
    - `pos` *(Vector)*: Specifies the text position.
    - `v_space` *(number, optional)*: Controls the vertical space between lines for multiline text.
    - `font_size` *(str, optional)*: Specifies the font size. The provided value should include a unit (e.g. `"10.5pt"`, `"18px"`, etc.). If no unit is provided, `"px"` is appended by default. The getter returns only the numeric portion as a float.

```py
from pydreamplet import SVG, Text, Vector

svg = SVG(300, 200).append(
    Text(
        "Hello,\nWorld!",
        pos=Vector(60, 80),
        v_space=84,
        font_size=64,
        fill="#1b313b"
    )
)
```

![Result](assets/multiline_text_example.svg){.img-light-dark-bg}

### <span class="prop"></span>`pos`

**Getter:** Returns the text position as a [`Vector`](../math/vector.md).

**Setter:** Updates the text position.

```py
print(text_elem.pos)
text_elem.pos = Vector(60, 60)
```

### <span class="prop"></span>`content`

**Getter:** Returns the raw text content.

**Setter:** Updates the text content. For multiline text, the content is split into <tspan> elements.

```py
print(text_elem.content)
text_elem.content = "Line 1\nLine 2"
```
