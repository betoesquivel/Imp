#!/bin/python
import ply.lex as lex

# literal characters
literals = "#(){}<>=+*/,|&:;"

# reserved words
reserved = {
    'vars'      : 'VARS',
    'decisions' : 'DECISIONS',
    'complexity': 'COMPLEXITY',
    'some'      : 'SOME',
    'all'       : 'ALL',
    'most'      : 'MOST',
    'none'      : 'NONE',
    'yes'       : 'YES',
    'no'        : 'NO',
    'main'      : 'MAIN',
    'if'        : 'IF',
    'else'      : 'ELSE',
    'print'     : 'PRINT',
    'track'     : 'TRACK',
    'forget'    : 'FORGET',
    'show'      : 'SHOW',
    'decision'  : 'DECISION',
    'true'      : 'TRUE',
    'false'     : 'FALSE',
    'while'     : 'WHILE',
    'int'       : 'INT',
    'float'     : 'FLOAT',
    'void'      : 'VOID',
    'for'       : 'FOR',
    'input'     : 'INPUT',
    'return'    : 'RETURN',
    'bool'      : 'BOOL'
}

tokens = [
          # Constantes
          'STRING','ICONST','FCONST','ID'
] +  list(reserved.values())

# non-terminals or tokens
t_STRING = r'".*"'
t_ICONST = r'[\+-]?\d+'
t_FCONST = r'[\+-]?\d+\.\d+'
t_ignore = ' \t\n\r'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t

# get error
def t_error(t):
    if(t.value[0] != None):
        print "Illegal character ", t.value[0] ,
        t.lexer.skip(1)

# Build the lexer
lex.lex()
