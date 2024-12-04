import re

def read_file(file_path):
    with open(file_path, 'r') as file:
        lines_of_code = []
        for line in file:
            lines_of_code.append(line)

    return lines_of_code

lines_of_code = read_file('input.txt')

mul_pattern = r'mul\(([1-9]|[1-9][0-9]|[1-9][0-9][0-9]),([1-9]|[1-9][0-9]|[1-9][0-9][0-9])\)|do\(\)|don\'t\(\)'

sum_of_multiplications = 0

process_mul = True
for line in lines_of_code:
	for match in re.finditer(mul_pattern, line):
			full_match = match.group(0)
			if full_match == "do()":
					process_mul = True
			elif full_match == "don't()":
					process_mul = False
			else:
				if process_mul:
					sum_of_multiplications += int(match.group(1)) * int(match.group(2))


print(sum_of_multiplications)
