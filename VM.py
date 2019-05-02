# The main VM class. Interprets the running program


# Assembly code example (from arch-spec):
# - The program "9,32768,32769,4,19,32768" occupies six memory addresses and should:
#   - Store into register 0 the sum of 4 and the value contained in register 1.
#   - Output to the terminal the character with the ascii code contained in register 0.

# Translation of the above
#   add r0, 4, r1 
#   mov sysout, r0
#   syscall

class VM:
    def __init__(self):
        # The only way to start is to get started
        # Makes sense to just use simple arrays for now for time complexity purposes
        # We'll see if they try to send invalid values later.
        self.stack = []             # The stack
        self.memory = [0] * 32776   # Register file at 32768, it makes sense to just store the register file here since 
                                    # creating a whole new array would be another linear construction
        self.counter = 0            # Program counter. Increment the counter for every operation by the amount of operands
                                    # in an instruction + 1 for the opcode

        