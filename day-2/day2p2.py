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

def is_safe(report):
    direction = None
    for i in range(len(report)):
        if i == len(report) - 1:
            return True
        first = report[i]
        second = report[i+1]
        if first == second:
            break
        if first > second:
            if direction is None:
                direction = "descending"
            elif direction == "ascending":
                break
            elif abs(first - second) > 3:
                break
        if first < second:
            if direction is None:
                direction = "ascending"
            elif direction == "descending":
                break
        # the difference should be between 1 and 3
        if abs(first - second) > 3:
            break
    return False


safe_reports = 0

for report in report_list:
    if is_safe(report):
        safe_reports += 1
        continue
    for i in range(len(report)):
        report_copy = report.copy()
        report_copy.pop(i)
        if is_safe(report_copy):
            safe_reports += 1
            break


print(safe_reports)
