from functools import cache

with open('d21.txt', 'r') as file:
    codes = file.read().splitlines()

# Coords are such that (0,0) is the empty space on both
keypad = {
    '7' : (0,-3), '8' : (1,-3), '9' : (2,-3),
    '4' : (0,-2), '5' : (1,-2), '6' : (2,-2),
    '1' : (0,-1), '2' : (1,-1), '3' : (2,-1),
                  '0' : (1, 0), 'A' : (2, 0)
    }

dpad = {
                  '^' : (1, 0), 'A' : (2, 0),
    '<' : (0, 1), 'v' : (1, 1), '>' : (2, 1)
    }

def vectorDif(v1,v2):
    return (v1[0]-v2[0], v1[1]-v2[1])

@cache
def calcLength(target, cur_pos, max_depth):
    target_pos, num_presses = target
    if max_depth == 0:
        return num_presses
    length = 0
    xdif, ydif = vectorDif(cur_pos, target_pos)
    if xdif < 0:
        xmov = (dpad['>'], -xdif)
    else:
        xmov = (dpad['<'],  xdif)
    if ydif < 0:
        ymov = (dpad['v'], -ydif)
    else:
        ymov = (dpad['^'],  ydif)
    endmov = (dpad['A'], num_presses)

    if xdif == 0:
        length += calcLength(  ymov, dpad['A'], max_depth-1)
        length += calcLength(endmov,   ymov[0], max_depth-1)
    elif ydif == 0:
        length += calcLength(  xmov, dpad['A'], max_depth-1)
        length += calcLength(endmov,   xmov[0], max_depth-1)
    elif cur_pos[1] == 0 and target_pos[0] == 0:
        # Avoiding (0,0) is the highst priority
        length += calcLength(  ymov, dpad['A'], max_depth-1)
        length += calcLength(  xmov,   ymov[0], max_depth-1)
        length += calcLength(endmov,   xmov[0], max_depth-1)
    elif (cur_pos[0] == 0 and target_pos[1] == 0) or xdif > 0:
        # '<' is the furthest from 'A', and itself takes two '<' pushes to reach
        # Move to it first when possible to avoid splitting the two '<'
        length += calcLength(  xmov, dpad['A'], max_depth-1)
        length += calcLength(  ymov,   xmov[0], max_depth-1)
        length += calcLength(endmov,   ymov[0], max_depth-1)
    else:
        length += calcLength(  ymov, dpad['A'], max_depth-1)
        length += calcLength(  xmov,   ymov[0], max_depth-1)
        length += calcLength(endmov,   xmov[0], max_depth-1)
    return length

complexity1 = 0
complexity2 = 0
for code in codes:
    length1 = 0
    length2 = 0
    for i in range(len(code)):
        length1 += calcLength((keypad[code[i]],1), keypad[code[i-1]], 3)
        length2 += calcLength((keypad[code[i]],1), keypad[code[i-1]], 26)
    complexity1 += int(code[:-1]) * length1
    complexity2 += int(code[:-1]) * length2

print(complexity1)
print(complexity2)
# ref https://github.com/manucordova/adventofcode/blob/main/aoc_python/2024/day_21/solution.py#L170