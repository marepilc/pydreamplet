import math
from typing import Any

from pydreamplet.colors import hex_to_rgb, rgb_to_hex


class LinearScale:
    """
    A linear scale that maps a numeric value from a given domain
    to an output range.
    """

    def __init__(self, domain: tuple[float, float], output_range: tuple[float, float]):
        self._domain = domain
        self._output_range = output_range
        self._calculate_slope()

    def _calculate_slope(self):
        """Calculates the slope for the linear scale."""
        self.slope = (self._output_range[1] - self._output_range[0]) / (
            self._domain[1] - self._domain[0]
        )

    def map(self, value: float) -> float:
        """Scales a value from the domain to the output range."""
        return self._output_range[0] + self.slope * (value - self._domain[0])

    def invert(self, value: float) -> float:
        """Maps a value from the output range back to the domain."""
        return self._domain[0] + (value - self._output_range[0]) / self.slope

    @property
    def domain(self) -> tuple[float, float]:
        return self._domain

    @domain.setter
    def domain(self, new_domain: tuple[float, float]):
        self._domain = new_domain
        self._calculate_slope()

    @property
    def output_range(self) -> tuple[float, float]:
        return self._output_range

    @output_range.setter
    def output_range(self, new_output_range: tuple[float, float]):
        self._output_range = new_output_range
        self._calculate_slope()


class BandScale:
    """
    Maps categorical values (strings) to evenly spaced positions in the output range.
    The mapping includes a configurable inner padding and outer padding.
    """

    def __init__(
        self,
        domain: list[Any],
        output_range: tuple[float, float],
        padding: float = 0.1,
        outer_padding: float | None = None,
    ):
        self._domain = domain
        self._output_range = output_range
        self._padding = padding
        self._outer_padding = outer_padding if outer_padding is not None else padding
        self._calculate_band_properties()

    def _calculate_band_properties(self):
        """Calculates the band width and step size for the band scale."""
        num_bands = len(self._domain)
        total_padding = (num_bands - 1) * self._padding + 2 * self._outer_padding
        total_width = self._output_range[1] - self._output_range[0]

        # Compute the band width considering the total padding.
        self._band_width = total_width / (num_bands + total_padding)
        # Step size includes the band width and the padding between bands.
        self.step = self._band_width * (1 + self._padding)

    def map(self, value: Any) -> float:
        """
        Maps a value from the domain to the start position of its band in the output range.
        Raises a ValueError if the value is not found in the domain.
        """
        index = self._domain.index(value)
        return (
            self._output_range[0]
            + self._band_width * self._outer_padding
            + self.step * index
        )

    @property
    def bandwidth(self) -> float:
        """Returns the computed width of each band."""
        return self._band_width

    @property
    def domain(self) -> list[Any]:
        return self._domain

    @domain.setter
    def domain(self, new_domain: list[Any]):
        self._domain = new_domain
        self._calculate_band_properties()

    @property
    def output_range(self) -> tuple[float, float]:
        return self._output_range

    @output_range.setter
    def output_range(self, new_output_range: tuple[float, float]):
        self._output_range = new_output_range
        self._calculate_band_properties()

    @property
    def padding(self) -> float:
        return self._padding

    @padding.setter
    def padding(self, new_padding: float):
        self._padding = new_padding
        self._calculate_band_properties()

    @property
    def outer_padding(self) -> float:
        return self._outer_padding

    @outer_padding.setter
    def outer_padding(self, new_outer_padding: float):
        self._outer_padding = new_outer_padding
        self._calculate_band_properties()


class PointScale:
    """
    Maps categorical values to discrete points within the output range,
    placing a specified amount of padding at both ends.
    """

    def __init__(
        self, domain: list[Any], output_range: tuple[float, float], padding: float = 0.5
    ):
        self._domain = domain
        self._output_range = output_range
        self._padding = padding
        self._calculate_step()

    def _calculate_step(self):
        """Calculates the step size based on the domain length and padding."""
        if not self._domain:
            raise ValueError("Domain must contain at least one value")
        r0, r1 = self._output_range
        n = len(self._domain)
        self._step = (r1 - r0) / (n - 1 + 2 * self._padding)

    def map(self, value: Any) -> float | None:
        """
        Maps a categorical value to a point in the output range.
        Returns None if the value is not in the domain.
        """
        try:
            index = self._domain.index(value)
        except ValueError:
            return None
        return self._output_range[0] + self._step * (index + self._padding)

    @property
    def domain(self) -> list[Any]:
        return self._domain

    @domain.setter
    def domain(self, new_domain: list[Any]):
        self._domain = new_domain
        self._calculate_step()

    @property
    def output_range(self) -> tuple[float, float]:
        return self._output_range

    @output_range.setter
    def output_range(self, new_output_range: tuple[float, float]):
        self._output_range = new_output_range
        self._calculate_step()

    @property
    def padding(self) -> float:
        return self._padding

    @padding.setter
    def padding(self, new_padding: float):
        self._padding = new_padding
        self._calculate_step()


class OrdinalScale:
    """
    Maps categorical values to a set of output values in a cyclic fashion.
    For example, if the output range is a list of colors, the scale will
    assign each domain value one of those colors in order (wrapping around if needed).
    """

    def __init__(self, domain: list[Any], output_range: list):
        if not output_range:
            raise ValueError("Output range must contain at least one value")
        self._domain = domain
        self._output_range = output_range
        self._generate_mapping()

    def _generate_mapping(self):
        self._mapping = {
            d: self._output_range[i % len(self._output_range)]
            for i, d in enumerate(self._domain)
        }

    def map(self, value: Any) -> object:
        """Returns the mapped output value for the given domain value."""
        return self._mapping.get(value)

    @property
    def domain(self) -> list[Any]:
        return self._domain

    @domain.setter
    def domain(self, new_domain: list[Any]):
        self._domain = new_domain
        self._generate_mapping()

    @property
    def output_range(self) -> list:
        return self._output_range

    @output_range.setter
    def output_range(self, new_output_range: list):
        if not new_output_range:
            raise ValueError("Output range must contain at least one value")
        self._output_range = new_output_range
        self._generate_mapping()


