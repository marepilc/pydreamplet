# `Transformable`

The Transformable mixin adds transformation capabilities—translation, rotation, and scaling—to SVG elements. It is intended for use with group elements.

## <span class=class></span>`pydreamplet.core.Transformable`

```py
Transformable(
    pos: Vector = None,
    scale: Vector = None,
    angle: float = 0,
    *args,
    **kwargs
)
```

Initializes transformation properties with position, scale, and rotation angle.

<span class="param">**Parameters**</span>

- `pos` *(Vector, optional)*: Position vector (default: (0, 0)).
- `scale` *(Vector, optional)*: Scale vector (default: (1, 1)).
- `angle` *(float)*: Rotation angle (default: 0).

```py
t = Transformable(pos=Vector(10, 20), scale=Vector(2, 2), angle=45)
```

### <span class="prop"></span>`pos`
**Getter:** Returns the current position as a Vector.

**Setter:** Updates the position and refreshes the transform.

```py
print(t.pos)
t.pos = Vector(30, 40)
```

### <span class="prop"></span>`scale`

**Getter:** Returns the current scale as a Vector.

**Setter:** Updates the scale and refreshes the transform.

```py
print(t.scale)
t.scale = Vector(1, 1)
```

### <span class="prop"></span>`angle`

**Getter:** Returns the current rotation angle.

**Setter:** Updates the angle and refreshes the transform.

```py
print(t.angle)
t.angle = 90
```