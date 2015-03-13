#!env/bin/python
import ply.yacc as yacc
import logging
import lexer
import sys
from semantics import current, add_var_to_dict, add_func_to_dict, var_exists_in_dict, func_exists_in_dict, print_current, print_var_dict, print_func_dict, errors, clear_current, clear_local

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
        print errors['REPEATED_DECLARATION']
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
        add_func_to_dict(current['id'], current['type'], current['params'])

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

def p_assignfunccallB(p):
    '''assignfunccallB : '(' funccallB
                       | assignB'''

# <localdirective>
def p_localdirective(p):
    '''localdirective : localvardirective
                      | localdecisiondirective
                      | localmsgdirective'''

# <superexpression>
def p_superexpression(p):
    '''superexpression : expression superexpressionB'''

def p_superexpressionB(p):
    '''superexpressionB : '&' '&' superexpression
                        | '|' '|' superexpression
                        | empty'''

# <expression>
def p_expression(p):
    '''expression : exp expressionB'''

def p_expressionB(p):
    '''expressionB : '<' exp
                   | '>' exp
                   | '<' '>' exp
                   | '=' '=' exp
                   | '<' '=' exp
                   | '>' '=' exp
                   | empty'''

# <exp>
def p_exp(p):
    '''exp : term expB'''

def p_expB(p):
    '''expB : '-' exp
            | '+' exp
            | empty'''

# <term>
def p_term(p):
    '''term : factor termB'''

def p_termB(p):
    '''termB : '/' term
             | '*' term
             | empty'''

# our lexer gets the sign with the int in case it has one.
# And I just found out this is wrong. Removed the sign from the lexer and added it here.
# <factor>
def p_factor(p):
    '''factor : signB constant
              | '(' superexpression ')'
              | funccall
              | ID dimensionsOpt'''

def p_signB(p):
    '''signB : sign
             | empty'''

# <constant>
def p_constant(p):
    '''constant : FCONST
                | ICONST
                | TRUE
                | FALSE'''

# <sign>
def p_sign(p):
    """sign : '+'
            | '-' """

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

# <returntype>
def p_returntype(p):
    '''returntype : VOID
                  | type'''
    current['type'] = p[1]

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
    '''funccall : ID '(' funccallB '''

def p_funccallB(p):
    '''funccallB : superexpression funccallC
                 | ')' '''

def p_funccallC(p):
    '''funccallC : ',' superexpression funccallC
                 | ')' '''

# <dimensions>
def p_dimensions(p):
    '''dimensions : '[' superexpression ']' dimensionsB '''
    current['dimensionx'] = 1

def p_dimensionsB(p):
    '''dimensionsB : '[' superexpression ']'
                   | empty '''
    current['dimensiony'] = ( 1 if p[1] == '[' else 0 )

# <return>
def p_return(p):
    '''return : RETURN superexpression'''

# <params>
def p_params(p):
    '''params : type ID '''
    current['params'].append(p[1])
    if var_exists_in_dict(current['scope'], p[2]):
        print errors['REPEATED_DECLARATION'].format(p[2], p.lineno(2))
        exit(1)
    else:
        add_var_to_dict(current['scope'], p[2], p[1], 0, 0)

def p_paramsB(p):
    '''paramsB : ',' params paramsB
               | empty'''

def p_empty(p):
    '''empty : '''

def p_error(p):
    print "Syntax error in input token {0} with value {1}, in line {2}".format(p.type, p.value, p.lineno(1))
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
