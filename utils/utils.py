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

from enum import Enum
import numpy as np
import math


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


# Unless otherwise specified, all directions are represented by a tuple (row, col) ie y, x.
# This to make it easier to reference lists.
NORTH = (-1, 0)
EAST = (0, 1)
SOUTH = (1, 0)
WEST = (0, -1)
NORTHEAST = (-1, 1)
SOUTHEAST = (1, 1)
SOUTHWEST = (1, -1)
NORTHWEST = (-1, -1)

# Clockwise 90 degrees
ROTATE = {
    EAST: SOUTH, SOUTH: WEST, WEST: NORTH, NORTH: EAST
}


DIRECTIONS_ALL = [
    NORTH,
    EAST,
    SOUTH,
    WEST,
    NORTHEAST,
    SOUTHEAST,
    SOUTHWEST,
    NORTHWEST,
]

DIRECTION_DELTAS = {
    # (row, col)
    Direction.EAST: EAST,
    Direction.NORTH: NORTH,
    Direction.WEST: WEST,
    Direction.SOUTH: SOUTH
}

ARROWS_TO_DIRECTION = {
    '>': Direction.EAST,
    'v': Direction.SOUTH,
    '<': Direction.WEST,
    '^': Direction.NORTH,
}

ARROWS_TO_DIRECTION2 = {
    '>': EAST,
    'v': SOUTH,
    '<': WEST,
    '^': NORTH,
}

DIRECTION2_TO_ARROWS = {
    EAST: '>',
    SOUTH: 'v',
    WEST: '<',
    NORTH: '^',
}


def into_range(x, n, m):
    # for x returns value in range n-m (inclusive)
    return ((x-n) % (m-n+1))+n


def next_neighbour(position, direction):
    return (position[0] + DIRECTION_DELTAS[direction][0], position[1] + DIRECTION_DELTAS[direction][1])


def next_neighbour2(position, direction):
    # a faster version if direction is stored as tuple instead of enum
    return (position[0] + direction[0], position[1] + direction[1])


def in_grid(position, grid):
    return 0 <= position[0] < len(grid) and 0 <= position[1] < len(grid[0])


def tile(grid, p):
    return grid[p[0]][p[1]]


def add_pos(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])


def subtract_pos(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1])


direction = subtract_pos


def print_grid(grid, axis=False):
    if axis:
        print('  ' + ''.join([str(i % 10) for i in range(len(grid[0]))]))

    for r, row in enumerate(grid):
        if axis:
            print(r % 10, end=' ')
        print(''.join(row))


def make_grid(rows, cols, value=0):
    #  return np.array([[point(x, y) for x in range(cols)] for y in range(rows)])
    return [[value] * cols for _ in range(rows)]


# return all positions of value in grid
def find_in_grid(grid, value):
    result = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == value:
                result.append((i, j))

    return result


def neighbours(position, grid, check_in_bounds=True, condition=lambda g, x: True):
    def in_grid_bound(p):
        if check_in_bounds:
            return in_grid(p, grid)
        else:
            return True

    result = []
    for d in DIRECTION_DELTAS.keys():
        new_position = next_neighbour(position, d)
        if in_grid_bound(new_position) and condition(grid, new_position):
            result.append(new_position)

    return result


def reverse_direction(direction):
    if direction == Direction.EAST:
        return Direction.WEST
    if direction == Direction.WEST:
        return Direction.EAST
    if direction == Direction.NORTH:
        return Direction.SOUTH
    if direction == Direction.SOUTH:
        return Direction.NORTH


# rotate 90 degrees clockwise or anticlockwise
def rotate_direction(current_direction, anticlockwise=False):
    directions = list(Direction)

    # Determine the step: +1 for clockwise, -1 for anticlockwise
    step = -1 if anticlockwise else 1

    # Calculate the next index using modular arithmetic
    next_index = (current_direction.value + step) % len(directions)
    return directions[next_index]


