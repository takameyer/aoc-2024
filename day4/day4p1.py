def read_file_to_matrix(file_path):
    with open(file_path, 'r') as file:
        return [list(line.strip()) for line in file]

matrix = read_file_to_matrix('input.txt')

rows = len(matrix)
columns = len(matrix[0])
xmas_count = 0

directions = [
				(0, 1), # right
				(1, 0), # down
				(0, -1), # left
				(-1, 0), # up
				(1, 1), # down-right
				(1, -1), # down-left
				(-1, 1), # up-right
				(-1, -1), # up-left
			 ]

def direction_in_bounds(row, column, direction_one, direction_two):
	row_in_bounds = row + direction_one in range(rows)
	column_in_bounds = column + direction_two in range(columns)
	return row_in_bounds and column_in_bounds

for row in range(rows):
    for column in range(columns):
        if matrix[row][column] == 'X':
            for direction in directions:
                if direction_in_bounds(row, column, direction[0], direction[1]):
                    if matrix[row + direction[0]][column + direction[1]] == 'M':
                        if direction_in_bounds(row, column, direction[0] * 2, direction[1] * 2):
                            if matrix[row + direction[0] * 2][column + direction[1] * 2] == 'A':
                                if direction_in_bounds(row, column, direction[0] * 3, direction[1] * 3):
                                    if matrix[row + direction[0] * 3][column + direction[1] * 3] == 'S':
                                        xmas_count += 1


print(xmas_count)
