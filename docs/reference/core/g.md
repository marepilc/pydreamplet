# `G`

The G class represents a group (`<g>`) element in SVG. It inherits from both SvgElement and Transformable to allow grouped elements to be transformed together.

## <span class=class></span>`pydreamplet.core.G`

```py
G(
    pos: Vector = None,
    scale: Vector = None,
    angle: float = 0,
    pivot: Vector = None,
    order: str = "trs",
    **kwargs
)
```

Initializes a group element with optional transformation properties and a pivot point.

<span class="param">**Parameters**</span>

- `pos` *(Vector, optional)*: Position vector (default: (0, 0)).
- `scale` *(Vector, optional)*: Scale vector (default: (1, 1)).
- `angle` *(float)*: Rotation angle (default: 0).
- `pivot` *(Vector, optional)*: Pivot point for rotation (default: (0, 0)).
- `order` *(str)*: Transformation order (combination of 't', 'r', 's'; default: "trs").

```py
group = G(pos=Vector(10, 20), angle=30)
```

### <span class="prop"></span>`pivot`

**Getter:** Returns the pivot point as a Vector.

**Setter:** Updates the pivot point and refreshes the transform.

```py
print(group.pivot)
group.pivot = Vector(5, 5)
```

### <span class="prop"></span>`order`

*Getter:* Returns the current transformation order.

*Setter:* Updates the order and refreshes the transform.

```py
print(group.order)
group.order = "rts"
```

### <span class="meth"></span>`remove`

```py
remove(self, child) -> G
```

Removes a child element. If the group becomes empty, it removes itself from its parent.

### <span class="meth"></span>`attrs`

```py
attrs(self, attributes: dict) -> G
```

Sets multiple attributes on the group, including parsing transformation details.

### <span class="meth"></span>`from_element`

```py
G.from_element(element: ET.Element)
```

Creates a G instance from an ElementTree element by parsing its transformation attributes.