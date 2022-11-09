import ply.lex as lex

reserved_words = {
    'sijag'     : 'START',
    'gibon'     : 'MAIN',
    'heolag'    : 'VAR',
    'iblyeog'   : 'READ',
    'inswae'    : 'WRITE',
    'man'       : 'IF',
    'tto'       : 'ELSE',
    'hada'      : 'DO',
    'dong'      : 'WHILE',
    'gijun'     : 'FUNCTION',
    'banpum'    : 'RETURN',
    'kkeut'     : 'END',
    'jeo'       : 'INT',
    'tteuda'    : 'FLOAT',
    'kkeun'     : 'STRING',
    'muhyoui'   : 'VOID',
    'keugi'     : 'SIZE',
    'pyeong'    : 'MEAN',
    'jung'      : 'MEDIAN',
    'byeon'     : 'VARIANCE',
    'std'       : 'STD',
    'habji'     : 'SUM',
    'bun'       : 'MIN',
    'choe'      : 'MAX',
    'hiseu'     : 'HIST',
    'suljib'    : 'BAR'
}

tokens = [
    'ID',
    'CTE_I',
    'CTE_F',
    'CTE_S',
    'EXPONENT',
    'MOD',
    'PERCENT',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'INT_DIV',
    'LT',
    'LE',
    'GT',
    'GE',
    'EQ',
    'NE',
    'AND',
    'OR',
    'ASSIGN',
    'COLON',
    'SEMICOLON',
    'COMA',
    'LPAREN',
    'RPAREN',
    'L_SBRKT',
    'R_SBRKT',
    'L_CURLY',
    'R_CURLY'
] + list(reserved_words.values())

t_EXPONENT      = r'\^'
t_PERCENT       = r'\%\%'
t_MOD           = r'\%'
t_PLUS          = r'\+'
t_MINUS         = r'-'
t_MULTIPLY      = r'\*'
t_INT_DIV       = r'//'
t_DIVIDE        = r'/'
t_ASSIGN         = r'\='
t_LE            = r'\<='
t_LT            = r'\<'
t_GE            = r'>='
t_GT            = r'>'
t_EQ            = r'\=\='
t_NE            = r'\!\='
t_AND           = r'\&'
t_OR            = r'\|'         
t_COLON         = r'\:'
t_SEMICOLON     = r'\;'
t_COMA          = r'\,'
t_LPAREN        = r'\('
t_RPAREN        = r'\)'
t_L_SBRKT       = r'\['
t_R_SBRKT       = r'\]'
t_L_CURLY       = r'\{'
t_R_CURLY       = r'\}'

t_ignore = ' \t\n\r\f'


def t_ID(t):
    r'[a-zA-Z_]\w*'
    if t.value in reserved_words.keys():
        t.type = reserved_words[t.value]
    else:
        t.type = 'ID'
    return t

def t_CTE_F(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_CTE_I(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CTE_S(t):
    r'"([^\\"\n]+|\\.)*"'
    t.type = 'CTE_S'
    return t

def t_error(t):
    print("불법 문자 '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

# data = input('meep ')
# lexer.input(data)

# while True:
#     tok = lexer.token()
#     if not tok:
#         break      # No more input
#     print(tok)