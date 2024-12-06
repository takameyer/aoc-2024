GUARD_SYMBOLS = ['^', '>', 'v', '<']
GUARD_DIRECTIONS = ['N', 'E', 'S', 'W']
OBSTACLE_SYMBOL = '#'

def read_file(file_path):
	with open(file_path, 'r') as file:
		guard_position = (0,0)
		guard_direction = 'N'
		obstacles = []
		width = 0
		height = 0
		grid = []

		for line in file:
			row = list(line.strip())
			grid.append(row)
			height += 1
			width = len(row)

			for i in range(len(row)):
				if row[i] in GUARD_SYMBOLS:
					guard_position = (i, height-1)
					guard_direction = GUARD_DIRECTIONS[GUARD_SYMBOLS.index(row[i])]
				if row[i] == OBSTACLE_SYMBOL:
					obstacles.append((i, height-1))
				grid[height-1][i] = row[i]

	return guard_position, guard_direction, obstacles, width, height, grid

guard_position, guard_direction, obstacles, width, height, grid = read_file('input.txt')

guard_positions = set()
loop_positions = set()

def next_position(guard_position, guard_direction):
	guard_x, guard_y = guard_position
	if guard_direction == 'N':
		guard_y -= 1
	elif guard_direction == 'E':
		guard_x += 1
	elif guard_direction == 'S':
		guard_y += 1
	elif guard_direction == 'W':
		guard_x -= 1
	return (guard_x, guard_y)

def is_position_in_bound(position, width, height):
	x, y = position
	return x >= 0 and x < width and y >= 0 and y < height

def is_position_obstacle(position, obstacles):
	return position in obstacles

def rotate_guard(guard_direction):
	guard_index = GUARD_DIRECTIONS.index(guard_direction)
	return GUARD_DIRECTIONS[(guard_index + 1) % 4]

def print_grid(grid):
	for row in grid:
		print(''.join(row))
	print()

done = False

loop_positions = set()

def simulate_guard_path(test_obstacle_position, guard_position, guard_direction, width, height, obstacles):
	current_position = guard_position
	current_direction = guard_direction
	visited_states = set()
	path = []

	#copy obstacles and add test_obstacle_position
	obstacles_with_test = obstacles.copy()
	obstacles_with_test.append(test_obstacle_position)

	while True:
		state = (current_position, current_direction)
		if state in visited_states:
			return state == (guard_position, guard_direction)
		visited_states.add(state)
		path.append(current_position)

		next_pos = next_position(current_position, current_direction)

		if not is_position_in_bound(next_pos, width, height):
			return False

		if is_position_obstacle(next_pos, obstacles_with_test):
			current_direction = rotate_guard(current_direction)
			turn_count += 1
		else:
			current_position = next_pos

while not done:
	next_guard_position = next_position(guard_position, guard_direction)
	next_position_is_in_bound = is_position_in_bound(next_guard_position, width, height)
	if not next_position_is_in_bound:
		guard_positions.add(guard_position)
		grid[guard_position[1]][guard_position[0]] = 'X'
		done = True
		break
	if is_position_obstacle(next_guard_position, obstacles):
		guard_direction = rotate_guard(guard_direction)
		grid[guard_position[1]][guard_position[0]] = GUARD_SYMBOLS[GUARD_DIRECTIONS.index(guard_direction)]
	else:
		# Test all adjacent unvisited positions for loops
		for test_dir in GUARD_DIRECTIONS:
				test_pos = next_position(guard_position, test_dir)
				if (test_pos not in guard_positions and
						test_pos not in obstacles and
						is_position_in_bound(test_pos, width, height)):
						if simulate_guard_path(test_pos, guard_position, guard_direction, width, height, obstacles):
								loop_positions.add(test_pos)

		grid[guard_position[1]][guard_position[0]] = 'X'
		guard_positions.add(guard_position)
		guard_position = next_guard_position
		grid[guard_position[1]][guard_position[0]] = GUARD_SYMBOLS[GUARD_DIRECTIONS.index(guard_direction)]


print_grid(grid)
print(len(loop_positions))


for position in loop_positions:
	grid[position[1]][position[0]] = 'O'

print_grid(grid)
