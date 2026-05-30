# SVG definitions

pyDreamplet provides thin wrappers for common SVG definition elements. They behave like regular `SvgElement` instances, but `find()` and `find_all()` return typed wrappers for registered tags.

## <span class="class"></span>`Defs`

<!--skip-->
```py
Defs(**kwargs)
```

Represents a `<defs>` container. Use `SVG.ensure_defs()` to create or reuse one on the root SVG.

```py
import pydreamplet as dp

svg = dp.SVG(200, 100)
defs = svg.ensure_defs()
defs.append(dp.LinearGradient("fade"))
```

### <span class="meth"></span>`SVG.ensure_defs`

<!--skip-->
```py
ensure_defs(self) -> Defs
```

Returns the first existing `<defs>` element or creates one as the first child of the SVG. The returned object is a live wrapper, so appending to it updates the SVG tree.

## <span class="class"></span>`LinearGradient` and `RadialGradient`

<!--skip-->
```py
LinearGradient(id: str | None = None, *, x1=None, y1=None, x2=None, y2=None, **kwargs)
RadialGradient(id: str | None = None, *, cx=None, cy=None, r=None, fx=None, fy=None, **kwargs)
```

Gradient wrappers expose `id_ref`, which returns a `url(#id)` reference for use in `fill`, `stroke`, `mask`, and similar SVG attributes.

```py
import pydreamplet as dp

svg = dp.SVG(200, 100)
gradient = (
    dp.LinearGradient("fade", x1="0%", y1="0%", x2="100%", y2="0%")
    .add_stop("0%", "#1f77b4")
    .add_stop("100%", "#ff7f0e")
)

svg.ensure_defs().append(gradient)
svg.append(dp.Rect(x=20, y=20, width=160, height=60, fill=gradient.id_ref))
```

### <span class="meth"></span>`add_stop`

<!--skip-->
```py
add_stop(offset, color: str, opacity=None, **kwargs) -> Self
```

Appends a `Stop` to the gradient and returns the gradient for chaining.

## <span class="class"></span>`Stop`

<!--skip-->
```py
Stop(offset, color: str | None = None, opacity=None, **kwargs)
```

Represents a `<stop>` element. `color` maps to `stop-color`; `opacity` maps to `stop-opacity`.

## Other resource wrappers

The following wrappers are available for definition resources that contain other SVG elements:

- `Pattern(id: str | None = None, **kwargs)`
- `Mask(id: str | None = None, **kwargs)`
- `ClipPath(id: str | None = None, **kwargs)`
- `Filter(id: str | None = None, **kwargs)`

Each exposes `id_ref`.
