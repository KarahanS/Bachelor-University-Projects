#!/usr/bin/env python3  
# To run the script from terminal
from Assembler import Assembler
import sys

# argv[0] - .py file name
f = sys.argv[1]
assembler = Assembler(f)
if(assembler.assemble() is False):
    print("An error is found in the .asm file. .bin file is not created.")
else:
    assembler.write()
