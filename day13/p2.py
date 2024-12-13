import re


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
                    "prize": (
                        10000000000000 + int(prize_x),
                        10000000000000 + int(prize_y),
                    ),
                }
            )

    return machines


machines = read_file(INPUT_FILE)

token_cost = 0

for machine in machines:

    x1, y1 = machine["button_a"]
    x2, y2 = machine["button_b"]
    tx, ty = machine["prize"]

    a = (tx * y2 - x2 * ty) / (y2 * x1 - x2 * y1)
    b = (ty * x1 - tx * y1) / (y2 * x1 - x2 * y1)

    if a.is_integer() and b.is_integer():
        token_cost += a * 3 + b

print(int(token_cost))