class ColorScale:
    """
    Creates a color scale that maps a numeric value (from a given domain)
    to an interpolated hex color between two provided hex color strings.
    """

    def __init__(self, domain: tuple[float, float], output_range: tuple[str, str]):
        self._domain = domain
        self._output_range = output_range
        d0, d1 = domain
        if d1 == d0:
            raise ValueError("Domain minimum and maximum must be distinct")
        self._start_color = output_range[0]
        self._end_color = output_range[1]
        self._rgb_start = hex_to_rgb(self._start_color)
        self._rgb_end = hex_to_rgb(self._end_color)

    def map(self, value: float) -> str:
        """Maps the input value to an interpolated hex color."""
        d0, d1 = self._domain
        t = (value - d0) / (d1 - d0)
        # Clamp t to [0, 1]
        t = max(0, min(1, t))
        r = int(self._rgb_start[0] + t * (self._rgb_end[0] - self._rgb_start[0]))
        g = int(self._rgb_start[1] + t * (self._rgb_end[1] - self._rgb_start[1]))
        b = int(self._rgb_start[2] + t * (self._rgb_end[2] - self._rgb_start[2]))
        return rgb_to_hex((r, g, b))

    @property
    def domain(self) -> tuple[float, float]:
        return self._domain

    @domain.setter
    def domain(self, new_domain: tuple[float, float]):
        self._domain = new_domain

    @property
    def output_range(self) -> tuple[str, str]:
        return self._output_range

    @output_range.setter
    def output_range(self, new_output_range: tuple[str, str]):
        if len(new_output_range) != 2:
            raise ValueError("Output range must contain exactly two colors")
        self._output_range = new_output_range
        self._start_color = new_output_range[0]
        self._end_color = new_output_range[1]
        self._rgb_start = hex_to_rgb(self._start_color)
        self._rgb_end = hex_to_rgb(self._end_color)


class SquareScale:
    """
    Maps an input value (such as an area) to an output using a square-root transformation.
    This is useful when a visual property (like a square’s side length) should be proportional
    to the square root of the area.
    """

    def __init__(self, domain: tuple[float, float], output_range: tuple[float, float]):
        self._domain = domain
        self._output_range = output_range
        d0, d1 = domain
        if d0 < 0 or d1 < 0:
            raise ValueError("Domain values must be non-negative for square scale")
        self._sqrt_d0 = math.sqrt(d0)
        self._sqrt_d1 = math.sqrt(d1)
        if self._sqrt_d1 == self._sqrt_d0:
            raise ValueError("Invalid domain: sqrt(d1) and sqrt(d0) cannot be equal")

    def map(self, value: float) -> float:
        """Scales the value using a square-root transformation."""
        r0, r1 = self._output_range
        return r0 + (
            (math.sqrt(value) - self._sqrt_d0) / (self._sqrt_d1 - self._sqrt_d0)
        ) * (r1 - r0)

    @property
    def domain(self) -> tuple[float, float]:
        return self._domain

    @domain.setter
    def domain(self, new_domain: tuple[float, float]):
        self._domain = new_domain
        d0, d1 = new_domain
        if d0 < 0 or d1 < 0:
            raise ValueError("Domain values must be non-negative for square scale")
        self._sqrt_d0 = math.sqrt(d0)
        self._sqrt_d1 = math.sqrt(d1)
        if self._sqrt_d1 == self._sqrt_d0:
            raise ValueError("Invalid domain: sqrt(d1) and sqrt(d0) cannot be equal")

    @property
    def output_range(self) -> tuple[float, float]:
        return self._output_range

    @output_range.setter
    def output_range(self, new_output_range: tuple[float, float]):
        self._output_range = new_output_range


class CircleScale:
    """
    Maps an input value to the radius of a circle such that the circle's area
    is linearly proportional to the input value. Given a domain (vmin, vmax)
    and a desired radius range (rmin, rmax), the radius is computed as:

        radius(v) = sqrt( ((v - vmin)/(vmax - vmin))*(rmax^2 - rmin^2) + rmin^2 )
    """

    def __init__(self, domain: tuple[float, float], output_range: tuple[float, float]):
        self._domain = domain
        self._output_range = output_range
        d0, d1 = domain
        if d1 == d0:
            raise ValueError("Domain values must be distinct")

    def map(self, value: float) -> float:
        """Maps the input value to a circle radius such that the circle's area is proportional to the value."""
        d0, d1 = self._domain
        r0, r1 = self._output_range
        r_squared = ((value - d0) / (d1 - d0)) * (r1**2 - r0**2) + r0**2
        return math.sqrt(r_squared)

    @property
    def domain(self) -> tuple[float, float]:
        return self._domain

    @domain.setter
    def domain(self, new_domain: tuple[float, float]):
        self._domain = new_domain
        d0, d1 = new_domain
        if d1 == d0:
            raise ValueError("Domain values must be distinct")

    @property
    def output_range(self) -> tuple[float, float]:
        return self._output_range

    @output_range.setter
    def output_range(self, new_output_range: tuple[float, float]):
        self._output_range = new_output_range
