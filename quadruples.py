#!env/bin/python
from sets import Set

id_dict = {
    'id': 'X',
    'type': 'int'
}
operators = [] # Pila de Operadores
operands = [] # Pila de Operandos
types = [] # Pila de Tipos
jumps = [] # Pila de saltos

quadruples = [] # Lista de cuadruplos

unused_temps = Set([])
used_temps = Set([])
next_temp = 1
def get_temp():
    if len( unused_temps ) == 0:
        temp = 't' + next_temp
        used_temps.add( temp )
        next_temp += 1
    else:
        temp = unused_temps.pop()
        used_temps.add(temp)
    return temp

def add_quadruple(operator, op1, type1,  op2, type2):
    result_type = semantics_cube.get( (type1, operator, type2) , 'error')
    if (result_type is not 'error'):
        if operator is '=':
            quadruples.append( [operator, op2, -1, op1] )
        else:
            quadruples.append( [operator, op1, op2, get_temp()] )
        if op1 in used_temps:
            used_temps.remove(op1)
        if op2 in used_temps:
            used_temps.remove(op2)
