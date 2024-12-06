import curses
import os
import time
from typing import List

import numpy as np

from log_util import get_logger
from timeit import time_it
from timeout import timeout

logger = get_logger(__name__)
os.environ["TERM"] = "xterm-256color"

with open("d06.txt", "r") as file:
    data = [list(line.strip()) for line in file]

test_data = [
    ['.', '.', '.', '.', '#', '.', '.', '.', '.', '.', ],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.', '#', ],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', ],
    ['.', '.', '#', '.', '.', '.', '.', '.', '.', '.', ],
    ['.', '.', '.', '.', '.', '.', '.', '#', '.', '.', ],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', ],
    ['.', '#', '.', '.', '^', '.', '.', '.', '.', '.', ],
    ['.', '.', '.', '.', '.', '.', '.', '.', '#', '.', ],
    ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', ],
    ['.', '.', '.', '.', '.', '.', '#', '.', '.', '.', ],
]  # should take 41 steps, exit at 9,7


def visualize_simulation(grid):
    rows, cols = len(grid), len(grid[0])

    # Directions: up, right, down, left
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    direction_chars = ["^", ">", "v", "<"]
    direction_idx = 0  # Start facing "up"

    # Find the starting position of the guard
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] in "^>v<":
                start_pos = (r, c)
                break

    guard_pos = start_pos
    visited_positions = set()  # Track distinct positions
    visited_positions.add(guard_pos)

    def display_grid():
        os.system("clear")  # Use "cls" if on Windows
        for r in range(rows):
            for c in range(cols):
                if (r, c) == guard_pos:
                    print(direction_chars[direction_idx], end="")
                elif (r, c) in visited_positions:
                    print("X", end="")
                else:
                    print(grid[r][c], end="")
            print()
        time.sleep(0.3)

    while True:
        display_grid()
        r, c = guard_pos
        dr, dc = directions[direction_idx]

        # Calculate the next position
        next_r, next_c = r + dr, c + dc

        # Check if the next position is out of bounds
        if not (0 <= next_r < rows and 0 <= next_c < cols):
            break

        # Check if the next position is an obstacle
        if grid[next_r][next_c] == "#":
            # Turn right
            direction_idx = (direction_idx + 1) % 4
        else:
            # Move forward
            guard_pos = (next_r, next_c)
            visited_positions.add(guard_pos)

    display_grid()  # Final display

    return len(visited_positions)


# Simulate and visualize the guard's patrol
# distinct_positions = visualize_simulation(test_data)
# print(f"The guard visited {distinct_positions} distinct positions.")

# distinct_positions = visualize_simulation(data)
# print(f"The guard visited {distinct_positions} distinct positions.")


