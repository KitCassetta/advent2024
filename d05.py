from logging import DEBUG
from venv import logger

rules_str = []
rules_arr = []
rules = dict()
manuals = []
from log_util import get_logger

logger = get_logger(__name__, DEBUG)

with open("d05.txt", "r") as file:
    for line in file:
        if line == "" or line == "\n":
            continue
        if "|" in line:
            rules_str.append(line.strip())
            rules_arr.append(line.strip().split("|"))
        else:
            manuals.append(line.strip())

logger.debug(rules_arr)
logger.debug(manuals)

for a, b in rules_arr:
    if a in rules.keys():
        rules[a].append(b)
    else:
        rules[a] = [b]

for page in rules:
    rules[page].sort()
logger.debug(rules)


def is_valid(manual: str) -> bool:
    logger.debug(manual)
    pages = manual.split(",")
    for i in range(1, len(pages) - 1):
        f, b = pages[:i], pages[i + 1:]
        if pages[i] in rules.keys():
            for j in rules[pages[i]]:
                if j in f:
                    logger.warning(f"Problem child {j} of {pages}")
                    return False
    return True


# Function to get the middle value
def get_middle(array):
    middle_index = len(array) // 2
    return array[middle_index]


r1_pass = []
r1_fail = []
for manual in manuals:
    if is_valid(manual):
        pages = manual.split(",")
        r1_pass.append(pages)
    else:
        r1_fail.append(pages)

logger.info(f"p1 valid manuals: {len(r1_pass)}")

middle_values = [get_middle(array) for array in r1_pass if array]  # Check for non-empty arrays
logger.debug(middle_values)
logger.info(f"p1 answer: {sum(int(n) for n in middle_values)}")

# part 2

### community answer:
import re
from graphlib import TopologicalSorter

with open("d05.txt", "r") as f:
    rules: list[str] = []
    updates: list[str] = []

    flag: bool = False
    for x in f.readlines():
        line = x.strip()
        if not len(line):
            flag = True
        else:
            if flag:
                updates.append(line)
            else:
                rules.append(line)

# Collect all rules as a giant raw graph (looks like it may contain cycles)
graph_raw: dict[int, set[int]] = dict()
pattern_full = re.compile(r"\d+\|\d+")
pattern_num = re.compile(r"\d+")
for rule in rules:
    assert re.fullmatch(pattern_full, rule)
    pred, node = (int(x) for x in re.findall(pattern_num, rule))
    if node not in graph_raw:
        graph_raw[node] = set()
    graph_raw[node].add(pred)

valid_mids: list[int] = []
fixed_mids: list[int] = []
pattern_update = re.compile(r"\d+(,\d+)+")
for update in updates:
    assert re.fullmatch(pattern_update, update)
    pages: list[int] = [int(x) for x in re.findall(pattern_num, update)]

    # Prepare sub_graph of rules pertaining to pages in this update
    sub_graph: dict[int, set[int]] = dict()
    pages_set = set(pages)
    for x in pages_set:
        sub_graph[x] = graph_raw[x].intersection(pages_set)

    # Check that the sub_graph is a DAG and get the order
    ts = TopologicalSorter(sub_graph)
    order = list(ts.static_order())

    if order == pages:
        valid_mids.append(pages[len(pages) // 2])
    else:
        fixed_mids.append(order[len(pages) // 2])

print(sum(valid_mids))
print(sum(fixed_mids))
