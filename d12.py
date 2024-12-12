import matplotlib.pyplot as plt
from log_util import get_logger
from typing import Any

logger = get_logger(__name__)

t_data = """AAAA
BBCD
BBCC
EEEC"""  # result = 140
# The type A and C plants are each in a region with perimeter 10. regions A, C have price 4 * 10 = 40 each
# The type B plants are in a region with perimeter 8. regions B has price 4 * 8 = 32 each
# The type E plants has price 3 * 8 = 24
# The lone D plot forms its own region with perimeter 4. region D has price 1 * 4 = 4

t2_data = """
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
"""  # result = 772

t3_data = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
""" # result = 1930


def welsh_powell_coloring_with_stats(char_matrix):
    """Colors the characters in a 2D character matrix using the Welsh-Powell algorithm and calculates adjacent characters and perimeter.

    Args:
        char_matrix: A 2D list of characters.

    Returns:
        A tuple containing:
            1. A dictionary mapping each unique character to its assigned color.
            2. A dictionary mapping each unique character to its number of adjacent characters.
            3. A dictionary mapping each unique character to its perimeter.
    """

    rows, cols = len(char_matrix), len(char_matrix[0])
    char_freq = {}
    char_adj = {}
    char_perimeter = {}

    # Calculate frequencies and initialize adjacency and perimeter
    for i in range(rows):
        for j in range(cols):
            char = char_matrix[i][j]
            char_freq[char] = char_freq.get(char, 0) + 1
            char_adj[char] = char_perimeter[char] = 0

    # Calculate adjacency and perimeter
    for i in range(rows):
        for j in range(cols):
            char = char_matrix[i][j]
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < rows and 0 <= nj < cols:
                    neighbor = char_matrix[ni][nj]
                    if neighbor != char:
                        char_adj[char] += 1
                        char_perimeter[char] += 2  # Edge between the two characters

    # Sort characters by decreasing frequency
    sorted_chars = sorted(char_freq.items(), key=lambda x: x[1], reverse=True)

    # Assign colors to characters
    colors = {}
    color_index = 0
    for char, freq in sorted_chars:
        used_colors = set()
        for row in char_matrix:
            for neighbor in row:
                if neighbor != char and neighbor in colors:
                    used_colors.add(colors[neighbor])

        # Assign the smallest unused color
        for color in range(1, len(used_colors) + 2):
            if color not in used_colors:
                colors[char] = color
                break

    return colors, char_adj, char_perimeter

# Example usage:
char_matrix = [['A','A','A','A'],['B','B','C','D'],['B','B','C','C'],['E','E','E','C']]
colors, adj_counts, perimeters = welsh_powell_coloring_with_stats(char_matrix)
logger.info(f"Colors: {colors}")
logger.info(f"Adjacent Characters: {adj_counts}")
logger.info(f"Perimeters: {perimeters}")


def print_colored_matrix(char_matrix, colors):
    color_map = {1: 'red', 2: 'green', 3: 'blue', 4: 'yellow', 5: 'cyan', 6: 'magenta'}  # Adjust colors as needed

    for row in char_matrix:
        for char in row:
            color_code = color_map[colors[char]]
            print(f"\033[{color_code}m{char}\033[0m", end='')
        print()


def plot_colored_matrix(char_matrix, colors):
    color_map = {1: 'red', 2: 'green', 3: 'blue', 4: 'yellow', 5: 'cyan', 6: 'magenta'}

    plt.figure(figsize=(5, 5))
    plt.imshow([[color_map[colors[char]] for char in row] for row in char_matrix], cmap='viridis')
    plt.axis('off')
    plt.show()



Grid = list[list[str]]
Position = tuple[int, int]
Region = set[Position]

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def is_valid(grid: Grid, row: int, col: int):
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])


def find_region( grid: Grid, area: str, row: int, col: int, seen: set[Position],) -> Region:
    if not is_valid(grid, row, col):
        return set()

    if grid[row][col] != area:
        return set()

    if (row, col) in seen:
        return set()

    seen.add((row, col))

    result = {(row, col)}

    for dx, dy in DIRECTIONS:
        new_row = row + dx
        new_col = col + dy

        if is_valid(grid, new_row, new_col) and (new_row, new_col) not in seen:
            result.update(find_region(grid, area, new_row, new_col, seen))

    return result


def find_all_regions(grid: Grid) -> list[Region]:
    seen = set()
    regions = []

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if (row, col) not in seen:
                region = find_region(grid, grid[row][col], row, col, set())

                seen.update(region)
                regions.append(region)

    return regions


def part_1() -> Any:
    grid: Grid = [list(x) for x in open("d12.txt").read().splitlines()]
    regions = find_all_regions(grid)

    result = 0

    for region in regions:
        area = len(region)
        perimeter = 0

        for row, col in region:
            for dx, dy in DIRECTIONS:
                new_row = row + dx
                new_col = col + dy

                if (new_row, new_col) not in region:
                    perimeter += 1

        result += area * perimeter

    return result


def part_2() -> Any:
    grid: Grid = [list(x) for x in open("d12.txt").read().splitlines()]
    regions = find_all_regions(grid)

    result = 0

    for region in regions:
        area = len(region)

        seen = set()
        corners = 0

        for row, col in region:
            for dx, dy in [
                (-0.5, -0.5),
                (0.5, -0.5),
                (0.5, 0.5),
                (-0.5, 0.5),
            ]:
                new_row = row + dx
                new_col = col + dy

                if (new_row, new_col) in seen:
                    continue

                seen.add((new_row, new_col))

                adjacent = sum(
                    (new_row + r, new_col + c) in region
                    for r, c in [
                        (-0.5, -0.5),
                        (0.5, -0.5),
                        (0.5, 0.5),
                        (-0.5, 0.5),
                    ]
                )

                if adjacent == 1 or adjacent == 3:
                    corners += 1
                elif adjacent == 2:
                    # diagonal
                    pattern = [
                        (r, c) in region
                        for r, c in [
                            (new_row - 0.5, new_col - 0.5),
                            (new_row + 0.5, new_col + 0.5),
                        ]
                    ]

                    if pattern == [True, True] or pattern == [False, False]:
                        corners += 2

        result += area * corners

    return result

logger.info(part_1())
logger.info(part_2())