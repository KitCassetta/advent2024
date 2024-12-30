from datetime import time


def parse_data(my_file) -> tuple:
    with open(my_file) as f:
        schematics = f.read().split('\n\n')
        keys = []
        locks = []
        for scheme in schematics:
            pins = [p.count('#') for p in zip(*scheme.split('\n'))]
            if scheme.startswith('#'):
                locks.append(pins)
            else:
                keys.append(pins)
        return locks, keys

def part1(locks:list, keys:list) -> int:
    return sum(all(sum(pair)<=7 for pair in zip(lock,key)) for lock in locks for key in keys)

data = parse_data('d25.txt')
print('Part 1: ', part1(*data))
