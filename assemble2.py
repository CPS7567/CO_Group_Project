
def bin_to_imm(binary_str):
    """Convert a binary string (two's complement) back to an integer."""
    bits = len(binary_str)  
    num = int(binary_str, 2) 
  
    if binary_str[0] == '1':
        num -= 2**bits
    
    return num

def imm_to_bin(x ,bits = 12):
    num = int(x) 
    
    twos_complement = format(num & (2**bits - 1), f'0{bits}b')  
    return twos_complement


ans_values  = {
    'x0': 0, 'x1': 0, 'x2': 0, 'x3': 0, 'x4': 0, 'x5': 0, 'x6': 0, 'x7': 0, 
    'x8': 0, 'x9': 0, 'x10': 0, 'x11': 0, 'x12': 0, 'x13': 0, 'x14': 0, 'x15': 0, 
    'x16': 0, 'x17': 0, 'x18': 0, 'x19': 0, 'x20': 0, 'x21': 0, 'x22': 0, 'x23': 0, 
    'x24': 0, 'x25': 0, 'x26': 0, 'x27': 0, 'x28': 0, 'x29': 0, 'x30': 0, 'x31': 0
}

register_dict = {
    0: 'x0', 1: 'x1', 2: 'x2', 3: 'x3', 4: 'x4', 5: 'x5', 6: 'x6', 7: 'x7',
    8: 'x8', 9: 'x9', 10: 'x10', 11: 'x11', 12: 'x12', 13: 'x13', 14: 'x14', 15: 'x15',
    16: 'x16', 17: 'x17', 18: 'x18', 19: 'x19', 20: 'x20', 21: 'x21', 22: 'x22', 23: 'x23',
    24: 'x24', 25: 'x25', 26: 'x26', 27: 'x27', 28: 'x28', 29: 'x29', 30: 'x30', 31: 'x31'
}



# r_dict = ['add','sub','slt','srl','or','and']  
i_dict = ['lw','addi','jalr']     

b_dict = ['beq','bne','blt']

s_dict = ['sw'] 

j_dict = [ 'jal']

def rtype(s):
    rd = s [20:25]
    rs = s[12:17]
    rs2 = s[7:12]
    func3 = s[17:20]
    funct7 = s[:7]
    rs = bin_to_imm(rs)
    rs2 = bin_to_imm(rs2)
    rd = bin_to_imm(rd)
    a = register_dict[rs]
    b = register_dict[rs2]
    c = register_dict[rd]
    a = ans_values[a]
    b = ans_values[b]
    if func3 == '000':
        if funct7 == '0100000':
            k = a-b
            ans_values[c] = k
        else:
            k = a+b
            ans_values[c] = k
    elif func3 == '110':
        k = a|b
        ans_values[c] = k
    elif func3 == '111':
        k = a&b
        ans_values[c] = k
    elif func3 == '010':
        if a < b:      # slttttttttttt
            k = 1
            ans_values[c] = k
    elif func3 == '101':
          ###       srllllllllllllllllllll
          pass
    

global pc 
pc = 0

def itype(s):
    imm = s[0:12]
    rs = s[12:17]
    funct3 = s[17:20]
    rd = s[20:25]
    rs = bin_to_imm(rs)
    rd = bin_to_imm(rd)
    imm = bin_to_imm(imm)
    a = register_dict[rs]
    c = register_dict[rd]
    a = ans_values[a]
    if s [-7:] == '0000011':
        # lwwwwww
        pass
    elif s[-7:] == '0010011':
        # rd = rs + sext(imm)
        k = a+imm
        ans_values[c] = k
        # adiiiiiiii
        pass
    elif s[-7:] == '1101111':
        # ans_values[c] = pc+4
        # jalrrrrrr
        pass

def stype(s):
    imm1 = s[0:7]
    rs2 = s[7:12]
    rs1 = s[12:17]
    func3 = s[17:20]
    imm2 = s[20:25]
    imm = imm1+imm2
    rs1 = bin_to_imm(rs1)
    rs2 = bin_to_imm(rs2)
    imm = bin_to_imm(imm)
    reg = register_dict[rs1]
    reg2 = register_dict[rs2]
    #  k = # calculate mem( reg + sext (imm))
    ans_values[reg2] = k # storing the final value in ans_values
    

lst = ["00000010011101010000001001100011"]

for i in lst :
    k = i[-7:]
    if k == '0110011':
        rtype()
        pass
    elif k == '1100011':
        # b_type()
        pass
    elif k == '0100011':
        stype()
        pass
    elif k == '1101111':
        # jtype()
        pass
    elif k in [ '0000011' , '0010011' , '1100111'] :
        itype()
        pass
    else:
        print("erros")



# 0000000       01010    00000       000          01010        0010011


# 00000000000000000000001010010011
# 00000000000100000000001100010011
# 00000000000100000000001110010011
# 00000010000001010000001001100011
# 00000010011101010000001001100011
# 00000000011000101000010110110011
# 00000000000000110000001010010011
# 00000000000001011000001100010011
# 00000000000100111000001110010011
# 11111110101000111001100011100011
# 00000101110100000000100010010011
# 00000000000000000000010100010011
# 00000000000000000000010110010011
# 00000000000100000000010110010011
# 00000000000000000000000001100011