INPUT_FILE = "input.txt"
WALL = "#"
ROBOT = "@"
BOX = "O"

BOX_LEFT = "["
BOX_RIGHT = "]"

MOVES = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)}


class Warehouse:
    def __init__(self, width):
        self.width = width
        self.robot_location = (0, 0)
        self.walls = []
        self.boxes = {}
        self.moves = []

    def print(self):
        for y in range(self.height):
            for x in range(self.width):
                p = (x, y)
                if p == self.robot_location:
                    print(ROBOT, end="")
                elif p in self.boxes:
                    print(self.boxes[p], end="")
                elif p in self.walls:
                    print(WALL, end="")
                else:
                    print(".", end="")
            print()

    def add_wall(self, wall):
        wall_position = (wall[0] * 2, wall[1])
        self.walls.append(wall_position)
        self.walls.append((wall_position[0] + 1, wall_position[1]))

    def add_box(self, box):
        box_position = (box[0] * 2, box[1])
        self.boxes[box_position] = BOX_LEFT
        self.boxes[(box_position[0] + 1, box_position[1])] = BOX_RIGHT

    def set_robot_location(self, location):
        self.robot_location = (location[0] * 2, location[1])

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

        if self.boxes[box] == BOX_RIGHT:
            box_left = (box[0] - 1, box[1])
            box_right = box
            new_box_left = (box_left[0] + dx, box_left[1] + dy)
            new_box_right = (box_right[0] + dx, box_right[1] + dy)
        else:
            box_left = box
            box_right = (box[0] + 1, box[1])
            new_box_left = (box_left[0] + dx, box_left[1] + dy)
            new_box_right = (box_right[0] + dx, box_right[1] + dy)

        # if horizontal
        if move == "<" or move == ">":
            if self.boxes[box] == BOX_RIGHT:
                if new_box_left in self.walls or new_box_right in self.walls:
                    return False
                if new_box_right != box_left:
                    if new_box_left in self.boxes or new_box_right in self.boxes:
                        if not self.move_box(new_box_left, move):
                            return False
                if new_box_left in self.boxes:
                    if not self.move_box(new_box_left, move):
                        return False
                self.boxes.pop(box_left)
                self.boxes.pop(box_right)
                self.boxes[new_box_left] = BOX_LEFT
                self.boxes[new_box_right] = BOX_RIGHT
            elif self.boxes[box] == BOX_LEFT:
                if new_box_left in self.walls or new_box_right in self.walls:
                    return False
                if new_box_left != box_right:
                    if new_box_left in self.boxes or new_box_right in self.boxes:
                        if not self.move_box(new_box_right, move):
                            return False
                if new_box_right in self.boxes:
                    if not self.move_box(new_box_right, move):
                        return False
                self.boxes.pop(box_left)
                self.boxes.pop(box_right)
                self.boxes[new_box_left] = BOX_LEFT
                self.boxes[new_box_right] = BOX_RIGHT
        else:
            if self.collision_check(box, move):
                return False
            if new_box_left in self.walls or new_box_right in self.walls:
                return False
            if new_box_left in self.boxes:
                if not self.move_box(new_box_left, move):
                    return False
            if new_box_right in self.boxes:
                if not self.move_box(new_box_right, move):
                    return False
            self.boxes.pop(box_left)
            self.boxes.pop(box_right)
            self.boxes[new_box_left] = BOX_LEFT
            self.boxes[new_box_right] = BOX_RIGHT

        return True

    def collision_check(self, box, move):
        collision = False
        dx, dy = MOVES[move]

        if self.boxes[box] == BOX_RIGHT:
            box_left = (box[0] - 1, box[1])
            box_right = box
            new_box_left = (box_left[0] + dx, box_left[1] + dy)
            new_box_right = (box_right[0] + dx, box_right[1] + dy)
        else:
            box_left = box
            box_right = (box[0] + 1, box[1])
            new_box_left = (box_left[0] + dx, box_left[1] + dy)
            new_box_right = (box_right[0] + dx, box_right[1] + dy)
        if new_box_left in self.walls or new_box_right in self.walls:
            return True
        if new_box_left in self.boxes:
            if self.collision_check(new_box_left, move):
                return True
        if new_box_right in self.boxes:
            if self.collision_check(new_box_right, move):
                return True
        return collision

    def run(self):
        for move in self.moves:
            self.move(move)

    def sum_of_box_locations(self):
        result = 0
        for x, y in self.boxes:
            if self.boxes[(x, y)] == BOX_LEFT:
                result += x + 100 * y
        return result


def read_file():
    with open(INPUT_FILE, "r") as f:
        lines = f.readlines()
        width = len(lines[0].strip()) * 2
        warehouse = Warehouse(width)
        moves = []
        for y, line in enumerate(lines):
            if line[0] == "#":
                for x, c in enumerate(line.strip()):
                    p = (x, y)
                    if c == WALL:
                        warehouse.add_wall(p)
                    elif c == ROBOT:
                        warehouse.set_robot_location(p)
                    elif c == BOX:
                        warehouse.add_box(p)
            elif line[0] == "\n":
                warehouse.set_height(y)
            else:
                for move in line.strip():
                    moves.append(move)

            warehouse.moves = moves

        return warehouse


warehouse = read_file()

warehouse.print()
warehouse.run()
print(warehouse.sum_of_box_locations())
