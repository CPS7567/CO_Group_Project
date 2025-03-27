import sys
input = "input.txt"
output = "output.txt"

abi_to_register = {"zero":"x0","ra":"x1","sp":"x2","gp":"x3","tp":"x4","t0":"x5","t1":"x6","t2":"x7","s0":"x8","fp":"x8","s1":"x9","a0":"x10","a1":"x11","a2":"x12","a3":"x13","a4":"x14","a5":"x15","a6":"x16","a7":"x17","s2":"x18","s3":"x19","s4":"x20","s5":"x21","s6":"x22","s7":"x23","s8":"x24","s9":"x25","s10":"x26","s11":"x27","t3":"x28","t4":"x29","t5":"x30","t6":"x31"}
registers = ['x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12', 'x13', 'x14', 'x15', 'x16', 'x17', 'x18', 'x19', 'x20', 'x21', 'x22', 'x23', 'x24', 'x25', 'x26', 'x27', 'x28', 'x29', 'x30', 'x31']

r_dict = ['add','sub','slt','srl','or','and']
i_dict = ['lw','addi','jalr']
b_dict = ['beq','bne','blt']

regs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
memory_dict = {"0x00010000": 0, "0x00010004": 0, "0x00010008": 0, "0x0001000C": 0, "0x00010010": 0, "0x00010014": 0, "0x00010018": 0, "0x0001001C": 0, "0x00010020": 0, "0x00010024": 0, "0x00010028": 0, "0x0001002C": 0, "0x00010030": 0, "0x00010034": 0, "0x00010038": 0, "0x0001003C": 0, "0x00010040": 0, "0x00010044": 0, "0x00010048": 0, "0x0001004C": 0, "0x00010050": 0, "0x00010054": 0, "0x00010058": 0, "0x0001005C": 0, "0x00010060": 0, "0x00010064": 0, "0x00010068": 0, "0x0001006C": 0, "0x00010070": 0, "0x00010074": 0, "0x00010078": 0, "0x0001007C": 0}

# def twos_complement_to_decimal(binary_str):
#     binary_str = binary_str.strip()
#     bits = len(binary_str)  
#     num = int(binary_str, 2) 
  
#     if binary_str[0] == '1':
#         num -= 2**bits
    
#     return num

def bin_to_imm(binary_str):
    """Convert a binary string (two's complement) back to an integer."""
    bits = len(binary_str)  
    num = int(binary_str, 2) 
  
    if binary_str[0] == '1':
        num -= 2**bits
    
    return num

def sext(st,bits = 32):
    x = st[0]
    n = bits - len(st)
    st = x*n + st
    return (st)
    

def b_type(st,PC,regs = regs):
    rs2 = st[7:12]
    rs1 = st[12:17]
    rs1 = bin_to_imm(rs1)
    rs2 = bin_to_imm(rs2)
    f3 = st[17:20]
    imm = st[0] + st[24] + st[1:7] + st[20:24]

    if f3 == "000":
        PC = PC + bin_to_imm(sext(imm)) if regs[rs2] == regs[rs1] else PC + 4
    elif f3 == "001":
        PC = PC + bin_to_imm(sext(imm)) if regs[rs2] != regs[rs1] else PC + 4
    elif f3 == "100":
        PC = PC + bin_to_imm(sext(imm)) if regs[rs2] < regs[rs1] else PC + 4

file = open(input,'r')
lines = []
line = file.readline()
i = 0
while line:
    if '\n' in line:
        line = line[:-1]
    lines.append(line)
    line = file.readline()
    i += 1
file.close()

b_type("00000010011101010000001001100011",0)


