import ply.yacc as yacc
from lexer import tokens
from auxiliar import *

#Begining of grammar
def p_prog(p):
    """
    prog : START ID COLON global END 
    """
    p[0] = p[1],p[2],p[3],p[4],p[5]

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

def p_fun(p):
    """
    fun : FUNCTION funtype ID LPAREN funparam RPAREN LCURLY block RCURLY 
    """
    p[0] = p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9]

def p_main(p):
    """
    main : VOID MAIN LPAREN RPAREN LCURLY block RCURLY 
    """
    p[0] = p[1],p[2],p[3],p[4],p[5],p[6],p[7]

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

def p_var(p):
    """
    var : ID dimvar
    """
    p[0] = p[1],p[2]

def p_assign(p):
    """
    assign : var ASSIGN expression
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

def p_declare(p):
    """
    declare : VAR type ID array SEMICOLON
    """
    p[0] = p[1],p[2],p[3],p[4],p[5]
    
def p_read(p):
    """
    read : READ LPAREN ID RPAREN SEMICOLON
    """
    p[0] = p[1],p[2],p[3],p[4],p[5]

def p_write(p):
    """
    write : WRITE LPAREN logic RPAREN SEMICOLON
    """
    p[0] = p[1],p[2],p[3],p[4],p[5]

def p_return(p):
    """
    return : RETURN expression
    """
    p[0] = p[1],p[2]

def p_type(p):
    """
    type : INT
         | FLOAT
         | STRING
    """
    p[0] = p[1]

#Compound statement
def p_while(p):
    """
    while : WHILE LPAREN logic RPAREN LCURLY block RCURLY
    """
    p[0] = p[1],p[2],p[3],p[4],p[5],p[6],p[7]

def p_else(p):
    """
    else : ELSE LCURLY block RCURLY
         | empty
    """
    if p[1]:
        p[0] = p[1],p[2],p[3],p[4]

def p_if(p):
    """
    if : IF LPAREN logic RPAREN LCURLY block RCURLY else
    """
    p[0] = p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8]

#Begining of expresion
def p_pop(p):
    """
    pop : 
    """
    if typestack:
       symbolstack.pop()
       typestack.pop()

def p_pushoperator(p):
    """
    pushoperator :
    """
    opstack.append(p[-1])

def p_addexpresion(p):
    """
    addexpresion :
    """
    addexpresion(p[-3])

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
          | MINUS factor
    """
    if len(p)>2:
        p[0] = p[1],p[2]
    else:
        p[0] = p[1]

def p_factor(p):
    """
    factor : LPAREN logic RPAREN 
           | value
           | var
           | call
    """
    if len(p)>2:
        p[0] = p[1],p[2],p[3]
    else:
        p[0] = p[1]

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
    call : ID LPAREN callparam RPAREN
    """
    p[0] = p[1],p[2],p[3],p[4]

def p_value(p):
    """
    value : CTE_I addint
          | CTE_F addfloat
          | CTE_S addstring
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
    
def p_stats(p):
    """
    stats : STATS COLON statfun SEMICOLON
    """
    p[0] = p[1],p[2],p[3],p[4]

def p_empty(p):
    """
    empty :
    """
    p[0] = None

def p_error(p):
    print("구문 오류")

parse = yacc.yacc()
test = open(input("meep "))
source = test.read()
test.close()
result = parse.parse(source)
print(result)
print(symbolstack)
print(typestack)
print(constant_table)
print(cuadruplos)
