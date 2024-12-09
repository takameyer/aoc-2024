FREE_SPACE = '.'

class DiskMap:
	def __init__(self, digits):
		self.digits = digits
		self.size = len(digits)

	def __str__(self):
		return ' '.join(self.digits)

	def __repr__(self):
		return self.__str__()

	def __getitem__(self, index):
		return self.digits[index]


def read_file(file_path):
	with open(file_path, 'r') as file:
		digits = file.readline().strip()

	return DiskMap(digits)

disk_map = read_file('input.txt')

def generate_block_representation(disk_map):
	block_representation = []
	cur_id = 0
	block_file_phase = True

	for i in range(disk_map.size):
		if block_file_phase:
			for j in range(int(disk_map[i])):
				block_representation.append(cur_id)
			cur_id += 1
		else:
			for j in range(int(disk_map[i])):
				block_representation.append(FREE_SPACE)
		block_file_phase = not block_file_phase

	return block_representation

block_representation = generate_block_representation(disk_map)

def find_next_free_space_index_and_size(block_representation, start_index=0):
	free_space_index = -1
	free_space_size = 0
	for i in range(start_index, len(block_representation)):
		if block_representation[i] == FREE_SPACE:
			if free_space_index == -1:
				free_space_index = i
			free_space_size += 1
		elif free_space_index != -1:
			break

	return free_space_index, free_space_size

def find_block_size(block_id, block_representation, start_index=0):
	block_size = 0
	block_found = False
	# Search forwards from start_index
	for i in range(start_index, len(block_representation)):
		if block_representation[i] == block_id:
			block_size += 1
			block_found = True
		elif block_found:
			break

	return block_size

def compact_block_representation(block_representation):
	# copy the block representation
	compacted_representation = block_representation.copy()
	compacted_block_ids = set()

	for i in range(len(compacted_representation) - 1, -1, -1):
		if compacted_representation[i] == FREE_SPACE:
			continue

		if compacted_representation[i] in compacted_block_ids:
			continue

		block_size = find_block_size(compacted_representation[i], compacted_representation)

		next_free_space_index, next_free_space_size = find_next_free_space_index_and_size(compacted_representation)

		while next_free_space_size < block_size:
			next_free_space_index, next_free_space_size = find_next_free_space_index_and_size(compacted_representation, next_free_space_index + 1)

			if next_free_space_index == -1:
				break

		if next_free_space_index == -1 or next_free_space_index > i:
			compacted_block_ids.add(compacted_representation[i])
			continue

		# move the block into the free space
		for j in range(block_size):
			compacted_representation[next_free_space_index + j] = compacted_representation[i - j]
			compacted_representation[i - j] = FREE_SPACE
		compacted_block_ids.add(compacted_representation[i])

	return compacted_representation


compacted_block_representation = compact_block_representation(block_representation)


def generate_checksum(compacted_block_representation):
	checksum = 0

	for i in range(len(compacted_block_representation)):
		if compacted_block_representation[i] == FREE_SPACE:
			continue

		checksum += i * compacted_block_representation[i]

	return checksum


print(generate_checksum(compacted_block_representation))
