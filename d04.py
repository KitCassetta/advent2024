import re

import numpy as np

pattern = r"XMAS|SAMX"
data = []
cnt = 0

with open("d04.txt") as file:
    for line in file:
        line = line.strip()
        # handles east-west matches
        cnt += len(re.findall(pattern, line))

        data.append(list(line))

print(f"Total matches: {cnt}")

# Transpose the matrix
np_data = np.array(data)
t_data = np.transpose(np_data)

for row in t_data:
    line = "".join([i for i in row])
    # handles north-south matches
    cnt += len(re.findall(pattern, line))
print("After Transpose")
print(f"Total matches: {cnt}")


# now for the diagonals
# Function to get all diagonals
def extract_diagonals(matrix):
    n = len(matrix)
    m = len(matrix[0])
    diagonals = []

    # Top-right to bottom-left (anti-diagonals)
    for d in range(n + m - 1):
        diagonal = ''.join(matrix[i][d - i] for i in range(max(0, d - m + 1), min(n, d + 1)))
        diagonals.append(diagonal)

    # Top-left to bottom-right (primary diagonals)
    for d in range(-(n - 1), m):
        diagonal = ''.join(matrix[i][i - d] for i in range(max(d, 0), min(n, m + d)))
        diagonals.append(diagonal)

    return diagonals


breakpoint()
# Extract all diagonals
diagonals = extract_diagonals(data)

for row in diagonals:
    line = "".join([i for i in row])
    # handles north-south matches
    cnt += len(re.findall(pattern, line))
print("After Diagonals")
print(f"Total matches: {cnt}")


def count_occurrences(grid, word):
    """
    ref: ChatGPT
    Explanation
    Directions:
        The function uses 8 directions to account for horizontal, vertical, and diagonal matches in both forward and
        backward orientations.
    Match Verification:
        Starting from each cell in the grid, the code attempts to match the word in each of the 8 possible directions.
        If the word is found, it increments the count.
    Boundary Checks:
        The loop ensures that the search doesn't exceed grid boundaries.
    Efficiency:
        The grid is traversed once for each direction, making this approach computationally efficient for typical
        word searches.
    :param grid: matrix of str
    :param word: word to find
    :return: int of occurrences
    """
    n = len(grid)  # Number of rows
    m = len(grid[0])  # Number of columns
    word_len = len(word)
    total_count = 0

    # Directions: (row_delta, col_delta)
    directions = [
        (0, 1),  # Horizontal right
        (0, -1),  # Horizontal left
        (1, 0),  # Vertical down
        (-1, 0),  # Vertical up
        (1, 1),  # Diagonal down-right
        (1, -1),  # Diagonal down-left
        (-1, 1),  # Diagonal up-right
        (-1, -1)  # Diagonal up-left
    ]

    # Iterate through each cell in the grid
    for i in range(n):
        for j in range(m):
            # Check for the word starting at grid[i][j] in each direction
            for d in directions:
                row, col = i, j
                match = True

                for k in range(word_len):
                    if 0 <= row < n and 0 <= col < m and grid[row][col] == word[k]:
                        # Move to the next cell in the current direction
                        row += d[0]
                        col += d[1]
                    else:
                        match = False
                        break

                if match:
                    total_count += 1

    return total_count


# Input grid
grid = [
    "MMMSXXMASM",
    "MSAMXMSMSA",
    "AMXSXMAAMM",
    "MSAMASMSMX",
    "XMASAMXAMM",
    "XXAMMXXAMA",
    "SMSMSASXSS",
    "SAXAMASAAA",
    "MAMMMXMMMM",
    "MXMXAXMASX",
]

# Word to search for
word = "XMAS"

# Count occurrences
occurrences = count_occurrences(grid, word)
print(f"The word '{word}' occurs a total of {occurrences} times.")

print(f"The word '{word}' occurs a total of {count_occurrences(data, word)} times.")


# part 2
# X-MAS
# M.S
# .A.
# M.S
def count_xmas_patterns(grid):
    n = len(grid)  # Number of rows
    m = len(grid[0])  # Number of columns
    total_count = 0

    # Iterate through the grid, looking for "X-MAS" patterns
    for i in range(1, n - 1):  # Middle of the "X" cannot be on the edge
        for j in range(1, m - 1):  # Same for columns
            if (grid[i][j] == 'A' and
                    grid[i - 1][j - 1] == 'M' and grid[i + 1][j + 1] == 'M' and  # Top-left to bottom-right
                    grid[i - 1][j + 1] == 'S' and grid[i + 1][j - 1] == 'S'):  # Top-right to bottom-left
                total_count += 1

    return total_count


# Input grid
grid = [
    "MMMSXXMASM",
    "MSAMXMSMSA",
    "AMXSXMAAMM",
    "MSAMASMSMX",
    "XMASAMXAMM",
    "XXAMMXXAMA",
    "SMSMSASXSS",
    "SAXAMASAAA",
    "MAMMMXMMMM",
    "MXMXAXMASX",
]

# Count X-MAS patterns
occurrences = count_xmas_patterns(grid)
print(f"The X-MAS pattern appears a total of {occurrences} times.")

print(f"The X-MAS pattern appears a total of {count_xmas_patterns(data)} times.")


def count_xmas_patterns_modified(grid):
    """
        Explanation
        Grid Iteration:
            The middle of the "X" (the 'A') cannot be on the border of the grid.
            Thus, the loop starts and ends one row/column away from the edges.
        Pattern Check:
            At each cell (i, j), check if:
            The cell contains 'A' (middle of the X).
            if any two corners are 'M' and their opposite are 'S' we found an X-MAS
        Count Matches:
            For every pair of matches found, increment the total_count.
        :param grid: matrix of str
        :return: int count
        """
    n = len(grid)  # Number of rows
    m = len(grid[0])  # Number of columns
    total_count = 0

    # Iterate through the grid to find 'A'
    for i in range(1, n - 1):  # Avoid edges
        for j in range(1, m - 1):  # Avoid edges
            if grid[i][j] == 'A':  # Found the center 'A'
                found = []  # we need to track how many we found (must be exactly 2)
                # Check all four diagonal "X-MAS" possibilities
                if (grid[i - 1][j - 1] == 'M' and grid[i + 1][j + 1] == 'S'):  # Top-left 'M', bottom-right 'S'
                    found.append(1)
                if (grid[i - 1][j + 1] == 'M' and grid[i + 1][j - 1] == 'S'):  # Top-right 'M', bottom-left 'S'
                    found.append(1)
                if (grid[i + 1][j + 1] == 'M' and grid[i - 1][j - 1] == 'S'):  # Bottom-right 'M', top-left 'S'
                    found.append(1)
                if (grid[i + 1][j - 1] == 'M' and grid[i - 1][j + 1] == 'S'):  # Bottom-left 'M', top-right 'S'
                    found.append(1)
                if sum(found) == 2:
                    total_count += 1

    return total_count


# Input grid
grid = [
    "MMMSXXMASM",
    "MSAMXMSMSA",
    "AMXSXMAAMM",
    "MSAMASMSMX",
    "XMASAMXAMM",
    "XXAMMXXAMA",
    "SMSMSASXSS",
    "SAXAMASAAA",
    "MAMMMXMMMM",
    "MXMXAXMASX",
]

# Count X-MAS patterns
occurrences = count_xmas_patterns_modified(grid)
print(f"The X-MAS pattern appears a total of {occurrences} times.")

print(f"The X-MAS pattern appears a total of {count_xmas_patterns_modified(data)} times.")