class Direction2(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


def read_file_str(filename, strip=False):
    """ return list of strings, one line per list entry"""
    result = []
    with open(filename) as f:
        for line in f:
            l = line
            if strip:
                l = line.strip()
            result.append(l)

    return result


def read_file_int(filename):
    """ file consists of a rows of numbers"""
    result = []
    with open(filename) as f:
        for line in f:
            result.append(list(map(int, line.split())))

    return result


def lcm(l):
    #  https://en.wikipedia.org/wiki/Least_common_multiple
    result = 1
    for n in l:
        result = (n*result) // math.gcd(n, result)
    return result


# Boolean, unsigned integer, signed integer, float, complex.
NUMERIC_KINDS = set('buifc')
NOT_NUMERIC = [object(), 'string', u'unicode', None]


def replace(s, index, new_char):
    """ change single char at index in string s """
    return s[:index] + new_char + s[index + 1:]


def is_blank(s):
    """ Return true if string is not defined or empty"""
    return not (s and s.strip())


def is_numeric(array):
    return np.asarray(array).dtype.kind in NUMERIC_KINDS


def is_valid(enum, s):
    """ checks if s is a valid value for an enum class"""
    for l in list(enum):
        if l.value == s:
            return True

    return False


def to_numpy_array(a):
    # Turn list of strings into 2D numpy array with one character per cell

    rows = [list(l) for l in a]
    return np.array(rows, str)


def print_np_info(a):
    print('size: ', a.size)
    print('shape: ', a.shape)
    if is_numeric(a):
        print('max:', a.max(axis=0))
        print('min:', a.min(axis=0))


def determinant(p1, p2):
    #  print(p1, p2)
    return p1[0] * p2[1] - p1[1] * p2[0]


def internal_area(boundary_points, boundary_length):
    # https://en.wikipedia.org/wiki/Pick%27s_theorem
    # Pick's theorem: total area = internal_area + boundary_length/2 - 1
    # We have the boundary points and need the internal area.
    # Rearranging, we get: internal_area = area + 1 - boundary_length/2
    # We use the shoelace formula to get the total area
    return (shoelace_area(boundary_points) + 1 - boundary_length / 2)


def shoelace_area(input):
    # https://en.wikipedia.org/wiki/Shoelace_formula

    area = 0
    for i in range(len(input)):
        p1 = input[i]
        p2 = input[(i + 1) % len(input)]
        area += determinant(p1, p2)

    return abs(area)/2


def hex_to_dec(s):
    return int(s, 16)

# class Point:
#     def __init__(self, x=0, y=0):
#         self.x = x
#         self.y = y
#         np.array

#     def __eq__(self, other):
#         if isinstance(other, Point):
#             return self.x == other.x and self.y == other.y
#         return False

#     def __hash__(self) -> int:
#         return hash((self.x, self.y))

#     def __add__(self, other):
#         return self.add(other)

#     def add(self, p, count=1):
#         return Point(self.x + (p.x * count), self.y + (p.y * count))

#     def __repr__(self):
#         return "".join(["Point(", str(self.x), ",", str(self.y), ")"])

#     def distance_from_origin(self):
#         return ((self.x ** 2) + (self.y ** 2)) ** 0.5

#     def print_point(self):
#         print('({0}, {1})'.format(self.x, self.y))

#     def distanceFromOrigin(self):
#         origin = Point(0, 0)
#         dist = self.distanceFromPoint(origin)
#         return dist

#     def distanceFromPoint(self, point):
#         return math.sqrt(self.x - point.x)**2 + (self.y - point.y)**2

#     def is_adjacent(self, p, include_diagonal=True):
#         adj = ADJACENT_DIAG if include_diagonal else ADJACENT
#         return any([self + a == p for a in adj])


def point(x=0, y=0):
    return np.array([x, y])


def manhattan_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    return abs(x2 - x1) + abs(y2 - y1)


def is_adjacent(p1, p2, include_diagonal=True):
    adj = ADJACENT_DIAG if include_diagonal else ADJACENT
    return any([np.array_equal(p1 + a, p2) for a in adj])


ADJACENT = [point(0, 1), point(0, -1), point(1, 0), point(-1, 0)]
ADJACENT_DIAG = [*ADJACENT,
                 point(1, 1), point(1, -1), point(-1, 1), point(-1, -1)]

# provide equation of line coefficients (A, B, C) for Ax+By=C


def intersection_point(line1, line2):

    A = np.array([line1[:2], line2[:2]])
    b = np.array([line1[2], line2[2]])
    try:
        return np.linalg.solve(A, b)
    except np.linalg.LinAlgError:
        return None  # Lines are parallel


# return A, B, C for Ax+By=C
def equation_of_line_coefficients(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    # m = slope
    if x2 - x1 != 0:  # Avoid div by zero
        m = (y2 - y1) / (x2 - x1)
    else:
        m = float('inf')  # Vertical line

    # Use one of the points to find the equation
    # For vertical lines (x2 - x1 == 0), the equation is x = x1
    if m != float('inf'):
        C = y1 - m * x1
        #  equation = f'y = {m}x + {b}'
        B = 1
        A = -m
    else:
        C = 0
        #  equation = f'x = {x1}'
        B = 0
        A = x1

    return (A, B, C)


def rgb(r, g, b):
    # for printing coloured text in a terminal
    return f"\033[38;2;{r};{g};{b}m"


def rgb_bg(r, g, b):
    # for printing coloured text in a terminal
    return f"\033[48;2;{r};{g};{b}m"


# For example usage, see ../../2023/src/day10.py. For example output, see
# ../../2023/data/day10-visualisation.txt
COLOUR_BLACK = rgb(0, 0, 0)
COLOUR_RED = rgb(255, 0, 0)
COLOUR_GREEN_BACKGROUND = rgb_bg(0, 255, 0)
COLOUR_RED_BACKGROUND = rgb_bg(255, 0, 0)
COLOUR_RESET = "\033[0m"  # always reset after changing colour


class ReprMixin:
    def __repr__(self):
        return "<{klass} @{id:x} {attrs}>".format(
            klass=self.__class__.__name__,
            id=id(self) & 0xFFFFFF,
            attrs=" ".join("{}={!r}".format(k, v)
                           for k, v in self.__dict__.items()),
        )


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __str__(self):
        return str(self.data)


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return

        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def insert_after(self, prev_node, data):
        new_node = Node(data)
        new_node.next = prev_node.next
        prev_node.next = new_node
        return new_node

    def prepend(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def update(self, node, data):
        node.data = data

    def delete(self, data):
        current = self.head
        if current and current.data == data:
            self.head = current.next
            return
        previous = None
        while current and current.data != data:
            previous = current
            current = current.next
        if current:
            previous.next = current.next

    def search(self, data):
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False

    @property
    def count(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def display(self):
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")