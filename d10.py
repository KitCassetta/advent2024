from log_util import get_logger

"""
Key Steps to Solve
Parse the Input:

Read the grid into a 2D array.
Identify all positions with height 0 (trailheads).
Traverse from Each Trailhead:

Start a traversal (DFS or BFS) from each trailhead.
Keep track of visited positions to avoid re-traversing them.
Apply the movement constraints:
Only move to positions where the height difference is at most 1.
Count the Target Positions:

During the traversal, count how many height 9 positions are reachable from the current trailhead.
Aggregate Results:

Sum the scores of all trailheads for a final result.
"""

logger = get_logger(__name__)

with open("d10_t.txt", "r") as file:
    t_data = [line.strip() for line in file]

with open("d10_t.txt", "r") as file:
    data = [line.strip() for line in file]


# !/usr/bin/python3
# ref: Minimum-Meal5723
def findTrailHeads(input: list[list[str]]):
    trailHeadLocations = []
    for row, line in enumerate(input):
        for col, val in enumerate(line):
            if val == '0':
                trailHeadLocations.append((row, col))
    return trailHeadLocations


def isInWorld(row, col, world: list[list]):
    return row >= 0 and row < len(world) and col >= 0 and col < len(world[row])


def find9s(row: int, col: int, input: list[list[str]], found: set[str], prev: int = -1):
    if not isInWorld(row, col, input):
        return 0
    curVal = input[row][col]
    if curVal == '.':
        return 0
    curVal = int(curVal)
    if prev + 1 != curVal:
        return 0
    if curVal == 9:
        found.add(f"{row}:{col}")
        return 1
    return (find9s(row, col - 1, input, found, curVal) +
            find9s(row, col + 1, input, found, curVal) +
            find9s(row - 1, col, input, found, curVal) +
            find9s(row + 1, col, input, found, curVal))


def parseInput(fileName: str):
    input = []
    with open(fileName, 'r') as file:
        for line in file:
            input.append(line.strip())
        trailHeads = findTrailHeads(input)
        part1Count = 0
        part2Count = 0
        for trailHead in trailHeads:
            row, col = trailHead
            found = set()
            part2Count = part2Count + find9s(row, col, input, found)
            part1Count = part1Count + len(found)
        return part1Count, part2Count


def main():
    print(parseInput('d10_t.txt'))
    print(parseInput('d10.txt'))


if __name__ == "__main__":
    main()


