# Working with text

Below is a step-by-step tutorial on how to measure and visualize text dimensions using pyDreamplet. We’ll cover:

- Overview of text measurement
- Creating an SVG canvas and adding text
- Measuring text using [`TypographyMeasurer`](../reference/typography/index.md#typographymeasurer)
- Visualizing bounding boxes
- Tips & tricks for more accurate results

## Overview of Text Measurement

When working with text in **pyDreamplet**, you often need to know the approximate dimensions of the text to handle layout correctly. For instance, if you want to center text within a rectangle or place shapes around your text, you must know how wide and tall the text will be.

pyDreamplet uses **Pillow** (the Python Imaging Library) to compute this estimate. Pillow’s text measurement is not as precise as layout engines like a web browser (e.g., using `<canvas>` or `SVG` in an actual HTML environment), but it is lightweight and good enough for most design tasks.

Key points about measurement:

- Measurements are approximate.
- Complex or uncommon fonts may yield slightly inconsistent results.
- You have control over font family, font size, and font weight.

## Creating an SVG Canvas and Adding Text

Below is a minimal example of how to create an SVG canvas and place a text label in the center. We will go step by step.

```py
import pydreamplet as dp
from pydreamplet.typography import TypographyMeasurer

# 1. Create an SVG with specified width and height
svg = dp.SVG(400, 200)

# 2. Create a group (dp.G) positioned at the center of the canvas.
#    We'll use this group to append our shapes and text so that
#    everything is centered relative to this position.
g = dp.G(dp.Vector(svg.w / 2, svg.h / 2))
svg.append(g)

# 3. (Optional) Add a small circle to visualize the center point.
center = dp.Circle(pos=dp.Vector(0, 0), r=5, fill="red")
g.append(center)

# 4. Create your text element.
txt = dp.Text("pyDreamplet")
txt.font_family = "Verdana"
txt.font_size = "48"
txt.font_weight = 700
txt.text_anchor = "middle"
txt.dominant_baseline = "middle"

# Append the text element to the group
g.append(txt)
```

![Current state](assets/text_measure_01.png){.img-light-dark-bg}

## Understanding Text Properties

- `font_family`: The font used to render the text (e.g., `"Verdana"`, `"Arial"`).
- `font_size`: The size of the text in points.
- `font_weight`: Use a numeric value like `400` (normal) or `700` (bold).
- `text_anchor`: Determines horizontal alignment. Common values are:
    - `start` (left-aligned),
    - `middle` (center-aligned),
    - `end` (right-aligned).
- `dominant_baseline`: Determines vertical alignment. Common values are:
    - `alphabetic` (default baseline),
    - `middle` (centers the text vertically relative to its bounding box),
    - `hanging`,
    - `baseline` (similar to alphabetic).

At this point, we already have our text placed at the center of the SVG. However, we might want to see how large it is in order to align other shapes around it.

## Measuring Text Using TypographyMeasurer

To measure the width and height of any text string, pyDreamplet provides the TypographyMeasurer class. Under the hood, it uses Pillow for measurement:

```py
measurer = TypographyMeasurer()

width, height = measurer.measure_text(
    txt.content,
    font_family=txt.font_family,
    font_size=txt.font_size,
    weight=txt.font_weight
)

print(f"Measured text width: {width}, height: {height}") #  prints Width: 347.0, Height: 47.0
```

- `txt.content` is the string you want to measure.
- `font_family=txt.font_family`, `font_size=txt.font_size`, and `weight=txt.font_weight` match the same styling you set on your `Text` object.

The returned `width` and `height` are floating-point values representing the approximate bounding box in pixels.

## Visualizing Bounding Boxes
Often, it helps to draw a rectangle around the text to see exactly how it’s placed. We can use the measured `width` and `height` for that.

```py
# Create a rectangle based on the measured text dimensions
rect = dp.Rect(
    pos=dp.Vector(-width / 2, -height / 2),
    width=width,
    height=height,
    fill="none",
    stroke="blue",
    stroke_width=1,
)

# Append the rectangle to the same group
g.append(rect)
```

Because we used `text_anchor="middle"` and `dominant_baseline="middle"`, the text’s center aligns with the origin of the `G` group (which we placed at the center of the SVG). Hence, to align our rectangle with the text:

- We offset its position by `-width/2` and `-height/2`.
- This ensures the rectangle’s center is also at `(0,0)`.

Your final output might look like this:

![Current state](assets/text_measure_02.png){.img-light-dark-bg}

## Tips & Tricks for More Accurate Results

**Use the same font settings**
Make sure you pass the exact same font properties (font_family, font_size, font_weight, etc.) to both your Text element and to the TypographyMeasurer. If there is a mismatch, your measured dimensions will not match the on-screen text.

**Mind the environment**
Some systems may have different font renderers or default fonts when the specified font is unavailable. Verify that Pillow can find the font you’re requesting. If it can’t, it might fall back to a default (often DejaVuSans).

**Adjust for vertical offsets**
Depending on the chosen dominant_baseline, the text might render slightly differently than the bounding box you expect. If precise alignment is crucial, experiment with different baseline settings or manually offset using dy or the pos property.

**Measuring multiple lines**
If you have multiline text, consider measuring each line separately or measure the joined lines with newline characters ("\n"). Keep in mind that line spacing might not be accurately reflected by Pillow. You may need to add additional spacing based on your design needs.

**Performance considerations**
Measuring text repeatedly can be somewhat expensive. If you are repeatedly measuring the same text (e.g., in a loop), cache the result.