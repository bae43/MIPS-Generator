# MIPSgen.py
# Bryce Evans

import sys
import random as r

class ref:
    def __init__(self, obj): self.obj = obj
    def get(self):    return self.obj
    def set(self, obj):      self.obj = obj
    
#registers
r = [0,0,0,0,0,0,0,0]
##rDict = {0:ref(r[0]), 1:ref(r[1]), 2:ref(r[2]), 3:ref(r[3]),
##         4:ref(r[4]), 5:ref(r[5]), 6:ref(r[6]), 7:ref(r[7])}


def program(f):
    f.write(SET(1,100))
    f.write(SET(2,200))
    f.write(ADDIU(3,2,50))
    f.write(SUB(4,3,2))
    f.write(SET(5,123))
    f.write(SUB(6,5,1))
    f.write(XOR(7,5,6))
    return

# returns binary string of integer, allows for negatives
# returns 16 bits unless reg is True
# requires: if reg = true -> integer cannot be negative
def getBin(integer, reg = False):
    
    if integer >= 0:
        ret = bin(integer)[2:]
    else:        
        ret = bin(integer & 0b1111111111111111)[3:]
    
    if reg:
        return (5-len(ret))*"0" + ret
    else:
        return (16-len(ret))*"0" + ret

# returns string(NOT a)
def invert(a):
    return''.join('1' if x == '0' else '0' for x in a)

# returns random 15 bit integer
def randInt():
    return round(random.random()*2**15)

#sets register reg to value val
def setReg(reg,val):
    if reg == 0:
        print("SET R0 -> ERROR")
    elif reg >= 1 and reg <= 7:
        r[reg] = val
    else:
        print("ATTEMPTED SET OF INVALID REGISTER " + str(reg))
    return

#returns value of register reg
def getReg(reg):
##    if reg < 8:
##        return rDict[reg].get()
    if reg >= 0 and reg <= 7:
        return r[reg]
    else:
        print("ATTEMPTED GET OF INVALID REGISTER " + str(reg))
        return

#returns a string representation of the current value of all registers
def string_of_regs():
    return ("r0: " + str(r[0]) +"\nr1: " + str(r[1]) +"\nr2: " +str(r[2]) +"\nr3: " + str(r[3]) +
            "\nr4: " + str(r[4]) + "\nr5: " + str(r[5]) +"\nr6: " + str(r[6]) +"\nr7: " + str(r[7]))
    
    
#sets register reg to 0
def CLEAR(reg):
    setReg(reg,0)
    op = "001100"
    t = getBin(reg,True)
    s = getBin(0,True)
    i = "0"*16
    return op + s + t + i + "\n"

# sets register reg to value val
def SET(reg,val):
    setReg(reg,val)
    return CLEAR(reg) + "\n" + ADDIU(reg,0,val) + "\n"


def ADD(dest, reg1, reg2):
    setReg(dest,getReg(reg1)+getReg(reg2))
    op = "000000"
    return op +  getBin(reg1,True) + getBin(reg2,True) + getBin(dest,True) + "00000100000\n"

def ADDI(dest, reg, num):
    setReg(dest,getReg(reg)+num)
    op = "001000"
    return op +  getBin(reg,True) + getBin(dest,True) + getBin(num) + "\n"

def ADDIU(dest, reg, num):
    setReg(dest,getReg(reg)+num)
    op = "001001"
    return op +  getBin(reg,True) + getBin(dest,True) + getBin(num) + "\n"

def SUB(dest, reg1, reg2):
    setReg(dest,getReg(reg1)-getReg(reg2))
    op = "000000"
    return op +  getBin(reg1,True) + getBin(reg2,True) + getBin(dest,True) + "00000100010\n"

def SUBU(dest, reg1, reg2):
    setReg(dest,getReg(reg1)-getReg(reg2))
    op = "000000"
    return op +  getBin(reg1,True) + getBin(reg2,True) + getBin(dest,True) + "00000100011\n"

def OR(dest, reg1, reg2):
    setReg(dest,getReg(reg1) | getReg(reg2))
    op = "000000"
    return op +  getBin(reg1,True) + getBin(reg2,True) + getBin(dest,True) + "00000100101\n"

def XORI(dest, reg1, val):
    setReg(dest,getReg(reg1) | val)
    op = "001101"
    return op +  getBin(reg1,True) +  getBin(dest,True) + getBin(val) +"\n"

def XOR(dest, reg1, reg2):
    setReg(dest,getReg(reg1) ^ getReg(reg2))
    op = "000000"
    return op +  getBin(reg1,True) + getBin(reg2,True) + getBin(dest,True) + "00000100110\n"

def XORI(dest, reg1, val):
    setReg(dest,getReg(reg1) ^ val)
    op = "001110"
    return op +  getBin(reg1,True) +  getBin(dest,True) + getBin(val) +"\n"

def writeTest(f):
    program(f)
    f.write("\n \n REGISTER VALUES: \n")
    f.write(string_of_regs())

def main():
    if len(sys.argv) != 2:
        print(len(sys.argv))
        sys.stderr.write("Usage: %s out.txt\n" % sys.argv[0])
        sys.exit(1)

    f = open(sys.argv[1]+".txt", 'w')
    writeTest(f)
    
    f.close()
    
if __name__ == "__main__":
    main()
