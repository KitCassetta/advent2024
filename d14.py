"""
--- Day 14: Restroom Redoubt ---

Link:
    https://adventofcode.com/2024/day/14

"""
import math
from collections import defaultdict
from pathlib import Path
from sys import argv

from tqdm import tqdm

from utils.utils import Grid, Point


DEMO_INPUT = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""


def remap(lines: str) -> list[tuple[int, int], tuple[int, int]]:
    """
    Remap example list input provided in "Advent of Code"
    format.
    """
    robot_pos_and_velocities = lines.strip().split('\n')

    # noinspection PyTypeChecker
    return [(tuple(map(int, (res := pv.split(' ', 1))[0][2:].split(','))),
             tuple([int(r) for r in res[1][2:].split(',')]))
    for pv in robot_pos_and_velocities]


def part_1(equations: list[tuple[int, int], tuple[int, int]],
           width=101, height=103, default=0):

    g = Grid([[default] * width] * height)

    robot_to_point: dict[int, Point] = {}
    robot_to_velocity: dict[int, Point] = {}
    quadrant_to_num_robots: dict[int, int] = defaultdict(int)

    for i, (start, velocity) in enumerate(equations):

        robot_to_point[i] = pt = Point(*start)
        robot_to_velocity[i] = Point(*velocity)

        g.set_value_at_point(pt, 1)
        quadrant_to_num_robots[g.quadrant_for_pt(pt)] += 1

    for i in range(100):
        for robot, pt in robot_to_point.items():
            velocity = robot_to_velocity[robot]
            # noinspection PyTypeChecker
            new_pt: Point = pt + velocity
            new_pt = Point(new_pt.x % g.width, new_pt.y % g.height)
            robot_to_point[robot] = new_pt

            # Set robots in quadrants
            qd = g.quadrant_for_pt(pt)
            new_qd = g.quadrant_for_pt(new_pt)
            if quadrant_to_num_robots[qd] >= 1:
                quadrant_to_num_robots[qd] -= 1
            quadrant_to_num_robots[new_qd] += 1

            # Update value in grid
            value = g.value_at_point(pt)
            g.set_value_at_point(pt, max(value - 1, 0))
            g.set_value_at_point(new_pt, g.value_at_point(new_pt) + 1)

    safety_factor = 1
    for i in range(1, 5):
        safety_factor *= quadrant_to_num_robots[i]

    return safety_factor


def part_2(equations: list[tuple[int, int], tuple[int, int]],
           width=101, height=103,
           default='.',
           max_iterations=100_000):

    g = Grid([[default] * width] * height)

    robot_to_point: dict[int, Point] = {}
    robot_to_velocity: dict[int, Point] = {}
    quadrant_to_num_robots: dict[int, int] = defaultdict(int)

    min_safety_factor = math.inf
    final_t = None
    final_grid = None

    for i, (start, velocity) in enumerate(equations):
        robot_to_point[i] = pt = Point(*start)
        robot_to_velocity[i] = Point(*velocity)

        g.set_value_at_point(pt, 1)
        quadrant_to_num_robots[g.quadrant_for_pt(pt)] += 1

    for t in tqdm(range(1, max_iterations + 1)):

        for robot, pt in robot_to_point.items():
            velocity = robot_to_velocity[robot]
            new_pt = pt + velocity
            new_pt = Point(new_pt.x % g.width, new_pt.y % g.height)
            qd = g.quadrant_for_pt(pt)

            robot_to_point[robot] = new_pt

            if quadrant_to_num_robots[qd] >= 1:
                quadrant_to_num_robots[qd] -= 1

            quadrant_to_num_robots[g.quadrant_for_pt(new_pt)] += 1

            value = g.value_at_point(pt)
            if value == default:
                value = 0
            g.set_value_at_point(pt, max(value - 1, 0) or default)

            new_value = g.value_at_point(new_pt)
            if new_value == default:
                new_value = 0
            g.set_value_at_point(new_pt, new_value + 1)

        safety_factor = 1
        for i in range(1, 5):
            safety_factor *= quadrant_to_num_robots[i]

        if safety_factor < min_safety_factor:
            min_safety_factor = safety_factor
            final_t = t
            final_grid = str(g)

    print(final_grid)

    print(f'Minimum seconds: {final_t}')
    print(f'Safety Factor: {min_safety_factor}')

    return final_t


def solve(input_file=None):
    if input_file:
        demo = False
        default = ' '
        print(f"Solving with input file {input_file}")
        try:
            INPUT = open(input_file).read()
        except FileNotFoundError:
            print('File not found, using default ...')
            INPUT = open(Path(__file__).parent.parent / 'd14').read()
        _width = 101
        _height = 103

    else:
        demo = True
        default = '.'
        INPUT = DEMO_INPUT
        _width = 11
        _height = 7

    print("Solving Day 14 Problem! 🎄")

    _equations = remap(INPUT)

    # Part 1
    _safety_factor = part_1(_equations, _width, _height)
    print('Part 1:', _safety_factor)

    # Part 2
    _t = part_2(_equations, default=default)
    print('Part 2:', _t)


if __name__ == '__main__':
    solve('d14.txt')