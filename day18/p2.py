from collections import deque
from pprint import pprint

INPUT_FILE = "input.txt"
# INPUT_FILE = "test.txt"

GRID_RANGE = 70
# GRID_RANGE = 6
START = (0, 0)
END = (70, 70)
# END = (6, 6)
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
BYTE_RANGE = 1024
# BYTE_RANGE = 12


class TreeNode:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.current_cost = 0
        self.children = []

    def add_child(self, position):
        child = TreeNode(position, self)
        child.current_cost = self.current_cost + 1
        self.children.append(child)
        return child

    def get_path_to_root(self):
        path = []
        current = self
        while current:
            path.append(current.position)
            current = current.parent
        return path

    def get_state(self):
        return (self.position, self.current_cost)


def read_file(file):
    byte_positions = []
    with open(file, "r") as f:
        for ln in f:
            position = ln.split(",")
            (x, y) = (int(position[0]), int(position[1]))
            byte_positions.append((x, y))
    return byte_positions


# memory space is a 2d grid that range 0 to 70 horizontally and vertically
# test will use 6


def create_grid(grid_range):
    return [["." for _ in range(grid_range + 1)] for _ in range(grid_range + 1)]


def add_byte_positions(grid, byte_positions):
    for x, y in byte_positions:
        grid[y][x] = "#"
    return grid


def print_grid(grid):
    for row in grid:
        print("".join(row))


def find_shortest_path(grid, start, end):
    root_node = TreeNode(start)
    stack = [root_node]
    end_nodes = []

    while stack:
        next = stack.pop()

        if next.get_state()[0] == end:
            end_nodes.append(next)

        for move in get_next_moves(grid, *next.get_state()[0]):
            if move not in next.get_path_to_root():
                stack.append(next.add_child(move))

    if not end_nodes:
        print("no path found")
        return None
    return min(end_nodes, key=lambda x: x.get_state()[1])


def find_shortest_path_bfs(grid, start, end):
    """
    Breadth first search approach
    """
    rows, cols = len(grid), len(grid[0])
    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        (current_x, current_y), path = queue.popleft()

        if (current_x, current_y) == end:
            print("found path")
            print(path)
            print(len(path) - 1)
            return path, len(path) - 1

        for dx, dy in DIRECTIONS:
            next_x, next_y = current_x + dx, current_y + dy
            next_pos = (next_x, next_y)

            if (
                0 <= next_x < rows
                and 0 <= next_y < cols
                and next_pos not in visited
                and grid[next_y][next_x] != "#"
            ):
                visited.add(next_pos)
                queue.append((next_pos, path + [next_pos]))

    return None, None


def get_next_moves(grid, x, y):
    moves = []
    for dx, dy in DIRECTIONS:
        if is_valid_move(grid, x + dx, y + dy):
            moves.append((x + dx, y + dy))
    return moves


def is_valid_move(grid, x, y):
    if x < 0 or x > GRID_RANGE or y < 0 or y > GRID_RANGE:
        return False
    if grid[y][x] == "#":
        return False
    return True


def print_grid_with_path(grid, path):
    for row in grid:
        print("".join(row))
    for x, y in path:
        grid[y][x] = "O"
    print()
    for row in grid:
        print("".join(row))


byte_positions = read_file(INPUT_FILE)

grid = create_grid(GRID_RANGE)
grid = add_byte_positions(grid, byte_positions[:BYTE_RANGE])

byte_range_fail = BYTE_RANGE
while True:
    prev_byte_range_fail = byte_range_fail
    byte_range_fail += 1
    grid = add_byte_positions(grid, byte_positions[:byte_range_fail])
    (path, steps) = find_shortest_path_bfs(grid, START, END)
    if not path:
        print(
            "Failed to find path for byte range at position",
            byte_positions[byte_range_fail - 1],
        )
        break


# print(byte_positions)
