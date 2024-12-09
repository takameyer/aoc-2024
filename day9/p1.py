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

def find_next_free_space(block_representation, start_index=0):
	for i in range(start_index, len(block_representation)):
		if block_representation[i] == FREE_SPACE:
			return i
	return -1

def compact_block_representation(block_representation):
	# copy the block representation
	compacted_representation = block_representation.copy()


	for i in range(len(compacted_representation) - 1, -1, -1):
		if compacted_representation[i] == FREE_SPACE:
			continue

		next_free_space = find_next_free_space(compacted_representation)

		# if the next free space is greater than the current index, we have reached the end of the compacted representation
		if next_free_space > i:
			break

		# swap the block with the free space
		byte = compacted_representation[i]
		compacted_representation[next_free_space] = byte
		compacted_representation[i] = FREE_SPACE

	return compacted_representation

compacted_block_representation = compact_block_representation(block_representation)


def generate_checksum(compacted_block_representation):
	checksum = 0

	for i in range(len(compacted_block_representation)):
		if compacted_block_representation[i] == FREE_SPACE:
			break

		checksum += i * compacted_block_representation[i]

	return checksum


print(generate_checksum(compacted_block_representation))
