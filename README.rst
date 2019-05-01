##########################################
Pynacor -- The Synacor Challenge in Python
##########################################

The Synacor Challenge
*********************
In this challenge, your job is to use this architecture spec to create a
virtual machine capable of running the included binary. 

Architecture
^^^^^^^^^^^^
- Three storage regions
    - Memory with 15-bit address space storing 16-bit value
    - Eight registers
    - An unbounded stack which holds individual 16-bit values
- All numbers are unsigned integers 0..32767 (15-bit)
- All math is modulo 32768; 32758 + 15 => 5

Binary Format
^^^^^^^^^^^^^
- Each number is stored as a 16-bit little-endian pair (low byte, high byte)
- Numbers 0..32767 mean a literal value
- Numbers 32768..32775 instead mean registers 0..7
- Numbers 32776..65535 are invalid
- Programs are loaded into memory starting at address 0
- Address 0 is the first 16-bit value, address 1 is the second 16-bit value, etc

Opcode Listing
^^^^^^^^^^^^^^

+------+------+----------+-------------------------------------------------------------------------------+
| Code |  Op  | Operands |                                  Description                                  |
+------+------+----------+-------------------------------------------------------------------------------+
|   0  | halt |          | Stop execution and terminate the program                                      |
+------+------+----------+-------------------------------------------------------------------------------+
|   1  |  set | a, b     | Set the register <a> to the value of <b>                                      |
+------+------+----------+-------------------------------------------------------------------------------+
|   2  | push | a        | Push <a> onto the stack                                                       |
+------+------+----------+-------------------------------------------------------------------------------+
|   3  |  pop | a        | Pop the top element from the stack and write it into <a>. Empty stack = error |
+------+------+----------+-------------------------------------------------------------------------------+
|   4  |  eq  | a, b, c  | Set <a> to 1 if <b> is equal to <c>, otherwise set <a> to 0                   |
+------+------+----------+-------------------------------------------------------------------------------+
|   5  |  gt  | a, b, c  | Set <a> to 1 if <b> is greater than <c>, otherwise set <a> to 0               |
+------+------+----------+-------------------------------------------------------------------------------+
|   6  |  jmp | a        | Jump to <a>                                                                   |
+------+------+----------+-------------------------------------------------------------------------------+
|   7  |  jt  | a, b     | If <a> is nonzero, jump to <b>                                                |
+------+------+----------+-------------------------------------------------------------------------------+
|   8  |  jf  | a, b     | If <a> is zero, jump to <b>                                                   |
+------+------+----------+-------------------------------------------------------------------------------+
|   9  |  add | a, b, c  | Assign into <a> the sum of <b> and <c>                                        |
+------+------+----------+-------------------------------------------------------------------------------+
|  10  | mult | a, b, c  | Assign into <a> the product of <b> and <c>                                    |
+------+------+----------+-------------------------------------------------------------------------------+
|  11  |  mod | a, b, c  | Assign into <a> the remainder of <b> divided by <c>                           |
+------+------+----------+-------------------------------------------------------------------------------+
|  12  |  and | a, b, c  | Assign into <a> the bitwise and of <b> and <c>                                |
+------+------+----------+-------------------------------------------------------------------------------+
|  13  |  or  | a, b, c  | Assign into <a> the bitwise or of <b> and <c>                                 |
+------+------+----------+-------------------------------------------------------------------------------+
|  14  |  not | a, b     | Stores 15-bit bitwise inverse of <b> in <a>                                   |
+------+------+----------+-------------------------------------------------------------------------------+
|  15  | rmem | a, b     | Read memory at address <b> and write it to <a>                                |
+------+------+----------+-------------------------------------------------------------------------------+
|  16  | wmem | a, b     | Write the value from <b> into memory at address <a>                           |
+------+------+----------+-------------------------------------------------------------------------------+
|  17  | call | a        | Write the address of the next instruction to the stack and jump to <a>        |
+------+------+----------+-------------------------------------------------------------------------------+
|  18  |  ret |          | Remove the top element of the stack and jump to it, empty stack = halt        |
+------+------+----------+-------------------------------------------------------------------------------+
|  19  |  out | a        | Write the ASCII value <a> to the terminal                                     |
+------+------+----------+-------------------------------------------------------------------------------+
|  20  | in   | a        | Read a character from the terminal and write its ASCII code to <a>            |
+------+------+----------+-------------------------------------------------------------------------------+
|  21  | noop |          | No operation                                                                  |
+------+------+----------+-------------------------------------------------------------------------------+
