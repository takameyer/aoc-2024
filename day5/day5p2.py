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

incorrect_updates = []

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

def check_if_update_is_correct(pages):
	for page in pages:
		# check if there's a rule for the page
		if page in page_rules:
			if not rule_check(pages, page):
				return False
	return True

for pages in updates:
	if not check_if_update_is_correct(pages):
		incorrect_updates.append(pages)

corrected_updates = []

def fix_updates(pages):
	fixed_pages = pages
	while(not check_if_update_is_correct(fixed_pages)):
		fixed = False
		# check if there's a rule for the page
		for i in range(len(fixed_pages)):
			cur_page = fixed_pages[i]
			if fixed_pages[i] in page_rules:
				direction = 'before'
				for j in range(len(fixed_pages)):
					check_page = fixed_pages[j]
					if cur_page == check_page:
						direction = 'after'
						continue
					if check_page in page_rules[cur_page]:
						if direction == 'before':
							# swap the pages
							temp = fixed_pages[i]
							fixed_pages[i] = fixed_pages[j]
							fixed_pages[j] = temp
							fixed = True
							break
			if fixed:
				break
	return fixed_pages

for updates in incorrect_updates:
	fixed_updates = fix_updates(updates)
	corrected_updates.append(fixed_updates)

print(corrected_updates)

def get_middle_page(pages):
	page_count = len(pages)
	return pages[page_count // 2]

middle_page_sum = 0

for pages in corrected_updates:
	middle_page = get_middle_page(pages)
	middle_page_sum += int(middle_page)


print(middle_page_sum)
