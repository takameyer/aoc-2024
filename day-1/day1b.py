
def read_file(file_name):
	# Read the file and split into two lists
	with open(file_name, 'r') as file:
			# Initialize empty lists for each column
			left_list = []
			right_list = []

			# Read each line and split the columns
			for line in file:
					# Split line on whitespace and convert to integers
					num1, num2 = line.strip().split()
					left_list.append(int(num1))
					right_list.append(int(num2))

	return left_list, right_list

left_list, right_list = read_file('input-b.txt')

similar_count_list = []

for left_number in left_list:
	print(left_number)
	in_right_count = 0
	for right_number in right_list:
		if left_number == right_number:
			in_right_count += 1
	print(in_right_count)
	similar_count_list.append(in_right_count * left_number)

print(similar_count_list)

# Sum the list
sum_similar_count_list = sum(similar_count_list)

print(sum_similar_count_list)
