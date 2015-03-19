#!env/bin/python
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
    'def'       : 'DEF',
    'string'    : 'STRING'
}


tokens = [
          # Config vars
          'VARSCONFIG', 'DECISIONSCONFIG', 'COMPLEXITYCONFIG',
          # Decision directives
          'TRACKDECISION', 'FORGETDECISION',
          # Logical operators
          'AND', 'OR',
          # Relational operators
          'DIFF','EQ','GTEQ','LTEQ',
          # Constantes
          'SCONST','ICONST','FCONST','ID'
] +  list(reserved.values())

# non-terminals or tokens
t_VARSCONFIG = r'\#vars'
t_DECISIONSCONFIG = r'\#decisions'
t_COMPLEXITYCONFIG = r'\#complexity'
t_TRACKDECISION = r'\#trackdecision'
t_FORGETDECISION = r'\#forgetdecision'
t_SCONST = r'".*"'
t_ICONST = r'\d+'
t_FCONST = r'\d+\.\d+'
t_DIFF = r'<>'
t_EQ = r'=='
t_GTEQ = r'>='
t_LTEQ = r'<='
t_AND = r'&&'
t_OR = r'||'
t_ignore = ' \t'

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
        print "Illegal character {0} in {1}. Line number: {2}".format( t.value[0] , t.value, t.lexer.lineno ),
        t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()
