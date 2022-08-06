import math
def f(space,memory,len_inst,len_reg):
    if (space[-1]=="B"):
        if(space[-2]=="M"):
            x=int(space[0])
            y=math.log(x,2)
            a=y+20
            b=len_inst-a-len_reg
            c=len_inst-(2*len_reg)-b
            d=2**b
            e=2**(len_reg)
        if(space[-2]=="k"):
            x=int(space[0])
            y=math.log(x,2)
            a=y+10
            b=len_inst-a-len_reg
            c=len_inst-(2*len_reg)-b
            d=2**b
            e=2**(len_reg)
        if(space[-2]=="G"):
            x=int(space[0])
            y=math.log(x,2)
            a=y+40
            b=len_inst-a-len_reg
            c=len_inst-(2*len_reg)-b
            d=2**b
            e=2**(len_reg)
    elif (space[-1]=="b"):
        if(space[-2]=="M"):
            x=int(space[0])
            y=math.log(x,2)
            a=y+17
            b=len_inst-a-len_reg
            c=len_inst-(2*len_reg)-b
            d=2**b
            e=2**(len_reg)
        if(space[-2]=="k"):
            x=int(space[0])
            y=math.log(x,2)
            a=y+7
            b=len_inst-a-len_reg
            c=len_inst-(2*len_reg)-b
            d=2**b
            e=2**(len_reg)
        if(space[-2]=="G"):
            x=int(space[0])
            y=math.log(x,2)
            a=y+37
            b=len_inst-a-len_reg
            c=len_inst-(2*len_reg)-b
            d=2**b
            e=2**(len_reg)
    return a,b,c,d,e
#def g(cpu_size,enhancement,space):

        
space=(input("Enter the size of memory: "))
memory=str(input("Enter type of memory: "))
query=int(input("Enter the query(1/2): "))
if query==1:
    len_inst=int(input("Enter the length of instruction: "))
    len_reg=int(input("Enter the length of register: "))
    a,b,c,d,e=f(space,memory,len_inst,len_reg)
    print(a)
    print(b)
    print(c)
    print(d)
    print(e)