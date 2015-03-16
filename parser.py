#!env/bin/python
import ply.yacc as yacc
import logging
import lexer
import sys
from semantics import current, add_var_to_dict, add_func_to_dict, var_exists_in_dict, func_exists_in_dict, print_current, print_var_dict, print_func_dict, errors, clear_current, clear_local, var_dict, func_dict, semantics_cube
from copy import deepcopy


tokens = lexer.tokens

# sintaxis rules

# <program>
def p_program(p):
    '''program : config body'''

# <config>
def p_config(p):
    '''config : configdirective config
              | empty'''

# <configdirective>
def p_configdirective(p):
    '''configdirective : VARSCONFIG '=' options
                       | DECISIONSCONFIG '=' options
                       | COMPLEXITYCONFIG '=' optionsyesno'''

def p_options(p):
    '''options : SOME
               | ALL
               | MOST
               | NONE'''

def p_optionsyesno(p):
    '''optionsyesno : YES
                    | NO'''

# <body>
def p_body(p):
    '''body : declarationsOpt funcsOpt main funcsOpt'''

def p_funcsOpt(p):
    '''funcsOpt : suprafunc funcsOpt
                | empty'''

def p_declarationsOpt(p):
    '''declarationsOpt : declaration declarationsOpt
                       | empty'''

# <declaration>
def p_declaration(p):
    '''declaration : type declarationB declarationC'''

def p_declarationB(p):
    '''declarationB : ID dimensionsOpt '''
    current['id'] = p[1]

    if var_exists_in_dict(current['scope'], current['id']):
        print errors['REPEATED_DECLARATION'].format(current['id'], p.lineno(1))
        exit(1)
    else:
        add_var_to_dict(
                current['scope'],
                current['id'],
                current['type'],
                current['dimensionx'],
                current['dimensiony']
        )
        current['dimensionx'] = 0
        current['dimensiony'] = 0

def p_declarationC(p):
    '''declarationC : '=' superexpression declarationD
                    | ',' declarationB declarationC
                    | ';' '''
    if p[1] == ';':
        clear_current()
    elif p[1] == ',':
        current['dimensionx'] = 0
        current['dimensiony'] = 0

def p_declarationD(p):
    '''declarationD : ',' declarationB declarationC
                    | ';' '''

# <main>
def p_main(p):
    '''main : MAIN '(' ')' block'''

# <func>
def p_suprafunc(p):
    '''suprafunc : func block'''
    clear_current()
    clear_local()

def p_func(p):
    '''func : DEF returntype ID '(' paramsOpt ')' '''
    current['id'] = p[3]
    current['scope'] = 'local'
    current['type'] = p[2]
    if func_exists_in_dict(current['id']):
        print errors['REPEATED_FUNC_DECLARATION'].format(current['id'], p.lineno(1))
        exit(1)
    else:
        add_func_to_dict(current['id'], current['type'], deepcopy(current['params']))

def p_paramsOpt(p):
    '''paramsOpt : params paramsB
                 | empty'''

# <block>
def p_block(p):
    '''block : '{' instructionsOpt '}' '''

def p_instructionsOpt(p):
    '''instructionsOpt : instruction instructionsOpt
                       | empty'''

# <assign>
def p_assign(p):
    '''assign : ID dimensionsOpt '=' superexpression'''
    current['id'] = p[1]
    if not var_exists_in_dict(current['scope'], current['id']):
        print errors['UNDECLARED_VARIABLE'].format(p[1], p.lineno(1))
        exit(1)

def p_assignB(p):
    '''assignB : dimensionsOpt '=' superexpression'''

def p_dimensionsOpt(p):
    '''dimensionsOpt : dimensions
                     | empty'''
    p[0] = p[1]


# <condition>
def p_condition(p):
    '''condition : IF '(' superexpression ')' block else'''

# <else>
def p_else(p):
    '''else : ELSE block
            | empty'''

