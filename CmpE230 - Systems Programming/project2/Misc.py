
# parameter for testing purposes
FILL_BIN = 16

## Conversion

def decToBin(dec):
    if dec >= 0:
        return bin(dec)[2:].zfill(FILL_BIN)
    else:
        return bin(2**FILL_BIN + dec)[2:]

def hexToDec(hex):
    binary = hexToBin(hex)
    l = len(binary)
    if binary[0] == '1':
        return -(2**l - int(binary, 2))
    else:
        return int(binary, 2)

def hexToBin(hex):
    return bin(int(hex, 16))[2:].zfill(len(hex)*4)

def binToHex(bin):
    return hex(int(bin, 2))[2:].zfill(int(len(bin)/4))

## Arithmetic

def addToHex(value, add):
    return hex(int(value, 16) + add)[2:].zfill(int(FILL_BIN / 4))

def subFromHex(value, sub):
    return hex(int(value, 16) - sub)[2:].zfill(int(FILL_BIN / 4))

# input: dec, ouptut: dec
def notOperation(dec):
    a = decToBin(dec)
    A = ['1' if i == '0' else '0' for i in a]

    result = "".join(A)
    result = twos_comp(int(result,2), 16)

    SF = (A[0] == '1') 
    ZF = (result == 0)
        
    flags = [SF, ZF]
    return (result, flags)
    

# input: dec: output: dec
def xorOperation(dec1, dec2):
    a = decToBin(dec1)
    b = decToBin(dec2)
    
    A = ['1' if (i == '0' and j == '1') or(i == '1' and j =='0') else '0' for (i, j) in zip(a, b)]

    result = "".join(A)
    result = twos_comp(int(result,2), 16)

    SF = (A[0] == '1') 
    ZF = (result == 0)
        
    flags = [SF, ZF]
    return (result, flags)

# input: dec: output: dec
def andOperation(dec1, dec2):
    a = decToBin(dec1)
    b = decToBin(dec2)

    A = ['1' if (i == '1' and j == '1')  else '0' for (i, j) in zip(a, b)]

    result = "".join(A)
    result = twos_comp(int(result,2), 16)

    SF = (A[0] == '1') 
    ZF = (result == 0)
        
    flags = [SF, ZF]
    return (result, flags)

# input: dec: output: dec
def orOperation(dec1, dec2):
    a = decToBin(dec1)
    b = decToBin(dec2)

    A = ['1' if (i == '1' or j == '1')  else '0' for (i, j) in zip(a, b)]

    result = "".join(A)
    result = twos_comp(int(result,2), 16)

    SF = (A[0] == '1') 
    ZF = (result == 0)
        
    flags = [SF, ZF]
    return (result, flags)

def shrOperation(dec1):
    a = decToBin(dec1)
    A = '0' + a[:15] # shift right

    result = "".join(A)
    result = twos_comp(int(result,2), 16)

    SF = (A[0] == '1')  # impossible
    ZF = (result == 0)
        
    flags = [SF, ZF]
    return (result, flags)

def shlOperation(dec1):
    a = decToBin(dec1)

    A = a[1:] + '0'

    result = "".join(A)
    result = twos_comp(int(result,2), 16)
    
    SF = (A[0] == '1')
    ZF = (result == 0)
    CF = (a[0] == '1')  # (n+1). bit
        
    flags = [SF, ZF, CF]
    return (result, flags)


def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is

# Use addOperation for both addition and subtraction. For subtraction, a - b = a + not(b) + 1
# input: a, b (decimal - positive)   output: CF (boolen), c (decimal) 
def addOperation(a, b):
    a = decToBin(a)
    b = decToBin(b)
    
    result = ['0' for i in range(16)]
    carry = 0

    for i in range(15, -1, -1):
        if(a[i] == '0' and b[i] == '0'):
            if(carry):
                result[i] = '1'
                carry = 0
            else:
                result[i] = '0'
        elif(a[i] == '1' and b[i] == '1'):
            if(carry):
                result[i] = '1'
            else:
                result[i] = '0'
                carry = 1
        else:  # a[i] is 1 xor b[i] is 1
            if(carry):
                result[i] = '0'
            else:
                result[i] = '1'


    c = "".join(result)
    c = twos_comp(int(c, 2), 16)

    SF = (result[0] == '1')
    CF = carry == 1
    ZF = (c == 0)

    
    flags = [SF, ZF, CF]
    return (c, flags)



