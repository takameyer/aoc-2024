from pprint import pprint
from collections import deque

INPUT_FILE = "input.txt"
WALL = "#"
EMPTY = "."
START = "S"
END = "E"
NORTH = "^"
SOUTH = "v"
EAST = ">"
WEST = "<"

DIRS = {NORTH: (0, -1), EAST: (1, 0), SOUTH: (0, 1), WEST: (-1, 0)}
MOVE_COST = 1
TURN_COST = 1000

DIRECTIONS = [NORTH, EAST, SOUTH, WEST]

START_DIRECTION = EAST


def get_turns_needed(current_dir, next_dir):
    current_index = DIRECTIONS.index(current_dir)
    next_index = DIRECTIONS.index(next_dir)

    # Calculate minimum turns (clockwise or counterclockwise)
    turns = (next_index - current_index) % 4

    if turns > 2:
        turns = turns - 4  # Convert to counterclockwise if it's shorter
    return abs(turns)


class TreeNode:
    def __init__(self, position, facing, cost, parent=None):
        self.position = position
        self.facing = facing
        self.parent = parent
        self.cost = cost
        self.children = []

    def add_child(self, position, facing):
        movement_cost = self.movement_cost(self.facing, facing)
        total_cost = self.cost + movement_cost
        child = TreeNode(position, facing, total_cost, self)
        self.children.append(child)
        return child

    def movement_cost(self, dir, new_dir):
        turn_count = get_turns_needed(dir, new_dir)
        return MOVE_COST + (TURN_COST * turn_count)

    def get_state(self):
        return (self.position, self.facing, self.cost)


class Maze:
    def __init__(self, filename):
        self.maze = []
        self.start = None
        self.end = None
        self.filename = filename
        self.possible_paths = []
        self.optimal_path = {}
        self.read_maze()
        self.find_optimal_path2()

    def read_maze(self):
        with open(INPUT_FILE) as f:
            lines = f.readlines()
            for line in lines:
                line_list = list(line.strip())
                self.maze.append(line_list)
                for x, char in enumerate(line_list):
                    match char:
                        case "S" if not self.start:
                            self.start = (x, len(self.maze) - 1)
                        case "E" if not self.end:
                            self.end = (x, len(self.maze) - 1)
        return lines

    def print_maze(self):
        for line in self.maze:
            print("".join(line))

    def print_maze_with_path(self):
        maze = self.maze
        optimal_path = self.optimal_path
        cost = optimal_path.get("cost", 0)
        optimal_path.pop("cost")
        for (x, y), direction in self.optimal_path.items():
            maze[y][x] = direction
        for line in maze:
            print("".join(line))
        print(f"Cost: {cost}")

    def find_optimal_path(self):
        self.print_maze()
        cur_pos = self.start
        travel_path = {}
        travel_path[cur_pos] = START_DIRECTION
        travel_path["cost"] = 0
        self.travel(cur_pos, travel_path)
        for path in self.possible_paths:
            if not self.optimal_path or path["cost"] < self.optimal_path["cost"]:
                self.optimal_path = path

    def travel(self, pos, travel_path):
        moves = self.get_possible_moves(pos, travel_path)
        cur_direction = travel_path[pos]
        for move in moves:
            new_travel_path = travel_path.copy()
            direction, new_pos = move
            cur_cost = new_travel_path.get("cost", 0)
            new_cost = cur_cost + self.movement_cost(cur_direction, direction)
            new_travel_path[new_pos] = direction
            new_travel_path["cost"] = new_cost
            if new_pos == self.end:
                self.possible_paths.append(new_travel_path)
                return
            self.travel(new_pos, new_travel_path)
        return

    def find_optimal_path2(self):
        root = TreeNode(self.start, START_DIRECTION, 0)
        cheapest_path = None
        queue = deque([root])
        visited_states = {(self.start, START_DIRECTION): 0}

        while queue:
            current = queue.popleft()
            moves = self.get_possible_moves2(current.position)
            for move in moves:
                new_pos = move[1]
                new_dir = move[0]
                new_state = (new_pos, new_dir)
                if (
                    new_state in visited_states
                    and visited_states[new_state] <= current.cost
                ):
                    continue

                child = current.add_child(new_pos, new_dir)

                if cheapest_path and child.cost >= cheapest_path.cost:
                    continue

                if new_pos == self.end:
                    if not cheapest_path or child.cost < cheapest_path.cost:
                        cheapest_path = child
                    continue
                visited_states[new_state] = child.cost
                queue.append(child)

        pprint(cheapest_path.cost)

        # self.optimal_path = travel_path

    def movement_cost(self, dir, new_dir):
        turn_count = get_turns_needed(dir, new_dir)
        return MOVE_COST + (TURN_COST * turn_count)

    def get_possible_moves2(self, pos):
        x, y = pos
        possible_moves = []
        for direction, (dx, dy) in DIRS.items():
            new_x, new_y = x + dx, y + dy
            if self.maze[y][x] != WALL:
                possible_moves.append((direction, (new_x, new_y)))
        return possible_moves

    def get_possible_moves(self, pos, travel_path):
        x, y = pos
        possible_moves = []
        for direction, (dx, dy) in DIRS.items():
            new_x, new_y = x + dx, y + dy
            if self.is_valid_move(new_x, new_y, travel_path):
                possible_moves.append((direction, (new_x, new_y)))
        return possible_moves

    def is_valid_move(self, x, y, travel_path):
        return self.maze[y][x] != WALL and not (x, y) in travel_path


maze = Maze(INPUT_FILE)


# print(maze.start)
# print(maze.end)
# print(maze.optimal_path)
# print(maze.print_maze_with_path())
