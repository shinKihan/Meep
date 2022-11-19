from collections.abc import Iterable
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
functiondirectory = []
recursivecalls = []

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

def flattenids(ids):
    for item in ids:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for id in flattenids(item):
                yield id
        else:
            yield item

def enviroment(p):
    if p[-2]=='sijag':
        cuadruplos.append(['GotoMain', None, None, None])
        env.append(-2)
        functiondirectory.append([p[-1], -2, len(cuadruplos), var_table, None, None])
    elif p[-1]=='gibon':
        cuadruplos[0][3]=len(cuadruplos)
        env[0] = -1
    else:
        if p[-2] == 'muhyoui':
            env[0] = -1
        elif p[-2] == 'jeo':
            env[0] = 0
        elif p[-2] == 'tteuda':
            env[0] = 1
        elif p[-2] == 'kkeun':
            env[0] = 2
        elif p[-2] == 'buul':
            env[0] = 3

        if env[0] > -2:
            type , address = None, -1
            for function in functiondirectory:
                if function[0] == p[-1]:
                    print(f'오류: 함수가 {p[-1]} 이미 존재합니다.')
                    quit()
            if check(p[-1], 'variable') is not False:
                print(f'오류: 변수가 {p[-1]} 이미 존재합니다.')
                quit()
            if env[0] == 0:
                type = 'int'
                address = global_int[0]+global_int[1]
                global_int[1] += 1
            elif env[0] == 1:
                type = 'float'
                address = global_float[0]+global_float[1]
                global_float[1] += 1
            elif env[0] == 2:
                type = 'string'
                address = global_string[0]+global_string[1]
                global_string[1] += 1
            elif env[0] == 3:
                type = 'bool'
                address = global_bool[0]+global_bool[1]
                global_bool[1] += 1
            var_table.append([p[-1], address, type, 1])
        functiondirectory.append([p[-1], env[0], len(cuadruplos), None, None, None]) 

def addparams(p):
    if p[-1] is None:
        return
    else:
        params, ptype, address = [], None, None
        ids = [id for id in list(flattenids(p[-1])) if id is not None]
        size = len(ids)
        for x in range(1, size, 2):
            if ids[x] == 'jeo':
                ptype = 'int'
                address = local_int[0]+local_int[1]
                local_int[1] += 1
            elif ids[x] == 'tteuda':
                ptype = 'float'
                address = local_float[0]+local_float[1]
                local_float[1] += 1    
            elif ids[x] == 'kkeun':
                ptype = 'string'
                address = local_string[0]+local_string[1]
                local_string[1] += 1
            elif ids[x] == 'buul':
                ptype = 'bool'
                address = local_bool[0]+local_bool[1]
                local_bool[1] += 1
            params.append([ptype, address])
            var_table.append(ids[x-1], address, ptype, 1)
        functiondirectory[-1][4] = params

def endfun():
    global temp
    global var_table
    temp, env[0] = 0, -2
    params = [[0, 0, 0, 0],[0, 0, 0, 0]]
    tempvar, aux = var_table.copy(), []
    size = len(tempvar)
    for x in range(size):
        if local_int[0] <= tempvar[x][1] < local_float[0]:
            params[0][0] += 1
        elif local_float[0] <= tempvar[x][1] < local_string[0]:
            params[0][1] += 1
        elif local_string[0] <= tempvar[x][1] < local_bool[0]:
            params[0][2] += 1
        elif local_bool[0] <= tempvar[x][1] < temporal_int[0]:
            params[0][3] += 1
        elif temporal_int[0] <= tempvar[x][1] < temporal_float[0]:
            params[1][0] += 1
        elif temporal_float[0] <= tempvar[x][1] < temporal_string[0]:
            params[1][1] += 1
        elif temporal_string[0] <= tempvar[x][1] < temporal_bool[0]:
            params[1][2] += 1
        elif temporal_bool[0] <= tempvar[x][1] < constant_int[0]:
            params[1][3] += 1
        else:
            aux.append(tempvar[x])

    functiondirectory[-1][3], functiondirectory[-1][5] = tempvar, params
    if recursivecalls:
        for x in range(len(recursivecalls)):
            call, info = recursivecalls[x][0], recursivecalls[x][1]
            era =  cuadruplos[call]
            # return here
    local_int[1] = 0
    local_float[1] = 0
    local_string[1] = 0
    local_bool[1] = 0

    temporal_int[1] = 0
    temporal_float[1] = 0
    temporal_string[1] = 0
    temporal_bool[1] = 0

    var_table = aux
    cuadruplos.append(['Endfun', None, None, None])
