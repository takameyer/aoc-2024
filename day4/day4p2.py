def read_file_to_matrix(file_path):
    with open(file_path, 'r') as file:
        return [list(line.strip()) for line in file]

matrix = read_file_to_matrix('test.txt')

rows = len(matrix)
columns = len(matrix[0])
xmas_count = 0

directions =[
				(1, 1), # down-right
				(1, -1), # down-left
				(-1, 1), # up-right
				(-1, -1), # up-left
			 ]

def direction_in_bounds(row, column, direction):
	row_in_bounds = row + direction[0] in range(rows)
	column_in_bounds = column + direction[1] in range(columns)
	return row_in_bounds and column_in_bounds

def is_x_mas(row, column):
	# check if all direction are in bounds
	for direction in directions:
		if not direction_in_bounds(row, column, direction):
			return False

	if is_back_diagonal_mas(row, column) and is_forward_diagonal_mas(row, column):
		return True

	return False

def is_back_diagonal_mas(row, column):
	# check if 'M' is down-right
	if matrix[row + 1][column + 1] == 'M':
		# check if 'S' is up-left
		if matrix[row - 1][column - 1] == 'S':
			return True
	# check if 'S' is down-right
	elif matrix[row + 1][column + 1] == 'S':
		# check if 'M' is up-left
		if matrix[row - 1][column - 1] == 'M':
			return True
	return False

def is_forward_diagonal_mas(row, column):
	# check if 'M' is down-left
	if matrix[row + 1][column - 1] == 'M':
		# check if 'S' is up-right
		if matrix[row - 1][column + 1] == 'S':
			return True
	# check if 'S' is down-left
	elif matrix[row + 1][column - 1] == 'S':
		# check if 'M' is up-right
		if matrix[row - 1][column + 1] == 'M':
			return True
	return False

for row in range(rows):
	for column in range(columns):
		if matrix[row][column] == 'A':
			if is_x_mas(row, column):
				xmas_count += 1


print(xmas_count)
