from pprint import pprint

# puzzle input is a map of garden plots
# each plot contains since plant indicted by a letter
# plots of the same type that are touching horizontally or vertically form a region
# need to calculate the fencing needed to enclose each region
# plants of the same type can appear in multiple regions and regions can appear within other regions

DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


class GardenMap:
    def __init__(self, garden_map):
        self.garden_map = garden_map
        self.width = len(garden_map)
        self.height = len(garden_map[0])
        self.regions = {}
        self.parameters = {}
        self.visited_plots = set()
        print(f"Width: {self.width}, Height: {self.height}")
        self._calculate_regions()

    def _calculate_regions(self):
        # region is a list of tuples which contain it's area and parameter
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.visited_plots:
                    self.visited_plots.add((i, j))
                    type = self.garden_map[i][j]
                    plot_hash = (type, (i, j))

                    print(f"Finding region for plot {i}, {j} of type {type}")
                    self.regions[plot_hash] = [(i, j)]
                    self.parameters[plot_hash] = 0
                    self._find_region_and_parameter(i, j, type, plot_hash)
                    print(f"Regions: {self.regions}")
        print(f"Visited Plots: {self.visited_plots}")

    def _find_region_and_parameter(self, i, j, type, plot_hash):
        # recursively find all neighbours of the same type
        for direction in DIRECTIONS:
            new_i, new_j = i + direction[0], j + direction[1]
            print(f"Checking neighbour at {new_i}, {new_j} From {i}, {j}")
            if (
                self._is_in_bounds(new_i, new_j)
                and (new_i, new_j) not in self.visited_plots
                and self.garden_map[new_i][new_j] == type
            ):
                print(f"Found neighbour at {new_i}, {new_j}")
                self.visited_plots.add((new_i, new_j))
                self.regions[plot_hash].append((new_i, new_j))
                self._find_region_and_parameter(new_i, new_j, type, plot_hash)
            elif (
                self._is_in_bounds(new_i, new_j)
                and self.garden_map[new_i][new_j] != type
            ):
                self.parameters[plot_hash] += 1
            elif not self._is_in_bounds(new_i, new_j):
                self.parameters[plot_hash] += 1

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


def read_file(file_path):
    with open(file_path, "r") as file:
        map = []
        for line in file:
            map.append(list(line.strip()))
        print(map)
    return GardenMap(map)


garden_map = read_file("input.txt")
print(garden_map)
pprint(garden_map.get_regions())
pprint(garden_map.get_parameters())

total_price = 0
for plot_hash in garden_map.get_parameters():
    parameter = garden_map.get_parameters()[plot_hash]
    area = len(garden_map.get_regions()[plot_hash])
    cost = parameter * area
    total_price += cost
    print(f"The Region {plot_hash} with price {area} * {parameter} = {cost}")
print(f"Total Price: {total_price}")
