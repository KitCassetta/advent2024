from collections import defaultdict
from enum import verify
from logging import Logger

from log_util import get_logger

logger = get_logger(__name__)

known = defaultdict()
formulas = defaultdict()
operators = {
    "OR": lambda x, y: x | y,
    "XOR": lambda x, y: x ^ y,
    "AND": lambda x, y: x & y
}

with open("d24.txt", "r") as file:
    for line in file:
        if line.isspace(): break
        key, value = line.strip().split(': ')
        known[key] = int(value.strip())
    for line in file:
        x, op, y, junk, key = line.strip().split(" ")
        formulas[key] = [op, x, y]

logger.debug(known)
logger.debug(formulas)


def calc(wire):
    if wire in known: return known[wire]
    op, x, y = formulas[wire]
    known[wire] = operators[op](calc(x),calc(y))
    return known[wire]

z = []
i = 0

while True:
    key = "z" + str(i).rjust(2,"0")
    if key not in formulas: break
    z.append(calc(key))
    i += 1

res = int("".join([str(i) for i in z[::-1]]), 2)

logger.info(f"Part 1: {res}")

# pt2 focus on the formulas
# this requires binary mathmatics shout out to ref: https://www.youtube.com/watch?v=SU6lp6wyd3I&t=359s
# lets visualize
"""
 c   111
 x   1101 
 y + 0111
 z  10100
    from the right if x and y = 0, z = 0, if x or y = 1
"""


def pp(wire, depth=0):
    if wire[0] in "xy" and wire[1:].isdigit(): return "  " * depth + wire
    op, x ,y = formulas[wire]
    return "  " * depth + op + " (" + wire + ")\n" + pp(x, depth + 1) + "\n" + pp(y, depth + 1)

# logger.debug(pp("z00"))
# logger.debug(pp("z01"))

# we have to figure out how to follow the structure

def make_wire(char, num):
    return char + str(num).rjust(2, "0")


def verify_intermediate_xor(wire, num) -> bool:
    logger.debug(f"verify xor, {wire}, {num}")
    if wire not in formulas: return False
    op, x, y = formulas[wire]
    if op != "XOR": return False
    return sorted([x, y]) == [make_wire("x", num), make_wire("y", num)]


def verify_direct_carry(wire, num):
    logger.debug(f"verify direct carry bit, {wire}, {num}")
    if wire not in formulas: return False
    op, x, y = formulas[wire]
    if op != "AND": return False
    return sorted([x, y]) == [make_wire("x", num), make_wire("y", num)]


def verify_recarry(wire, num):
    logger.debug(f"verify re-carry bit, {wire}, {num}")
    if wire not in formulas: return False
    op, x, y = formulas[wire]
    if op != "AND": return False
    return (verify_intermediate_xor(x, num) and verify_carry_bit(y, num)
            or verify_intermediate_xor(y, num) and verify_carry_bit(x, num))


def verify_carry_bit(wire, num):
    logger.debug(f"verify carry bit, {wire}, {num}")
    op, x, y = formulas[wire]
    if num == 1:
        # return op == "AND" and sorted([x, y]) == ["x00", "y00"]  # left the other way for consistency
        if op != "AND": return False
        return sorted([x, y]) == ["x00", "y00"]  # the first carry bit is the and of the first two bits
    if op != "OR": return False
    return (verify_direct_carry(x, num - 1) and verify_recarry(y, num - 1)
            or verify_direct_carry(y, num - 1) and verify_recarry(x, num - 1))

def verify_z(wire, num):
    """
    :param wire: expected
    :param num: which bit are we at
    :return:
    """
    logger.debug(f"verify z, {wire}, {num}")
    op, x, y = formulas[wire]
    if wire not in formulas: return False
    if op != "XOR": return False
    if num == 0 : return sorted([x,y]) == ["x00", "y00"]
    # intermediate check is easier to check and fail so place it first to avoid deep recursion for no reason.
    return (verify_intermediate_xor(x, num) and verify_carry_bit(y, num)
            or verify_intermediate_xor(y, num) and verify_carry_bit(x, num))

def verify(num):
    return verify_z(make_wire("z", num), num)

logger.debug(f"Part 2 test: {verify(0)}")  # should be true
logger.debug(f"Part 2 test: {verify(1)}")  # should be true
logger.debug(f"Part 2 test: {verify(2)}")  # should be true

# brute force find a break
def progress():
    i = 0
    while True:
        if not verify(i): break
        i += 1
    return i

swaps = []
for i in range (4):
    baseline = progress()
    for x in formulas:
        for y in formulas:
            if x == y: continue
            formulas[x], formulas[y] = formulas[y], formulas[x]
            if progress() > baseline:
                break
            formulas[x], formulas[y] = formulas[y], formulas[x]
        else:
            continue
        break
    swaps += [x, y]

logger.info(",".join(sorted(swaps)))