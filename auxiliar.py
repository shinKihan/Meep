from cube import fetch

#compilation stacks
temp = 0
env = []
cuadruplos = []
opstack = []
symbolstack=[]
typestack = []
jumpstack = []

#compiler tables
constant_table = []
var_table = []

#memory addresses
global_int = [1_000,0]
global_float = [2_000,0]
global_string = [3_000,0]
global_bool = [4_000,0]

local_int = [5_000,0]
local_float = [6_000,0]
local_string = [7_000,0]
local_bool = [8_000,0]

temporal_int = [9_000,0]
temporal_float = [11_000,0]
temporal_string = [13_000,0]
temporal_bool = [15_000,0]

constant_int = [17_000,0]
constant_float = [18_000,0]
constant_string = [19_000,0]
constant_bool = [20_000,0]

#auxiliary functions
def check(id, tablename):
    if tablename == "constant":    
        if not constant_table:
            return False
        for row in constant_table:
            if row[0] == id:
                return row
                
    elif tablename == "declaration":
        if not var_table:
            return False
        for row in var_table:
            if row[0] != id:
                continue
            else:
                if env[0] < -1 and 1000 <= row[1] < 5000:
                    return row
                elif env[0] >= -1 and 5000 <= row[1] < 9000:
                    return row

    elif tablename == 'variable':
        if not var_table:
            return False
        else:
            table = var_table.copy()[::-1]
            for row in table:
                if row[0] == id:
                    return row
    return False

def addconstant(p, const, append = True):
    if append:
        symbolstack.append(p[-1])
        typestack.append(const)
    if check(p[-1],'constant'):
        return check(p[-1],'constant')
    else:
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
        
        elif const == "bool":
            if p[-1] == 'true':
                address=20000
            else:
                address=20001
    constant_table.append([p[-1],address])

def addtemporary(type, append = True):
    if type == 'int':
        address = temporal_int[0]+temporal_int[1]
        temporal_int[1] += 1
    elif type == 'float':
        address = temporal_float[0]+temporal_float[1]
        temporal_float[1] += 1
    elif type == 'string':
        address = temporal_string[0]+temporal_string[1]
        temporal_string[1] += 1
    elif type == 'bool':
        address = temporal_bool[0]+temporal_bool[1]
        temporal_bool[1] += 1
    global temp
    temp+=1
    t = f't{temp}'
    if append:
        typestack.append(type)
        symbolstack.append(t)
    var_table.append([t, address, type, 1])
    return address

def addexpresion(op, negative=False):
    fullsize = len(opstack)
    try:
        size =  fullsize-1-opstack.index('(')
    except:
        size = fullsize
    if size>0 and opstack[-1] == op:
        right_type, operator = typestack.pop(),opstack.pop()
        if not negative:
            left_type = typestack.pop()
            semantic = fetch((operator,left_type,right_type))
        else:
            semantic = fetch((operator,right_type))
        if not semantic:
            print(f'불법 문자: 정수와 문자열 {operator} 사이의 연산을 {left_type} 수 {right_type}.')
            quit()
        right_address = finder()
        if not negative:
            left_address = finder()
            t = addtemporary(semantic)
            cuadruplos.append([operator, left_address, right_address, t])
        else:
            t = addtemporary(semantic)
            cuadruplos.append([operator, None, right_address, t])

def createvariable(id, type):
    if check(id,'declaration'):
        print(f'오류 변수가 {id} 이미 있습니다.')
        quit()
    if type=="int":
        if env[0] >= -1:
            address = local_int[0]+local_int[1]
            local_int[1]+=1
        else:
            address = global_int[0]+global_int[1]
            global_int[1]+=1
    elif type=="float":
        if env[0] >= -1:
            address = local_float[0]+local_float[1]
            local_float[1]+=1
        else:
            address = global_float[0]+global_float[1]
            global_float[1]+=1
    elif type=="string":
        if env[0] >= -1:
            address = local_string[0]+local_string[1]
            local_string[1]+=1
        else:
            address = global_string[0]+global_string[1]
            global_string[1]+=1
    else: 
        if env[0] >= -1:
            address = local_bool[0]+local_bool[1]
            local_bool[1]+=1
        else:
            address = global_bool[0]+global_bool[1]
            global_bool[1]+=1
    var_table.append([id,address, type,1])

def finder(var = None):
    # print(symbolstack) return here
    if not var:
        var = symbolstack.pop()
    symbol = check(var, 'constant')
    if not symbol:
        symbol = check(var, 'variable')
    if not symbol:
        print(f'오류: 변수가 {symbol} 존재하지 않습니다')
        quit()
    return symbol[1]
