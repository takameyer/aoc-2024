from pprint import pprint

# puzzle input is a map of garden plots
# each plot contains since plant indicted by a letter
# plots of the same type that are touching horizontally or vertically form a region
# need to calculate the fencing needed to enclose each region
# plants of the same type can appear in multiple regions and regions can appear within other regions

DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
DIRECTION_NAMES = ["Right", "Left", "Down", "Up"]


class GardenMap:
    def __init__(self, garden_map):
        self.garden_map = garden_map
        self.width = len(garden_map)
        self.height = len(garden_map[0])
        self.regions = {}
        self.parameters = {}
        self.sides = {}
        self.side_counts = {}
        self.visited_plots = set()
        self._calculate_regions()
        self._calculate_sides()

    def _calculate_regions(self):
        # region is a list of tuples which contain it's area and parameter
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.visited_plots:
                    self.visited_plots.add((i, j))
                    type = self.garden_map[i][j]
                    plot_hash = (type, (i, j))

                    self.regions[plot_hash] = [(i, j)]
                    self.parameters[plot_hash] = set()
                    self._find_region_and_parameter(i, j, type, plot_hash)

    def _find_region_and_parameter(self, i, j, type, plot_hash):
        # recursively find all neighbours of the same type
        for di in range(len(DIRECTIONS)):
            direction = DIRECTIONS[di]
            direction_name = DIRECTION_NAMES[di]
            new_i, new_j = i + direction[0], j + direction[1]
            if (
                self._is_in_bounds(new_i, new_j)
                and (new_i, new_j) not in self.visited_plots
                and self.garden_map[new_i][new_j] == type
            ):
                self.visited_plots.add((new_i, new_j))
                self.regions[plot_hash].append((new_i, new_j))
                self._find_region_and_parameter(new_i, new_j, type, plot_hash)
            elif (
                self._is_in_bounds(new_i, new_j)
                and self.garden_map[new_i][new_j] != type
            ):
                self.parameters[plot_hash].add((direction_name, (i, j)))
            elif not self._is_in_bounds(new_i, new_j):
                self.parameters[plot_hash].add((direction_name, (i, j)))

    def _calculate_sides(self):
        for plot_hash in self.parameters:
            print(f"Parameters for {plot_hash}: {self.parameters[plot_hash]}")
            unique_down_i_side = set()
            unique_up_i_side = set()
            unique_left_j_side = set()
            unique_right_j_side = set()
            for side in self.parameters[plot_hash]:
                direction = side[0]
                i, j = side[1]
                if direction == "Down":
                    unique_down_i_side.add(i)
                elif direction == "Up":
                    unique_up_i_side.add(i)
                elif direction == "Left":
                    unique_left_j_side.add(j)
                elif direction == "Right":
                    unique_right_j_side.add(j)
            self.sides[plot_hash] = {
                "Down": len(unique_down_i_side),
                "Up": len(unique_up_i_side),
                "Left": len(unique_left_j_side),
                "Right": len(unique_right_j_side),
            }
            print(f"Sides for {plot_hash}: {self.sides[plot_hash]}")
            side_count = (
                len(unique_up_i_side)
                + len(unique_down_i_side)
                + len(unique_left_j_side)
                + len(unique_right_j_side)
            )
            self.side_counts[plot_hash] = side_count

    def _is_in_bounds(self, i, j):
        return 0 <= i < self.height and 0 <= j < self.width

    def __str__(self):
        return "\n".join(["".join(row) for row in self.garden_map])

    def get_garden_map(self):
        return self.garden_map

    def get_regions(self):
        return self.regions

    def get_parameters(self):
        return self.parameters

    def get_side_counts(self):
        return self.side_counts


def read_file(file_path):
    with open(file_path, "r") as file:
        map = []
        for line in file:
            map.append(list(line.strip()))
    return GardenMap(map)


garden_map = read_file("test2p2.txt")

total_price = 0
for plot_hash in garden_map.get_parameters():
    side_count = garden_map.get_side_counts()[plot_hash]
    area = len(garden_map.get_regions()[plot_hash])
    cost = side_count * area
    total_price += cost
    print(f"The Region {plot_hash} with price {area} * {side_count} = {cost}")
print(f"Total Price: {total_price}")
