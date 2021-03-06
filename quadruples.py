#!env/bin/python
from sets import Set
from semantics import semantics_cube, debug_var_const_dict, debug, temp_dict, add_to_memory, current
from MemoryBlock import MemoryBlock
import pprint
pp = pprint.PrettyPrinter()

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
    print 'QUADRUPLES KEY'
    pp.pprint( debug_var_const_dict )
    print 'QUADRUPLES'
    i = 0
    for q in quadruples:
        print i, debug_quadruple(q) if debug else q
        i += 1

def is_number(s):
    if s is None: return False
    try:
        int(s)
        return True
    except ValueError:
        return False

def debug_quadruple(q):
    debugged = []
    for elem in q:
        if is_number(elem) and elem > 0:
            debugged.append( debug_var_const_dict.get(elem, elem) )
        else:
            debugged.append(elem)
    return debugged

temps = {
    'bool': { 'unused': Set([]), 'used': Set([])},
    'int': {'unused': Set([]), 'used': Set([])},
    'float': {'unused': Set([]), 'used': Set([])},
    'char': {'unused': Set([]), 'used': Set([])},
    'string': {'unused': Set([]), 'used': Set([])}
}
next_temp = 1

def clear_temps(mem_temps):
    global temps, next_temp
    temps = {
        'bool': { 'unused': Set([]), 'used': Set([])},
        'int': {'unused': Set([]), 'used': Set([])},
        'float': {'unused': Set([]), 'used': Set([])},
        'char': {'unused': Set([]), 'used': Set([])},
        'string': {'unused': Set([]), 'used': Set([])}
    }
    next_temp = 1
    mem_temps = MemoryBlock(15000, 16000, 17000, 18000, 19000, 20000)

def get_temp(temp_type, mem_temps):
    global next_temp, temps
    if len( temps[temp_type]['unused'] ) == 0:
        temp = 't{0}'.format( next_temp )
        next_temp += 1
        address = add_to_memory(mem_temps, temp_type)
        temp_dict[temp] = address
        debug_var_const_dict[temp_dict[temp]] = temp
    else:
        address = temps[temp_type]['unused'].pop()

    temps[temp_type]['used'].add( address )
    return address

global_temps = {
    'bool': { 'unused': Set([]), 'used': Set([])},
    'int': {'unused': Set([]), 'used': Set([])},
    'float': {'unused': Set([]), 'used': Set([])},
    'char': {'unused': Set([]), 'used': Set([])},
    'string': {'unused': Set([]), 'used': Set([])}
}
next_global_temp = 1
def get_global_temp(temp_type, mem_global_temps):
    global next_global_temp, global_temps
    if len( global_temps[temp_type]['unused'] ) == 0:
        temp = 'gt{0}'.format( next_global_temp )
        next_global_temp += 1
        address = add_to_memory(mem_global_temps, temp_type)
        temp_dict[temp] = address
        debug_var_const_dict[temp_dict[temp]] = temp
    else:
        address = global_temps[temp_type]['unused'].pop()

    global_temps[temp_type]['used'].add( address )
    return address

relational_operators = Set(['<', '>', '<>', '==', '<=', '>='])
logical_operators = Set(['AND', 'OR'])
ignored_checks = Set(['PRINT', 'READ', 'INPUT', 'GOTOF', 'GOTO', 'RETURN', 'PARAMETER', 'ERA', 'GOSUB', 'ENDPROC', 'TRACK', 'FORGET', '#TRACKDECISION', '#FORGETDECISION', 'SHOW', 'DECLARE', 'VERIFY', 'SUMDIR', 'ROWOFFSET', 'COLUMNOFFSET'])

