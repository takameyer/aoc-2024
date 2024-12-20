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
        self.insruction_pointer = 0
        self.output = []
        self.program_input = program_input

    def is_done(self):
        return self.insruction_pointer >= len(self.program_input)

    def tick(self):
        instruction_code = self.program_input[self.insruction_pointer]
        operand = self.program_input[self.insruction_pointer + 1]

        instruction = INSTRUCTION_MAP[instruction_code]

        match instruction:
            case (
                "adv"
            ):  # 0: take register a, and shift it right by the combo operand -> A
                self.register_a = int(
                    self.register_a / (2 ** self.get_combo_operand(operand))
                )
            case "bxl":  # 1: take register b, and bitwise xor it with the operand -> B
                self.register_b = self.register_b ^ operand
            case "bst":  # 2: take the combo operand, and keep the lowest 3 bits
                self.register_b = self.get_combo_operand(operand) % 8
            case (
                "jnz"
            ):  # 3: if register a is not 0, set the instruction pointer to the operand
                if self.register_a != 0:
                    self.insruction_pointer = operand
                    return
            case "bxc":  # 4: take register b, and bitwise xor it with register c -> B
                self.register_b = self.register_b ^ self.register_c
            case "out":  # 5: take the combo operand, and keep the lowest 3 bits
                self.output.append(str(self.get_combo_operand(operand) % 8))
            case (
                "bdv"
            ):  # 6: take register a, and shift it right by the combo operand -> B
                self.register_b = int(
                    self.register_a / (2 ** self.get_combo_operand(operand))
                )
            case (
                "cdv"
            ):  # 7: take register a, and shift it right by the combo operand -> C
                self.register_c = int(
                    self.register_a / (2 ** self.get_combo_operand(operand))
                )

        self.insruction_pointer += 2
        return

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
            f"Register A: {self.register_a}, Register B: {self.register_b}, Register C: {self.register_c}, Instruction Pointer: {self.insruction_pointer}"
        )

    def run(self):
        while not self.is_done():
            self.tick()
        return

    def find_a(self):
        a = 0
        t = 0
        print("Finding a")
        goal = list(map(str, self.program_input))
        print(f"Output should be: {goal}")
        aprime = 0
        while True:
            aprime = (a << 3) + t
            self.register_a = aprime
            # print(f"Trying a: {aprime}")
            self.run()
            # print(f"Output: {self.output}")
            if goal == self.output:
                a = aprime
                break
            self.output = []
            self.insruction_pointer = 0
            self.register_b = 0
            self.register_c = 0
            t += 1
        return a

    def get_output_string(self):
        return ",".join(self.output)


register_a, register_b, register_c, program_input = read_file()

computer = Computer(int(register_a), int(register_b), int(register_c), program_input)


for input in program_input:
    a = 0
    target_found = False
    print(f"Trying input: {input}")
    while not target_found:
        computer = Computer(a, 0, 0, program_input)
        computer.run()
        output = computer.get_output_string()
        print(output)
        if output == input:
            target_found = True
            print(f"Found a: {a}")
        a += 1


computer.print_state()
computer.print_output()

# print(computer.find_a())

# computer.print_state()


# while not computer.is_done():
# computer.tick()
# computer.print_state()

# computer.print_output()
# computer.print_output_joined()
