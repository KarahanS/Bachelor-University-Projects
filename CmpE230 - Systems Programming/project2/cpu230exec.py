#!/usr/bin/env python3 
# # To run the script from terminal
from CPU import CPU
from Memory import Memory
import sys

# argv[0] - .py file name
f = sys.argv[1]

memory = Memory(64)
memory.loadProgram(f)

cpu = CPU(memory, f)
cpu.runProgram()
cpu.writeFile()

