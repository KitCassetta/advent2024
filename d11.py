from typing import List
from log_util import get_logger
from timeit import time_it
from timeout import timeout
from tqdm import tqdm
import math

logger = get_logger(__name__)

with open("d11_t.txt", "r") as test:
    t_data = [line.strip().split(" ") for line in test]
    t_data = t_data.pop()

with open("d11.txt", "r") as file:
    data = [line.strip().split(" ") for line in file]
    data = data.pop()


logger.debug(f"test data: {t_data}")
logger.info(f"data: {data}")


def split_array(arr: List[str]) -> (List[str], List[str]):
    """Splits an even-length array into two equal halves.

    Args:
    arr: The input array.

    Returns:
    A tuple of two subarrays.
    """

    mid = len(arr) // 2
    return arr[:mid], arr[mid:]


def rules_check(stones: List[str]) -> List[str]:
    """
    As you observe them for a while, you find that the stones have a consistent behavior. Every time you blink,
    the stones each simultaneously change according to the first applicable rule in this list:

    If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
    If the stone is engraved with a number that has an even number of digits, it is replaced by two stones. The left half
    of the digits are engraved on the new left stone, and the right half of the digits are engraved on the new right
    stone. (The new numbers don"t keep extra leading zeroes: 1000 would become stones 10 and 0.)
    If none of the other rules apply, the stone is replaced by a new stone; the old stone"s number multiplied by 2024 is
    engraved on the new stone.
    """
    result = []
    for stone in stones:
        logger.debug(f"stone: {stone}")
        if stone == "0":
            stone = "1"
            result.append(stone)
            continue
        elif len(stone) % 2 == 0:
            f, b = split_array(stone)
            f = str(int(f))  # remove leading zeros
            b = str(int(b))  # remove leading zeros
            result.append(f)
            result.append(b)
            continue
        else:
            stone = str(int(stone) * 2024)
            result.append(stone)
    logger.debug(f"rules check result: {result}")
    return result


@timeout(180)
@time_it
def blink(data: List[str], blinks: int) -> List[str]:
    """
    Initial arrangement:
    125 17

    After 1 blink:
    253000 1 7

    After 2 blinks:
    253 0 2024 14168

    After 3 blinks:
    512072 1 20 24 28676032

    After 4 blinks:
    512 72 2024 2 0 2 4 2867 6032

    After 5 blinks:
    1036288 7 2 20 24 4048 1 4048 8096 28 67 60 32

    After 6 blinks:
    2097446912 14168 4048 2 0 2 4 40 48 2024 40 48 80 96 2 8 6 7 6 0 3 2
    :param data: list of str numbers, ex: ["125", "17"]
    :param blinks: n blinks to process ex: 6
    :return: the result of running each item through the rules as writen for n blinks,
     ex: 2097446912 14168 4048 2 0 2 4 40 48 2024 40 48 80 96 2 8 6 7 6 0 3 2
    """
    n = 0
    pbar = tqdm(desc="Blinking & thinking", total=blinks)
    while n < blinks:
        data = rules_check(data)
        n += 1
        pbar.update(n)
    pbar.close()
    return data


rules_check(t_data)  # Expected result = 1 2024 1 0 9 9 2021976
logger.setLevel(20)
# second test
t2_data = ["125", "17"]
result = blink(t2_data, 6)
logger.info(f"Result after blinks we have {len(result)} stones")

result = blink(data, 25)
logger.info(f"Result after blinks we have {len(result)} stones")

# result = blink(data, 75) # brute force to slow and memory intensive
# logger.info(f"Result after blinks we have {len(result)} stones")

def calc(mem, stone, blink):
    if blink == 0:
        return 1

    if stone in mem[blink]:
        return mem[blink][stone]
    if stone == 0:
        mem[blink][stone]=calc(mem, 1, blink - 1)
    elif (int(math.log10(stone))+1)%2==0:
        s = str(stone)
        mem[blink][stone] = calc(mem, int(s[:len(s) // 2]), blink - 1) + calc(mem, int(s[len(s) // 2:]), blink - 1)
    else:
        mem[blink][stone]=calc(mem, stone * 2024, blink - 1)
    return mem[blink][stone]

blinks = 76

mem = [{} for i in range(blinks)]

for i in tqdm(range(blinks)):
    print(sum([calc(mem,int(x),i) for x in data]))
