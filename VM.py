# Assembly code example (from arch-spec):
# - The program "9,32768,32769,4,19,32768" occupies six memory addresses and should:
#   - Store into register 0 the sum of 4 and the value contained in register 1.
#   - Output to the terminal the character with the ascii code contained in register 0.

# My solution:
# First off, this is hard. Like. HARD. But once I figured out how to actually execute an instruction, the process
#     became immediately easier and easier.
# Firstly we create a stack and memory array. A counter variable for the program counter, and a flag to see
#     if the program is running. Then in the run() method we load the program into an array using numpy, ensuring 
#     the numbers in the array are less than 2 bytes long.
# After that all we gotta do is execute the instruction at memory[0] and go on. 
# I used a dictionary to help make opcodes easier. So, all we need to do is call the function at opcode[memory[0]]
import numpy    # numpy makes loading the binary file extremely easier
class VM:
    def __init__(self):
        # The only way to start is to get started
        # Makes sense to just use simple arrays for now for time complexity purposes
        # We'll see if they try to send invalid values later.
        self.stack = []             # The stack
        self.memory = [0] * 32776   # Register file at 32768, it makes sense to just store the register file here since 
                                    #     creating a whole new array would be another linear construction
        self.counter = 0            # Program counter. Increment the counter for every operation by the amount of operands
                                    #     in an instruction + 1 for the opcode
        self.is_running = False     # Flag to check if the "program" is "running"

    def run(self):
        self.is_running = True
        f = numpy.fromfile("challenge.bin".encode(), dtype=numpy.dtype("<u2"))
        # Loads the binary file as an array of readable ints
        self.memory[0:len(f)] = f.copy() # Loads the copy of f into memory
        while self.is_running:
            self.opcodes[self.memory[self.counter]](self)
    def get_r(self):
        # Originally this took an index parameter. I figured that I'd need to get registers at other operand indexes.
        return self.memory[self.counter + 1]
    def get_operand(self, i):
        op = self.memory[self.counter + i]
        if op >= 32768:
            return self.memory[op]
        return op
    def print_registers(self):
        # Prints registers for debug purposes
        print(self.memory[32768:])
    
    # Opcodes 

    def halt(self): # op 0
        print("Halting!")
        print(f"Registers: {self.memory[32768:]}")
        self.is_running = False
    
    def set_r(self): # op 1
        self.memory[self.get_r()] = self.get_operand(2)
        self.counter += 3

    def push(self): # op 2
        self.stack.append(self.get_operand(1))
        self.counter += 2

    def pop(self): # op 3
        self.memory[self.get_r()] = self.stack.pop()
        self.counter += 2

    def eq(self): # op 4
        self.memory[self.get_r()] = int(self.get_operand(2) == self.get_operand(3))
        self.counter += 4

    def gt(self): # op 5
        self.memory[self.get_r()] = int(self.get_operand(2) > self.get_operand(3))
        self.counter += 4

    def jmp(self): # op 6
        self.counter = self.get_operand(1)

    def jt(self): # op 7
        if self.get_operand(1) != 0:
            self.counter = self.get_operand(2)
        else:
            self.counter += 3

    def jf(self): # op 8
        if self.get_operand(1) == 0:
            self.counter = self.get_operand(2)
        else:
            self.counter += 3

    def add(self): # op 9
        tot = self.get_operand(2) + self.get_operand(3)
        self.memory[self.get_r()] = tot % 32768
        self.counter += 4

    def mul(self): # op 10
        # Thanks to stupid MATH we have to cast the multiplicand and multiplier to integers to avoid overflow.
        prod = int(self.get_operand(2)) * int(self.get_operand(3))
        self.memory[self.get_r()] = prod % 32768
        self.counter += 4

    def mod(self): # op 11
        rem = self.get_operand(2) % self.get_operand(3)
        self.memory[self.get_r()] = rem
        self.counter += 4

    def bit_and(self): # op 12
        self.memory[self.get_r()] = self.get_operand(2) & self.get_operand(3)
        self.counter += 4

    def bit_or(self): # op 13
        self.memory[self.get_r()] = self.get_operand(2) | self.get_operand(3)
        self.counter += 4

    def bit_not(self): # op 14
        # We need to perform a "15-bit bitwise inverse". Binary operations are wierd
        # Anyways I Googled it. Just OR it with 2^15 - 1
        self.memory[self.get_r()] = self.get_operand(2) ^ 2**15 - 1
        self.counter += 3

    def call(self): # op 17
        self.stack.append(self.counter + 2)
        self.counter = self.get_operand(1)

    def out(self): # op 19
        char = self.get_operand(1)
        print(chr(char), end="")
        self.counter += 2

    def noop(self): # op 21
        self.counter += 1

    opcodes = {
        0: halt,
        1: set_r,
        2: push,
        3: pop,
        4: eq,
        5: gt,
        6: jmp,
        7: jt,
        8: jf,
        9: add,
        10: mul,
        11: mod,
        12: bit_and,
        13: bit_or,
        14: bit_not,
        17: call,
        19: out,
        21: noop,
    }


x = VM()
x.run()