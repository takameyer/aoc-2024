
# hiking trail is any path that starts at height 0 , ends at height 9, and always increases by a height of exactly 1 at each step
# trail will never include diagonal steps
# trail goes up down left right
# trailhead is any position that starts one or more hiking trails
# these positions will always have a height of 0
# trailheads score is the number of 9-height positions that are reachable from the trailhead

directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

class TrailMap:
	def __init__(self, map):
		self.map = map
		self.trailheads = self.get_trailheads()

	def get_trailheads(self):
		trailheads = []
		for i in range(len(self.map)):
			for j in range(len(self.map[i])):
				if self.map[i][j] == 0:
					trailheads.append((i, j))
		return trailheads

	def is_position_in_bounds(self, position):
		return position[0] >= 0 and position[0] < len(self.map) and position[1] >= 0 and position[1] < len(self.map[position[0]])

	def find_possible_paths(self, trailhead, level):
		possible_paths = []
		for direction in directions:
			new_position = (trailhead[0] + direction[0], trailhead[1] + direction[1])
			if self.is_position_in_bounds(new_position) and self.map[new_position[0]][new_position[1]] == level:
				possible_paths.append(new_position)
		return possible_paths

	def follow_path(self, location, level, unique_nine_paths):
		if level == 9:
			unique_nine_paths.add(location)
			return
		possible_paths = self.find_possible_paths(location, level + 1)
		for path in possible_paths:
			self.follow_path(path, level + 1, unique_nine_paths)


def read_file(file_path):
	with open(file_path, 'r') as file:
		map = []
		for line in file:
			map.append([int(x) for x in line.strip()])
	return TrailMap(map)

trail_map = read_file('input.txt')

total_score = 0

for trailhead in trail_map.trailheads:
	unique_nine_paths = set()
	trail_map.follow_path(trailhead, 0, unique_nine_paths)
	total_score += len(unique_nine_paths)
print(total_score)
