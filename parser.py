#!env/bin/python
import ply.yacc as yacc
import logging
import lexer
import sys
from semantics import current, add_var_to_dict, add_func_to_dict, var_exists_in_dict, func_exists_in_dict, print_current, print_var_dict, print_func_dict, errors, clear_current, clear_local, var_dict, func_dict, semantics_cube
from quadruples import operators, operands, jumps, quadruples, types, add_quadruple, return_pending_quadruple, print_quadruples, print_operators, print_operands, print_types
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
    '''declaration : type push_type declarationB declarationC'''
    print "Una declaration"

def p_declarationB(p):
    '''declarationB : ID push_operand dimensionsOpt '''
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


def p_push_operand(p):
    '''push_operand :'''
    if var_exists_in_dict(current['scope'], p[-1]):
        types.append(var_dict[ current['scope'] ] [ p[-1] ] [ 'type' ] )

    operands.append(p[-1])

def p_push_type(p):
    '''push_type :'''
    types.append(p[-1])

def p_repush_type(p):
    '''repush_type :'''
    print_current()
    types.append(current['type'])

def p_push_operator(p):
    '''push_operator :'''
    operators.append(p[-1])

def p_quadruple_assign(p):
    '''quadruple_assign :'''
    print "assigning a quadruple... "
    print_operators()
    print_operands()
    print_types()

    if operands and types and operators:

        op2 = operands.pop() if operands else -1
        type2 = types.pop() if types else -1
        op1 = operands.pop() if operands else -1
        type1 = types.pop() if types else -1

        op = operators.pop()
        add_quadruple(op, op1, type1, op2, type2)


def p_declarationC(p):
    '''declarationC : '=' push_operator hyperexpression quadruple_assign declarationD
                    | ',' repush_type declarationB declarationC
                    | ';' '''
    if p[1] == ';':
        clear_current()
    elif p[1] == ',':
        current['dimensionx'] = 0
        current['dimensiony'] = 0

