import numpy as np

# Looking at a collection of stones
# arranged in a stright line, each with a number
# every time a blink occurs, the stones change
# stones will change based on the following rules:
# - 0 is replaced by 1
# - even number of digits, splits in two. Left half of digits on the new left
#    stone, and right half of digits on the right stones
#    - Extra leading zeros are removed, (1000 becomes 10 and 0)
# - else stone is replaced with a new stone with it's number mulipled by 2024

BLINK_COUNT = 75
INPUT_FILE = "input.txt"


def read_file(file_path):
    with open(file_path, "r") as file:
        return list(map(int, file.readline().strip().split()))


def get_digit_count(n):
    return 1 if n == 0 else len(str(n))


def blink(counts_dict):
    new_counts = {}

    for number, count in counts_dict.items():
        if number == 0:
            new_counts[1] = new_counts.get(1, 0) + count
            continue

        length = get_digit_count(number)
        if length % 2 == 0:
            divisor = 10 ** (length // 2)
            first = number // divisor
            second = number % divisor
            new_counts[first] = new_counts.get(first, 0) + count
            new_counts[second] = new_counts.get(second, 0) + count
        else:
            new_num = number * 2024
            new_counts[new_num] = new_counts.get(new_num, 0) + count

    return new_counts


# Convert initial list to counts dictionary
stones = read_file(INPUT_FILE)
counts = {}
for stone in stones:
    counts[stone] = counts.get(stone, 0) + 1

for _ in range(BLINK_COUNT):
    counts = blink(counts)

# Final result is sum of all counts
print(counts)

print(sum(counts.values()))
