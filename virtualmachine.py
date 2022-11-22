import numpy as np
import seaborn as sns
from auxiliar import global_int, global_float, global_string, global_bool
from auxiliar import local_int, local_float, local_string, local_bool
from auxiliar import temporal_int, temporal_float, temporal_string, temporal_bool
from auxiliar import constant_int, constant_float, constant_string, constant_bool
import json

filename = input('실행할 이름 파일: ')
file = open(filename,'r')
content = json.load(file)
file.close()

constants = content['constants']
cuadruplos = content['cuadruplos']
functions = content['functions']


#virtual memory
gbl = {
    'variables'  : [[],[],[],[]],
    'constants'  : constants
}

lcl = {
    'variables'  : [[],[],[],[]],
    'temporales' : [[],[],[],[]]
}

IP = 0
pointerstack = [IP]
functionstack = []
memorystack = [lcl]

def find(memory, space = None, address = None):
    if space is None:
        for row in constants:
            if row[1] == address:
                return row[0]
    else:
        if not memory or len(memory) - 1 < space:
            pass
        else:
            return memory[space]
    return None

def memorystore(memory, space, value):
    if not memory:
        memory.append(value)
    elif len(memory) > space:
        memory[space] = value
    else:
        while len(memory) < space:
            memory.append(None)
        memory.append(value) 

def memoryop(address, value = None):
    space = None
    if global_int[0] <= address < global_float[0]:
        memory = gbl['variables'][0]
        space = address-global_int[0]
    elif global_float[0] <= address < global_string[0]:
        memory = gbl['variables'][1]
        space = address-global_float[0]
    elif global_string[0] <= address < global_bool[0]:
        memory = gbl['variables'][2]
        space = address-global_string[0]
    elif global_bool[0] <= address < local_int[0]:
        memory = gbl['variables'][3]
        space = address-global_bool[0]

    elif local_int[0] <= address < local_float[0]:
        memory = memorystack[-1]['variables'][0]
        space = address-local_int[0]
    elif local_float[0] <= address < local_string[0]:
        memory = memorystack[-1]['variables'][1]
        space = address-local_float[0]
    elif local_string[0] <= address < local_bool[0]:
        memory = memorystack[-1]['variables'][2]
        space = address-local_string[0]
    elif local_bool[0] <= address < temporal_int[0]:
        memory = memorystack[-1]['variables'][3]
        space = address-local_bool[0]

    elif temporal_int[0] <= address < temporal_float[0]: 
        memory = memorystack[-1]['temporales'][0]
        space = address-temporal_int[0]
    elif temporal_float[0] <= address < temporal_string[0]:
        memory = memorystack[-1]['temporales'][1]
        space = address-temporal_float[0]
    elif temporal_string[0] <= address < temporal_bool[0]:
        memory = memorystack[-1]['temporales'][2]
        space = address-temporal_string[0]
    elif temporal_bool[0] <= address < 17000:
        memory = memorystack[-1]['temporales'][3]
        space = address-temporal_bool[0]
    else:
        memory = gbl['constants']
    if value is not None:
        memorystore(memory, space, value)
    else:
        if space is None:
            return find(memory, address = address)
        else:
            return find(memory, space = space)

