import csv

# The levels are either all increasing or all decreasing.
# Any two adjacent levels differ by at least one and at most three.

safe = 0
data = []
unsafe = []

def validate_differences(arr):
    """Check if differences between adjacent levels are between 1 and 3."""
    return all(1 <= abs(arr[i] - arr[i + 1]) <= 3 for i in range(len(arr) - 1))

def is_strictly_increasing(arr):
    """Check if the array is strictly increasing."""
    return all(arr[i] > arr[i - 1] for i in range(1, len(arr)))

def is_strictly_decreasing(arr):
    """Check if the array is strictly decreasing."""
    return all(arr[i] < arr[i - 1] for i in range(1, len(arr)))

def is_safe(arr):
    """Check if the array satisfies the safety rules."""
    if len(arr) < 2:  # Single-level or empty arrays are trivially safe
        return True

    # Check if the array is strictly monotonic
    if not (is_strictly_increasing(arr) or is_strictly_decreasing(arr)):
        return False

    # Validate the differences
    return validate_differences(arr)

def can_dampen(arr):
    """Check if removing one level can make the array strictly monotonic and safe."""
    for i in range(len(arr)):
        adjusted_array = arr[:i] + arr[i + 1:]  # Remove the level at index i
        if is_safe(adjusted_array):
            return True  # Safe after adjustment
    return False  # Unsafe even after adjustment attempts

# Test Cases
print("Test Cases:")
print(can_dampen([1, 3, 2, 4, 5]))  # Expected: True (remove 3 -> [1, 2, 4, 5])
print(can_dampen([1, 2, 2, 4, 5]))  # Expected: True (remove 2 -> [1, 2, 4, 5])
print(can_dampen([1, 2, 3, 2, 1]))  # Expected: True (remove 3 -> [1, 2, 2, 1])
print(can_dampen([10, 20, 30, 40]))  # Expected: False (already safe, no changes needed)
print(can_dampen([22, 25, 28, 31, 32, 36]))  # Expected: True (remove 36 -> [22, 25, 28, 31, 32])


with open("d02.txt", "r") as file:
    csv_reader = csv.reader(file, delimiter=' ')  # Use space as the delimiter
    for row in csv_reader:
        int_array = [int(value) for value in row]  # Convert each value to an integer
        data.append(int_array)

print(data)

for row in data:
    if is_safe(row):
        safe += 1
    else:
        unsafe.append(row)
print(safe)

# part 2 dampener, system can tolerate one bad level change
# Now, the same rules apply as before,
# except if removing a single level from an unsafe report would make it safe,
# the report instead counts as safe.
# ex: 1 3 2 4 5 can be made safe by removing the second level; 3.
print(unsafe)
dampened = 0
for row in unsafe:
    if can_dampen(row):
        dampened += 1
print(dampened)

print(f"total safe = {safe + dampened}")
print("fin")