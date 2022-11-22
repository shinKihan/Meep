import ply.yacc as yacc
from lexer import tokens
from auxiliar import *
import json

#Begining of grammar
def p_prog(p):
    """
    prog : START ID env COLON global END endprog
    """
    p[0] = p[1],p[2],p[4],p[5],p[6]

def p_endprog(p):
    """
    endprog :
    """
    cuadruplos.append(['End', None, None, None])
    obj = {}
    fd = []
    for function in functiondirectory[1:]:
        fd.append([function[x] for x in [0, 4, 5]])
    obj['functions'] = fd 
    obj['constants'] = constant_table
    obj['cuadruplos'] = cuadruplos
    with open(f'{p[-5]}.json','w') as file:
        json.dump(obj, file, ensure_ascii=False, indent=2)

def p_env(p):
    """
    env :
    """
    enviroment(p)
            
def p_global(p):
    """
    global : declare global
           | fun global
           | main 
    """
    if len(p)>2:
        p[0] = p[1],p[2]
    else:
        p[0]=p[1]

def p_funtype(p):
    """
    funtype : type
            | VOID 
    """
    p[0] = p[1]

def p_addparams(p):
    """
    addparams :
    """
    addparams(p)

def p_moreparam(p):
    """
    moreparam : moreparam COMA type ID 
              | empty 
    """
    if p[1]:
        p[0] = p[1],p[2],p[3],p[4]

def p_funparam(p):
    """
    funparam : type ID moreparam
             | empty 
    """
    if p[1]:
        p[0] = p[1],p[2],p[3]

def p_endfun(p):
    '''
    endfun :
    '''
    endfun()

def p_fun(p):
    """
    fun : FUNCTION funtype ID env LPAREN funparam addparams RPAREN LCURLY block RCURLY endfun 
    """
    p[0] = p[1],p[2],p[3],p[5],p[6],p[8],p[9],p[10],p[11]

def p_main(p):
    """
    main : VOID MAIN env LPAREN RPAREN LCURLY block RCURLY 
    """
    p[0] = p[1],p[2],p[4],p[5],p[6],p[7],p[8]

#Linear statement
def p_next(p):
    """
    next : statement next
         | empty
    """
    if p[1]:
        p[0]=p[1],p[2]

def p_block(p):
    """
    block : statement next
    """
    p[0]=p[1],p[2]

def p_statement(p):
    """
    statement : assign
              | declare
              | while
              | if
              | write
              | read
              | return
              | stats
              | expression pop
    """
    p[0] = p[1]

def p_creatematrix(p):
    '''
    creatematrix :
    '''
    dimensioncounter[0] += 1
    dimensionhandle(dimensioncounter[0])

def p_dimension(p):
    """
    dimension : COLON logic creatematrix
              | empty
    """
    if p[1]:
        p[0] = p[1],p[2]

def p_createarray(p):
    '''
    createarray :
    '''
    id = symbolstack.pop()
    type = typestack.pop()

    if not dimensions:
        print('오류: 크기가 없습니다.')
        quit()
    else:
        dimenstionstack.append([id, 1])
        opstack.append('[')

def p_evaluate(p):
    '''
    evaluate :
    '''
    if typestack[-1] != 'int':
        print('오류: 차원이 int가 아닙니다.')
        quit()
    dimensioncounter.append(1)
    dimensionhandle(dimensioncounter[0])

def p_endarray(p):
    '''
    endarray :
    '''
    if dimensioncounter[0] == 1 and type(dimensions[0][1]) == list:
        print('오류: 오류 치수')
        quit()
    aux = symbolstack.pop()
    pointer = addtemporary('pointer')
    base = finder(dimensions[0])
    cuadruplos.append(['++', finder(aux), base, pointer])
    opstack.pop()

def p_dimvar(p):
    """
    dimvar : LBRKT createarray logic evaluate dimension RBRKT endarray
           | empty
    """
    if p[1]:
        p[0] = p[1],p[3],p[4],p[5]

#variable logic
def p_addvariable(p):
    """
    addvariable :
    """
    var = check(p[-1],'variable')
    if not var:
        print(f'오류: 변수가 {p[-1]} 존재하지 않습니다')
        quit()
    symbolstack.append(var[0])
    typestack.append(var[2])
    # if type(var[3][1]) == list or var[3][0][1] > 0:
    #     dimensions.append(var)
    #     addconstant(var[1], 'int', False)

def p_var(p):
    """
    var : ID addvariable dimvar
    """
    p[0] = p[1],p[3]

#return here
def p_assignvalue(p):
    """
    assignvalue :
    """
    right_address, right_type = finder(), typestack.pop()
    left_address, left_type= finder(), typestack.pop()
    semantic = fetch((p[-2], left_type, right_type))
    if not semantic:
        print(f'불법 문자: 정수와 문자열 {p[-2]} 사이의 연산을 {left_type} 수 {right_type}.')
        quit()
    cuadruplos.append([p[-2], None, right_address, left_address])

def p_assign(p):
    """
    assign : var ASSIGN expression assignvalue
    """
    p[0] = p[1],p[2],p[3]

