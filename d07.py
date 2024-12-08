from logging import DEBUG
from itertools import product
from tqdm import tqdm

from log_util import get_logger

logger = get_logger(__name__, DEBUG)
# Check the current logging level
current_level = logger.getEffectiveLevel()

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
}  # answer should be 3749 p2 should be 11387


def parse_line(line):
    """Parse a single line of input into the test value and numbers."""
    test_value, numbers = line.split(":")
    return int(test_value), list(map(int, numbers.split()))


def concatenate(a, b):
    """Concatenate two numbers as digits."""
    return int(str(a) + str(b))


def evaluate_expression(numbers, operators, test_value):
    """Evaluate the expression with left-to-right evaluation, including concatenation."""
    result = numbers[0]
    for i, op in enumerate(operators):
        if op == "+":
            result += numbers[i + 1]
        elif op == "*":
            result *= numbers[i + 1]
        elif op == "||":
            result = concatenate(result, numbers[i + 1])
        if result > test_value:
            return result
    return result


def is_valid_equation(test_value, numbers):
    """Check if the test value can be produced using +, *, and ||."""
    n = len(numbers)
    if n < 2:
        return False

    # Generate all combinations of operators
    for operators in product("+-*", repeat=n - 1):
        if evaluate_expression(numbers, operators, test_value) == test_value:
            return True

    # Generate all combinations including concatenation
    # for operators in product("+-*||", repeat=n - 1):
    #     if evaluate_expression(numbers, operators) == test_value:
    #         return True

    return False


def calculate_calibration_sum(data):
    """Calculate the total sum of valid test values."""
    total = 0
    for line in tqdm(data.strip().split("\n")):
        test_value, numbers = parse_line(line)
        if is_valid_equation(test_value, numbers):
            total += test_value
    return total


# Example input
test_data = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

# Compute calibration sum
result = calculate_calibration_sum(test_data)
logger.info(f"Calibration Sum: {result}")


with open("d07.txt", "r") as file:
    data = file.read().strip()

result = calculate_calibration_sum(data)
logger.info(f"Calibration Sum: {result}")  # correct answer 1430271835320


# pt 2  ref: Critical_Method_993
def runBL():
    inpt = ''
    ok_results = 0

    with open('d07.txt', 'r') as file:
        inpt = file.readlines()

    for line in tqdm(inpt):
        temp_line = line.replace('\n', '')

        equation = temp_line.split(':')
        expected_res = int(equation[0])
        vals = equation[1].strip().split(' ')
        possible_operator_combos = pow(3, len(vals) - 1)

        for i in range(0, possible_operator_combos):
            ternary_ops = ternary(i, len(vals) - 1)

            temp_res = 0
            # 2 = OR
            for n in range(0, len(vals)):
                if n == 0:
                    if ternary_ops[n] == '0':
                        temp_res += int(vals[n]) + int(vals[n + 1])
                    elif ternary_ops[n] == '1':
                        temp_res += int(vals[n]) * int(vals[n + 1])
                    elif ternary_ops[n] == '2':
                        temp_res = int(str(vals[n]) + str(vals[n + 1]))
                elif n > 0 and n < len(ternary_ops):
                    if ternary_ops[n] == '0':
                        temp_res = temp_res + int(vals[n + 1])
                    elif ternary_ops[n] == '1':
                        temp_res = temp_res * int(vals[n + 1])
                    elif ternary_ops[n] == '2':
                        temp_res = int(str(temp_res) + str(vals[n + 1]))

            if temp_res == expected_res:
                ok_results += temp_res
                break

    print(ok_results)
    return

def ternary(n, length):
    if n == 0:
        return '0'.rjust(length, '0')
    nums = []
    while n:
        n, r = divmod(n, 3)
        nums.append(str(r))
    return ''.join(reversed(nums)).rjust(length, '0')

runBL()  # correct answer 456565678667482