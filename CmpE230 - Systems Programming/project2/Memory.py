from Misc import *

class Memory:
    
    # 
    # PARAMETERS:
    # Size: Accepts an integer n. Size of the memory is set to n*2^10 bits
    #
    def __init__(self, size):
        self.size = size
        self.memorySlots = None # Each slot has 1 byte/ 8 bits

    def loadProgram(self, file):
        self.memorySlots = ['00'] * self.size*2**10 # CHECK LATER
        nextSlot = 0

        with open(file, 'r') as f:
            lines = f.readlines()

            for line in lines:

                for byte in [line[_*2:(_+1)*2] for _ in range(3)]:
                    self.memorySlots[nextSlot] = byte
                    nextSlot += 1

    # address: decimal
    # operand: decimal
    def write(self, address, operand):
        binary = decToBin(operand)
        hex = binToHex(binary)
        for i in range(2):
            self.memorySlots[address+i] = hex[2*i: 2*(i+1)]

    # address: decimal
    # nBytes: number of bytes to read
    # returns 2 bytes in decimal
    def read(self, address, nBytes):
        res = ""
        for i in range(nBytes):
            res += self.memorySlots[address + i]
        return int(res,16)

    # assuming that the computer is not somehow 16 bits
    def readInstruction(self, address):
        return self.read(address, 3)

# create and load
#m = Memory(64)
#m.loadProgram("input.txt")

# print instructions
#for i in range(10):
#    print (i+1), m.readInstruction(hex(i*3)[2:]).zfill(2)

# print instrucions manually
#for i in range(0, 21, 3):
#    print (i/3+1), m.memorySlots[i:i+3]