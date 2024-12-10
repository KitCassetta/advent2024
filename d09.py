from log_util import get_logger
from timeit import time_it
from timeout import timeout
import re

logger = get_logger(__name__)

"""
# test data
2333133121414131402

# step 1 convert to individual blocks:
00...111...2...333.44.5555.6666.777.888899

# step 2 'compress':
00...111...2...333.44.5555.6666.777.888899
009..111...2...333.44.5555.6666.777.88889.
0099.111...2...333.44.5555.6666.777.8888..
00998111...2...333.44.5555.6666.777.888...
009981118..2...333.44.5555.6666.777.88....
0099811188.2...333.44.5555.6666.777.8.....
009981118882...333.44.5555.6666.777.......
0099811188827..333.44.5555.6666.77........
00998111888277.333.44.5555.6666.7.........
009981118882777333.44.5555.6666...........
009981118882777333644.5555.666............
00998111888277733364465555.66.............
0099811188827773336446555566..............

step 3 update checksum by multiplying position by value then summing
the first few blocks' position multiplied by its file ID number are 
0 * 0 = 0, 1 * 0 = 0, 2 * 9 = 18, 3 * 9 = 27, 4 * 8 = 32, and so on...
In this example, the checksum is the sum of these, 1928.
"""

@time_it
@timeout(30)
def convert_to_blocks(text) -> str:
    """
    Test data
    2333133121414131402

    Step 1 convert to individual blocks:
    00...111...2...333.44.5555.6666.777.888899
    :param str:
    :return:
    """
    bytes = []
    block = ""
    while len(text) >= 2:
        bytes.append(text[:2])
        text = text[2:]
    if text:
        bytes.append(text)
    logger.debug(bytes)
    for i in range(len(bytes)):
        if len(bytes[i]) == 2:
            block += str(i) * int(bytes[i][0])
            block += "." * int(bytes[i][-1])
        else:
            block += str(i) * int(bytes[i][0])
        logger.debug(block)
    return block


@time_it
@timeout(180)
def compress_blocks(text) -> str:
    """
    Step 2 'compress':
    00...111...2...333.44.5555.6666.777.888899
    009..111...2...333.44.5555.6666.777.88889.
    0099.111...2...333.44.5555.6666.777.8888..
    00998111...2...333.44.5555.6666.777.888...
    009981118..2...333.44.5555.6666.777.88....
    0099811188.2...333.44.5555.6666.777.8.....
    009981118882...333.44.5555.6666.777.......
    0099811188827..333.44.5555.6666.77........
    00998111888277.333.44.5555.6666.7.........
    009981118882777333.44.5555.6666...........
    009981118882777333644.5555.666............
    00998111888277733364465555.66.............
    0099811188827773336446555566..............
    :param text:
    :return:
    """
    # The dot between gigit regex pattern
    dot_pattern = r'\d\.\d'
    while re.search(dot_pattern, text):
        logger.debug(text)
        text = swap_last_digit_with_dot(text)
    logger.info(f"Compressed: {text}")
    return text


def swap_last_digit_with_dot(text: str) -> str:
    """
    using list to move
    :param text:
    :return:
    """
    # Find the last digit using regex
    match = re.search(r'\d(?!.*\d)', text)  # Match the last digit in the string
    if match:
        last_digit_index = match.start()
        # Find the index of the first "."
        dot_index = text.find('.')
        if dot_index != -1:  # Ensure there's a dot to swap with
            # Convert string to list for easy swapping
            s_list = list(text)
            # Swap the last digit with the "."
            s_list[dot_index], s_list[last_digit_index] = s_list[last_digit_index], s_list[dot_index]
            return ''.join(s_list)
    return text  # Return the original string if no digit or dot is found


