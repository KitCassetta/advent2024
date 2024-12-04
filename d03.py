import re
import math
matches = []
digit_matches = []

# Regex to find all occurrences of mul(digit, digit)
cmd_pattern = r"mul\(\d+,\d+\)"
digit_pattern = r"mul\((\d+),(\d+)\)"

with open("d03.txt", "r") as file:
    for input_string in file:
        # Find all matches in the input string
        matches += re.findall(cmd_pattern, input_string)
        # Process the matches
        print("Matches found:", matches)

        digit_matches += re.findall(digit_pattern, input_string)

        # Convert the extracted strings to integers and process
        int_pairs = [(int(a), int(b)) for a, b in digit_matches]
        print("Extracted integer pairs:", int_pairs)


prods = [math.prod(tup) for tup in int_pairs]
result = sum(prods)
print(f"final sum of products: {result}")

# part two

mul_matches = []
parsed_values = []

with open("d03.txt", "r") as file:
    input_string = file.read().strip().replace("\n","")
    # for input_string in file:
    print(f"input line p2: {input_string}")
    # Step 1: Remove the `don't()...do()` pair
    cleaned_str = re.sub(r"don't\([^)]*\).*?do\([^)]*\)", '', input_string).strip()
    print("Cleaned String s1:", cleaned_str)
    # Step 2: Remove trailing `don't()` and everything after it
    cleaned_str = re.sub(r"don't\([^)]*\).*?$", '', cleaned_str)
    print("Cleaned String s2:", cleaned_str)
    # Step 3: Extract the `mul(digit,digit)` patterns
    mul_matches += re.findall(r"mul\((\d+),(\d+)\)", cleaned_str)
    print("mul() matches:", mul_matches)
    # Convert the extracted pairs into integers
    parsed_values += [(int(a), int(b)) for a, b in mul_matches]
    # Output
    print("Extracted Values:", parsed_values)

prods = [math.prod(tup) for tup in parsed_values]
result = sum(prods)
print(f"final sum of products p2: {result}")