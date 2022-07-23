import sys

A ={"10000":"add", "10001":"sub", "10110":"mul", "11010":"xor", "11011":"or", "11100":"and"}
B={"10010":"movi", "11000":"rs", "11001":"ls"}
C={"11110":"cmp", "10011":"movr", "10111":"div", "11101":"not"}
D={"10100":"ld", "10101":"st"}
E={"11111":"jmp", "01100":"jlt", "01101":"jgt", "01111":"je"}
F={"01010":"hlt"}

Registers ={"000":0, "001":1, "010":2, "011":3, "100":4, "101":5, "110":6}
Variables = {}

RF=[0, 0, 0, 0, 0, 0, 0] # R0-R6 registers
FLAGS=[0, 0, 0, 0]
PC, Cycle, halted, flag_flip=0, 0, 0, 0

def load_memory(Mem, Inp, n):
    for i in range(0, n):
        Mem[i]=Inp[i].strip()
    return

def decimal_binary(n):
    res=0
    pow=0
    while(n>0):
        res=res+ (n%2)*(10**pow)
        pow+=1
        n=n//2    
    return res
    
def binary_decimal(s):
    pow=len(s)-1
    res=0
    for i in s:
        res+=(2**pow)*int(i)
        pow-=1
    return res

def bit_extender(s, size):
    diff=size-len(s)
    s=("0"*diff)+s
    return s

def display_state():
    global PC
    print(bit_extender( str(decimal_binary(PC)), 8), end=" ")    
    for i in RF:
        print(bit_extender( str(decimal_binary(i)), 16), end=" ")
    flg=""
    for i in FLAGS:
        flg+=str(i)    
    print(bit_extender(flg, 16))
    return

def display_Memory():
    for i in Mem:
        print(i)

def A_execute(operator, r1, r2, r3):
    global flag_flip, PC
    res=0
    if operator=="add":
        res=RF[r2] + RF[r3]
    elif operator=="sub":
        res=RF[r2] - RF[r3]
    elif operator=="mul":
        res=RF[r2] * RF[r3]
    elif operator=="xor":
        res=RF[r2] ^ RF[r3]
    elif operator=="or":
        res=RF[r2] | RF[r3]
    elif operator=="and":
        res=RF[r2] & RF[r3]

    if res>65535:
        flag_flip=1
        RF[r1]=255
        FLAGS[0]=1
        
    elif res<0:
        flag_flip=1
        RF[r1]=0
        FLAGS[0]=1
    else:
        RF[r1]=res
    PC+=1
    return

def B_execute(operator, r1, val):
    global PC
    if operator=="ls":
        RF[r1]=RF[r1]<<val
    elif operator=="rs":
        RF[r1]=RF[r1]>>val
    elif operator=="movi":
        RF[r1]=val    
    PC+=1
    return 
    
def C_execute(operator, r1, r2):
    global flag_flip, PC
    if operator=="movr":
        RF[r1]=RF[r2]
    elif operator=="not":
        RF[r1]= 65535 - RF[r2]
    elif operator=="div":
        RF[0]=RF[r1] // RF[r2]
        RF[1]=RF[r1] % RF[r2]
    elif operator=="cmp":
        if RF[r1]==RF[r2]:
            flag_flip=1
            FLAGS[3]=1
        elif RF[r1]>RF[r2]:
            flag_flip=1
            FLAGS[1]=1
        elif RF[r1]<RF[r2]:
            if FLAGS[2]==1:
                flag_flip=0
            else:
                flag_flip=1
            FLAGS[2]=1    
    PC+=1
    return

def D_execute(operator, r1, address): 
    global PC
    if operator=="st":
        Variables[address]=RF[r1]
    elif operator=="ld":
        RF[r1]=Variables[address]       
    PC+=1
    return

def E_Execute(operator, jmp_address):
    global PC
    if operator=="jmp":
        PC=jmp_address
    elif operator=="jlt":
        if FLAGS[1]==1:
            PC=jmp_address
        else:
            PC+=1
    elif operator=="jgt":
        if FLAGS[2]==1:
            PC=jmp_address
        else:
            PC+=1
    elif operator=="je":
        if FLAGS[3]==1:
            PC=jmp_address
        else:
            PC+=1
    return
        
def Execute(Inst):
    global PC, flag_flip
    hlt=0
    op=Inst[0:5]    
    if op in A:
        A_execute(A[op], Registers[Inst[7:10]], Registers[Inst[10:13]], Registers[Inst[13:16]])
        
    elif op in B:
        B_execute(B[op], Registers[Inst[5:8]] , binary_decimal(Inst[8:16]))  

    elif op in C:
        C_execute(C[op], Registers[Inst[10:13]], Registers[Inst[13:16]])

    elif op in D:
        D_execute(D[op], Registers[Inst[5:8]], Inst[8:16])

    elif op in E:
        E_Execute(E[op], binary_decimal(Inst[8:16]))
    elif op in F:
        hlt=1
    return hlt, flag_flip

Mem=["0"*16]*256
Inp=sys.stdin.readlines()
n=len(Inp)
load_memory(Mem, Inp, n)
while halted==0:
    Cycle+=1
    flag_flip=0
    Inst=Mem[PC]
    halted, flag_flip = Execute(Inst)
    display_state()
    if(flag_flip==0):
        FLAGS=[0, 0, 0, 0]
display_Memory()