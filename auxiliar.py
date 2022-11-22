from collections.abc import Iterable
from cube import fetch

#compilation stacks
temp = 0
currentfunction = []
env = []
dimensions = []
dimensioncounter = []
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
dimenstionstack = []

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
            if ids[x-1] == 'jeo':
                ptype = 'int'
                address = local_int[0]+local_int[1]
                local_int[1] += 1
            elif ids[x-1] == 'tteuda':
                ptype = 'float'
                address = local_float[0]+local_float[1]
                local_float[1] += 1    
            elif ids[x-1] == 'kkeun':
                ptype = 'string'
                address = local_string[0]+local_string[1]
                local_string[1] += 1
            elif ids[x-1] == 'buul':
                ptype = 'bool'
                address = local_bool[0]+local_bool[1]
                local_bool[1] += 1
            params.append([ptype, address])
            var_table.append([ids[x], address, ptype, 1])
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
            current = cuadruplos[call]
            era = finishcall(current, *info, do_modify = True)
            current[2], current[3] = era[2], era[3]

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

def finishcall(era, ids, temp, do_modify = False):
    addresses = [[],[]]
    era[2], era[3] = addresses[0], addresses[1]
    params, locals, aux = [], None, None 
    if currentfunction[0][5] is not None:
        locals = currentfunction[0][5][0].copy()
    else:
        aux = [ids, temp.copy()]
    for x in range(len(ids)):
        pt = currentfunction[0][4][x][0]
        param = temp.pop()
        if pt != param[1]:
            print('오류: 호출 및 함수와 다른 매개변수')
            quit()
        if pt == 'int':
            pt=0
        elif pt == 'float':
            pt=1
        elif pt == 'string':
            pt=2
        elif pt == 'bool':
            pt=3
        var = check(param[0], 'constant')
        if var is False:
            var = check(param[0], 'variable')
        if currentfunction[0][5] is not None and local_int[0] <= var[1] < temporal_int[0]:
            locals[pt] -= 1
            addresses[0].append(var[1])
        if do_modify is False:
            params.append(['PARAM', None, var[1], x+1])
    if currentfunction[0][5] is not None:
        for x in range(len(locals)):
            if locals[x] == 0:
                continue
            for y in range(locals[x]):
                if x == 0:
                    address = local_int[0]+local_int[1]
                    local_int[1] += 1
                elif x == 1:
                    address = local_float[0]+local_float[1]
                    local_float[1] += 1
                elif x == 2:
                    address = local_string[0]+local_string[1]
                    local_string[1] += 1
                elif x == 3:
                    address = local_bool[0]+local_bool[1]
                    local_bool[1] += 1
                addresses[0].append(address)
        size = currentfunction[0][5][1]
        for x in range(len(size)):
            if size[x] == 0:
                continue
            for _ in range(size[x]):
                if x == 0:
                    type = 'int'
                elif x == 1:
                    type = 'float'
                elif x == 2:
                    type = 'string'
                elif x == 3:
                    type = 'bool'
                address = addtemporary(type, False)
                addresses[1].append(address)
        if do_modify is False:
            cuadruplos.append(era)
    else:
        cuadruplos.append(['ERA', currentfunction[0][0], None, None])
        recursivecalls.append([len(cuadruplos)-1, aux])
    if do_modify is False:
        for cuad in params:
            cuadruplos.append(cuad)
        cuadruplos.append(['GoSub', None, None, currentfunction[0][2]])
    else:
        return era

def processcall(p):
    global currentfunction
    if p[-1] is None:
        if currentfunction[0][4] is None:
            cuadruplos.append(['GoSub', None, None, currentfunction[0][2]])
            currentfunction = []
            return
        else:
            print(f'오류: 매개변수 {currentfunction[0][4]} 제외')
            quit()
    
    ids = list((flattenids(p[-1])))
    removeid, size = [], len(ids)
    for x in range(size):
        if ids[x] is None:
            removeid.append(ids[x])
    ids =  [id for id in ids if id not in removeid]
    if ids and currentfunction[0][4] is None:
        print('오류: 인수가 예상되지 않았습니다.')
        quit()

    if len(ids) != len(currentfunction[0][4]):
        print('오류: 현재 인수가 유효하지 않음')
        quit()

    temp = [(symbolstack.pop(), typestack.pop()) for _ in ids]
    era = ['ERA', currentfunction[0][0], None, None]
    finishcall(era, ids, temp)

def dimensionhandle(dimension):
    value = finder(symbolstack[-1])
    if type(dimensions[0][1]) != list:
        current = dimensions[0]
    else:
        current = dimensions[0][0]
    left = check(current[0][0], 'constant')
    right = check(current[0][1], 'constant')
    cuadruplos.append(['Verify', value, left[1], right[1]])
    if type(dimensions[0][1]) == list:
        symbolstack.pop() 
        typestack.pop()
        temporal = addtemporary('int')
        cuadruplos.append(['*', value, right[1], temporal])
    if dimension > 1:
        right = [finder(symbolstack.pop()), typestack.pop()]
        left = [finder(symbolstack.pop()), typestack.pop()]
        temporal = addtemporary('int')
        cuadruplos.append(['+', left[0], right[0], temporal])
        