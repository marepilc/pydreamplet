import math

type Real = int | float


class Vector:
    def __init__(self, x: Real, y: Real):
        """Creates a new 2D vector."""
        self._x: float = float(x)
        self._y: float = float(y)

    def set(self, x: Real, y: Real) -> None:
        """Changes the x and y coordinates."""
        self._x = float(x)
        self._y = float(y)

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: Real) -> None:
        self._x = float(value)

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: Real) -> None:
        self._y = float(value)

    @property
    def xy(self) -> tuple[float, float]:
        """Returns the (x, y) coordinates as a tuple."""
        return (self._x, self._y)

    def copy(self) -> "Vector":
        """Returns a duplicate of the vector."""
        return Vector(self._x, self._y)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Vector):
            return self._x == other._x and self._y == other._y
        return NotImplemented

    # Operator overloading for addition
    def __add__(self, other: object) -> "Vector":
        if not isinstance(other, Vector):
            raise TypeError(f"unsupported operand type(s) for +: 'Vector' and '{type(other).__name__}'")
        return Vector(self._x + other.x, self._y + other.y)

    def __iadd__(self, other: object) -> "Vector":
        if not isinstance(other, Vector):
            raise TypeError(f"unsupported operand type(s) for +=: 'Vector' and '{type(other).__name__}'")
        self._x += other.x
        self._y += other.y
        return self

    # Operator overloading for subtraction
    def __sub__(self, other: object) -> "Vector":
        if not isinstance(other, Vector):
            raise TypeError(f"unsupported operand type(s) for -: 'Vector' and '{type(other).__name__}'")
        return Vector(self._x - other.x, self._y - other.y)

    def __isub__(self, other: object) -> "Vector":
        if not isinstance(other, Vector):
            raise TypeError(f"unsupported operand type(s) for -=: 'Vector' and '{type(other).__name__}'")
        self._x -= other.x
        self._y -= other.y
        return self

    # Operator overloading for scalar multiplication
    def __mul__(self, scalar: Real) -> "Vector":
        return Vector(self._x * scalar, self._y * scalar)

    def __rmul__(self, scalar: Real) -> "Vector":
        return self.__mul__(scalar)

    def __imul__(self, scalar: Real) -> "Vector":
        self._x *= scalar
        self._y *= scalar
        return self

    # Operator overloading for scalar division
    def __truediv__(self, scalar: Real) -> "Vector":
        return Vector(self._x / scalar, self._y / scalar)

    def __itruediv__(self, scalar: Real) -> "Vector":
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
    def direction(self, angle_deg: Real) -> None:
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
    def magnitude(self, new_magnitude: Real) -> None:
        """
        Sets the magnitude of the vector while preserving its direction.
        """
        # Get the current direction in degrees, then convert to radians.
        angle_deg = self.direction
        angle_rad = math.radians(angle_deg)
        self._x = math.cos(angle_rad) * new_magnitude
        self._y = math.sin(angle_rad) * new_magnitude

    def limit(self, limit_scalar: Real) -> None:
        """
        Limits the vector's magnitude to the specified value.
        If the current magnitude exceeds the limit, the vector is scaled down.
        """
        if self.magnitude > limit_scalar:
            self.magnitude = limit_scalar

    def __repr__(self) -> str:
        return f"Vector(x={self._x}, y={self._y})"
