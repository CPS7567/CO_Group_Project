import sys
input_file = sys.argv[1]
output_file = sys.argv[2]


abi_to_register = {"zero":"x0","ra":"x1","sp":"x2","gp":"x3","tp":"x4","t0":"x5","t1":"x6","t2":"x7","s0":"x8","fp":"x8","s1":"x9","a0":"x10","a1":"x11","a2":"x12","a3":"x13","a4":"x14","a5":"x15","a6":"x16","a7":"x17","s2":"x18","s3":"x19","s4":"x20","s5":"x21","s6":"x22","s7":"x23","s8":"x24","s9":"x25","s10":"x26","s11":"x27","t3":"x28","t4":"x29","t5":"x30","t6":"x31"}
registers = ['x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12', 'x13', 'x14', 'x15', 'x16', 'x17', 'x18', 'x19', 'x20', 'x21', 'x22', 'x23', 'x24', 'x25', 'x26', 'x27', 'x28', 'x29', 'x30', 'x31']


r_dict = ['add','sub','slt','srl','or','and']
i_dict = ['lw','addi','jalr']
b_dict = ['beq','bne','blt']


def regis_to_bin(x):
    y = ''
    while x != 0:
        k = x%2
        y += str(k)
        x = x//2
    return y[::-1] , len(y)


def imm_to_bin(x ,bits = 12):
    num = int(x) 
    
    twos_complement = format(num & (2**bits - 1), f'0{bits}b')  
    return twos_complement


def s_type(ins,ops,index):
    try:
        ops = ops.split(',')
        ops[1:2] = ops[1].split('(')
        ops[0] = ops[0].strip()
        ops[1] = ops[1].strip()
        ops[2] = ops[2].strip(" )")
        if ops[0] not in registers:
            ops[0] = abi_to_register[ops[0]]
        if ops[2] not in registers:
            ops[2] = abi_to_register[ops[2]]
        ops[0] = int(ops[0][1:])
        ops[2] = int(ops[2][1:])
        result = ""
        rs2,n = regis_to_bin(ops[0])
        while(len(rs2) < 5):
            rs2 = '0' + rs2
        imm = imm_to_bin(ops[1])
        rs1,n = regis_to_bin(ops[2])
        while(len(rs1) < 5):
            rs1 = '0' + rs1
        result = imm[0:7] + rs2 + rs1 + '010' + imm[7:] + '0100011'
        return result
    except:
        print(f"ERROR at line {index+1}")
        return f"ERROR at line {index+1}"


def r_type(a,l,index):
    try:
        l = l.split(',')
        b,c,d = l[0], l[1], l[2]
        r_type = {'add' : {'funct7' : '0000000' , 'funct3' : '000' , 'opcode' : '0110011'} , 'sub' : {'funct7' : '0100000' , 'funct3' : '000' , 'opcode' : '0110011'} ,
        'slt' : {'funct7' : '0000000' , 'funct3' : '010' , 'opcode' : '0110011'} , 
        'srl' : {'funct7' : '0000000' , 'funct3' : '101' , 'opcode' : '0110011'} , 'or' : {'funct7' : '0000000' , 'funct3' : '110' , 'opcode' : '0110011'} ,
        'and' : {'funct7' : '0000000' , 'funct3' : '111' , 'opcode' : '0110011'}}
        k = r_type[a]

        if b in abi_to_register or b in registers:
            b = abi_to_register[b] if b in abi_to_register else b
            b = int(b[1:])
            b ,i = regis_to_bin(b) 
            b = '0'*(5-i) + b
        else:
            print (f"ERROR at line {index+1}")
            return f"ERROR at line {index+1}"
        if c in abi_to_register or c in registers:
            c = abi_to_register[c] if c in abi_to_register else c
            c = int(c[1:])
            c ,i= regis_to_bin(c) 
            c = '0'*(5-i) + c
        else:
            print (f"ERROR at line {index+1}")
            return f"ERROR at line {index+1}"
        if d in abi_to_register or d in registers:
            d = abi_to_register[d] if d in abi_to_register else d
            d = int(d[1:])
            d , i = regis_to_bin(d)
            d = '0'*(5-i) + d
        else:
            print (f"ERROR at line {index+1}")
            return f"ERROR at line {index+1}"
        t = f"{k['funct7']}{d}{c}{k['funct3']}{b}{k['opcode']}"

        return t
    except:
        print(f"ERROR at line {index+1}")
        return f"ERROR at line {index+1}"


