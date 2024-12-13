import re
from pprint import pprint
from heapq import heappush, heappop


BUTTON_PATTERN = re.compile(r"Button [A,B]: X\+(\d+), Y\+(\d+)")
PRIZE_PATTERN = re.compile(r"Prize: X=(\d+), Y=(\d+)")
BUTTON_A_PRICE = 3
BUTTON_B_PRICE = 1
INPUT_FILE = "input.txt"


def read_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
        machines = []

        # get four lines at a time
        for i in range(0, len(lines), 4):
            (button_a_x, button_a_y) = BUTTON_PATTERN.match(lines[i]).groups()
            (button_b_x, button_b_y) = BUTTON_PATTERN.match(lines[i + 1]).groups()
            (prize_x, prize_y) = PRIZE_PATTERN.match(lines[i + 2]).groups()
            machines.append(
                {
                    "button_a": (int(button_a_x), int(button_a_y)),
                    "button_b": (int(button_b_x), int(button_b_y)),
                    "prize": (int(prize_x), int(prize_y)),
                }
            )

    return machines


def find_paths(target, move1, cost1, move2, cost2):
    target_x, target_y = target
    start = (0, 0)
    queue = [(0, start, [])]
    valid_paths = []
    visited = set()

    while len(queue) > 0:
        total_cost, (cur_x, cur_y), path = queue.pop()

        if (cur_x, cur_y) in visited:
            continue
        visited.add((cur_x, cur_y))

        if (cur_x, cur_y) == (target_x, target_y):
            valid_paths.append((total_cost, path))
            continue

        if cur_x > target_x or cur_y > target_y:
            continue

        for (dx, dy), cost in [(move1, cost1), (move2, cost2)]:
            new_x = cur_x + dx
            new_y = cur_y + dy
            if new_x <= target_x and new_y <= target_y:
                queue.append((total_cost + cost, (new_x, new_y), path + [(dx, dy)]))

    return valid_paths


machines = read_file(INPUT_FILE)

token_count = 0

for machine in machines:
    paths = find_paths(
        machine["prize"],
        machine["button_a"],
        BUTTON_A_PRICE,
        machine["button_b"],
        BUTTON_B_PRICE,
    )
    if len(paths) > 0:
        token_count += paths[0][0]

print(token_count)
