import re

def read_file(file_path):
    with open(file_path, 'r') as file:
        lines_of_code = []
        for line in file:
            lines_of_code.append(line)

    return lines_of_code

lines_of_code = read_file('input.txt')

mul_pattern = r'mul\(([1-9]|[1-9][0-9]|[1-9][0-9][0-9]),([1-9]|[1-9][0-9]|[1-9][0-9][0-9])\)'

sum_of_multiplications = 0

for line in lines_of_code:
    matches = re.findall(mul_pattern, line)
    if len(matches) > 0:
        for match in matches:
            sum_of_multiplications += int(match[0]) * int(match[1])



print(sum_of_multiplications)
