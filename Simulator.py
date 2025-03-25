import sys
input = "input.txt"
output = "output.txt"

abi_to_register = {"zero":"x0","ra":"x1","sp":"x2","gp":"x3","tp":"x4","t0":"x5","t1":"x6","t2":"x7","s0":"x8","fp":"x8","s1":"x9","a0":"x10","a1":"x11","a2":"x12","a3":"x13","a4":"x14","a5":"x15","a6":"x16","a7":"x17","s2":"x18","s3":"x19","s4":"x20","s5":"x21","s6":"x22","s7":"x23","s8":"x24","s9":"x25","s10":"x26","s11":"x27","t3":"x28","t4":"x29","t5":"x30","t6":"x31"}
registers = ['x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12', 'x13', 'x14', 'x15', 'x16', 'x17', 'x18', 'x19', 'x20', 'x21', 'x22', 'x23', 'x24', 'x25', 'x26', 'x27', 'x28', 'x29', 'x30', 'x31']

r_dict = ['add','sub','slt','srl','or','and']
i_dict = ['lw','addi','jalr']
b_dict = ['beq','bne','blt']


def b_type(st,PC):
    pass



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