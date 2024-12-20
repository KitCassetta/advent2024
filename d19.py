import math


def get_base6_digit_count(n: int) -> int:
    return math.floor(math.log(n, 6)) + 1


def base6_digit_from_colour(c: str) -> int:
    match c:
        case 'w': return 1
        case 'u': return 2
        case 'b': return 3
        case 'r': return 4
        case 'g': return 5
    raise RuntimeError('Invalid digit')


def colour_from_base6_digit(i: int) -> str:
    match i:
        case 1: return 'w'
        case 2: return 'u'
        case 3: return 'b'
        case 4: return 'r'
        case 5: return 'g'
    raise RuntimeError('Invalid digit')


def base6_str_to_base10_int(s: str) -> int:
    n = 0
    for c in s:
        n *= 6
        n += base6_digit_from_colour(c)
    return n


def base10_int_to_base6_str(i: int) -> str:
    s = ''
    while i > 0:
        d = i % 6
        s = colour_from_base6_digit(d) + s
        i //= 6
    return s


import sys
from functools import cache


@cache
def do_design_is_possible(d: int, m: int, ps: tuple) -> bool:
    dcount = get_base6_digit_count(d)
    mcount = get_base6_digit_count(m)
    if dcount == mcount:
        return d == m

    matches = [
        p * 6**mcount + m
        for p in ps
        if p * 6**mcount + m == d % 6**(mcount + get_base6_digit_count(p))
    ]

    result = False
    for ms in matches:
        result = result or do_design_is_possible(d, ms, ps)
        if result:
            break

    return result


def design_is_possible(d: int, ps: tuple):
    matches = [
        p
        for p in ps
        if d % 6**get_base6_digit_count(p) == p
    ]
    for m in matches:
        if do_design_is_possible(d, m, ps):
            return True
    return False


# if __name__ == '__main__':
#     if len(sys.argv) < 2:
#         print(f'Usage: python3 {sys.argv[0]} <input.txt>')
#         sys.exit(1)
#
#     with open(sys.argv[1]) as f:
#         patterns, designs = f.read().strip().split('\n\n')
#
#     patterns = tuple(i for i in map(base6_str_to_base10_int, patterns.split(', ')))
#     designs = [i for i in map(base6_str_to_base10_int, designs.split('\n'))]
#
#     possible_count = 0
#     for d in designs:
#         if design_is_possible(d, patterns):
#             possible_count += 1
#
#     print(f'Number of possible designs: {possible_count}')

# p2

@cache
def do_design_combination_count(d: int, m: int, ps: tuple) -> bool:
    if d == m:
        return 1

    mcount = get_base6_digit_count(m)

    matches = [
        p * 6**mcount + m
        for p in ps
        if p * 6**mcount + m == d % 6**(mcount + get_base6_digit_count(p))
    ]

    count = 0
    for ms in matches:
        count += do_design_combination_count(d, ms, ps)

    return count


def design_combination_count(d: int, ps: tuple):
    matches = [
        p
        for p in ps
        if d % 6**get_base6_digit_count(p) == p
    ]
    count = 0
    for m in matches:
        count += do_design_combination_count(d, m, ps)
    return count


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: python3 {sys.argv[0]} <input.txt>')
        sys.exit(1)

    with open(sys.argv[1]) as f:
        patterns, designs = f.read().strip().split('\n\n')

    patterns = tuple(i for i in map(base6_str_to_base10_int, patterns.split(', ')))
    designs = [i for i in map(base6_str_to_base10_int, designs.split('\n'))]

    combination_count = 0
    for d in designs:
        combination_count += design_combination_count(d, patterns)

    print(f'Number of possible designs: {combination_count}')

# ref https://github.com/Cdawn99/AoC2024/blob/master/Day19/day19_p2.py