def i_type(a,l,index):
    try:
        i_type = {'lw' : {'funct3' : '010' , 'opcode' : '0000011'} , 'addi' : {'funct3' : '000' , 'opcode' : '0010011'} ,
                'jalr' : {'funct3' : '000' , 'opcode' : '1100111'} }
        k = i_type[a]

        if a == 'lw':
            t = l.split(',')
            b  , c= t[0] , t[1]
            c = c.split('(')
            imm = c[0]
            q = c[1].rstrip(')')
        else:
            t = l.split(",")
            b,q ,imm= t[0] , t[1], t[2]
        if b in abi_to_register or b in registers:
            b = abi_to_register[b] if b in abi_to_register else b
            b = int(b[1:])
            b ,i = regis_to_bin(b) 
            b = '0'*(5-i) + b
        else:
            print (f"ERROR at line {index+1}")
            return f"ERROR at line {index+1}"
        if q in abi_to_register or q in registers:
            q = abi_to_register[q] if q in abi_to_register else q
            q = int(q[1:])
            q, i = regis_to_bin(q)
            q = '0' * (5 - i) + q
        else:
            print (f"ERROR at line {index+1}")
            return f"ERROR at line {index+1}"
        if imm.isdigit() or '-' in imm: 
            imm = imm_to_bin(imm)

        t = f"{imm}{q}{k['funct3']}{b}{k['opcode']}"

        return t 
    except:
        print(f"ERROR at line {index+1}")
        return f"ERROR at line {index+1}"
        

def b_type(a,l,index):
    try:
        b_type = {"beq" : {'funct3' : '000' , 'opcode' : '1100011'}, "bne" : {'funct3' : '001' , 'opcode' : '1100011'},
                'blt' : {'funct3' : '100' , 'opcode' : '1100011'} }
        
        k = b_type[a]
        l  = l.split(',')
        b,c,imm = l[0] , l[1] , l[2]
        
        if b in abi_to_register or b in registers:
            b = abi_to_register[b] if b in abi_to_register else b
            b = int(b[1:])
            b ,i = regis_to_bin(b) 
            b = '0'*(5-i) + b
        else:
            print (f"ERROR at line {index+1}")
            return f"ERROR at line {index+1}"
        if c in abi_to_register or c in registers:
            c = abi_to_register[c] if c in abi_to_register else c
            c = int(c[1:])
            c ,i= regis_to_bin(c) 
            c = '0'*(5-i) + c
        else:
            print (f"ERROR at line {index+1}")
            return f"ERROR at line {index+1}"
        if imm.isdigit() or '-' in imm: 
            imm = imm_to_bin(imm,13)
        else:
            if imm in labels:
                imm = labels[imm] - index
                imm *= 4
                imm = imm_to_bin(imm,13)
            else:
                print (f"ERROR at line {index+1}")
                return f"ERROR at line {index+1}"
        
        t = f"{imm[0]}{imm[2:8]}{c}{b}{b_type[a]['funct3']}{imm[8:12]}{imm[1]}{b_type[a]['opcode']}"
        return t
    except:
        print(f"ERROR at line {index+1}")
        return f"ERROR at line {index+1}"


def j_type(a,l,index):
    try:
        j_type = {"jal" :{ 'opcode' : '1101111'}}
        l = l.split(',')
        b = l[0]
        if b in abi_to_register or b in registers:
            b = abi_to_register[b] if b in abi_to_register else b
            b = int(b[1:])
            b ,i = regis_to_bin(b) 
            b = '0'*(5-i) + b
        else:
            print (f"ERROR at line {index+1}")
            return f"ERROR at line {index+1}"
        imm = l[1]
        
        if imm.isdigit() or '-' in imm: 
            num = int(imm) 
            bits = 21
            imm = format(num & (2**bits - 1), f'0{bits}b')
        else:
            if imm in labels:
                imm = labels[imm] - index
                imm *= 4
                num = int(imm)
                bits = 21
                imm = format(num & (2**bits - 1), f'0{bits}b')
            else:
                print(f"ERROR at line {index+1}")
                return f"ERROR at line {index+1}"
        imm = imm[0] + imm[10:20] + imm[9] + imm[1:9]
        t = f"{imm}{b}{j_type['jal']['opcode']}"
        return t
    except:
        print(f"ERROR at line {index+1}")
        return f"ERROR at line {index+1}"


file = open(input_file,'r')
lines = []
line = file.readline()
labels = {}
i = 0
while line:
    if '\n' in line:
        line = line[:-1]
    if ":" in line:
        line = line.split(":")
        line[0] = line[0].strip()
        line[1] = line[1].strip()
        if line[0] not in labels:
            labels[line[0]] = i
        else:
           print(f"ERROR at line {i+1}") 
           exit()
        line[0],line[1] = line[1],line[0]
    line = [line] if type(line) == str else line
    line[0:1] = line[0].split()
    lines.append(line)
    line = file.readline()
    i += 1
file.close()


file = open(output_file,'w')
for i in lines:
    if i[0] in r_dict:
        st = r_type(i[0],i[1],lines.index(i))
    elif i[0] in b_dict:
        st = b_type(i[0],i[1],lines.index(i))
    elif i[0] in i_dict:
        st = i_type(i[0],i[1],lines.index(i))
    elif i[0] == 'sw':
        st = s_type(i[0],i[1],lines.index(i))
    elif i[0] == 'jal':
        st = j_type(i[0],i[1],lines.index(i))
    else:
        st = f"ERROR at line {lines.index(i)+1}"
        print(f"ERROR at line {lines.index(i)+1}")
    file.write(st+'\n')
file.close()
