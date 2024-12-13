import re


def main():
    machines = getMachines()
    result = solveMachines(machines)
    print(result)


# Returns a list of sets with each list representing one machine's properties
def getMachines():
    machines = []

    # Regex pattern to extract X and Y button values from input
    button_pattern = r'X([+-]?\d+), Y([+-]?\d+)'

    # Regex pattern to extract X and Y values for the Prize
    prize_pattern = r'X=([+-]?\d+), Y=([+-]?\d+)'

    with open('d13.txt', 'r') as file:
        input_lines = file.read().splitlines()
        for i in range(0, len(input_lines), 4):
            match_a = re.search(button_pattern, input_lines[i])
            match_b = re.search(button_pattern, input_lines[i + 1])
            match_prize = re.search(prize_pattern, input_lines[i + 2])

            button_a = (int(match_a.group(1)), int(match_a.group(2)))
            button_b = (int(match_b.group(1)), int(match_b.group(2)))
            prize = (int(match_prize.group(1)), int(match_prize.group(2)))

            machines.append([button_a, button_b, prize])
        return machines


def solveMachines(machines):
    total_cost = 0
    for machine in machines:
        min_cost = 0
        a_x, a_y = machine[0][0], machine[0][1]
        b_x, b_y = machine[1][0], machine[1][1]
        prize_x, prize_y = machine[2][0], machine[2][1]

        for a in range(1, 100):
            for b in range(1, 100):
                if (a_x * a) + (b_x * b) == prize_x and (a_y * a) + (b_y * b) == prize_y:
                    cost = (3 * a) + (b)
                    if min_cost == 0:
                        min_cost = cost
                    elif cost < min_cost:
                        min_cost = cost
        if min_cost > 0:
            total_cost += min_cost

    return total_cost


main()

# pt 2
import re


def main2():
    machines = getMachines2()
    result = solveMachines2(machines)
    print(result)


# Returns a list of sets with each list representing one machine's properties
def getMachines2():
    machines = []

    # Regex pattern to extract X and Y button values from input
    button_pattern = r'X([+-]?\d+), Y([+-]?\d+)'

    # Regex pattern to extract X and Y values for the Prize
    prize_pattern = r'X=([+-]?\d+), Y=([+-]?\d+)'

    with open('d13.txt', 'r') as file:
        input_lines = file.read().splitlines()
        for i in range(0, len(input_lines), 4):
            match_a = re.search(button_pattern, input_lines[i])
            match_b = re.search(button_pattern, input_lines[i + 1])
            match_prize = re.search(prize_pattern, input_lines[i + 2])

            button_a = (int(match_a.group(1)), int(match_a.group(2)))
            button_b = (int(match_b.group(1)), int(match_b.group(2)))
            prize = (int(match_prize.group(1)), int(match_prize.group(2)))

            machines.append([button_a, button_b, prize])
        return machines


def solveMachines2(machines):
    total_cost = 0
    for machine in machines:
        a_x, a_y = machine[0][0], machine[0][1]
        b_x, b_y = machine[1][0], machine[1][1]
        prize_x, prize_y = machine[2][0], machine[2][1]

        prize_x += 10000000000000
        prize_y += 10000000000000

        # solve using elimination
        a = round((prize_y - ((b_y * prize_x) / b_x)) / (a_y - ((b_y * a_x) / b_x)))
        b = round((prize_x - a_x * a) / b_x)

        # ensure solution is valid before calculating cost
        if (a_x * a) + (b_x * b) == prize_x and (a_y * a) + (b_y * b) == prize_y:
            total_cost += a * 3 + b

    return total_cost


main2()