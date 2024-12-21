KEYPAD = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], [None, 0, "A"]]
DIRECTIONAL_KEYPAD = [[None, "^", "A"], ["<", "v", ">"]]

DIRECTIONS = {
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1),
}

KEYPAD_START = (3, 2)
DIRECTIONAL_KEYPAD_START = (0, 2)

INPUT_FILE = "test.txt"


def get_inputs():
    inputs = []
    with open(INPUT_FILE, "r") as f:
        for line in f:
            inputs.append(list(line.strip()))

    return inputs


inputs = get_inputs()

for input in inputs:
    get_button_sequence(input, KEYPAD, KEYPAD_START)


def get_button_sequence_keypad(input):
    current_pos = KEYPAD_START
