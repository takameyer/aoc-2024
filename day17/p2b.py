from typing import List

# 3-bit computer
# program is a list of 3-bit numbers (0-7)
# three registers named A, B, C
# registers can hold an integer
# eight instructions
# each instructions reads the 3-bit number after it's input (operand)
# instructions pointer starts at 0
# increases by 2 after each instruction
# program halts when the instruction pointer is out of bounds

# two types of operands
# literal: 0-7
# combo operands:
# 0-3 are literal
# 4 is A
# 5 is B
# 6 is C
# 7 is reserved

# eight instructions;
# adv: 0 - division (A register / 2 to the power of combo operand) -> A
# bxl: 1 - bitwise XOR (B register and literal operand) -> B
# bst: 2 - combo operand % 8 -> B (keeps lowest 3 bits)
# jnz: 3 - if A == 0, nothing. otherwise jump (set instruction pointer to literal operand)
#          do not increase by 2
# bxc: 4 - bitwise XOR (B register XOR C register) -> B (ignores the operand)
# out: 5 - combo operand % 8 -> output (multiple values are seperated by commas)
# bdv: 6 - like adv, but the result is stored in B register
# cdv: 7 - like adv, but the result is stored in C register

INPUT_FILE = "input.txt"


def read_file():
    with open(INPUT_FILE, "r") as f:
        lines = f.read().split("\n")
        register_a = int(lines[0].split(":")[1].strip())
        register_b = int(lines[1].split(":")[1].strip())
        register_c = int(lines[2].split(":")[1].strip())
        program_input = list(map(int, lines[4].split(":")[1].strip().split(",")))
        return register_a, register_b, register_c, program_input


INSTRUCTION_MAP = {
    0: "adv",
    1: "bxl",
    2: "bst",
    3: "jnz",
    4: "bxc",
    5: "out",
    6: "bdv",
    7: "cdv",
}


class Computer:
    def __init__(self, register_a=0, register_b=0, register_c=0, program_input=[]):
        self.register_a = register_a
        self.register_b = register_b
        self.register_c = register_c
        self.instruction_pointer = 0
        self.output = []
        self.program_input = program_input
        self.instruction_count = len(program_input) // 2

    def reset(self, new_a):
        self.register_a = new_a
        self.register_b = 0
        self.register_c = 0
        self.instruction_pointer = 0
        self.output = []

    def is_done(self):
        return self.instruction_pointer >= len(self.program_input)

    def simulate_until_diverge(self, target_output):
        while self.instruction_pointer < len(self.program_input):
            instruction = self.program_input[self.instruction_pointer]
            operand = self.program_input[self.instruction_pointer + 1]

            # Special handling for jump instruction
            if instruction == 3:  # jnz
                if self.register_a != 0:
                    self.instruction_pointer = operand
                    continue
                self.instruction_pointer += 2
                continue

            # Handle output instruction
            if instruction == 5:  # out
                output_val = str(self.get_combo_operand(operand) % 8)
                if (
                    len(self.output) >= len(target_output)
                    or output_val != target_output[len(self.output)]
                ):
                    return False
                self.output.append(output_val)
            # Handle register A modifications
            elif instruction == 0:  # adv
                self.register_a = int(
                    self.register_a / (2 ** self.get_combo_operand(operand))
                )
            # Handle register B modifications
            elif instruction == 1:  # bxl
                self.register_b = self.register_b ^ operand
            elif instruction == 2:  # bst
                self.register_b = self.get_combo_operand(operand) % 8
            elif instruction == 4:  # bxc
                self.register_b = self.register_b ^ self.register_c
            elif instruction == 6:  # bdv
                self.register_b = int(
                    self.register_a / (2 ** self.get_combo_operand(operand))
                )
            # Handle register C modifications
            elif instruction == 7:  # cdv
                self.register_c = int(
                    self.register_a / (2 ** self.get_combo_operand(operand))
                )

            self.instruction_pointer += 2

        return len(self.output) == len(target_output)

    def get_combo_operand(self, operand):
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return self.register_a
            case 5:
                return self.register_b
            case 6:
                return self.register_c
            case 7:
                return 0
        return 0

    def print_output(self):
        print(",".join(self.output))
        return

    def print_output_joined(self):
        print("".join(self.output))
        return

    def print_state(self):
        print(
            f"Register A: {self.register_a}, Register B: {self.register_b}, Register C: {self.register_c}, Instruction Pointer: {self.instruction_pointer}"
        )

    def run(self):
        while not self.is_done():
            self.tick()
        return

    def find_a_optimized(self):
        target_output = list(map(str, self.program_input))
        max_shift = 0

        for i in range(0, len(self.program_input), 2):
            instruction = self.program_input[i]
            operand = self.program_input[i + 1]
            if instruction in [0, 6, 7]:  # adv, bdv, cdv
                if operand <= 3:
                    max_shift = max(max_shift, operand)
                else:
                    max_shift = max(max_shift, 7)

        max_required_bits = len(target_output) * 3 + max_shift
        max_a = 1 << max_required_bits
        step_size = 1 << 3

        print(f"Max required bits: {max_required_bits}")
        print(f"Max A: {max_a}")

        for base_a in range(max_a - step_size, -1, -step_size):
            for fine_a in range(7, -1, -1):
                a = base_a + fine_a
                self.reset(a)
                if self.simulate_until_diverge(target_output):
                    print(f"Found a: {a}")
                    print(f"Output: {self.output}")
                    print(f"Target: {target_output}")
                    return a

        return None


register_a, register_b, register_c, program_input = read_file()

computer = Computer(int(register_a), int(register_b), int(register_c), program_input)

print(computer.find_a_optimized())

# computer.print_state()


# while not computer.is_done():
# computer.tick()
# computer.print_state()

# computer.print_output()
# computer.print_output_joined()
