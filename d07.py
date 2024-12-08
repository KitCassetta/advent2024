from logging import DEBUG, INFO

from numpy.random.mtrand import operator

from log_util import get_logger

logger = get_logger(__name__, DEBUG)
# Check the current logging level
current_level = logger.getEffectiveLevel()
logger.debug(current_level)

ops = ("add", "mul")

test_data = {
    190: [10, 19],
    3267: [81, 40, 27],
    83: [17, 5],
    156: [15, 6],
    7290: [6, 8, 6, 15],
    161011: [16, 10, 13],
    192: [17, 8, 14],
    21037: [9, 7, 18, 13],
    292: [11, 6, 16, 20]
}

# operations 2 (+ , *)
# C(n, k) = n! / (k!(n-k)!) equation
# C(4, 2) = 4! / (2! * 2!) = 6 possible pairs
# Total combinations = Number of pairs * Number of operations per pair = 6 * 2 = 12

data = dict()
with open("d07.txt", "r") as file:
    for line in file:
        k, v = line.strip().split(":")
        v = [int(i) for i in v.strip().split(" ")]
        data[int(k)] = v

logger.debug(test_data)
logger.debug(test_data.keys())

# Set the logging level to DEBUG
logger.setLevel(INFO)
logger.debug(data)


