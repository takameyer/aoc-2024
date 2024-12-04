
def read_file(file_path):
    with open(file_path, 'r') as file:
        report_list = []
        i = 0
        for line in file:
            if line == '\n':
                continue
            report_list.append([])
            for num in line.strip().split():
                report_list[i].append(int(num))
            i += 1

    return report_list

report_list = read_file('input.txt')

print(report_list)

safe_reports = 0

for report in report_list:
    direction = None
    for i in range(len(report)):
        if i == len(report) - 1:
            safe_reports += 1
            break
        first = report[i]
        second = report[i+1]
        if first == second:
            break
        if first > second:
            if direction == None:
                direction = "descending"
            elif direction == "ascending":
                break
            elif abs(first - second) > 3 and direction == "descending":
                break
        if first < second:
            if direction == None:
                direction = "ascending"
            elif direction == "down":
                break
        # the difference should be between 1 and 3
        if abs(first - second) > 3:
            break

print(safe_reports)
