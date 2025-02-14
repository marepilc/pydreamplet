# `Text`

The `Text` class represents an SVG text element. It supports setting the position and content, and for multiline text, it automatically splits the content into <tspan> elements.

!!! info

    This class inherites from [**`SvgElement`**](svgelement.md).

## <span class=class></span>`pydreamplet.core.Text`

```py
Text(initial_text: str = "", **kwargs)
```

Initializes a new text element with optional initial content. If pos is provided, it sets the text position.

<span class="param">**Parameters**</span>

- `initial_text` *(str, optional)*: The initial text content.
- `**kwargs`: Additional attributes for the text element, including pos (a Vector).

```py
text_elem = Text("Hello, World!", pos=Vector(50, 50), fill="black")
```

### <span class="prop"></span>`pos`
**Getter:** Returns the text position as a Vector.

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
