import numpy as np

# for debugging
def display_grid():
    for r in range(rows):
        for c in range(cols):
            if grid[r,c] == WALL:
                print('##', end='')
            elif (r,c) in path:
                if 0<= grid[r,c] <= 9:
                    print(' ' + str(grid[r,c]), end='')
                else:
                    print(grid[r,c], end='')
            else:
                print('..', end='')
        print('')
    print('')


with open('d20.txt', 'r') as f:
    lines = f.read().split('\n')

WALL = -1
PATH = 0
rows = len(lines)
cols = len(lines[0])
grid = np.empty((rows, cols), dtype=int)
for i, L in enumerate(lines):
    for j, c in enumerate(L):
        if c == '#':
            grid[i,j] = WALL
        elif c == 'S':
            grid[i,j] = PATH
            start = (i,j)
        elif c == 'E':
            grid[i,j] = PATH
            end = (i,j)
        else:
            grid[i,j] = PATH

# generate the default path through the grid
path = []
current_cell = start
path.append(start)
grid[current_cell] = 0
while current_cell != end:
    r = current_cell[0]
    c = current_cell[1]

    if c - 1 >= 0 and grid[r, c-1] == PATH \
        and (r, c-1) not in path:
        path.append((r, c-1))
    elif c + 1 < cols and grid[r, c+1] == PATH \
        and (r, c+1) not in path:
        path.append((r, c+1))
    elif r - 1 >= 0 and grid[r-1, c] == PATH \
        and (r-1, c) not in path:
        path.append((r-1, c))
    else:
        path.append((r+1, c))
    current_cell = path[-1]
    grid[current_cell] = len(path) - 1

# calculate length for cheats
cheats = {}
for p in path:
    r = p[0]
    c = p[1]
    if c - 2 >= 0 and grid[r, c-1] == WALL \
        and grid[r, c-2] > grid[r,c]:
        cheats[(r, c, r, c-2)] = grid[r, c-2] - grid[r, c] - 2
    if c + 2 < cols and grid[r, c+1] == WALL \
        and grid[r, c+2] > grid[r,c]:
        cheats[(r, c, r, c+2)] = grid[r, c+2] - grid[r, c] - 2
    if r - 2 >= 0 and grid[r-1, c] == WALL \
        and grid[r-2, c] > grid[r,c]:
        cheats[(r, c, r-2, c)] = grid[r-2, c] - grid[r, c] - 2
    if r + 2 < rows and grid[r+1, c] == WALL \
        and grid[r+2, c] > grid[r,c]:
        cheats[(r, c, r+2, c)] = grid[r+2, c] - grid[r, c] - 2


total = 0
for c in cheats.keys():
    if cheats[c] >= 100:
        total += 1
print(total)

# p2

# for debugging
def display_grid2(cheat):
    for r in range(rows):
        for c in range(cols):
            # display cheat
            if (cheat[0] <= r <= cheat[2] or cheat[2] <= r <= cheat[0]) \
                and (cheat[1] <= c <= cheat[3]  or cheat[3] <= c <= cheat[1]) \
                    and (r == cheat[2] or c == cheat[1]):
                print('CC', end='')
            else:
                if grid[r,c] == WALL:
                    print('##', end='')
                elif (r,c) in path:
                    # print('O', end='')
                    if 0 <= grid[r,c] <= 9:
                        print(' ' + str(grid[r,c]), end='')
                    else:
                        print(grid[r,c], end='')
                else:
                    print('..', end='')
        print('')
    print('')


with open('d20.txt', 'r') as f:
    lines = f.read().split('\n')

WALL = -1
PATH = 0
rows = len(lines)
cols = len(lines[0])
grid = np.empty((rows, cols), dtype=int)
for i, L in enumerate(lines):
    for j, c in enumerate(L):
        if c == '#':
            grid[i,j] = WALL
        elif c == 'S':
            grid[i,j] = PATH
            start = (i,j)
        elif c == 'E':
            grid[i,j] = PATH
            end = (i,j)
        else:
            grid[i,j] = PATH

# generate the default path through the grid
path = []
current_cell = start
print(start)
path.append(start)
grid[current_cell] = 0
while current_cell != end:
    r = current_cell[0]
    c = current_cell[1]

    if c - 1 >= 0 and grid[r, c-1] == PATH \
        and (r, c-1) not in path:
        path.append((r, c-1))
    elif c + 1 < cols and grid[r, c+1] == PATH \
        and (r, c+1) not in path:
        path.append((r, c+1))
    elif r - 1 >= 0 and grid[r-1, c] == PATH \
        and (r-1, c) not in path:
        path.append((r-1, c))
    else:
        path.append((r+1, c))
    current_cell = path[-1]
    grid[current_cell] = len(path) - 1

# calculate path length for cheats, organized first by
# start location of cheat then by end location
cheats = {}
for p in path:
    r1 = p[0]
    c1 = p[1]
    for r2 in range(-20, 21):
        for c2 in range(-20 + abs(r2), 21 - abs(r2)):
            if r2 == 0 and c2 == 0:
                continue
            if 0 <= r1 + r2 < rows and 0 <= c1 + c2 < cols \
                and grid[r1+r2, c1+c2] > grid[r1, c1] + abs(r2) + abs(c2):
                cheats[(r1, c1, r1+r2, c1+c2)] = grid[r1+r2, c1+c2] - grid[r1, c1] - abs(r2) - abs(c2)

# total savings from cheats
total = 0
for c in cheats.keys():
    if cheats[c] >= 100:
        # print(c)
        # display_grid2(c)
        total += 1
print(total)

# ref: https://github.com/mathwolf/advent2024/blob/main/day20part2.py