def p_matrix(p):
    """
    matrix : COLON CTE_I 
           | empty 
    """
    if p[1]:
        p[0] = p[1],p[2]

def p_array(p):
    """
    array : LBRKT CTE_I matrix RBRKT
          | empty 
    """
    if p[1]:
        p[0] = p[1],p[2],p[3],p[4]    

# declaration functionality
def p_createvariable(p):
    """
    createvariable : 
    """
    type = None
    if p[-4] == 'jeo':
        type = 'int'
    elif p[-4] == 'tteuda':
        type = 'float'
    elif p[-4] == 'kkeun':
        type = 'string'
    elif p[-4] == 'buul':
        type = 'bool'    
    createvariable(p[-3],type)

def p_declare(p):
    """
    declare : VAR type ID array SEMICOLON createvariable
    """
    p[0] = p[1],p[2],p[3],p[4],p[5]

#Read fuctionality   
def p_readassign(p):
    """
    readassign : 
    """
    cuadruplos.append(['Read', None, None, finder(p[-3])])

def p_read(p):
    """
    read : READ LPAREN ID RPAREN SEMICOLON readassign
    """
    p[0] = p[1],p[2],p[3],p[4],p[5]

#Print fuctionality
def p_print(p):
    """
    print :
    """
    typestack.pop()
    cuadruplos.append(['Write', None, None, finder()])

def p_write(p):
    """
    write : WRITE LPAREN logic RPAREN SEMICOLON print
    """
    p[0] = p[1],p[2],p[3],p[4],p[5]

def p_return(p):
    """
    return : RETURN expression
    """
    p[0] = p[1],p[2]
    if env[0] < 0:
        print("오류: 이 컨텍스트에서 반환할 수 없습니다.")
        quit()
    type = typestack.pop()
    if (type == 'int' and env[0] > 0) or (type == 'float' and env[0] != 1) \
        or (type == 'string' and env[0] != 2) or (type == 'bool' and env[0] != 3): 
        print("오류: 유형 불일치.")
        quit()
    result = finder()
    function = finder(functiondirectory[-1][0])
    cuadruplos.append(['Return', None, result, function])

def p_type(p):
    """
    type : INT
         | FLOAT
         | STRING
         | BOOL
    """
    p[0] = p[1]

#Compound statement
def p_beginwhile(p):
    """
    beginwhile :
    """
    jumpstack.append(len(cuadruplos))

#come back later
def p_checklogic(p):
    """
    checklogic :
    """
    type = typestack.pop()
    if type != 'bool':
        print('오류: 표현식이 부울이 아닙니다.')
        quit()
    result = finder()
    cuadruplos.append(['GotoF', result, None, None])
    jumpstack.append(len(cuadruplos)-1)

def p_endwhile(p):
    """
    endwhile :
    """
    end = jumpstack.pop()
    goback = jumpstack.pop()
    cuadruplos.append(['Goto', None, None, goback])
    cuadruplos[end][3] = len(cuadruplos)

def p_while(p):
    """
    while : WHILE beginwhile LPAREN logic checklogic RPAREN LCURLY block RCURLY endwhile
    """
    p[0] = p[1],p[3],p[4],p[6],p[7],p[8],p[9]

def p_beginelse(p):
    """
    beginelse :
    """
    cuadruplos.append(['Goto', None, None, None])
    on_false = jumpstack.pop()
    jumpstack.append(len(cuadruplos)-1)
    cuadruplos[on_false][3] = len(cuadruplos)

def p_endif(p):
    """
    endif :
    """
    end = jumpstack.pop()
    cuadruplos[end][3] = len(cuadruplos)

def p_else(p):
    """
    else : ELSE beginelse LCURLY block RCURLY
         | empty
    """
    if p[1]:
        p[0] = p[1],p[3],p[4],p[5]

def p_if(p):
    """
    if : IF LPAREN logic checklogic RPAREN LCURLY block RCURLY else endif
    """
    p[0] = p[1],p[2],p[3],p[5],p[6],p[7],p[8],p[9]

#Begining of expresion
def p_pop(p):
    """
    pop : 
    """
    if symbolstack:
       symbolstack.pop()
       typestack.pop()

def p_pushoperator(p):
    """
    pushoperator :
    """
    opstack.append(p[-1])

def p_popparen(p):
    """
    popparen :
    """
    opstack.pop()

def p_addexpresion(p):
    """
    addexpresion :
    """
    addexpresion(p[-3])

def p_addnegative(p):
    """
    addnegative :
    """
    addexpresion(p[-3],True)

def p_expression(p):
    """
    expression : logic SEMICOLON
    """
    p[0] = p[1]

def p_oplogic(p):
    """
    oplogic : OR
            | AND
    """ 
    p[0] = p[1]

def p_logic(p):
    """
    logic : comp
          | logic oplogic pushoperator comp addexpresion
    """ 
    p[0] = p[1]

def p_opcomp(p):
    """
    opcomp : EQ
           | NE
           | GT
           | GE
           | LT
           | LE
    """ 
    p[0] = p[1]

def p_comp(p):
    """
    comp : sum
         | comp opcomp pushoperator sum addexpresion
    """ 
    p[0] = p[1]

