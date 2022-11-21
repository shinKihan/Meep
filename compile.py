import ply.yacc as yacc
from lexer import tokens
from auxiliar import *

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
    export = constant_table+['qu']+cuadruplos
    with open(f'{p[-5]}.obj','w') as file:
        for cuad in export:
            if len(cuad) == 4:
                line = f'{cuad[0]},{cuad[1]},{cuad[2]},{cuad[3]}\n'
            else:
                line = f'{cuad[0]},{cuad[1]}\n'
            file.write(line)

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

def p_dimension(p):
    """
    dimension : COLON logic
              | empty
    """
    if p[1]:
        p[0] = p[1],p[2]

def p_dimvar(p):
    """
    dimvar : LBRKT logic dimension RBRKT
           | empty
    """
    if p[1]:
        p[0] = p[1],p[2],p[3],p[4]

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
    if env < 1:
        print("오류: 이 컨텍스트에서 반환할 수 없습니다.")
        quit()
    type = typestack.pop()
    if (type == 'int' and env > 0) or (type == 'float' and env != 1) \
        or (type == 'string' and env != 2) or (type == 'bool' and env != 3): 
        print("오류: 유형 불일치.")
        quit()
    #return here
    cuadruplos.append(['Return', None, None, finder()])

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
    p[0] = p[1],p[2]

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
    if len(p)>2:
        p[0] = p[1],p[2],p[4]
    else:
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
    if len(p)>2:
        p[0] = p[1],p[2],p[4]
    else:
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
    if len(p)>2:
        p[0] = p[1],p[2],p[4]
    else:
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
    if len(p)>2:
        p[0] = p[1],p[2],p[4]
    else:
        p[0] = p[1]

def p_exp(p):
    """
    exp : unary
        | exp EXPONENT pushoperator unary addexpresion
    """
    if len(p)>2:
        p[0] = p[1],p[2],p[4]
    else:
        p[0] = p[1]

def p_unary(p):
    """
    unary : factor
          | MINUS pushoperator factor addnegative
    """
    if len(p)>2:
        p[0] = p[1],p[2]
    else:
        p[0] = p[1]

def p_factor(p):
    """
    factor : LPAREN pushoperator logic RPAREN popparen
           | value
           | var
           | call
    """
    if len(p)>2:
        p[0] = p[1],p[3],p[4]
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
    if p[1]:
        p[0] = p[1],p[2],p[3]

def p_callparam(p):
    """
    callparam : logic additionalparam
              | empty
    """
    if p[1]:
        p[0] = p[1],p[2]

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
result = parse.parse(source)
print("parsed:",result)
#print("symbols:",symbolstack)
#print("operators:",opstack)
#print("types:",typestack)
# print("quads:",cuadruplos)
#print("vars:",var_table)
#print("jumps:", jumpstack)
print(functiondirectory)