def main():
    while True:
        global memorystack
        global functionstack
        global pointerstack
        current = cuadruplos[pointerstack[-1]]
        if current[0] == 'End':
            break
        elif current[0] == 'GotoMain':
            pointerstack[-1] = current[3]
        elif current[0] == 'Goto':
            pointerstack[-1] = current[3]
        elif current[0] == 'GotoF':
            result = memoryop(current[1])
            if result is False:
                pointerstack[-1] = current[3]
            else:
                pointerstack[-1]+=1
        elif current[0] == 'Read':
            address = current[3]
            val = input()
            try:
                if global_int[0] <= address < global_float[0] or \
                        local_int[0] <= address < local_float[0] or \
                            temporal_int[0] <= address < temporal_float[0] or \
                                constant_int[0] <= address < constant_float[0]:
                    type = 'int'
                    value = int(val)
                elif global_float[0] <= address < global_string[0] or \
                        local_float[0] <= address < local_string[0] or \
                            temporal_float[0] <= address < temporal_string[0] or \
                                constant_float[0] <= address < constant_string[0]:
                    type = 'float'
                    value = float(val)
            except:
                print('오류: 예상치 못한 유형')
                quit()
            memoryop(address, value)
            pointerstack[-1]+=1

        elif current[0] == 'Write':
            address = current[3]
            message = memoryop(address)
            if message is None:
                print('오류: 값을 찾을 수 없습니다.')
                quit()
            print(message)
            pointerstack[-1]+=1

        elif current[0] == '=':
            value = memoryop(current[2])
            memoryop(current[3], value)
            pointerstack[-1]+=1

        elif current[0] == '+':
            addresses = current[1], current[2]
            left = memoryop(addresses[0])
            right = memoryop(addresses[1])
            result = left+right
            memoryop(current[3], result)
            pointerstack[-1]+=1

        elif current[0] == '-':
            addresses = current[1], current[2]
            left = memoryop(addresses[0])
            right = memoryop(addresses[1])
            result = left-right
            memoryop(current[3], result)
            pointerstack[-1]+=1

        elif current[0] == '*':
            addresses = current[1], current[2]
            left = memoryop(addresses[0])
            right = memoryop(addresses[1])
            result = left*right
            memoryop(current[3], result)
            pointerstack[-1]+=1

        elif current[0] == '/':
            addresses = current[1], current[2]
            left = memoryop(addresses[0])
            right = memoryop(addresses[1])
            if right == 0:
                print("0으로 나눌 수 없다")
                quit()
            result = left/right
            memoryop(current[3], result)
            pointerstack[-1]+=1

        elif current[0] == '//':
            addresses = current[1], current[2]
            left = memoryop(addresses[0])
            right = memoryop(addresses[1])
            if right == 0:
                print("0으로 나눌 수 없다")
                quit()
            result = int(left//right)
            memoryop(current[3], result)
            pointerstack[-1]+=1

        elif current[0] == '^':
            addresses = current[1], current[2]
            left = memoryop(addresses[0])
            right = memoryop(addresses[1])
            result = float(left**right)
            memoryop(current[3], result)
            pointerstack[-1]+=1
        
        elif current[0] == '==':
            addresses = current[1], current[2]
            left = memoryop(addresses[0])
            right = memoryop(addresses[1])
            result = left==right
            memoryop(current[3], result)
            pointerstack[-1]+=1

        elif current[0] == '>':
            addresses = current[1], current[2]
            left = memoryop(addresses[0])
            right = memoryop(addresses[1])
            result = left>right
            memoryop(current[3], result)
            pointerstack[-1]+=1

        elif current[0] == '<':
            addresses = current[1], current[2]
            left = memoryop(addresses[0])
            right = memoryop(addresses[1])
            result = left<right
            memoryop(current[3], result)
            pointerstack[-1]+=1

        elif current[0] == '>=':
            addresses = current[1], current[2]
            left = memoryop(addresses[0])
            right = memoryop(addresses[1])
            result = left>=right
            memoryop(current[3], result)
            pointerstack[-1]+=1

        elif current[0] == '<=':
            addresses = current[1], current[2]
            left = memoryop(addresses[0])
            right = memoryop(addresses[1])
            result = left<=right
            memoryop(current[3], result)
            pointerstack[-1]+=1
        
        elif current[0] == '!=':
            addresses = current[1], current[2]
            left = memoryop(addresses[0])
            right = memoryop(addresses[1])
            result = left!=right
            memoryop(current[3], result)
            pointerstack[-1]+=1
        
        elif current[0] == '|':
            addresses = current[1], current[2]
            left = memoryop(addresses[0])
            right = memoryop(addresses[1])
            result = left or right
            memoryop(current[3], result)
            pointerstack[-1]+=1

        elif current[0] == '&':
            addresses = current[1], current[2]
            left = memoryop(addresses[0])
            right = memoryop(addresses[1])
            result = left and right
            memoryop(current[3], result)
            pointerstack[-1]+=1

        elif current[0] == 'HABJI':
            value = memoryop(current[1])
            result = sum(value)
            print(result)
            pointerstack[-1]+=1
        
        elif current[0] == 'BUN':
            value = memoryop(current[1])
            result = min(value)
            print(result)
            pointerstack[-1]+=1
        
        elif current[0] == 'CHOE':
            value = memoryop(current[1])
            result = max(value)
            print(result)
            pointerstack[-1]+=1
        
        elif current[0] == 'PYEONG':
            value = memoryop(current[1])
            value = np.array(value)
            result = np.mean(value)
            print(result)
            pointerstack[-1]+=1
        
        elif current[0] == 'JUNG':
            value = memoryop(current[1])
            value = np.array(value)
            result = np.median(value)
            print(result)
            pointerstack[-1]+=1
        
        elif current[0] == 'BYEON':
            value = memoryop(current[1])
            value = np.array(value)
            result = np.var(value)
            print(result)
            pointerstack[-1]+=1

        elif current[0] == 'HISEU':
            value = memoryop(current[1])
            value = np.array(value)
            result = sns.histplot(data = value)
            print(result)
            pointerstack[-1]+=1
        
        elif current[0] == 'SULJIB':
            addresses = current[1], current[2]
            x = memoryop(addresses[0])
            y = memoryop(addresses[1])
            result = sns.barplot(x, y)
            pointerstack[-1]+=1
        
        elif current[0] == 'GoSub':
            params = functionstack[0][1]
            functionstack = functionstack[1:]
            newmemory = {
                'variables'  : [[],[],[],[]],
                'temporales' : [[],[],[],[]]
            }
            memorystack.append(newmemory)
            for x in range(len(params)):
                memoryop(params[x][1], functionstack[x])
            functionstack = []
            pointerstack[-1] += 1
            pointerstack.append(current[3])
        
        elif current[0] == 'Return':
            value = memoryop(current[2])
            memoryop(current[3], value)
            memorystack.pop()
            pointerstack.pop()

        elif current[0] == 'Endfun':
            memorystack.pop()
            pointerstack.pop()

        elif current[0] == 'ERA':
            for function in functions:
                if function[0] == current[1]:
                    functionstack.append(function)
                    break
            for address in current[2]:
                try:
                    if memoryop(address) is not None:
                        continue
                except:
                    memoryop(address, False)
            for address in current[3]:
                memoryop(address, False)
            pointerstack[-1] += 1
        
        elif current[0] == 'PARAM':
            functionstack.append(memoryop(current[2]))
            pointerstack[-1] += 1

        else:
            pointerstack[-1]+=1
if __name__ == '__main__':
    main()
    print('실행 완료')
    # print(gbl)
    # print(lcl)
