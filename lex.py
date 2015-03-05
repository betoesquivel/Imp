import ply.lex as lex

#var no terminales
t_EQUAL     = r'='
t_DIFFERENT = r'<>'
t_LESSTHAN  = r'<'
t_GREATHAN  = r'>'
t_GREATEQUAL = r'\>='
t_LESSEQUAL  = r'\<='
t_TWOEQUAL  = r'=='
t_AND       = r'&&'
t_OR        = r'\|\|'
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACE    = r'\{'
t_RBRACE    = r'\}'
t_SEMI      = r';'
t_COMMA     = r','
t_DOUBLEDOT = r':'
t_HASHTAG   = r'#'
t_STRING 	= r'\'.*\''
t_ICONST      = r'[\+-]?\d+'
t_FCONST     = r'[\+-]?\d+\.\d+'
t_ignore 	= ' \t\n\r' #ignorar espacios

#pal reservadas
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
    # 'and'       : 'AND',
    # 'or'        : 'OR',
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

# List of token names
tokens = [
          # Asign
          'EQUAL',
          # Comparison
          'DIFFERENT','LESSTHAN','GREATHAN','GREATEQUAL','LESSEQUAL','TWOEQUAL',
          # Logical
          'AND', 'OR',
          # Operators
          'PLUS','MINUS','TIMES','DIVIDE',
          # Separators
          'LPAREN','RPAREN','LBRACE','RBRACE','SEMI','COMMA','DOUBLEDOT', 'HASHTAG',
          # Constantes
          'STRING','ICONST','FCONST','ID'
         ] +  list(reserved.values())

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t

# get error
def t_error(t):
    if(t.value[0] != None):
        print "Caracter ilegal ", t.value[0] ,
        t.lexer.skip(1)

# Build the lexer
lex.lex()