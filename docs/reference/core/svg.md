# `SVG`

The `SVG` class represents the root SVG element. It manages the viewbox, provides properties for dimensions, and includes methods for displaying and saving the SVG.

!!! info

    This class inherits from [**`SvgElement`**](svgelement.md).

## <span class=class></span>`pydreamplet.core.SVG`

<!--skip-->
```py
SVG(*viewbox, **kwargs)
```

Initializes a new SVG element with the specified viewbox. The viewbox can be provided as a tuple of 2 (width, height) or 4 (min-x, min-y, width, height) numbers.

<span class="param">**Parameters**</span>

- `viewbox` *(tuple or list)*: Dimensions for the SVG.
- `**kwargs`: Additional attributes for the SVG element.

```py
svg = SVG(800, 600)
print(svg)  # <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" width="800px" height="600px" />
```

You can change the default values of width and height passing `**kwargs`.

```py
svg = SVG(800, 600, width="400px", height="300px")
print(svg)  # <svg xmlns="http://www.w3.org/2000/svg" width="400px" height="300px" viewBox="0 0 800 600" />
```

It does not need to be done during initialization. You can set any attribute of [SvgElement](svgelement.md) using `**kwargs`.

<!--skip-->
```py
svg = dp.SVG(300, 300)
svg.width = "600px"
svg.height = "600px"
```

### <span class="meth"></span>`from_element`

<!--skip-->
```py
SVG.from_element(element: ET.Element)
```

Creates an SVG instance from an ElementTree element.

### <span class="meth"></span>`from_file`

<!--skip-->
```py
SVG.from_file(filename: str)
```

```py title="Usage example"
from importlib.resources import files
from pydreamplet import SVG, resources

svg = SVG.from_file(files(resources) / "hummingbird.svg").attrs(
    {"width": 96, "height": 84}
)
svg.find("path").fill = "darkgreen"
```

![Result](assets/svg_from_file_example.svg){.img-light-dark-bg}

Creates an SVG instance by parsing an SVG file.

### <span class="prop"></span>`w` and `h`

**Getter:** Returns the width (w) and height (h) of the SVG based on its **`viewBox`**.

!!! warning

    Remember, based on `viewBox`. Do not confuse these properties with `width` and `height` attributes of the SVG element.

<!--skip-->
```py
import pydreamplet as dp

svg = dp.SVG(300, 300)
svg.width = "600px"
svg.height = "600px"
print(f"svg viewBox is {svg.viewBox}")  # Outputs svg viewBox is 0 0 300 300
print(f"svg.w is {svg.w}, svg.h is {svg.h}")  # Outputs svg.w is 300, svg.h is 300
print(f"svg.width is {svg.width}, svg.height is {svg.height}")  # Outputs svg.width is 600px, svg.height is 600px
```

### <span class="meth"></span>`style`

<!--skip-->
```py
def style(
    self, file_path: str, overwrite: bool = True, minify: bool = True
) -> None
```

Adds a `<style>` element to the SVG using CSS content loaded from an external file. When `overwrite` is set to `True`, any existing `<style>` elements are removed and the new one is inserted as the first child. When `minify` is `True`, the CSS content is minified before insertion.

=== "Usage example"

    <!--skip-->
    ```py
    from pydreamplet import SVG, Circle

    svg = SVG(200, 200)
    svg.append(Circle(cx=100, cy=100, r=50))

    svg.style("my_style.css")
    ```

=== "my_style.css"

    ```css
    circle {
      fill: rgb(160, 3, 68);
      stroke: #000;
      stroke-width: 20px;
    }
    ```

![Result](assets/svg_style_example.svg){.img-light-dark-bg}

### <span class="meth"></span>`display`

<!--skip-->
```py
display(self) -> None
```

Displays the SVG in an IPython environment.

### <span class="meth"></span>`save`

<!--skip-->
```py
save(self, filename: str) -> None
```

Saves the SVG to a file.
