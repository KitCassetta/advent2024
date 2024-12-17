from dataclasses import asdict, dataclass
from enum import Enum
from typing import NamedTuple, TYPE_CHECKING

#################################################################
# POINTS, VECTORS AND GRIDS
#################################################################


if TYPE_CHECKING:
    class Point:
        # noinspection PyUnusedLocal
        def __init__(self, x: int, y: int): ...


# noinspection PyRedeclaration
class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Point(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        return self * scalar  # for when int comes first


def yield_neighbours(self, include_diagonals=True, include_self=False):
    """ Generator to yield neighbouring Points """

    deltas: list
    if not include_diagonals:
        deltas = [vector.value for vector in Vectors if abs(vector.value.x) != abs(vector.value.y)]
    else:
        deltas = [vector.value for vector in Vectors]

    if include_self:
        deltas.append(Point(0, 0))

    for delta in deltas:
        yield self + delta

def neighbours(self, include_diagonals=True, include_self=False) -> list[Point]:
    return list(yield_neighbours(self, include_diagonals, include_self))

def get_specific_neighbours(self, directions) -> list[Point]:
    return [self + vector.value for vector in list(directions)]

def manhattan_distance(a_point: Point):
    return sum(abs(coord) for coord in asdict(a_point).values())

def manhattan_distance_from(self, other):
    diff = self - other
    return manhattan_distance(diff)

Point.yield_neighbours = yield_neighbours
Point.neighbours = neighbours
Point.get_specific_neighbours = get_specific_neighbours
Point.manhattan_distance = staticmethod(manhattan_distance)
Point.manhattan_distance_from = manhattan_distance_from
Point.__repr__ = lambda self: f"P({self.x},{self.y})"


class Grid:
    """ 2D grid of point values. """

    def __init__(self, grid_array: list) -> None:
        self._array = [list(row) for row in grid_array.copy()]
        self._width = len(self._array[0])
        self._height = len(self._array)

        self._all_points = [Point(x, y) for y in range(self._height) for x in range(self._width)]

    def quadrant_for_pt(self, pt: Point) -> int:
        half_width = self._width // 2
        half_height = self._height // 2

        if pt.x == half_width or pt.y == half_height:
            return 0
        if pt.x < half_width:
            return 1 if pt.y < half_height else 3
        else:
            return 2 if pt.y < half_height else 4


    def value_at_point(self, point: Point):
        """ The value at this point """
        return self._array[point.y][point.x]

    def set_value_at_point(self, point: Point, value):
        self._array[point.y][point.x] = value

    def valid_location(self, point: Point) -> bool:
        """ Check if a location is within the grid """
        if (0 <= point.x < self._width and 0 <= point.y < self._height):
            return True

        return False

    @property
    def width(self):
        """ Array width (cols) """
        return self._width

    @property
    def height(self):
        """ Array height (rows) """
        return self._height

    def all_points(self) -> list[Point]:
        return self._all_points

    @property
    def cols(self):
        """ Return the grid as columns """
        return list(zip(*self._array))

    @property
    def rows(self):
        return self._array

    def rows_as_str(self):
        """ Return the grid """
        return ["".join(str(char) for char in row) for row in self._array]

    def cols_as_str(self):
        """ Render columns as str. Returns: list of str """
        return ["".join(str(char) for char in col) for col in self.cols]

    def __repr__(self) -> str:
        return f"Grid(size={self.width}*{self.height})"

    def __str__(self) -> str:
        return "\n".join("".join(map(str, row)) for row in self._array)


class Vectors(Enum):
    """ Enumeration of 8 directions.
    Note: y axis increments in the North direction, i.e. N = (0, 1) """
    N = Point(0, 1)
    NE = Point(1, 1)
    E = Point(1, 0)
    SE = Point(1, -1)
    S = Point(0, -1)
    SW = Point(-1, -1)
    W = Point(-1, 0)
    NW = Point(-1, 1)

    @property
    def y_inverted(self):
        """ Return vector, but with y-axis inverted. I.e. N = (0, -1) """
        x, y = self.value
        return Point(x, -y)