# <instruction>
def p_instruction(p):
    '''instruction : assignfunccall ';'
                   | output ';'
                   | return ';'
                   | input ';'
                   | declaration
                   | condition
                   | whileloop
                   | forloop
                   | localdirective '''

# <assignfunccall>
# left factor the assign and funccall rules
def p_assignfunccall(p):
    '''assignfunccall : ID assignfunccallB'''
    current['id'] = p[1]
    if current['isfunc']:
        if func_exists_in_dict(current['id']):
            if len(current['params']) != len(func_dict[ current['id'] ]['params']):
                print errors['PARAMETER_LENGTH_MISMATCH'].format(current['id'], len(func_dict[ current['id'] ]['params']),len(current['params']), p.lineno(1))
                exit(1)
        else:
            print errors['UNDECLARED_FUNCTION'].format(current['id'], p.lineno(1))
            exit(1)
        clear_current()
    else:
        if not var_exists_in_dict(current['scope'], current['id']):
            print errors['UNDECLARED_VARIABLE'].format(current['id'], p.lineno(1))




def p_assignfunccallB(p):
    '''assignfunccallB : '(' funccallB funccallC
                       | assignB'''
    current['isfunc'] = True if p[1] == '(' else False

# <localdirective>
def p_localdirective(p):
    '''localdirective : localvardirective
                      | localdecisiondirective
                      | localmsgdirective'''

# <superexpression>
def p_superexpression(p):
    '''superexpression : expression superexpressionB'''
    p[0] = p[1] + p[2]

def p_superexpressionB(p):
    '''superexpressionB : '&' '&' superexpression
                        | '|' '|' superexpression
                        | empty'''
    if p[1] is '&' or p[1] is '|':
        p[0] = p[1] + p[2] + p[3]
    else:
        p[0] = p[1]

# <expression>
def p_expression(p):
    '''expression : exp expressionB'''
    p[0] = p[1] + p[2]


def p_expressionB(p):
    '''expressionB : '<' exp
                   | '>' exp
                   | '<' '>' exp
                   | '=' '=' exp
                   | '<' '=' exp
                   | '>' '=' exp
                   | empty'''
    args = list(p)[1:]
    if len( args ) == 3:
        p[0] = p[1] + p[2] + p[3]
    elif len ( args ) == 2:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]


# <exp>
def p_exp(p):
    '''exp : term expB'''
    p[0] = p[1] + p[2]

def p_expB(p):
    '''expB : '-' exp
            | '+' exp
            | empty'''
    args = list(p)[1:]
    if len( args ) == 2:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]

# <term>
def p_term(p):
    '''term : factor termB'''
    p[0] = p[1] + p[2]

def p_termB(p):
    '''termB : '/' term
             | '*' term
             | empty'''
    args = list(p)[1:]
    if len( args ) == 2:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]

# our lexer gets the sign with the int in case it has one.
# And I just found out this is wrong. Removed the sign from the lexer and added it here.
# <factor>
def p_factor(p):
    '''factor : signB constant
              | '(' superexpression ')'
              | funccall
              | ID seen_ID dimensionsOpt'''
    args = list(p)[1:]
    if len( args ) == 3:
        p[0] = p[1] + p[2] + p[3]
        if ( p[2] is 'UNDECLARED_VARIABLE' ):
            print errors['UNDECLARED_VARIABLE'].format(p[1], p.lineno(1))
            exit(1)
    elif len ( args ) == 2:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]






def p_seen_ID(p):
    '''seen_ID :'''
    if not var_exists_in_dict(current['scope'], p[-1]):
        p[0] = 'UNDECLARED_VARIABLE'
    else:
        p[0] = ""


def p_signB(p):
    '''signB : sign
             | empty'''
    p[0] = p[1]

# <constant>
def p_constant(p):
    '''constant : FCONST
                | ICONST
                | SCONST
                | TRUE
                | FALSE'''
    p[0] = p[1]

# <sign>
def p_sign(p):
    """sign : '+'
            | '-' """
    p[0] = p[1]

# <whileloop>
def p_whileloop(p):
    '''whileloop : WHILE '(' superexpression ')' block'''

