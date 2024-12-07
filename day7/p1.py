from itertools import product

OPERATORS = ['+', '*']

def read_file(file_path):
	with open(file_path, 'r') as file:
		equations = []

		for line in file:
			v = line.strip().split(':')
			test_value = v[0]
			remaining_digits = v[1].strip().split(' ')
			equations.append((test_value, remaining_digits))

	return equations

equations = read_file('input.txt')

valid_equations = []

def evaluate_equation(numbers, operators):
	if len(numbers) == 1:
		return int(numbers[0])

	result = int(numbers[0])

	for i in range(len(operators)):
		next_num = int(numbers[i+1])
		op = operators[i]

		if op == '+':
			result += next_num
		elif op == '*':
			result *= next_num

	return result


def validate_equation(equation):
	value = int(equation[0])
	operator_count = len(equation[1]) - 1
	operator_combinations = list(product(OPERATORS, repeat=operator_count))
	for operators in operator_combinations:
		remaining_digits = equation[1]
		result = evaluate_equation(remaining_digits, operators)
		if result == value:
			return True

	return False

for equation in equations:
	if validate_equation(equation):
		valid_equations.append(equation)

sum = 0

for equation in valid_equations:
	sum += int(equation[0])

print(sum)
