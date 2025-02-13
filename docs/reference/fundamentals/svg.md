# `SVG` class

The SVG class extends SvgElement to represent an SVG document's root. It simplifies creating, finding, and saving SVG documents by managing the viewbox and providing methods for common tasks.

Methods and Attributes
from_file(filename)
Class Method. Loads an SVG from a file and returns an SVG instance.

*init(viewbox, **kwargs)
Initializes the SVG root element with a specified viewbox and optional attributes. The viewbox can be provided as a tuple or separate numbers.

find(tag, nested=False)
Finds the first sub-element with the given tag. If nested is True, the search is performed recursively.

find_all(tag, nested=False)
Returns a list of all sub-elements with the given tag. If nested is True, the search is performed recursively.

width (property)
Calculates and returns the width of the SVG based on its viewBox attribute.

height (property)
Calculates and returns the height of the SVG based on its viewBox attribute.

display()
Renders the SVG in an IPython environment, such as Jupyter Notebook.

save(filename)
Saves the SVG document to a file.