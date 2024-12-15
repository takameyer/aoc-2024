INPUT_FILE = "input.txt"
WALL = "#"
ROBOT = "@"
BOX = "O"

MOVES = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)}


class Warehouse:
    def __init__(self, width):
        self.width = width
        self.robot_location = (0, 0)
        self.walls = []
        self.boxes = []
        self.moves = []

    def print(self):
        for y in range(self.height):
            for x in range(self.width):
                p = (x, y)
                if p == self.robot_location:
                    print(ROBOT, end="")
                elif p in self.boxes:
                    print(BOX, end="")
                elif p in self.walls:
                    print(WALL, end="")
                else:
                    print(".", end="")
            print()

    def set_robot_location(self, location):
        self.robot_location = location

    def set_height(self, height):
        self.height = height

    def print_moves(self):
        for move in self.moves:
            print(move)

    def move(self, move):
        dx, dy = MOVES[move]
        new_location = (self.robot_location[0] + dx, self.robot_location[1] + dy)
        if new_location in self.walls:
            return
        if new_location in self.boxes:
            self.move_box(new_location, move)
        if new_location in self.boxes or new_location in self.walls:
            return
        self.robot_location = new_location

    def move_box(self, box, move):
        dx, dy = MOVES[move]
        new_location = (box[0] + dx, box[1] + dy)
        if new_location in self.walls:
            return
        if new_location in self.boxes:
            self.move_box(new_location, move)
        if new_location in self.boxes or new_location in self.walls:
            return
        self.boxes.remove(box)
        self.boxes.append(new_location)

    def run(self):
        for move in self.moves:
            self.move(move)

    def sum_of_box_locations(self):
        return sum([x + 100 * y for x, y in self.boxes])


def read_file():
    with open(INPUT_FILE, "r") as f:
        lines = f.readlines()
        width = len(lines[0].strip())
        warehouse = Warehouse(width)
        moves = []
        for y, line in enumerate(lines):
            if line[0] == "#":
                for x, c in enumerate(line.strip()):
                    p = (x, y)
                    if c == WALL:
                        warehouse.walls.append(p)
                    elif c == ROBOT:
                        warehouse.set_robot_location(p)
                    elif c == BOX:
                        warehouse.boxes.append(p)
            elif line[0] == "\n":
                warehouse.set_height(y)
            else:
                for move in line.strip():
                    moves.append(move)

            warehouse.moves = moves

        return warehouse


warehouse = read_file()

warehouse.run()
warehouse.print()
print(warehouse.sum_of_box_locations())