@timeout(600)
@time_it
def simulate_with_curses(grid):
    def display_grid_with_scrolling(stdscr, grid, guard_pos, visited_positions, direction_idx):
        stdscr.clear()
        max_rows, max_cols = stdscr.getmaxyx()
        direction_chars = ["^", ">", "v", "<"]

        guard_row, guard_col = guard_pos
        direction_char = direction_chars[direction_idx]

        # Define viewport size (leave space for borders if necessary)
        viewport_height = max_rows
        viewport_width = max_cols

        # Calculate the viewport's top-left corner based on the guard's position
        viewport_row = max(0, min(guard_row - viewport_height // 2, len(grid) - viewport_height))
        viewport_col = max(0, min(guard_col - viewport_width // 2, len(grid[0]) - viewport_width))

        # Render only the visible portion of the grid
        for r in range(viewport_row, min(viewport_row + viewport_height, len(grid))):
            for c in range(viewport_col, min(viewport_col + viewport_width, len(grid[0]))):
                char = grid[r][c]
                if (r, c) == guard_pos:
                    char = direction_char
                elif (r, c) in visited_positions:
                    char = "X"
                stdscr.addch(r - viewport_row, c - viewport_col, char)

        stdscr.refresh()

    def display_grid(stdscr, guard_pos, visited_positions, direction_idx):
        stdscr.clear()
        rows, cols = len(grid), len(grid[0])
        direction_chars = ["^", ">", "v", "<"]

        for r in range(rows):
            for c in range(cols):
                if (r, c) == guard_pos:
                    stdscr.addch(r, c, direction_chars[direction_idx])
                elif (r, c) in visited_positions:
                    stdscr.addch(r, c, "X")
                else:
                    stdscr.addch(r, c, grid[r][c])

        stdscr.refresh()
        time.sleep(0.2)

    def main(stdscr):
        curses.curs_set(0)  # Hide the cursor
        rows, cols = len(grid), len(grid[0])

        # Directions: up, right, down, left
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        direction_idx = 0  # Start facing "up"

        # Find the starting position of the guard
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] in "^>v<":
                    start_pos = (r, c)
                    break

        guard_pos = start_pos
        visited_positions = set()  # Track distinct positions
        visited_positions.add(guard_pos)

        while True:
            display_grid(stdscr, guard_pos, visited_positions, direction_idx)
            r, c = guard_pos
            dr, dc = directions[direction_idx]

            # Calculate the next position
            next_r, next_c = r + dr, c + dc

            # Check if the next position is out of bounds
            if not (0 <= next_r < rows and 0 <= next_c < cols):
                break

            # Check if the next position is an obstacle
            if grid[next_r][next_c] == "#":
                # Turn right
                direction_idx = (direction_idx + 1) % 4
            else:
                # Move forward
                guard_pos = (next_r, next_c)
                visited_positions.add(guard_pos)

        display_grid(stdscr, guard_pos, visited_positions, direction_idx)

    return curses.wrapper(main)


# Simulate and visualize the guard's patrol
# simulate_with_curses(test_data)


@timeout(600)
@time_it
def another_traversal(grid):
    rows, cols = len(grid), len(grid[0])

    # Directions: up, right, down, left
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    direction_idx = 0  # Start facing "up"

    # Find the starting position of the guard
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] in "^>v<":
                start_pos = (r, c)
                logger.info(f"Guard found at {start_pos}")
                break

    guard_pos = start_pos
    visited_positions = set()  # Track distinct positions
    visited_positions.add(guard_pos)

    while True:
        r, c = guard_pos
        dr, dc = directions[direction_idx]

        # Calculate the next position
        next_r, next_c = r + dr, c + dc

        # Check if the next position is out of bounds
        if not (0 <= next_r < rows and 0 <= next_c < cols):
            break

        # Check if the next position is an obstacle
        if grid[next_r][next_c] == "#":
            # Turn right
            direction_idx = (direction_idx + 1) % 4
        else:
            # Move forward
            guard_pos = (next_r, next_c)
            visited_positions.add(guard_pos)
    return visited_positions


visited_position = list(another_traversal(test_data))
logger.debug(f"Visited {len(visited_position)} positions.")

# okay for real time
# simulate_with_curses(data)  # to big, maybe mess with scrolling later
logger.info(len(another_traversal(data)))

# Part 2
# find how many times the guard can get locked into a loop by adding exactly 1 obstruction
# test grid should produce 6 options

test_visited_positions = list(another_traversal(test_data))
logger.debug(test_visited_positions)
logger.debug(f"Visited {len(test_visited_positions)} positions.")


def simulate_with_obstacle(grid, start_pos, obstacle_pos, direction_idx):
    """
    Simulates the guard's traversal with a given obstacle and detects a loop.
    Returns True if a loop is detected, False otherwise.
    """
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Up, Right, Down, Left
    guard_pos = start_pos
    direction = direction_idx
    visited = set()
    max_steps = len(grid) * len(grid[0]) * 2  # Arbitrary limit to detect infinite loops

    steps = 0
    while steps < max_steps:
        if guard_pos in visited:
            return True  # Loop detected
        visited.add(guard_pos)

        # Calculate next position
        next_pos = (guard_pos[0] + directions[direction][0], guard_pos[1] + directions[direction][1])

        # Check if the guard exits the grid
        if not (0 <= next_pos[0] < len(grid) and 0 <= next_pos[1] < len(grid[0])):
            return False  # Guard exits the grid, no loop

        # Check for obstacles
        if next_pos == obstacle_pos or grid[next_pos[0]][next_pos[1]] == "#":
            direction = (direction + 1) % 4  # Turn right 90 degrees
        else:
            guard_pos = next_pos  # Move forward

        steps += 1

    return False  # No loop detected within max_steps


def find_loop_positions(grid, start_pos, visited_positions, direction_idx):
    """
    Identifies all positions where adding an obstacle causes the guard to loop.
    """
    loop_positions = []

    for pos in visited_positions:
        # Test each visited position as a potential obstacle
        if simulate_with_obstacle(grid, start_pos, pos, direction_idx):
            loop_positions.append(pos)

    return loop_positions


possible_loops = find_loop_positions(test_data, test_visited_positions[0], test_visited_positions, 0)
logger.debug(f"Possible loops {possible_loops}")


def user_fidelisakilan():
    file = open("d06.txt", "r").readlines()

    matrix = []
    dir = [
        (-1, 0),
        (0, 1),
        (1, 0),
        (0, -1),
    ]
    si, sj = 0, 0

    matrix = list(list(line.strip()) for line in file)
    rows = len(matrix)
    columns = len(matrix[0])

    for i in range(rows):
        for j in range(columns):
            if matrix[i][j] == "^":
                si, sj = (i, j)
                break

    count = 0
    for i in range(rows):
        for j in range(columns):
            if matrix[i][j] == "#" or matrix[i][j] == "^":
                continue
            matrix[i][j] = "#"
            seen = set()
            cd = 0
            ci, cj = si, sj
            while ci in range(rows) and cj in range(columns) and (ci, cj, cd) not in seen:
                seen.add((ci, cj, cd))
                cdir = dir[cd]
                ni, nj = ci + cdir[0], cj + cdir[1]
                if ni in range(rows) and nj in range(columns) and matrix[ni][nj] == "#":
                    cd = (cd + 1) % 4
                else:
                    ci, cj = ni, nj
            if (ci, cj, cd) in seen:
                count += 1
            matrix[i][j] = "."
    return count


logger.warning(user_fidelisakilan())  # 1443


def simulate_with_state_tracking(grid, start_pos, obstacle_pos, direction_idx):
    """
    Simulates the guard's path with an added obstacle and detects loops using state tracking.
    Returns True if a loop is detected, False otherwise.
    """
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Up, Right, Down, Left
    guard_pos = start_pos
    direction = direction_idx
    visited_states = set()  # Tracks (position, direction)

    while True:
        state = (guard_pos, direction)
        if state in visited_states:
            return True  # Loop detected
        visited_states.add(state)

        # Calculate the next position
        next_pos = (guard_pos[0] + directions[direction][0], guard_pos[1] + directions[direction][1])

        # Check if the guard exits the grid
        if not (0 <= next_pos[0] < len(grid) and 0 <= next_pos[1] < len(grid[0])):
            return False  # No loop, the guard exits

        # Check for obstacles
        if next_pos == obstacle_pos or grid[next_pos[0]][next_pos[1]] == "#":
            direction = (direction + 1) % 4  # Turn right 90 degrees
        else:
            guard_pos = next_pos  # Move forward


def find_loop_positions_with_state_tracking(grid, start_pos, visited_positions, direction_idx):
    """
    Finds all positions where adding an obstacle causes a loop using state tracking.
    """
    loop_positions = []

    for pos in visited_positions:
        # Test each visited position as a potential obstacle
        if simulate_with_state_tracking(grid, start_pos, pos, direction_idx):
            loop_positions.append(pos)

    return loop_positions


# Test data
test_grid = [
    "....#.....",
    ".........#",
    "..........",
    "..#.......",
    ".......#..",
    "..........",
    ".#........",
    "........#.",
    "#.........",
    "......#..."
]

# Convert grid to list of lists for mutability
test_grid = [list(row) for row in test_grid]

# Initial setup
visited_positions = [
    (3, 4), (4, 3), (5, 4), (4, 6), (8, 3), (8, 6), (1, 6), (2, 8), (7, 4), (6, 2),
    (7, 1), (7, 7), (6, 5), (6, 8), (4, 2), (4, 5), (5, 6), (4, 8), (8, 2), (9, 7),
    (8, 5), (2, 4), (1, 5), (1, 8), (6, 4), (7, 3), (6, 7), (7, 6), (5, 2), (4, 4),
    (3, 8), (8, 4), (5, 8), (8, 1), (8, 7), (1, 4), (1, 7), (7, 2), (6, 6), (7, 5), (6, 3)
]
start_pos = (6, 4)  # Guard's starting position
direction_idx = 0  # Facing up initially

# Find loop-causing positions
loop_positions = find_loop_positions_with_state_tracking(test_grid, start_pos, visited_positions, direction_idx)
logger.debug("Positions where adding 'O' causes a loop:", loop_positions)