# def swap_last_digit_with_dot(s: str) -> str:
#     """
#     using slicing to move
#     :param s:
#     :return:
#     """
#     # Use regex to find the last digit and the first '.'
#     dot_index = s.find('.')
#     if dot_index == -1:  # If no dot is found, return the string unchanged
#         logger.warning("No dot found")
#         return s
#
#     # Find the last digit by scanning the string in reverse
#     for i in range(len(s) - 1, -1, -1):
#         if s[i].isdigit():
#             # Perform the swap in-place using slicing
#             s = s[:dot_index] + s[i] + s[dot_index + 1:i] + '.' + s[i + 1:]
#             break
#
#     return s


def update_checksum(text) -> int:
    """
    Step 3 update checksum by multiplying position by value then summing
    the position multiplied by its file ID number.
    "0099811188827773336446555566.............."
    0 * 0 = 0, 1 * 0 = 0, 2 * 9 = 18, 3 * 9 = 27, 4 * 8 = 32, and so on...
    In this example, the checksum is the sum of these, 1928.
    :param text:
    :return:
    """
    checksum = 0
    for i in range(len(text)):
        if text[i] == ".":
            break
        else:
            checksum += i * int(text[i])

    return checksum


with open("d09_t.txt", "r") as test:
    t_data = test.read().strip().rstrip()
logger.debug(len(t_data))
logger.debug(t_data)

block = convert_to_blocks(t_data)
compress = compress_blocks(block)
checksum = update_checksum(compress)
logger.info(f"The checksum is: {checksum}")

# logger.setLevel(20)
# with open("d09.txt", "r") as test:
#     data = test.read().strip().rstrip()
# block = convert_to_blocks(data)
# compress = compress_blocks(block)
# checksum = update_checksum(compress)
# logger.info(f"The checksum is: {checksum}")

# ref: RiemannIntegirl
import numpy as np

blocks = np.array([int(z) for z in open('d09.txt').read()])
locs = np.cumsum(blocks)
locs = np.insert(locs,0,0)

mem = np.array([-1] * np.sum(blocks))
for ind in range(0,len(locs),2):
    val = ind//2
    for l in range(locs[ind], locs[ind + 1]):
        mem[l] = val
spaces = np.nonzero(mem == -1)[0]
vals = np.flip(np.nonzero(mem != -1)[0][-len(spaces):])
mem[spaces] = mem[vals]

logger.info(f"The checksum is: {np.sum(mem[:-len(spaces)] * np.arange(0,len(mem) - len(spaces)))}")

# p2

blocks = np.array([int(z) for z in open('d09.txt').read()])

locs = np.cumsum(blocks)  # get the starting address of each block
locs = np.insert(locs, 0, 0)

spaces = [np.arange(locs[i], locs[i + 1]) for i in range(1, len(locs) - 1, 2)]  # addresses of spaces
space_lens = blocks[1::2]  # lengths of empty memory chunks left

files = [np.arange(locs[i], locs[i + 1]) for i in
         range(len(locs) - 2, 0, -2)]  # addresses of files starting from the right
file_lens = [len(f) for f in files]  # file lengths

mem = np.zeros(np.sum(blocks), dtype=np.int16)  # initialize memory
for ind in range(0, len(locs), 2):
    val = ind // 2
    for l in range(locs[ind], locs[ind + 1]):
        mem[l] = val

file_num, space_num = len(files), len(spaces)

for j in range(file_num):  # loop through the files
    valids = [i for i in range(space_num) if
              file_lens[j] <= space_lens[i] and spaces[i][-1] < files[j][0]]  # get the leftmost valid space
    if len(valids) > 0:  # if such a space exists
        space = min(valids)  # get the leftmost one
        spaces_put = spaces[space][:file_lens[j]]  # only select the needed sub-portion of space
        spaces[space] = spaces[space][file_lens[j]:]  # update free space left
        space_lens[space] -= file_lens[j]  # update the length of this chunk of space
        mem[spaces_put] = mem[files[j]]  # copy the file
        mem[files[j]] = 0  # delete the file

logger.info(f"part 2 {np.sum(mem * np.arange(0, len(mem)))}")