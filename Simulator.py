import sys
# input = "input.txt"
# output = "output.txt"

input = sys.argv[1]
output = sys.argv[2]

abi_to_register = {"zero":"x0","ra":"x1","sp":"x2","gp":"x3","tp":"x4","t0":"x5","t1":"x6","t2":"x7","s0":"x8","fp":"x8","s1":"x9","a0":"x10","a1":"x11","a2":"x12","a3":"x13","a4":"x14","a5":"x15","a6":"x16","a7":"x17","s2":"x18","s3":"x19","s4":"x20","s5":"x21","s6":"x22","s7":"x23","s8":"x24","s9":"x25","s10":"x26","s11":"x27","t3":"x28","t4":"x29","t5":"x30","t6":"x31"}
registers = ['x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12', 'x13', 'x14', 'x15', 'x16', 'x17', 'x18', 'x19', 'x20', 'x21', 'x22', 'x23', 'x24', 'x25', 'x26', 'x27', 'x28', 'x29', 'x30', 'x31']

r_dict = ['add','sub','slt','srl','or','and']
i_dict = ['lw','addi','jalr']
b_dict = ['beq','bne','blt']

regs = [0, 0, 380, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
memory_dict = {"0x00010000": 0, "0x00010004": 0, "0x00010008": 0, "0x0001000C": 0, "0x00010010": 0, "0x00010014": 0, "0x00010018": 0, "0x0001001C": 0, "0x00010020": 0, "0x00010024": 0, "0x00010028": 0, "0x0001002C": 0, "0x00010030": 0, "0x00010034": 0, "0x00010038": 0, "0x0001003C": 0, "0x00010040": 0, "0x00010044": 0, "0x00010048": 0, "0x0001004C": 0, "0x00010050": 0, "0x00010054": 0, "0x00010058": 0, "0x0001005C": 0, "0x00010060": 0, "0x00010064": 0, "0x00010068": 0, "0x0001006C": 0, "0x00010070": 0, "0x00010074": 0, "0x00010078": 0, "0x0001007C": 0
}

stack_dict = {"0x00000100": 0, "0x00000104": 0, "0x00000108": 0, "0x0000010C": 0,"0x00000110": 0, "0x00000114": 0, "0x00000118": 0, "0x0000011C": 0,"0x00000120": 0, "0x00000124": 0,"0x00000128": 0, "0x0000012C": 0,"0x00000130": 0, "0x00000134": 0, "0x00000138": 0, "0x0000013C": 0,"0x00000140": 0, "0x00000144": 0, "0x00000148": 0, "0x0000014C": 0,"0x00000150": 0, "0x00000154": 0, "0x00000158": 0, "0x0000015C": 0,"0x00000160": 0, "0x00000164": 0, "0x00000168": 0, "0x0000016C": 0,"0x00000170": 0, "0x00000174": 0, "0x00000178": 0, "0x0000017C": 0
}

def bin_to_imm(binary_str):
    bits = len(binary_str)  
    num = int(binary_str, 2) 
  
    if binary_str[0] == '1':
        num -= 2**bits
    return num

def unsigned_bin_to_imm(st):
    num = int(st,2)
    return num

def hexa(n):
    result = f'{n:x}'
    result = [i for i in result]
    for i in range(len(result)):
        if result[i].isalpha():
            result[i] = result[i].upper()
    result = ''.join(result)
    l= len(result)
    final=''
    for i in range(0,8-l):
        final= final+'0'
    result='0x'+final+result
    return result

def bin(n):
    if n < 0:
        result = format(n & (2**32 - 1), f'0{32}b')  
        result = '0b' + result
    else:    
        result = f'{n:b}'
        l= len(result)
        zero=''
        for i in range(0,32-l):
            zero=zero+'0'
        result= '0b'+ zero+ result
    return result

def sext(st,bits = 32):
    x = st[0]
    n = bits - len(st)
    st = x*n + st
    return (st)
    

def b_type(st,PC):
    rs2 = st[7:12]
    rs1 = st[12:17]
    rs1 = unsigned_bin_to_imm(rs1)
    rs2 = unsigned_bin_to_imm(rs2)
    f3 = st[17:20]
    imm = st[0] + st[24] + st[1:7] + st[20:24] + '0'

    if f3 == "000":
        PC = PC + bin_to_imm(sext(imm)) if regs[rs2] == regs[rs1] else PC + 4
    elif f3 == "001":
        PC = PC + bin_to_imm(sext(imm)) if regs[rs2] != regs[rs1] else PC + 4
    elif f3 == "100":
        PC = PC + bin_to_imm(sext(imm)) if regs[rs2] < regs[rs1] else PC + 4
    else:
        print("ERROR")
        exit()
    return PC
        
def s_type(s):
    imm1 = s[0:7]
    rs2 = s[7:12]
    rs1 = s[12:17]
    func3 = s[17:20]
    imm2 = s[20:25]
    imm = imm1+imm2
    rs1 = unsigned_bin_to_imm(rs1)
    rs2 = unsigned_bin_to_imm(rs2)
    imm = bin_to_imm(imm)
    if func3 != "010":
        print("ERROR")
        exit()
    if (hexa(regs[rs1] + imm)) in memory_dict:
        memory_dict[hexa(regs[rs1] + imm)] = regs[rs2]
    elif (hexa(regs[rs1] + imm)) in stack_dict:
        stack_dict[hexa(regs[rs1] + imm)] = regs[rs2]
    else:
        print("ERROR")
        exit()
        
        
def j_type(st,PC):
    rd= st[20:25]
    imm = st[0] + st[12:20] + st[11] + st[1:11] +'0'
    rd= unsigned_bin_to_imm(rd)
    regs[rd]= PC +4
    PC= PC + bin_to_imm(sext(imm))
    return PC
    
def r_type(s):
    rd = s [20:25]
    rs1 = s[12:17]
    rs2 = s[7:12]
    func3 = s[17:20]
    funct7 = s[:7]
    rs1 = unsigned_bin_to_imm(rs1)
    rs2 = unsigned_bin_to_imm(rs2)
    rd = unsigned_bin_to_imm(rd)
    a = regs[rs1]
    b = regs[rs2]
    
    if func3 == '000':
        if funct7 == '0100000':
            k = a-b
            regs[rd] = k
        elif funct7 == '0000000':
            k = a+b
            regs[rd] = k
        else:
            print("ERROR")
            exit()
    elif func3 == '110' and funct7 == '0000000':
        k = a|b
        regs[rd] = k
    elif func3 == '111' and funct7 == '0000000':
        k = a&b
        regs[rd] = k
    elif func3 == '010' and funct7 == '0000000':
        if a < b:
            k = 1
            regs[rd] = k
    elif func3 == '101' and funct7 == '0000000':
        
        k = a>>(b%32)
        regs[rd] = k
    else: 
        print("ERROR")
        exit()
        
def i_type(s,PC):
    imm = s[0:12]
    rs = s[12:17]
    f3 = s[17:20]
    rd = s[20:25]
    rs = unsigned_bin_to_imm(rs)
    rd = unsigned_bin_to_imm(rd)
    imm = bin_to_imm(imm)
    
    if s [-7:] == '0000011' and f3 == '010':
        if (hexa(regs[rs] + imm)) in memory_dict:
            regs[rd] = memory_dict[hexa(regs[rs] + imm)]
        elif (hexa(regs[rs] + imm)) in stack_dict:
            regs[rd] = stack_dict.get(hexa(regs[rs] + imm),0)
        else:
            print("ERROR")
            exit()
            
    elif s[-7:] == '0010011' and f3 == '000':
        regs[rd]= regs[rs]+(imm)    
        
    elif s[-7:] == '1100111' and f3 == '000':
        PC3 = PC
        PC= (regs[rs]+ (imm))
        regs[rd]= PC3+4
        return PC

    else:
        print("ERROR")
        exit()
        
    return PC + 4

def mul(s):
    rd = s [20:25]
    rs1 = s[12:17]
    rs2 = s[7:12]
    func3 = s[17:20]
    funct7 = s[:7]
    rs1 = unsigned_bin_to_imm(rs1)
    rs2 = unsigned_bin_to_imm(rs2)
    rd = unsigned_bin_to_imm(rd)
    a = regs[rs1]
    b = regs[rs2]
    regs[rd] = a*b 

def rst():
    for i in range(32):
        regs[i] = 0
    regs[2] = 380
    
def rvrs(s):
    rd = s[20:25]
    rs1 = s[12:17]
    rs1 = unsigned_bin_to_imm(rs1)
    rd = unsigned_bin_to_imm(rd)
    x1 = bin(regs[rs1])[2:]
    x = ""
    for i in x1:
        x = i + x
    
    regs[rd] = bin_to_imm(x)
    
    
try:
    file = open(input,'r')
    lines = []
    line = file.readline()
    i = 0
    while line:
        if line == "" or line == "\n":
            line = file.readline()
            continue     
        if '\n' in line:
            line = line[:-1]
        if len(line) != 32:
            print("ERROR")
            exit()
        lines.append(line)
        line = file.readline()
        i += 1
    file.close()

    global PC
    PC = 0

    file = open(output,'w')
    while(1):
        PC2 = PC
        i = lines[(PC)//4]
        op= i[-7:]
        if op=='0110011':
            r_type(i)
            PC += 4
        elif op in [ '0000011' , '0010011' , '1100111'] :
            PC = i_type(i,PC)
        elif op=='0100011':
            s_type(i)
            PC += 4
        elif op=='1100011':
            PC = b_type(i,PC)
        elif op=='1101111':
            PC = j_type(i,PC)
        elif op == '1110111':
            func3 = i[17:20]
            if func3 == '000':
                mul(i)
                PC += 4
            elif func3 == '001':
                rst()
                PC += 4
            elif func3 == '010':
                PC = PC
            elif func3 == '011':
                rvrs(i)
                PC += 4
        else:
            print("ERROR")
            exit()
        if PC % 4 != 0:
            print("ERROR")
            exit()
        file.write(str(bin(PC)) + ' ')
        regs[0] = 0
        for i in regs:
            file.write(str(bin(i))+" ")
        if PC == PC2:
            file.write('\n')
            break
        file.write('\n')
    for i in memory_dict:
        file.write(f"{i}:{bin(memory_dict[i])}")
        file.write('\n')
    file.close()
except:
    print("ERROR")
    exit()
