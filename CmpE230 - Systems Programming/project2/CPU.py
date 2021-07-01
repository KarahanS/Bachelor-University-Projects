from Misc import *

class CPU:

    def __init__(self, memory, file):
        # Setting flags
        # ASSUMPTION: flags are initially false
        self.ZF = False
        self.CF = False
        self.SF = False

        # Setting registers
        # ASSUMPTION: registers are initially zero
        self.PC = 0
        self.A =  0
        self.B =  0
        self.C =  0
        self.D =  0
        self.E =  0
        self.S =  int('0xFFFE',16)

        self.out= file[:-3]+"txt"
        self.output = []
        self.memory = memory

    def getNextInstruction(self):
        instruction = self.memory.readInstruction(self.PC)
        self.PC += 3
        return instruction

    def decodeInstruction(self, instruction):
        res = bin(instruction)[2:].zfill(24)
        return [binToHex(res[:6]),
                res[6:-16],
                binToHex(res[-16:])]

    def pushStack(self, word):
        self.memory.write(self.S, word)
        self.S -= 2

    def popStack(self):
        self.S += 2
        res = self.memory.read(self.S, 2)
        return res

    def getRegister(self, i):
 
        if i==0:
            return self.PC
        elif i==1:
            return self.A
        elif i==2:
            return self.B
        elif i==3:
            return self.C
        elif i==4:
            return self.D
        elif i==5:
            return self.E
        else:   # Assuming that there are no errors in machine code
            return self.S

    # operand: decimal
    def setRegister(self, i, operand):    
        if i==0:
            self.PC = operand
        elif i==1:
            self.A = operand
        elif i==2:
            self.B  = operand
        elif i==3:
            self.C = operand
        elif i==4:
            self.D = operand
        elif i==5:
            self.E = operand
        else:   # Assuming that there are no errors in machine code
            self.S = operand

    
    def setFlagsWithList(self, flags):  # flags [SF, ZF, (CF)]
        self.SF = flags[0]
        self.ZF = flags[1]
        if(len(flags) == 3):
            self.CF = flags[2]
    

    
    def read(self, addressingMode, operand):
        if addressingMode == '00':
            return operand
        elif addressingMode == '01':
            return self.getRegister(operand)
        elif addressingMode == '10':
            operandAddress = self.getRegister(operand)
            return self.memory.read(operandAddress, 2)
        else:
            operandAddress = operand
            return self.memory.read(operandAddress, 2)

    # If you are taking the operand from address and adding to the register, do not use this function.
    # If you are taking the operand from outside (register etc.) and adding to an address (be it another address or register), use this function.
    
    # toWrite: decimal (value to be written)
    # operand: decimal (register or memory address we are going to write into)
    def write(self, addressingMode, operand, toWrite):

        if addressingMode == '00':
            pass
        # write to the register
        elif addressingMode == '01':  
            self.setRegister(operand, toWrite)
        # write to the memory pointed by register
        elif addressingMode == '10':
            operandAddress = self.getRegister(operand)
            self.memory.write(operandAddress, toWrite)
        # write to the memory
        else: 
            self.memory.write(operand, toWrite)

    # return false if we need to halt
    def runInstruction(self, instruction):
        opcode, addressingMode, operand = self.decodeInstruction(instruction)

        operand = hexToDec(operand)
        # print(opcode, addressingMode, operand)
        # opcode - hex  / addressing mode - bit / operand - hex
        # opcode = 6 bits / addressing mode = 2 bits / operand = 16 bits
        
        if(opcode == '1'): # HALT
            return False
        elif(opcode == '2'): # LOAD
            operand = self.read(addressingMode, operand)
            self.setRegister(1, operand)

        elif(opcode == '3'): # STORE

            # Value in register A (to be stored in operand)
            toWrite = self.getRegister(1)
            self.write(addressingMode, operand, toWrite)
            
        elif(opcode == '4'): # ADD

            operand = self.read(addressingMode, operand)
            a = self.getRegister(1)
            b = operand

            toWrite, flags = addOperation(a, b)
            self.setFlagsWithList(flags)
            self.setRegister(1, toWrite)


        elif(opcode == '5'): # SUB
            # Extract the value from the operand

            operand = self.read(addressingMode, operand)
            a = self.getRegister(1)
            b = operand

            b, flags = notOperation(b)
            self.setFlagsWithList(flags)  # NOT - flags

            b, flags = addOperation(b, 1)
            self.setFlagsWithList(flags)  # ADD - flags

            toWrite, flags = addOperation(a, b)
            self.setFlagsWithList(flags)  # ADD - flags
            self.setRegister(1, toWrite)

        elif(opcode == '6'): # INC

            a = self.read(addressingMode, operand)
            b = 1
            
            toWrite, flags = addOperation(a, b)
            self.setFlagsWithList(flags)
            self.write(addressingMode, operand, toWrite)
            
        elif(opcode == '7'): # DEC

            a = self.read(addressingMode, operand)
            b = 1
            b, flags = notOperation(b)
            self.setFlagsWithList(flags)    # NOT - flags

            b, flags = addOperation(b, 1)
            self.setFlagsWithList(flags)    # ADD - flags

            toWrite, flags = addOperation(a, b)
            self.setFlagsWithList(flags)    # ADD - flags
            self.write(addressingMode, operand, toWrite)

        elif(opcode == '8'): # XOR

            a = self.getRegister(1)
            b = self.read(addressingMode, operand)

            toWrite, flags = xorOperation(a,b)
            self.setFlagsWithList(flags)   # XOR - flags

            self.setRegister(1, toWrite)

        elif(opcode == '9'): # AND
            a = self.getRegister(1)
            b = self.read(addressingMode, operand)

            toWrite, flags = andOperation(a,b)
            self.setFlagsWithList(flags)   # AND - flags

            self.setRegister(1, toWrite)
        elif(opcode == 'a'): # OR
            a = self.getRegister(1)
            b = self.read(addressingMode, operand)

            toWrite, flags = orOperation(a,b)
            self.setFlagsWithList(flags)   # OR - flags

            self.setRegister(1, toWrite)
        elif(opcode == 'b'): # NOT
            a = self.read(addressingMode, operand)
            toWrite, flags = notOperation(a)
            self.setFlagsWithList(flags)    # NOT - flags

            self.write(addressingMode, operand, toWrite)

        elif opcode == 'c': # SHL
            content = self.getRegister(operand)
            toWrite, flags = shlOperation(content)

            self.setFlagsWithList(flags)   # SHL - flags
            self.setRegister(operand, toWrite) 

        elif opcode == 'd': # SHR
            content = self.getRegister(operand)
            toWrite, flags = shrOperation(content)

            self.setFlagsWithList(flags)   # SHR - flags
            self.setRegister(operand, toWrite) 
        elif opcode == 'e': # NOP: doing nothing
            pass
        elif opcode == 'f': # PUSH
            content = self.getRegister(operand)
            self.pushStack(content)
        elif opcode == '10': # POP
            content = self.popStack()
            self.setRegister(operand, content)
        elif opcode == '11': # CMP
            
            operand = self.read(addressingMode, operand)
            a = self.getRegister(1)
            b = operand
        
            b, flags = notOperation(b)
            self.setFlagsWithList(flags)    # NOT - flags

            b, flags = addOperation(b, 1)
            self.setFlagsWithList(flags)    # ADD - flags

            toWrite, flags = addOperation(a, b)
            self.setFlagsWithList(flags)

            
        elif opcode == '12': # JMP
            self.PC = operand
        elif opcode == '13': # JZ / JE
            if self.ZF:
                self.PC = operand
        elif opcode == '14': # JNZ / JNE
            if not self.ZF:
                self.PC = operand
        elif opcode == '15': # JC
            if self.CF:
                self.PC = operand
        elif opcode == '16': # JNC
            if not self.CF:
                self.PC = operand
        elif opcode == '17': # JA   => SF=0 and ZF=0 (equivalent to not(SF or ZF))
            if not(self.SF or self.ZF):
                self.PC = operand
        elif opcode == '18': # JAE  => SF=0
            if not(self.SF):
                self.PC = operand
        elif opcode == '19': # JB   => SF=1
            if self.SF:
                self.PC = operand
        elif opcode == '1a': # JBE  => SF=1 or ZF=1
            if self.SF or self.ZF:
                self.PC = operand
        elif opcode == '1b': # READ
            character = input()
            asciiCode = ord(character)
            self.write(addressingMode, operand, asciiCode)
        elif opcode == '1c': # PRINT
            res = self.read(addressingMode, operand)
            self.output.append(chr(res))
        else:
            print("ERROR: illegal instruction:", opcode)
            return False

        return True

    def runProgram(self):
        
        instruction = self.getNextInstruction()
        while (self.runInstruction(instruction)):
            instruction = self.getNextInstruction()

    
    def writeFile(self):
        out = open(self.out, "w")

        for o in self.output:
            out.write(o+"\n")
        out.close()

        