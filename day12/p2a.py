from pprint import pprint

# puzzle input is a map of garden plots
# each plot contains since plant indicted by a letter
# plots of the same type that are touching horizontally or vertically form a region
# need to calculate the fencing needed to enclose each region
# plants of the same type can appear in multiple regions and regions can appear within other regions

DIRECTIONS = ["right", "left", "down", "up"]


class GardenMap:
    def __init__(self, garden_map):
        self.garden_map = garden_map
        self.width = len(garden_map)
        self.height = len(garden_map[0])
        self.regions = {}
        self.edges = {}
        self.visited_plots = set()
        self._calculate_regions()

    def _calculate_regions(self):
        """Find all regions and calculate the parameters for each region"""
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.visited_plots:
                    plant_type = self.garden_map[i][j]
                    region_id = (plant_type, (i, j))

                    # find all cells in this region
                    region_cells, edges = self._flood_fill_with_edges(i, j, plant_type)
                    self.regions[region_id] = region_cells
                    self.edges[region_id] = edges

                    # I think we need to walk the parimeter.  We will save all the edges, do a starting point, and start walking along the edge
                    # If we hit a parameter, we turn left, if we hit a hole, we turn right

                    # We build a set of edges and then determine sets of continuous edges
                    # could probably do this really inneficently by just testing each edge and pushing it's left/right existing edges into a set

    def _flood_fill_with_edges(self, start_i, start_j, plant_type):
        """Use flood fill to find all connected cells of the same type"""
        stack = [(start_i, start_j)]
        region = set()

        edges = {
            "up": set(),
            "down": set(),
            "left": set(),
            "right": set(),
        }

        while stack:
            i, j = stack.pop()
            if (i, j) not in self.visited_plots:
                self.visited_plots.add((i, j))
                if self._is_in_bounds(i, j) and self.garden_map[i][j] == plant_type:
                    region.add((i, j))
                    for direction in DIRECTIONS:
                        match direction:
                            case "right":
                                ni, nj = i, j + 1
                            case "left":
                                ni, nj = i, j - 1
                            case "down":
                                ni, nj = i + 1, j
                            case "up":
                                ni, nj = i - 1, j

                        if not self._is_valid_same_type(ni, nj, plant_type):
                            edges[direction].add((i, j))
                        else:
                            stack.append((ni, nj))

        return region, edges

    def _is_valid_same_type(self, i, j, plant_type):
        return self._is_in_bounds(i, j) and self.garden_map[i][j] == plant_type

    def _is_in_bounds(self, i, j):
        return 0 <= i < self.height and 0 <= j < self.width

    def __str__(self):
        return "\n".join(["".join(row) for row in self.garden_map])

    def get_garden_map(self):
        return self.garden_map

    def get_regions(self):
        return self.regions

    def get_edges(self):
        return self.edges


def read_file(file_path):
    with open(file_path, "r") as file:
        map = []
        for line in file:
            map.append(list(line.strip()))
    return GardenMap(map)


garden_map = read_file("input.txt")

print(garden_map)
total_price = 0


def sort_edges(edges):
    sorted_edges = {}
    for direction in DIRECTIONS:
        match direction:
            case "right" | "left":
                print(edges[direction])
                sorted_edges[direction] = sorted(
                    edges[direction], key=lambda p: (p[1], p[0])
                )
            case "up" | "down":
                sorted_edges[direction] = sorted(
                    edges[direction], key=lambda p: (p[0], p[1])
                )
    return sorted_edges


def count_sides(edges):
    sides = {
        "up": 0,
        "down": 0,
        "left": 0,
        "right": 0,
    }
    for (
        direction
    ) in edges:  # Changed from DIRECTIONS to edges since we have the dictionary
        match direction:
            case "right" | "left":
                hz_edges = sorted(
                    edges[direction], key=lambda p: (p[1], p[0])
                )  # Sort by y then x
                if hz_edges:  # Add check for empty list
                    sides[direction] = 1  # Start with 1 for first segment
                    for i in range(len(hz_edges) - 1):
                        point = hz_edges[i]
                        following_point = hz_edges[i + 1]
                        if (
                            point[0] + 1 != following_point[0]
                            or point[1] != following_point[1]
                        ):  # Changed condition
                            sides[direction] += 1

            case "up" | "down":
                vt_edges = sorted(
                    edges[direction], key=lambda p: (p[0], p[1])
                )  # Sort by x then y
                if vt_edges:  # Add check for empty list
                    sides[direction] = 1  # Start with 1 for first segment
                    for i in range(len(vt_edges) - 1):
                        # Fixed variable name from hz_edges to vt_edges
                        point = vt_edges[i]
                        following_point = vt_edges[i + 1]
                        if (
                            point[1] + 1 != following_point[1]
                            or point[0] != following_point[0]
                        ):  # Changed condition
                            sides[direction] += 1

    sum_sides = sum(sides.values())
    return sum_sides


for plot_hash in garden_map.get_regions():
    edges = garden_map.get_edges()[plot_hash]
    side_count = count_sides(edges)
    area = len(garden_map.get_regions()[plot_hash])
    cost = side_count * area
    total_price += cost
    print(f"The Region {plot_hash} with price {area} * {side_count} = {cost}")

print(f"Total Price: {total_price}")
