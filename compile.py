import ply.yacc as yacc
from lexer import tokens

def p_prog(p):
    """
    prog : START ID COLON expression END 
    """
    p[0] = p[1],p[2],p[3],p[4],p[5]

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
          | logic oplogic comp
    """ 
    if len(p)>2:
        p[0] = p[1],p[2],p[3]
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
          | comp opcomp sum
    """ 
    if len(p)>2:
        p[0] = p[1],p[2],p[3]
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
        | sum opsum term
    """
    if len(p)>2:
        p[0] = p[1],p[2],p[3]
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
         | term opterm exp
    """
    if len(p)>2:
        p[0] = p[1],p[2],p[3]
    else:
        p[0] = p[1]

def p_exp(p):
    """
    exp : unary
        | exp EXPONENT unary
    """
    if len(p)>2:
        p[0] = p[1],p[2],p[3]
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
    factor : value 
           | LPAREN logic RPAREN
           | ID
    """
    if len(p)>2:
        p[0] = p[1],p[2],p[3]
    else:
        p[0] = p[1]

def p_value(p):
    """
    value : CTE_I
          | CTE_F
          | CTE_S
    """
    p[0] = p[1]

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
