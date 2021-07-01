# -*- coding: utf-8 -*-
from Misc import * 
class Assembler:


    # 
    # PARAMETERS:
    # file: Assembly code
    #
    def __init__(self, f):
        read = open(f, 'r')
        self.file = f
        self.lines = read.readlines()
        self.labels = {}
        self.instructions = []


    def assemble(self):
        counter = 0

        # Before iterating all of the code, find the labels
        for line in self.lines:
            l = line.strip().split()
            # Line with just one word can be either "HALT" operation or a label
            if(len(l) == 1):
                if(l[0].upper() not in  ['HALT', 'NOP']):
                    label = l[0][:-1].upper()
                    if(label in self.labels):
                        print("Duplicate definition of same label. Aborted.")
                        return False
                    else:
                        self.labels[label] = counter * 3
                    if(l[0][-1] != ':'):
                        print("There should be a label, however \":\" is not found.")
                        return False
                else:
                    counter += 1
            elif(len(l) == 2 and l[1] == ':'):   # to deal with cases when label is given like this = "LABEL :"
                label = l[0].upper()
                if (label in self.labels):
                    print("Duplicate definition of same label. Aborted.")
                    return False
                else:
                    self.labels[label] = counter * 3
            elif(len(l) != 0):
                counter += 1
            else:   # line is empty
                pass

        for line in self.lines:
            stl = line.strip() # getting rid of new lines and empty spaces around the main body of the string
            if len(stl) == 0: # continue if the line is empty
                continue
            stl = stl.replace('‘', "\'").replace('’', "\'")
            l = stl.split() # getting rid of the special quotation mark characters
            
            operation = l[0]

            # len(l) == 2 --> either an instruction or a label with space between name and colon (:)
            if(len(l) == 2):
                if(l[1] != ':'):
                    if(self.generateInstruction(l[1], operation) is False):
                        return False
                else:
                    pass # Label
            elif(len(l) == 1):   # Length of l may be one or more. If more, print error.
                if(operation.upper() == 'HALT'):
                    self.instructions.append('040000')
                elif (operation.upper() == 'NOP'):
                    self.instructions.append('380000')
                elif(l[0][-1] == ':'):  # Label
                    pass
                else:  # Error
                    print("A line with just one word. However, it is neither 'HALT' operation nor a label.")
                    return False
            else:
                # Special case - Given ASCII character is empty space - len(l) = 3
                if(l[1] == '\'' and l[2] == '\'' and "\' \'" in stl):
                    if(self.generateInstruction("\' \'", operation) is False):
                        return False
                else:
                    print("A line with three separate words/characters are invalid.")
                    print("    => ", l)
                    return False

    def generateInstruction(self, opr, operation):
        operand, addressingMode = self.toOperand(opr)
        opcode = self.toOpcode(operation, addressingMode)
        if(opcode is False or operand is False or addressingMode is False): 
            return False
        instruction = self.toInstruction(opcode, addressingMode, operand)
        self.instructions.append(instruction)

    def write(self):
        output = self.file[:-3]+"bin"
        out = open(output, "w")

        for ins in self.instructions:
            out.write(ins+"\n")

        out.close()

    def Debug(self, instruction):
        _3byte = bin(int(instruction, 16))[2:].zfill(24)
        print(_3byte[:6], _3byte[6:8], _3byte[8:24])
        
    def toInstruction(self, opcode, addressingMode, operand):
        _3byte = opcode + addressingMode + operand
        return hex(int(_3byte, 2))[2:].zfill(6)

    def register(self, opr):
        opr = opr.upper()
        if(opr == 'PC'):   # PC shouldn't be modified actually
            return '0000'.zfill(16)
        elif(opr == 'A'):
            return '0001'.zfill(16)
        elif(opr == 'B'):
            return '0010'.zfill(16)
        elif(opr == 'C'):
            return '0011'.zfill(16)
        elif(opr == 'D'):
            return '0100'.zfill(16)
        elif(opr == 'E'):
            return '0101'.zfill(16)
        elif(opr == 'S'):
            return '0110'.zfill(16)
        else:
            print("Invalid register.")
            return False


    # A label: marks the address, xxxx, at the point it is defined.
    # Wherever you use a label, you should substitute the marked address xxxx for the label.
    
    # An update may be required for memory addressing.
    def toOperand(self, opr):
        if(opr.upper() in ['PC','A','B','C','D','E','S']):
            return (self.register(opr), '01')
        elif(opr[0] == '[' and opr[-1] == ']'):
            address = opr[1:-1]
            if(address[0].isnumeric()):  # memory address
                processed = self.processHexadecimal(address)
                operand = hexToBin(processed) if processed else False
                return (operand, '11')
            else:  # register
                return (self.register(address), '10')
        else:  # immediate
            if(opr[0] == "'" and opr[-1] == "'"):  # ASCII character
                operand = bin(ord(opr[1:-1]))[2:].zfill(16) if (len(opr) == 3) else False
                return (operand, '00')
            elif(opr[0].isnumeric()):  # hexadecimal value
                processed = self.processHexadecimal(opr)
                operand = hexToBin(processed) if processed else False
                return (operand, '00')
            else:   # Most probably a label
                addr = self.labels.get(opr.upper(), "*") # decimal
                address =  bin(addr)[2:].zfill(16) if (addr != "*") else False
                return (address, '00')

    def processHexadecimal(self, hex):
        # remove 0s to the left
        l = len(hex)
        for i in range(l):
            if (hex[0] == '0'):
                hex = hex[1:]
            else:
                break
        if (len(hex)>4): # hex has more than 4 digits, it will not fit in 16 bits
            print("ERROR: Given hexadecimal does not fit in 16 bits: ", hex)
            print("Returned default value: 0000")
            return False
        else:
            return hex.zfill(4)

    # opcode: 6 bit
    def toOpcode(self, operation, addressingMode):
        operation = operation.upper()
        if(operation == 'LOAD'):
            return '000010'
        elif(operation == 'STORE' and addressingMode != '00'):
            return '000011'
        elif(operation == 'ADD'):
            return '000100'
        elif(operation == 'SUB'):
            return '000101'
        elif(operation == 'INC'):
            return '000110'
        elif(operation == 'DEC'):
            return '000111'
        elif(operation == 'XOR'):
            return '001000'
        elif(operation == 'AND'):
            return '001001'
        elif(operation == 'OR'):
            return '001010'
        elif(operation == 'NOT'):
            return '001011'
        elif(operation == 'SHL' and addressingMode == '01'):
            return '001100'
        elif(operation == 'SHR' and addressingMode == '01'):
            return '001101'
        elif(operation == 'PUSH' and addressingMode == '01'):
            return '001111'
        elif(operation == 'POP' and addressingMode == '01'):
            return '010000'
        elif(operation == 'CMP'):
            return '010001'
        elif(operation == 'JMP' and addressingMode == '00'):
            return '010010'
        elif( (operation == 'JZ' or operation =='JE') and addressingMode == '00'):
            return '010011'
        elif((operation == 'JNZ' or operation == 'JNE') and addressingMode == '00'):
            return '010100'
        elif(operation == 'JC' and addressingMode == '00'):
            return '010101'
        elif(operation == 'JNC' and addressingMode == '00'):
            return '010110'
        elif(operation == 'JA' and addressingMode == '00'):
            return '010111'
        elif(operation == 'JAE' and addressingMode == '00'):
            return '011000'
        elif(operation == 'JB' and addressingMode == '00'):
            return '011001'
        elif(operation == 'JBE' and addressingMode == '00'):
            return '011010'
        elif(operation == 'READ' and addressingMode != '00'):
            return '011011'
        elif(operation == 'PRINT'):
            return '011100'
        elif(operation == 'NOP' or operation == 'HALT'):
            print("Invalid operation. It consists of NOP/HALT and an operand.")
            return False
        else:
            print("Invalid opcode")
            return False

  

