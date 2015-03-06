#!/bin/python
import ply.lex as lex

# literal characters
literals = "#(){}<>=-+*/,|&:;"

# reserved words
reserved = {
    #'vars'      : 'VARS',
    #'decisions' : 'DECISIONS',
    #'complexity': 'COMPLEXITY',
    'SOME'      : 'SOME',
    'ALL'       : 'ALL',
    'MOST'      : 'MOST',
    'NONE'      : 'NONE',
    'YES'       : 'YES',
    'NO'        : 'NO',
    'main'      : 'MAIN',
    'if'        : 'IF',
    'else'      : 'ELSE',
    'print'     : 'PRINT',
    'track'     : 'TRACK',
    'forget'    : 'FORGET',
    'show'      : 'SHOW',
    #'decision'  : 'DECISION',
    'true'      : 'TRUE',
    'false'     : 'FALSE',
    'while'     : 'WHILE',
    'int'       : 'INT',
    'float'     : 'FLOAT',
    'void'      : 'VOID',
    'for'       : 'FOR',
    'input'     : 'INPUT',
    'return'    : 'RETURN',
    'bool'      : 'BOOL',
    'def'      : 'DEF'
}


tokens = [
          # Config vars
          'VARSCONFIG', 'DECISIONSCONFIG', 'COMPLEXITYCONFIG',
          # Decision directives
          'TRACKDECISION', 'FORGETDECISION',
          # Constantes
          'STRING','ICONST','FCONST','ID'
] +  list(reserved.values())

# non-terminals or tokens
t_VARSCONFIG = r'\#vars'
t_DECISIONSCONFIG = r'\#decisions'
t_COMPLEXITYCONFIG = r'\#complexity'
t_TRACKDECISION = r'\#trackdecision'
t_FORGETDECISION = r'\#forgetdecision'
t_STRING = r'".*"'
t_ICONST = r'\d+'
t_FCONST = r'\d+\.\d+'
t_ignore = ' \t\n\r'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t

# gather line info
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# get error
def t_error(t):
    if(t.value[0] != None):
        print "Illegal character ", t.value[0] ,
        t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()
