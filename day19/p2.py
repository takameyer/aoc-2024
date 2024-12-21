from pprint import pprint

WHITE = "w"
BLUE = "u"
BLACK = "b"
RED = "r"
GREEN = "g"

INPUT_FILE = "test.txt"

read_file = open(INPUT_FILE, "r")

lines = read_file.readlines()

available_towels = lines[0].strip().split(", ")

designs = []

for line in lines[2:]:
    designs.append(line.strip())


def find_first_pattern(design, start_index=0):
    for i in range(len(design), 0, -1):
        if design[start_index:i] in available_towels:
            return (i, design[start_index:i])
    return (None, None)


def find_last_pattern(design, end_index):
    for i in range(len(design)):
        if design[i:end_index] in available_towels:
            return (i, design[i:end_index])

    return (None, None)


def find_largest_from_start(design, start=0):
    largest_pattern_match = None
    end = 0
    for i in range(1 + start, len(design)):
        sub_string = design[start:i]
        print(sub_string)
        if sub_string in available_towels:
            largest_pattern_match = sub_string
            end = i

    return (largest_pattern_match, end)


results = []
impossible_designs = []


def can_build_pattern(target, patterns):
    def can_build(remaining, memo=None):
        if memo is None:
            memo = {}

        # Base cases
        if not remaining:  # Successfully used all letters
            return True
        if remaining in memo:  # Already tried this combo
            return memo[remaining]

        # Try each pattern at the start of our remaining string
        # We can reuse patterns, so no need to track what we've used
        for pattern in patterns:
            if remaining.startswith(pattern):
                new_remaining = remaining[len(pattern) :]
                if can_build(new_remaining, memo):
                    memo[remaining] = True
                    print(memo)
                    return True

        memo[remaining] = False
        return False

    return can_build(target)


can_build_count = 0

for design in designs:
    if can_build_pattern(design, available_towels):
        can_build_count += 1

print(can_build_count)

quit()

for design in designs:
    patterns = {}
    result = 0
    pattern_found = False
    while True:
        (result, pattern) = find_first_pattern(design, result)
        patterns[pattern] = patterns.get(pattern, 0) + 1
        if not result:
            pattern_found = False
            break
        if design[:result] == design:
            pattern_found = True
            break
    if pattern_found:
        results.append((design, patterns))
    else:
        patterns = {}
        result = len(design)
        pattern_found = False
        while True:
            (result, pattern) = find_last_pattern(design, result)
            patterns[pattern] = patterns.get(pattern, 0) + 1
            if result == None:
                pattern_found = False
                break
            if result == 0:
                pattern_found = True
                break
        if pattern_found:
            results.append((design, patterns))
        else:
            impossible_designs.append(design)