def add_quadruple(operator, op1, type1,  op2, type2, mem_temps, mem_global_temps, modIndex=0):
    print current['scope'], operator, op1, type1, op2 ,type2

    result_type = check_operation(type1, operator, type2)

    if result_type is 'error':
        print 'No se puede hacer la operacion con los tipos: {0}, {1}, {2}'.format(type1, operator, type2)
        exit(1)

    if operator is '=':
        quadruples.append( [operator, op2, modIndex, op1] )
    elif operator == 'PRINT':
        quadruples.append( [operator, op2, -1, op1] )
    elif operator == 'READ':
        quadruples.append( [operator, -1, -1, op1] )
    elif operator == 'GOTOF':
        quadruples.append( [operator, op1, op2, -1] )
    elif operator == 'GOTO':
        quadruples.append( [operator, -1, -1, op1] )
    elif operator == 'RETURN':
        quadruples.append( [operator, op2, -1, op1] )
    elif operator == 'PARAMETER':
        quadruples.append( [operator, op1, -1, op2] )
    elif operator == 'ERA':
        quadruples.append( [operator, -1, -1, op1] )
    elif operator == 'GOSUB':
        quadruples.append( [operator, op2, -1, op1] )
    elif operator == 'ENDPROC':
        quadruples.append( [operator, -1, -1, op1] )
    elif operator == 'TRACK':
        quadruples.append( [operator, -1, -1, op1] )
    elif operator == 'FORGET':
        quadruples.append( [operator, -1, -1, op1] )
    elif operator == '#TRACKDECISION':
        quadruples.append( ['TRACKDECISION', -1, -1, -1] )
    elif operator == '#FORGETDECISION':
        quadruples.append( ['FORGETDECISION', -1, -1, -1] )
    elif operator == 'SHOW':
        quadruples.append( [operator, -1, -1, op1] )
    elif operator == 'DECLARE':
        quadruples.append( [operator, op1, -1, op2] )
    elif operator == 'VERIFY':
        quadruples.append( [operator, op1, -1, op2] )
    elif operator == 'ROWOFFSET':
        result_type = type1
        if current['scope'] == 'global':
            temp = get_global_temp(result_type, mem_global_temps)
        else:
            temp = get_temp(result_type, mem_temps)

        quadruples.append( ['ROWOFFSET', op1, op2, temp] )
        operands.append( temp )
        types.append(result_type)
    elif operator == 'COLUMNOFFSET':
        result_type = type1
        if current['scope'] == 'global':
            temp = get_global_temp(result_type, mem_global_temps)
        else:
            temp = get_temp(result_type, mem_temps)

        quadruples.append( ['COLUMNOFFSET', op1, op2, temp] )
        operands.append(temp)
        types.append(result_type)
    elif operator == 'SUMDIR':
        result_type = type1
        if current['scope'] == 'global':
            temp = get_global_temp(result_type, mem_global_temps)
        else:
            temp = get_temp(result_type, mem_temps)

        quadruples.append( ['SUMDIR', op1, op2, temp] )
        operands.append(str( op1 )+'*'+str( temp ))
        types.append(type1)
    else:
        if current['scope'] == 'global':
            temp = get_global_temp(result_type, mem_global_temps)
        else:
            temp = get_temp(result_type, mem_temps)

        quadruples.append( [operator, op1, op2, temp] )
        operands.append(temp)
        types.append(result_type)

    print_quadruples()
    print_operators()
    print_operands()
    if current['scope'] == 'global':
        return_global_temp_operands(op1, type1,  op2, type2)
    else:
        if not ( operator == '=' and op1 in temps[type1]['used'] ):
            return_temp_operands(op1, type1,  op2, type2)


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

def parse_to_temp_address_if_necessary(value):
    s = str(value)
    if '*' in s:
        dirs = s.split('*')
        return int( dirs[1] )
    else:
        return value

def parse_to_base_address_if_necessary(value):
    s = str(value)
    if '*' in s:
        dirs = s.split('*')
        return int( dirs[0] )
    else:
        return value

def return_temp_operands(op1, type1,  op2, type2):
    ''' Note: We are asuming IDs that are introduced by the user cant be t[0-9] '''
    op1 = parse_to_temp_address_if_necessary(op1)
    op2 = parse_to_temp_address_if_necessary(op2)
    if type1 != -1 and op1 in temps[type1]['used']:
        temps[type1]['used'].remove( op1 )
        temps[type1]['unused'].add( op1 )
    if type2 != -1 and op2 in temps[type2]['used']:
        temps[type2]['used'].remove( op2)
        temps[type2]['unused'].add( op2)

def return_global_temp_operands(op1, type1,  op2, type2):
    ''' Note: We are asuming IDs that are introduced by the user cant be t[0-9] '''
    op1 = parse_to_temp_address_if_necessary(op1)
    op2 = parse_to_temp_address_if_necessary(op2)
    if type1 != -1 and op1 in global_temps[type1]['used']:
        global_temps[type1]['used'].remove( op1 )
        global_temps[type1]['unused'].add( op1 )
    if type2 != -1 and op2 in global_temps[type2]['used']:
        global_temps[type2]['used'].remove( op2 )
        global_temps[type2]['unused'].add( op2 )

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
