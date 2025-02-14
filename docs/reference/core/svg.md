# `SVG`

The `SVG` class represents the root SVG element. It manages the viewbox, provides properties for dimensions, and includes methods for displaying and saving the SVG.

!!! info

    This class inherites from [**`SvgElement`**](svgelement.md).

## <span class=class></span>`pydreamplet.core.SVG`

```py
SVG(*viewbox, **kwargs)
```

Initializes a new SVG element with the specified viewbox. The viewbox can be provided as a tuple of 2 (width, height) or 4 (min-x, min-y, width, height) numbers.

<span class="param">**Parameters**</span>

- `viewbox` *(tuple or list)*: Dimensions for the SVG.
- `**kwargs`: Additional attributes for the SVG element.

```py
svg = SVG(800, 600)
print(svg)  # Outputs the SVG XML.
```

### <span class="meth"></span>`from_element`

```py
SVG.from_element(element: ET.Element)
```

Creates an SVG instance from an ElementTree element.

### <span class="meth"></span>`from_file`

```py
SVG.from_file(filename: str)
```

Creates an SVG instance by parsing an SVG file.

### <span class="prop"></span>`w` and `h`

**Getter:** Returns the width (w) and height (h) of the SVG based on its **`viewBox`**.

!!! warning

    Remember, based on `viewBox`. Do not confuse these properties with `width` and `height` attributes of the SVG element.


```py
import pydreamplet as dp

svg = dp.SVG(300, 300)
svg.width = "600px"
svg.height = "600px"
print(f"svg viewBox is {svg.viewBox}")  # Outputs svg viewBox is 0 0 300 300
print(f"svg.w is {svg.w}, svg.h is {svg.h}")  # Outputs svg.w is 300, svg.h is 300
print(f"svg.width is {svg.width}, svg.height is {svg.height}")  # Outputs svg.width is 600px, svg.height is 600px
```

### <span class="meth"></span>`display`

```py
display(self) -> None
```

Displays the SVG in an IPython environment.

### <span class="meth"></span>`save`

```py
save(self, filename: str) -> None
```

Saves the SVG to a file.