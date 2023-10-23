import sys

class Brainf_ck:
    def __init__(self, program, DEBUG = False):
        self.program = program
        self.memory = [0] * 30_000
        self.instruction_pointer = 0
        self.data_pointer = 0
        self.call_stack = []
        self.DEBUG = DEBUG

    def execute(self):
        match self.program[self.instruction_pointer]:
            case ">":
                self.data_pointer += 1
            case "<":
                self.data_pointer -= 1
            case "+":
                self.memory[self.data_pointer] += 1
                self.memory[self.data_pointer] %= 256
            case "-":
                self.memory[self.data_pointer] -= 1
                self.memory[self.data_pointer] %= 256
            case ".":
                print(chr(self.memory[self.data_pointer]), end = "")
            case ",":
                self.memory[self.data_pointer] = ord(input()[0])
            case "[":
                if self.memory[self.data_pointer] == 0:
                    nesting_level = 1

                    while nesting_level > 0:
                        self.instruction_pointer += 1
                        
                        if self.program[self.instruction_pointer] == "[":
                            nesting_level += 1
                        elif self.program[self.instruction_pointer] == "]":
                            nesting_level -= 1
                else:
                    self.call_stack.append(self.instruction_pointer)
            case "]":
                if self.memory[self.data_pointer] != 0:
                    self.instruction_pointer = self.call_stack[-1]
                else:
                    self.call_stack.pop()

        self.instruction_pointer += 1

    def run_program(self):
        while len(self.program) > self.instruction_pointer:
            if self.DEBUG:
                print("\033c")
                print("\t\t\t------- Memory -------")
                print(*[f'{hex(num):^4}' for num in range(10)], sep = " | ")
                print(*[f'{self.memory[idx]:^4}' for idx in range(10)], sep = " | ")
                print(f"\nData Pointer: {self.data_pointer}\n")
                print(self.program[max(0, self.instruction_pointer - 20):self.instruction_pointer] + f"\033[4m{self.program[self.instruction_pointer]}\033[0m" + self.program[self.instruction_pointer + 1:self.instruction_pointer + 20])
                print(self.call_stack)
                print(f"\nInstruction Pointer: {self.instruction_pointer}")
                input()
            self.execute()

bf = Brainf_ck(sys.argv[1])
bf.run_program()
