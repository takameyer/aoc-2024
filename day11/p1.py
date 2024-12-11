# Looking at a collection of stones
# arranged in a stright line, each with a number
# every time a blink occurs, the stones change
# stones will change based on the following rules:
# - 0 is replaced by 1
# - even number of digits, splits in two. Left half of digits on the new left
#    stone, and right half of digits on the right stones
#    - Extra leading zeros are removed, (1000 becomes 10 and 0)
# - else stone is replaced with a new stone with it's number mulipled by 2024

BLINK_COUNT = 25
INPUT_FILE = "input.txt"


def read_file(file_path):
    with open(file_path, "r") as file:
        return list(map(int, file.readline().strip().split()))


def get_digit_count(n):
    if n == 0:
        return 1
    return len(str(n))


def blink(stones):
    new_stones = []
    new_stones_append = new_stones.append
    for stone in stones:
        if stone == 0:
            new_stones_append(1)
            continue

        length = get_digit_count(stone)

        if length % 2 == 0:
            divisor = 10 ** (length // 2)
            new_stones_append(stone // divisor)
            new_stones_append(stone % divisor)
        else:
            new_stones_append(stone * 2024)

    return new_stones


stones = read_file(INPUT_FILE)


for _ in range(BLINK_COUNT):
    stones = blink(stones)


print(len(stones))
