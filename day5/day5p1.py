import re

# regex for X|Y
page_rule_pattern = r'(\d+)\|(\d+)'

def read_file(file_path):
	with open(file_path, 'r') as file:
		page_rules = {}
		updates = []

		for line in file:
			pattern = re.match(page_rule_pattern, line)
			if pattern:
				if pattern.group(1) not in page_rules:
					page_rules[pattern.group(1)] = []
				page_rules[pattern.group(1)].append(pattern.group(2))
			else:
				# check if line is empty
				if line.strip() == '':
					continue

				pages = line.strip().split(',')
				updates.append(pages)

	return page_rules, updates

page_rules, updates = read_file('input.txt')

correct_pages = []

def rule_check(pages, page):
	direction = 'before'
	for p in pages:
		if p == page:
			direction = 'after'
			continue
		if p in page_rules[page]:
			if direction == 'before':
				return False
	return True

for pages in updates:
	correct = True
	for page in pages:
		# check if there's a rule for the page
		if page in page_rules:
			if not rule_check(pages, page):
				correct = False
				break
	if correct:
		correct_pages.append(pages)

def get_middle_page(pages):
	page_count = len(pages)
	return pages[page_count // 2]

middle_page_sum = 0

for pages in correct_pages:
	middle_page = get_middle_page(pages)
	middle_page_sum += int(middle_page)


print(middle_page_sum)
