Cube = {
    #        Int                                         Float                                      String                                   Bool                                 Pointer 
    '^'    : [['float', 'float', None, None, 'pointer'], ['float', 'float', None, None, 'pointer'], [None, None, None, None, 'pointer'],     [None, None, None, None, 'pointer'], ['pointer', 'pointer', 'pointer', None, 'pointer']],
    '%%'   : [['float', 'float', None, None, 'pointer'], ['float', 'float', None, None, 'pointer'], [None, None, None, None, 'pointer'],     [None, None, None, None, 'pointer'], ['pointer', 'pointer', 'pointer', None, 'pointer']],
    '%'    : [['int', 'int', None, None, 'pointer'],     ['int', 'int', None, None, 'pointer'],     [None, None, None, None, 'pointer'],     [None, None, None, None, 'pointer'], ['pointer', 'pointer', 'pointer', None, 'pointer']],
    '+'    : [['int', 'float', None, None, 'pointer'],   ['float', 'float', None, None, 'pointer'], [None, None, None, None, 'pointer'],     [None, None, None, None, 'pointer'], ['pointer', 'pointer', 'pointer', None, 'pointer']],
    '-'    : [['int', 'float', None, None, 'pointer'],   ['float', 'float', None, None, 'pointer'], [None, None, None, None, 'pointer'],     [None, None, None, None, 'pointer'], ['pointer', 'pointer', 'pointer', None, 'pointer']],
    '*'    : [['int', 'float', None, None, 'pointer'],   ['float', 'float', None, None, 'pointer'], [None, None, None, None, 'pointer'],     [None, None, None, None, 'pointer'], ['pointer', 'pointer', 'pointer', None, 'pointer']],
    '//'   : [['int', 'int', None, None, 'pointer'],     ['int', 'int', None, None, 'pointer'],     [None, None, None, None, 'pointer'],     [None, None, None, None, 'pointer'], ['pointer', 'pointer', 'pointer', None, 'pointer']],
    '/'    : [['float', 'float', None, None, 'pointer'], ['float', 'float', None, None, 'pointer'], [None, None, None, None, 'pointer'],     [None, None, None, None, 'pointer'], ['pointer', 'pointer', 'pointer', None, 'pointer']],
    '='    : [['int', None, None, None, 'pointer'],      [None, 'float', None, None, 'pointer'],    [None, None, "string", None, 'pointer'], [None, None, None, None, None],      ['int', 'float', 'string', None, 'pointer']],
    '<='   : [['bool', 'bool', None, None, 'bool'],      ['bool', 'bool', None, None, 'bool'],      [None, None, None, None, None],          [None, None, None, None, 'bool'],    ['bool', 'bool', None, None, 'pointer']],
    '<'    : [['bool', 'bool', None, None, 'bool'],      ['bool', 'bool', None, None, 'bool'],      [None, None, None, None, None],          [None, None, None, None, 'bool'],    ['bool', 'bool', None, None, 'pointer']],
    '>='   : [['bool', 'bool', None, None, 'bool'],      ['bool', 'bool', None, None, 'bool'],      [None, None, None, None, None],          [None, None, None, None, 'bool'],    ['bool', 'bool', None, None, 'pointer']],
    '>'    : [['bool', 'bool', None, None, 'bool'],      ['bool', 'bool', None, None, 'bool'],      [None, None, None, None, None],          [None, None, None, None, 'bool'],    ['bool', 'bool', None, None, 'pointer']],
    '=='   : [['bool', 'bool', None, None, 'bool'],      ['bool', 'bool', None, None, 'bool'],      [None, None, None, None, None],          [None, None, None, None, 'bool'],    ['bool', 'bool', None, None, 'pointer']],
    '!='   : [['bool', 'bool', None, None, 'bool'],      ['bool', 'bool', None, None, 'bool'],      [None, None, None, None, None],          [None, None, None, None, 'bool'],    ['bool', 'bool', None, None, 'pointer']],
    '&'    : [[None, None, None, None, None],            [None, None, None, None, None],            [None, None, None, None, None],          [None, None, None, 'bool', 'bool'],  [None, None, None, None, None]],
    '|'    : [[None, None, None, None, None],            [None, None, None, None, None],            [None, None, None, None, None],          [None, None, None, 'bool', 'bool'],  [None, None, None, None, None]]
}

def fetch(coord):
    if len(coord) == 2:
        opr, op = coord
        res = Cube[opr][op]
    else:
        opr, op1, op2 = coord
        res = Cube[opr][op1][op2]
    return res