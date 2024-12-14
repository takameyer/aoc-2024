import re
from pprint import pprint
from heapq import heappush, heappop


GUARD_PATTERN = re.compile(r"p=([\d,]+) v=([\d,-]+)")
HEADQUARTERS_WIDTH = 101
HEADQUARTERS_HEIGHT = 103
INPUT_FILE = "input.txt"

EMPTY_SYMBOL = "."


class Headquarters:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[EMPTY_SYMBOL for _ in range(width)] for _ in range(height)]
        self.guards = []

    def add_guard(self, guard):
        self.guards.append(guard)

    def move_guards(self):
        for i in range(len(self.guards)):
            guard_position, guard_velocity = self.guards[i]
            guard_position = (
                guard_position[0] + guard_velocity[0],
                guard_position[1] + guard_velocity[1],
            )
            if guard_position[0] < 0:
                guard_position = (self.width + guard_position[0], guard_position[1])
            if guard_position[1] < 0:
                guard_position = (
                    guard_position[0],
                    self.height + guard_position[1],
                )
            if guard_position[0] > self.width - 1:
                guard_position = (guard_position[0] - self.width, guard_position[1])
            if guard_position[1] > self.height - 1:
                guard_position = (
                    guard_position[0],
                    guard_position[1] - self.height,
                )
            self.guards[i] = (guard_position, guard_velocity)

    def print_grid(self):
        grid = [[EMPTY_SYMBOL for _ in range(self.width)] for _ in range(self.height)]
        for guard in self.guards:
            if grid[guard[0][1]][guard[0][0]] == ".":
                grid[guard[0][1]][guard[0][0]] = "1"
            else:
                guard_count = int(grid[guard[0][1]][guard[0][0]])
                grid[guard[0][1]][guard[0][0]] = str(guard_count + 1)
        for row in grid:
            print("".join(row))
        print("\n")
        return grid

    def count_guards_per_quadrant(self):
        quadrants = [0, 0, 0, 0]
        quadrant_dimensions = (self.width // 2, self.height // 2)
        for guard in self.guards:
            guard_position = guard[0]
            if (
                guard_position[0] == quadrant_dimensions[0]
                or guard_position[1] == quadrant_dimensions[1]
            ):
                continue
            if (
                guard_position[0] < quadrant_dimensions[0]
                and guard_position[1] < quadrant_dimensions[1]
            ):
                quadrants[0] += 1
            elif (
                guard_position[0] > quadrant_dimensions[0]
                and guard_position[1] < quadrant_dimensions[1]
            ):
                quadrants[1] += 1
            elif (
                guard_position[0] < quadrant_dimensions[0]
                and guard_position[1] > quadrant_dimensions[1]
            ):
                quadrants[2] += 1
            else:
                quadrants[3] += 1
        return quadrants

    def is_overlaps(self):
        grid = self.print_grid()
        for row in grid:
            for cell in row:
                if cell != EMPTY_SYMBOL and cell != "1":
                    return True

        return False


def read_file(file_path):
    with open(file_path, "r") as file:
        headquarters = Headquarters(HEADQUARTERS_WIDTH, HEADQUARTERS_HEIGHT)
        for line in file:
            (guard_position_string, guard_velocity_string) = GUARD_PATTERN.match(
                line
            ).groups()
            guard_position = tuple(map(int, guard_position_string.split(",")))
            guard_velocity = tuple(map(int, guard_velocity_string.split(",")))
            headquarters.add_guard((guard_position, guard_velocity))

    return headquarters


headquarters = read_file(INPUT_FILE)
seconds = 0

while True:
    while headquarters.is_overlaps():
        headquarters.move_guards()
        # press space to continue
        seconds += 1
        print(f"seconds elapsed: {seconds}")
    input("Press Enter to continue...")
    headquarters.move_guards()
    seconds += 1


headquarters.print_grid()
# pprint(headquarters.guards)
quadrant_count = headquarters.count_guards_per_quadrant()