# <type>
def p_type(p):
    '''type : INT
            | FLOAT
            | STRING
            | BOOL'''
    current['type'] = p[1]
    p[0] = p[1]

# <returntype>
def p_returntype(p):
    '''returntype : VOID
                  | type'''
    p[0] = p[1]

# <forloop>
def p_forloop(p):
    '''forloop : FOR '(' assign ';' superexpression ';' superexpression ')' block'''

# <input>
def p_input(p):
    """input : INPUT '(' ID inputB ')' """

def p_inputB(p):
    '''inputB : ',' ID inputB
              | empty'''
# <output>
def p_output(p):
    '''output : PRINT '(' outputB '''

def p_outputB(p):
    '''outputB : SCONST outputC
               | superexpression outputC'''

def p_outputC(p):
    '''outputC : ')'
               | ',' outputB '''

# <localvardirective>
def p_localvardirective(p):
    '''localvardirective : '#' localvardirectiveB ID'''

def p_localvardirectiveB(p):
    '''localvardirectiveB : TRACK
                          | FORGET'''

# <localmsgdirective>
def p_localmsgdirective(p):
    '''localmsgdirective : '#' SHOW SCONST'''

# <localdecisiondirective>
def p_localdecisiondirective(p):
    '''localdecisiondirective : TRACKDECISION
                              | FORGETDECISION
                              | empty'''

# <funccall>
def p_funccall(p):
    '''funccall : ID '(' funccallB funccallC  '''
    current['id'] = p[1]
    if func_exists_in_dict(current['id']):
        if len(current['params']) != len(func_dict[ current['id'] ]['params']):
            print errors['PARAMETER_LENGTH_MISMATCH'].format(current['id'], len(func_dict[ current['id'] ]['params']),len(current['params']), p.lineno(1))
            exit(1)
    else:
        print errors['UNDECLARED_FUNCTION'].format(current['id'], p.lineno(1))
        exit(1)
    p[0] = p[1] + p[2] + p[3] + p[4]
    clear_current()

def p_funccallB(p):
    '''funccallB : superexpression
                 | empty '''
    if  p[1] is not '':
        current['params'].append(1)
    p[0] = p[1]

def p_funccallC(p):
    '''funccallC : ',' funccallB funccallC
                 | ')' '''
    if p[1] is not ')':
        p[0] = p[1] + p[2] + p[3]
    else:
        p[0] = p[1]

# <dimensions>
def p_dimensions(p):
    '''dimensions : '[' superexpression ']' dimensionsB '''
    current['dimensionx'] = 1
    p[0] = p[1] + p[2] + p[3] + p[4]

def p_dimensionsB(p):
    '''dimensionsB : '[' superexpression ']'
                   | empty '''
    current['dimensiony'] = ( 1 if p[1] == '[' else 0 )
    if p[1] is not '':
        p[0] = p[1] + p[2] + p[3]
    else:
        p[0] = p[1]

# <return>
def p_return(p):
    '''return : RETURN superexpression'''

# <params>
def p_params(p):
    '''params : type ID '''
    current['params'].append(current['type'])
    if var_exists_in_dict('local', p[2]):
        print errors['REPEATED_DECLARATION'].format(p[2], p.lineno(2))
        exit(1)
    else:
        add_var_to_dict('local', p[2], p[1], 0, 0)

def p_paramsB(p):
    '''paramsB : ',' params paramsB
               | empty'''

def p_empty(p):
    '''empty : '''
    p[0] = ""

def p_error(p):
    print "Syntax error in input token {0} with value {1}, in line {2}".format(p.type, p.value, p.lineno)
    exit(1)

parser = yacc.yacc()

if(len(sys.argv) > 1):
    if sys.argv[1] == "-f":
        f = open(sys.argv[2], "r")
        s = f.readlines()
    string = ""
    for line in s:
        string += line
    print string
    logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)
    log = logging.getLogger()
    result = parser.parse(string, debug=log)
else:
    print "Error"