def p_opsum(p):
    """
    opsum : PLUS
          | MINUS
    """ 
    p[0] = p[1]

def p_sum(p):
    """
    sum : term
        | sum opsum pushoperator term addexpresion
    """
    p[0] = p[1]

def p_opterm(p):
    """
    opterm : MULTIPLY
           | DIVIDE
           | INT_DIV
           | MOD
           | PERCENT
    """ 
    p[0] = p[1]

def p_term(p):
    """
    term : exp 
         | term opterm pushoperator exp addexpresion
    """
    p[0] = p[1]

def p_exp(p):
    """
    exp : unary
        | exp EXPONENT pushoperator unary addexpresion
    """
    p[0] = p[1]

def p_unary(p):
    """
    unary : factor
          | MINUS pushoperator factor addnegative
    """
    if len(p)>2:
        p[0] = p[3]
    else:
        p[0] = p[1]

def p_addcall(p):
    '''
    addcall :
    '''
    currentfunction = []
    for function in functiondirectory:
        if function[0] == p[-1][0]:
            currentfunction.append(function)
    if currentfunction[0][1] >= 0:
        if currentfunction[0][1] == 0:
            type = 'int'
        elif currentfunction[0][1] == 1:
            type = 'float'
        elif currentfunction[0][1] == 2:
            type = 'string'
        elif currentfunction[0][1] == 3:
            type = 'bool'    
        address = addtemporary(type)
        cuadruplos.append(['=', None, finder(currentfunction[0][0]), address])

def p_factor(p):
    """
    factor : LPAREN pushoperator logic RPAREN popparen
           | value
           | var
           | call addcall
    """
    if len(p)>3:
        p[0] = p[3]
    else:
        p[0] = p[1]

def p_verify(p):
    """
    verify :
    """
    for function in functiondirectory:
        if function[0] == p[-1]:
            currentfunction.append(function)
            break
    if not function: 
        print(f'오류: {p[-1]} 함수가 존재하지 않습니다.')
        quit()

def p_processcall(p):
    """
    processcall :
    """
    processcall(p)

def p_additionalparam(p):
    """
    additionalparam : additionalparam COMA logic 
                    | empty
    """
    if len(p)>2:
        if p[1] is None:
            p[0] = p[3]
        p[0] = p[1], p[3]
    else:
        p[0] = p[1]

def p_callparam(p):
    """
    callparam : logic additionalparam
              | empty
    """
    if len(p)>2:
        if p[2] is None:
            p[0] = p[1]
        p[0] = p[1], p[2]
    else:
        p[0] = p[1]
        
def p_call(p):
    """
    call : ID verify LPAREN callparam processcall RPAREN
    """
    p[0] = p[1],p[3],p[4],p[6]

def p_boolean(p):
    """
    boolean : TRUE
            | FALSE
    """
    p[0] = p[1]

def p_value(p):
    """
    value : CTE_I addint
          | CTE_F addfloat
          | CTE_S addstring
          | boolean addbool
    """
    p[0] = p[1]

def p_addint(p):
    """
    addint : 
    """
    addconstant(p, 'int')

def p_addfloat(p):
    """
    addfloat :
    """
    addconstant(p, 'float')

def p_addstring(p):
    """
    addstring : 
    """
    addconstant(p, 'string')

def p_addbool(p):
    """
    addbool :
    """
    addconstant(p, 'bool')
    
#statistical function
def p_statfun(p):
    """
    statfun : SUM LPAREN ID RPAREN
            | MIN LPAREN ID RPAREN
            | MAX LPAREN ID RPAREN
            | MEAN LPAREN ID RPAREN
            | MEDIAN LPAREN ID RPAREN
            | VARIANCE LPAREN ID RPAREN
            | HIST LPAREN ID RPAREN
            | BAR LPAREN ID COMA ID RPAREN
    """
    if len(p)==7:
        p[0] = p[1],p[2],p[3],p[4],p[5],p[6]
    else:
        p[0] = p[1],p[2],p[3],p[4]
    
def p_createstats(p):
    """
    createstats :
    """
    #return here
    if p[-1][0] == 'suljib':
        cuadruplos.append([p[-1][0].upper(), None, check(p[-1][2], 'variable')[1], check(p[-1][4], 'variable')[1]])
    else:
        cuadruplos.append([p[-1][0].upper(), None, None, check(p[-1][2], 'variable')[1]])

def p_stats(p):
    """
    stats : STATS COLON statfun createstats SEMICOLON
    """
    p[0] = p[1],p[2],p[3],p[5]

def p_empty(p):
    """
    empty :
    """
    p[0] = None

def p_error(p):
    print(f"구문 오류 '{p.value}'")
    quit()

parse = yacc.yacc()
test = open(input("컴파일할 이름 파일: "))
source = test.read()
test.close()
parse.parse(source)
# print("parsed:",result)
#print("symbols:",symbolstack)
#print("operators:",opstack)
#print("types:",typestack)
# print("quads:",cuadruplos)
#print("vars:",var_table)
#print("jumps:", jumpstack)
# print(functiondirectory)
print('너프 컴파일')
