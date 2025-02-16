import math


class Vector:
    def __init__(self, x: float, y: float):
        """Creates a new 2D vector."""
        self._x = x
        self._y = y

    def set(self, x: float, y: float) -> None:
        """Changes the x and y coordinates."""
        self._x = x
        self._y = y

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        self._x = value

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        self._y = value

    @property
    def xy(self) -> tuple[float, float]:
        """Returns the (x, y) coordinates as a tuple."""
        return (self._x, self._y)

    def copy(self) -> "Vector":
        """Returns a duplicate of the vector."""
        return Vector(self._x, self._y)

    def __eq__(self, other):
        if isinstance(other, Vector):
            return self._x == other._x and self._y == other._y
        return NotImplemented

    # Operator overloading for addition
    def __add__(self, other: "Vector") -> "Vector":
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self._x + other.x, self._y + other.y)

    def __iadd__(self, other: "Vector") -> "Vector":
        if not isinstance(other, Vector):
            return NotImplemented
        self._x += other.x
        self._y += other.y
        return self

    # Operator overloading for subtraction
    def __sub__(self, other: "Vector") -> "Vector":
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self._x - other.x, self._y - other.y)

    def __isub__(self, other: "Vector") -> "Vector":
        if not isinstance(other, Vector):
            return NotImplemented
        self._x -= other.x
        self._y -= other.y
        return self

    # Operator overloading for scalar multiplication
    def __mul__(self, scalar: float) -> "Vector":
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return Vector(self._x * scalar, self._y * scalar)

    def __rmul__(self, scalar: float) -> "Vector":
        return self.__mul__(scalar)

    def __imul__(self, scalar: float) -> "Vector":
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        self._x *= scalar
        self._y *= scalar
        return self

    # Operator overloading for scalar division
    def __truediv__(self, scalar: float) -> "Vector":
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return Vector(self._x / scalar, self._y / scalar)

    def __itruediv__(self, scalar: float) -> "Vector":
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        self._x /= scalar
        self._y /= scalar
        return self

    def dot(self, other: "Vector") -> float:
        """Returns the dot product of two vectors."""
        return self._x * other.x + self._y * other.y

    def normalize(self) -> "Vector":
        """
        Returns a normalized copy of the vector (does not modify the original).
        Raises a ValueError if the vector is zero.
        """
        mag = self.magnitude
        if mag == 0:
            raise ValueError("Cannot normalize a zero vector")
        return Vector(self._x / mag, self._y / mag)

    @property
    def direction(self) -> float:
        """
        Returns the direction (angle in degrees) of the vector.
        """
        return math.degrees(math.atan2(self._y, self._x))

    @direction.setter
    def direction(self, angle_deg: float) -> None:
        """
        Sets the direction (angle in degrees) of the vector while preserving its magnitude.
        """
        mag = self.magnitude
        angle_rad = math.radians(angle_deg)
        self._x = math.cos(angle_rad) * mag
        self._y = math.sin(angle_rad) * mag

    @property
    def magnitude(self) -> float:
        """Returns the magnitude (length) of the vector."""
        return math.sqrt(self._x**2 + self._y**2)

    @magnitude.setter
    def magnitude(self, new_magnitude: float) -> None:
        """
        Sets the magnitude of the vector while preserving its direction.
        """
        # Get the current direction in degrees, then convert to radians.
        angle_deg = self.direction
        angle_rad = math.radians(angle_deg)
        self._x = math.cos(angle_rad) * new_magnitude
        self._y = math.sin(angle_rad) * new_magnitude

    def limit(self, limit_scalar: float) -> None:
        """
        Limits the vector's magnitude to the specified value.
        If the current magnitude exceeds the limit, the vector is scaled down.
        """
        if self.magnitude > limit_scalar:
            self.magnitude = limit_scalar

    def __repr__(self) -> str:
        return f"Vector(x={self._x}, y={self._y})"
