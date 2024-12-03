
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

left_list, right_list = read_file('input-a.txt')

# Sort the lists from smallest to largest
left_list.sort()
right_list.sort()

print(left_list)
print(right_list)

# Create a list of differences between the two lists
diff_list = [abs(left_list[i] - right_list[i]) for i in range(len(left_list))]

print(diff_list)

# Sum the differences
sum_diff = sum(diff_list)

print(sum_diff)
