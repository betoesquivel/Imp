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

