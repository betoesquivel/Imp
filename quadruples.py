#!env/bin/python
from sets import Set
from semantics import semantics_cube

id_dict = {
    'id': 'X',
    'type': 'int'
}
operators = [] # Pila de Operadores
operands = [] # Pila de Operandos
types = [] # Pila de Tipos
jumps = [] # Pila de saltos

quadruples = [] # Lista de cuadruplos

def print_operators():
    print 'OPERATORS'
    print operators

def print_operands():
    print 'OPERANDS'
    print operands

def print_types():
    print 'TYPES'
    print types


def print_quadruples():
    print 'QUADRUPLES'
    i = 0
    for q in quadruples:
        print i, q
        i += 1

unused_temps = Set([])
used_temps = Set([])
next_temp = 1
def get_temp():
    global next_temp, unused_temps, used_temps
    if len( unused_temps ) == 0:
        temp = 't{0}'.format( next_temp )
        used_temps.add( temp )
        next_temp += 1
    else:
        temp = unused_temps.pop()
        used_temps.add(temp)
    return temp

relational_operators = Set(['<', '>', 'DIFF', 'EQ', 'LTEQ', 'GTEQ'])
logical_operators = Set(['AND', 'OR'])
ignored_checks = Set(['PRINT', 'INPUT', 'GOTOF', 'GOTO', 'RETURN'])

def add_quadruple(operator, op1, type1,  op2, type2):

    result_type = check_operation(type1, operator, type2)

    if result_type is 'error':
        print 'Error, tonto!'
        exit(1)

    if operator is '=':
        quadruples.append( [operator, op2, -1, op1] )
    elif operator is 'PRINT':
        quadruples.append( [operator, -1, -1, op1] )
    elif operator is 'GOTOF':
        quadruples.append( [operator, op1, -1, -1] )
    elif operator is 'GOTO':
        quadruples.append( [operator, -1, -1, op1] )
    elif operator is 'RETURN':
        quadruples.append( [operator, -1, -1, op1] )
    else:
        temp = get_temp()
        quadruples.append( [operator, op1, op2, temp] )
        operands.append(temp)
        types.append(result_type)

    print_quadruples()
    print_operators()
    print_operands()
    return_temp_operands(op1, op2)


def check_operation(type1, operator,  type2):
    if operator is '=':
        return semantics_cube.get( (type1, operator, type2) , 'error')
    elif operator in ignored_checks:
        return 'continue'
    elif operator in relational_operators:
        result_type = semantics_cube.get( (type1, 'comp', type2) , 'error')
        if result_type is 'error':
            result_type = semantics_cube.get( (type2, 'comp', type1) , 'error')
        return result_type
    elif operator in logical_operators:
        result_type = semantics_cube.get( (type1, 'log', type2) , 'error')
        if result_type is 'error':
            result_type = semantics_cube.get( (type2, 'log', type1) , 'error')
        return result_type
    else:
        result_type = semantics_cube.get( (type1, operator, type2) , 'error')
        if result_type is 'error':
            result_type = semantics_cube.get( (type2, operator, type1) , 'error')
        return result_type

def return_temp_operands(op1, op2):
    ''' Note: We are asuming IDs that are introduced by the user cant be t[0-9] '''
    if op1 in used_temps:
        used_temps.remove(op1)
        unused_temps.add(op1)
    if op2 in used_temps:
        used_temps.remove(op2)
        unused_temps.add(op2)

def return_pending_quadruple(operator_list):
    operator_set = Set(operator_list)

    op = 'none_pending'
    op2 = 'none_pending'
    type2 = 'none_pending'
    op1 = 'none_pending'
    type1 = 'none_pending'

    if operators:
        top_op = operators.pop()
        if top_op in operator_set:
            op = top_op
            op2 = operands.pop()
            type2 = types.pop()
            op1 = operands.pop()
            type1 = types.pop()
        else:
             operators.append (top_op)

    return op, op1, type1, op2, type2
