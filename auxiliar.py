from cube import fetch

#compilation stacks
temp=0
cuadruplos=[]
opstack=[]
symbolstack=[]
typestack=[]
jumpstack=[]

#compiler tables
constant_table=[]
var_table=[]

#memory addresses
global_int=[1000,0]
global_float=[2000,0]
global_string=[3000,0]

local_int=[4000,0]
local_float=[5000,0]
local_string=[6000,0]

temporal_int=[7000,0]
temporal_float=[9000,0]
temporal_string=[11000,0]

constant_int=[13000,0]
constant_float=[14000,0]
constant_string=[15000,0]

#auxiliary functions
def check(id):
    if not constant_table:
        return False
    for row in constant_table:
        if row[0] == id:
            return row
    return False 

def addconstant(p, const):
    symbolstack.append(p[-1])
    typestack.append(const)

    if check(p[-1]):
        return check(p[-1])

    address=None

    if const == 'int':
        address=constant_int[0]+constant_int[1]
        constant_int[1]+=1

    elif const == 'float':
        address=constant_float[0]+constant_float[1]
        constant_float[1]+=1

    elif const == 'string':
        address=constant_string[0]+constant_string[1]
        constant_string[1]+=1

    constant_table.append([p[-1],address])

def addtemporary():
    global temp
    temp+=1
    t = f't{temp}'
    return t

def addexpresion(op):
    fullsize = len(opstack)
    size = None
    try:
        size =  fullsize-1-opstack.index('(')
    except:
        size = fullsize
    if size>0 and opstack[-1] == op:
        right,left,op = typestack.pop(),typestack.pop(),opstack.pop()
        semantic = fetch((op,left,right))
        print(typestack,opstack)
        if not semantic:
            print(f'불법 문자: 정수와 문자열 {op} 사이의 연산을 {left} 수 {right}.')
            quit()
        t=addtemporary()
        typestack.append('int')
        symbolstack.append(t)
        cuadruplos.append([op, left, right, t])