def p_declarationD(p):
    '''declarationD : ',' repush_type declarationB declarationC
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
        current['params'] = []

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
    '''assign : ID push_operand dimensionsOpt '=' push_operator hyperexpression quadruple_assign'''
    current['id'] = p[1]
    if not var_exists_in_dict(current['scope'], current['id']):
        print errors['UNDECLARED_VARIABLE'].format(p[1], p.lineno(1))
        exit(1)

def p_assignB(p):
    '''assignB : dimensionsOpt '=' push_operator hyperexpression quadruple_assign'''

def p_dimensionsOpt(p):
    '''dimensionsOpt : dimensions
                     | empty'''
    p[0] = p[1]


# <condition>
def p_condition(p):
    '''condition : IF '(' hyperexpression condition_quadruple ')' block else endcondition_quadruple'''

# <else>
def p_else(p):
    '''else : ELSE elsecondition_quadruple block
            | empty'''

def p_condition_quadruple(p):
    '''condition_quadruple :'''
    if types:
        type1 = types.pop() if types else -1
        if type1 == 'bool':
            op1 = operands.pop()
            add_quadruple('GOTOF', op1, -1, -1, -1)
            jumps.append(len(quadruples)-1)
        else:
            print 'se esperaba valor booleano!'

def p_elsecondition_quadruple(p):
    '''elsecondition_quadruple :'''
    add_quadruple('GOTO', -1, -1, -1, -1)
    if jumps:
        false = jumps.pop()
        quadruples[false][3] = len(quadruples)
        jumps.append(len(quadruples)-1)


def p_endcondition_quadruple(p):
    '''endcondition_quadruple :'''
    if jumps:
        end = jumps.pop()
        quadruples[end][3] = len(quadruples)
        print_quadruples()



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
    '''assignfunccall : ID push_operand assignfunccallB'''
    current['id'] = p[1]
    if current['isfunc']:
        if func_exists_in_dict(current['id']):
            if len(current['params']) != len(func_dict[ current['id'] ]['params']):
                print_current()
                print errors['PARAMETER_LENGTH_MISMATCH'].format(current['id'], len(func_dict[ current['id'] ]['params']),len(current['params']), p.lineno(1))
                exit(1)
        else:
            print errors['UNDECLARED_FUNCTION'].format(current['id'], p.lineno(1))
            exit(1)
        clear_current()
    else:
        if not var_exists_in_dict(current['scope'], current['id']):
            print errors['UNDECLARED_VARIABLE'].format(current['id'], p.lineno(1))

def p_pop_operand(p):
    '''pop_operand :'''
    if operands:
        operands.pop()


def p_assignfunccallB(p):
    '''assignfunccallB : '(' pop_operand funccallB funccallC
                       | assignB'''
    current['isfunc'] = True if p[1] == '(' else False

# <localdirective>
def p_localdirective(p):
    '''localdirective : localvardirective
                      | localdecisiondirective
                      | localmsgdirective'''

# <hyperexpression>
def p_hyperexpression(p):
    '''hyperexpression : superexpression hyperexpressionB'''

def p_hyperexpressionB(p):
    '''hyperexpressionB : OR push_operator hyperexpression
                        | empty'''
    if p[1] is not '':
        op, op1, type1, op2, type2 = return_pending_quadruple(['OR'])
        if op is not 'none_pending':
            add_quadruple(op, op1, type1, op2, type2)

# <superexpression>
def p_superexpression(p):
    '''superexpression : expression superexpressionB'''

def p_superexpressionB(p):
    '''superexpressionB : AND push_operator superexpression
                        | empty'''
    if p[1] is not '':
        op, op1, type1, op2, type2 = return_pending_quadruple(['AND'])
        if op is not 'none_pending':
            add_quadruple(op, op1, type1, op2, type2)

# <expression>
def p_expression(p):
    '''expression : exp expressionB'''


def p_expressionB(p):
    '''expressionB : '<' push_operator exp
                   | '>' push_operator exp
                   | DIFF push_operator exp
                   | EQ push_operator exp
                   | LTEQ push_operator exp
                   | GTEQ push_operator exp
                   | empty'''
    if p[1] is not '':
        op, op1, type1, op2, type2 = return_pending_quadruple(['<', '>', 'DIFF', 'EQ', 'LTEQ', 'GTEQ'])
        if op is not 'none_pending':
            add_quadruple(op, op1, type1, op2, type2)


# <exp>
def p_exp(p):
    '''exp : term seen_term  expB'''

def p_seen_term(p):
    '''seen_term :'''

    op, op1, type1, op2, type2 = return_pending_quadruple(['+', '-'])
    if op is not 'none_pending':
        add_quadruple(op, op1, type1, op2, type2)

def p_expB(p):
    '''expB : '-' push_operator exp
            | '+' push_operator exp
            | empty'''

# <term>
def p_term(p):
    '''term : factor seen_factor termB'''

def p_seen_factor(p):
    '''seen_factor :'''
    op, op1, type1, op2, type2 = return_pending_quadruple(['*', '/'])
    if op is not 'none_pending':
        add_quadruple(op, op1, type1, op2, type2)

def p_termB(p):
    '''termB : '/' push_operator term
             | '*' push_operator term
             | empty'''

# our lexer gets the sign with the int in case it has one.
# And I just found out this is wrong. Removed the sign from the lexer and added it here.
# <factor>
def p_factor(p):
    '''factor : signB constant
              | '(' seen_parentheses hyperexpression ')'
              | funccall
              | ID seen_ID dimensionsOpt'''
    if ( len(p) >= 3 ):
        if ( p[2] is 'UNDECLARED_VARIABLE' ):
            print errors['UNDECLARED_VARIABLE'].format(p[1], p.lineno(1))
            exit(1)
    if ( len(p) is 5 ):
        if ( p[4] is ')' ):
            operators.pop()

def p_seen_parentheses(p):
    '''seen_parentheses :'''
    operators.append(p[-1])

def p_seen_ID(p):
    '''seen_ID :'''
    if not var_exists_in_dict(current['scope'], p[-1]):
        p[0] = 'UNDECLARED_VARIABLE'
    else:
        p[0] = ""
        type_to_push = var_dict[ current['scope'] ] [ p[-1] ] [ 'type' ]
        types.append(type_to_push)
        operands.append( p[-1] )


def p_signB(p):
    '''signB : sign
             | empty'''
    p[0] = p[1]

# <seen_fconst>
def p_seen_fconst(p):
    '''seen_fconst :'''
    p[0] = 'float'

# <seen_iconst>
def p_seen_iconst(p):
    '''seen_iconst :'''
    p[0] = 'int'

# <seen_sconst>
def p_seen_sconst(p):
    '''seen_sconst :'''
    p[0] = 'string'

# <seen_true>
def p_seen_true(p):
    '''seen_true :'''
    p[0] = 'bool'

# <seen_false>
def p_seen_false(p):
    '''seen_false :'''
    p[0] = 'bool'

# <constant>
def p_constant(p):
    '''constant : FCONST seen_fconst
                | ICONST seen_iconst
                | SCONST seen_sconst
                | TRUE   seen_true
                | FALSE  seen_false'''
    p[0] = p[1]

    if p[-1] is '-':
        add_quadruple('*', '-1', 'int', p[1], p[2])
    else:
        operands.append(p[1])
        types.append(p[2])


# <sign>
def p_sign(p):
    """sign : '+'
            | '-' """
    p[0] = p[1]

# <whileloop>
def p_whileloop(p):
    '''whileloop : WHILE '(' hyperexpression ')' block'''

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
    '''forloop : FOR '(' assign ';' hyperexpression ';' hyperexpression ')' block'''

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
    '''outputB : SCONST push_operand print_quadruple outputC
               | hyperexpression print_quadruple outputC'''

def p_print_quadruple(p):
    '''print_quadruple :'''
    if operands:
        op1 = operands.pop()
        types.pop()
        add_quadruple('PRINT', op1, -1, -1, -1)

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
    clear_current()

def p_funccallB(p):
    '''funccallB : hyperexpression seen_param
                 | empty '''

def p_seen_param(p):
    '''seen_param :'''
    current['params'].append(1)

def p_funccallC(p):
    '''funccallC : ',' funccallB funccallC
                 | ')' '''

# <dimensions>
def p_dimensions(p):
    '''dimensions : '[' hyperexpression ']' dimensionsB '''
    current['dimensionx'] = 1

def p_dimensionsB(p):
    '''dimensionsB : '[' hyperexpression ']'
                   | empty '''
    current['dimensiony'] = ( 1 if p[1] == '[' else 0 )

# <return>
def p_return(p):
    '''return : RETURN hyperexpression'''

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
