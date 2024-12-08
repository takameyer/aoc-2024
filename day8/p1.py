
EMPTY_CELL = '.'
ANTINODE_CELL = '#'

class Grid:
	def __init__(self, cells):
		self.cells = cells
		self.height = len(cells)
		self.width = len(cells[0]) if self.height > 0 else 0
		self.antinode_locations = set()

	def __str__(self):
		return '\n'.join(''.join(row) for row in self.cells)

	def __repr__(self):
		return self.__str__()

	def append_row(self, row):
		self.cells.append(row)
		self.height += 1
		self.width = len(row)

	def get_cell(self, row, col):
		return self.cells[row][col]

	def is_location_in_grid(self, row, col):
		return 0 <= row < self.height and 0 <= col < self.width

	def add_antinode_location(self, row, col):
		if self.is_location_in_grid(row, col):
			self.antinode_locations.add((row, col))
			if self.cells[row][col] == EMPTY_CELL:
				self.cells[row][col] = ANTINODE_CELL


def read_file(file_path):
	with open(file_path, 'r') as file:
		grid = Grid([])
		unique_frequencies = set()
		frequency_locations = {}

		for line in file:
			grid.append_row(list(line.strip()))

			for i, cell in enumerate(grid.cells[-1]):
				if cell != EMPTY_CELL:
					unique_frequencies.add(cell)
					if cell not in frequency_locations:
						frequency_locations[cell] = []
					frequency_locations[cell].append((len(grid.cells) - 1, i))

	return grid, unique_frequencies, frequency_locations

grid, unique_frequencies, frequency_locations = read_file('input.txt')

for frequency in unique_frequencies:
	for location in frequency_locations[frequency]:
		for sister_location in frequency_locations[frequency]:
			if sister_location == location:
				continue
			direction_between_locations = (sister_location[0] - location[0], sister_location[1] - location[1])
			first_antinode_location = (sister_location[0] + direction_between_locations[0], sister_location[1] + direction_between_locations[1])
			second_antinode_location = (location[0] - direction_between_locations[0], location[1] - direction_between_locations[1])

			grid.add_antinode_location(first_antinode_location[0], first_antinode_location[1])
			grid.add_antinode_location(second_antinode_location[0], second_antinode_location[1])



print(grid)
print(len(grid.antinode_locations))
