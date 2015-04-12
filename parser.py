#!env/bin/python
import ply.yacc as yacc
import logging
import lexer
import sys
from semantics import current, add_var_to_dict, add_func_to_dict, var_exists_in_dict, func_exists_in_dict, print_current, print_var_dict, print_func_dict, errors, clear_current, clear_local, var_dict, func_dict, semantics_cube, constant_dict, get_constant_memory_address
from quadruples import operators, operands, jumps, quadruples, types, add_quadruple, return_pending_quadruple, print_quadruples, print_operators, print_operands, print_types
from MemoryBlock import MemoryBlock
from copy import deepcopy



tokens = lexer.tokens

# memory allocation (just variable counters representing: constants and local/global vars)
mem_local = MemoryBlock(0, 1000, 2000, 3000, 4000, 5000)
mem_global = MemoryBlock(5000, 6000, 7000, 8000, 9000, 10000)
mem_constants = MemoryBlock(10000, 11000, 12000, 13000, 14000, 15000)
mem_temps = MemoryBlock(15000, 16000, 17000, 18000, 19000, 20000)
mem_global_temps = MemoryBlock(20000, 21000, 22000, 23000, 24000, 25000)

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
    if operands:
        operands.pop()
    if types:
        types.pop()

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
                current['dimensiony'],
                mem_local if current['scope'] == 'local' else mem_global
        )
        current['dimensionx'] = 0
        current['dimensiony'] = 0
        operands.pop()
        operands.append(var_dict[ current['scope'] ] [ p[1] ] ['address'])


def p_push_operand(p):
    '''push_operand :'''
    if var_exists_in_dict(current['scope'], p[-1]):
        scope = current['scope'] if var_dict[current['scope']].get(p[-1], 'error') != 'error' else 'global'
        types.append(var_dict[ scope ] [ p[-1] ] [ 'type' ] )
        operands.append(var_dict[ scope ] [ p[-1] ] ['address'])
    else:
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
        add_quadruple(op, op1, type1, op2, type2, mem_temps, mem_global_temps)


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
    '''main : MAIN '(' ')' seen_main block'''

def p_seen_main(p):
    '''seen_main :'''
    print 'ENTRANDO A MAIN'
    current['scope'] = 'local'

# <func>
def p_suprafunc(p):
    '''suprafunc : func block'''
    print 'TERMINANDO EL SCOPE DE UNA FUNCION', current['scope']
    print mem_local
    print_current()
    print_func_dict()
    print_var_dict()
    func_dict[ p[1] ][ 'size_info' ] = {
            'bools': mem_local.bools[1],
            'ints': mem_local.ints[1],
            'floats': mem_local.floats[1],
            'chars': mem_local.chars[1],
            'strings': mem_local.strings[1]
    }


    clear_current()
    clear_local()

def p_func(p):
    '''func : DEF returntype ID '(' paramsOpt ')' '''
    p[0] = p[3]
    current['id'] = p[3]
    current['scope'] = 'local'
    current['type'] = p[2]
    print 'EMPEZANDO EL SCOPE DE UNA FUNCION', current['scope']
    if func_exists_in_dict(current['id']):
        print errors['REPEATED_FUNC_DECLARATION'].format(current['id'], p.lineno(1))
        exit(1)
    else:
        add_func_to_dict(current['id'], current['type'], deepcopy(current['params']), len(quadruples))
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
            add_quadruple('GOTOF', op1, -1, -1, -1, mem_temps, mem_global_temps)
            jumps.append(len(quadruples)-1)
        else:
            print 'se esperaba valor booleano!'
            exit(1)

def p_elsecondition_quadruple(p):
    '''elsecondition_quadruple :'''
    add_quadruple('GOTO', -1, -1, -1, -1, mem_temps, mem_global_temps)
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
                   | read ';'
                   | declaration
                   | condition
                   | whileloop
                   | forloop
                   | localdirective '''

# <assignfunccall>
# left factor the assign and funccall rules
def p_assignfunccall(p):
    '''assignfunccall : ID seen_funccall push_operand assignfunccallB'''
    current['id'] = p[1]
    if current['isfunc']:
        if func_exists_in_dict(current['id']):
            if len(current['params']) != len(func_dict[ current['id'] ]['params']):
                # validate that parameter types in funccall match parameter types in the func_dict
                print errors['PARAMETER_LENGTH_MISMATCH'].format(current['id'], len(func_dict[ current['id'] ]['params']),len(current['params']), p.lineno(1))
                exit(1)
            else:
                param_count = 0
                correct_call = True
                called_function = func_dict[ current['id'] ]
                while param_count < len(current['params']):
                    expected_param = called_function['params'][param_count]
                    if expected_param['type'] != current['params'][param_count]['type']:
                        print errors['PARAMETER_TYPE_MISMATCH'].format(current['id'], expected_param['type'], current['params'][param_count]['type'], param_count)
                        correct_call = False
                    param_count += 1
                if (not correct_call): exit(1)


        else:
            print errors['UNDECLARED_FUNCTION'].format(current['id'], p.lineno(1))
            exit(1)
        clear_current()
    else:
        if not var_exists_in_dict(current['scope'], current['id']):
            print errors['UNDECLARED_VARIABLE'].format(current['id'], p.lineno(1))
            exit(1)

def p_seen_funccall(p):
    '''seen_funccall :'''
    current['id'] = p[-1]
    p[0] = p[-1]

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
            add_quadruple(op, op1, type1, op2, type2, mem_temps, mem_global_temps)

# <superexpression>
def p_superexpression(p):
    '''superexpression : expression superexpressionB'''

def p_superexpressionB(p):
    '''superexpressionB : AND push_operator superexpression
                        | empty'''
    if p[1] is not '':
        op, op1, type1, op2, type2 = return_pending_quadruple(['AND'])
        if op is not 'none_pending':
            add_quadruple(op, op1, type1, op2, type2, mem_temps, mem_global_temps)

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
            add_quadruple(op, op1, type1, op2, type2, mem_temps, mem_global_temps)


# <exp>
def p_exp(p):
    '''exp : term seen_term  expB'''

def p_seen_term(p):
    '''seen_term :'''

    op, op1, type1, op2, type2 = return_pending_quadruple(['+', '-'])
    if op is not 'none_pending':
        add_quadruple(op, op1, type1, op2, type2, mem_temps, mem_global_temps)

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
        add_quadruple(op, op1, type1, op2, type2, mem_temps, mem_global_temps)

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
        # there is a clear current
        print "var {0} doesn't exist in dict".format(p[-1])
        print_var_dict()
        print_current()

        p[0] = 'UNDECLARED_VARIABLE'
    else:
        p[0] = ""
        print current['scope']
        scope = current['scope'] if var_dict[current['scope']].get(p[-1], 'error') != 'error' else 'global'
        type_to_push = var_dict [scope] [ p[-1] ] [ 'type' ]
        types.append(type_to_push)
        operands.append( var_dict [scope] [ p[-1] ] [ 'address' ])


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
        add_quadruple('*', '-1', 'int', get_constant_memory_address(p[1], p[2], mem_constants), p[2], mem_temps, mem_global_temps)
    else:
        operands.append( get_constant_memory_address(p[1], p[2], mem_constants) )
        types.append(p[2])


# <sign>
def p_sign(p):
    """sign : '+'
            | '-' """
    p[0] = p[1]

# <whileloop>
def p_whileloop(p):
    '''whileloop : WHILE init_while '(' hyperexpression ')' while_quadruple block endwhile_quadruple'''

def p_init_while(p):
    '''init_while :'''
    jumps.append(len(quadruples))

def p_while_quadruple(p):
    '''while_quadruple :'''
    if types:
        type1 = types.pop() if types else -1
        if type1 == 'bool':
            op1 = operands.pop()
            add_quadruple('GOTOF', op1, -1, -1, -1, mem_temps, mem_global_temps)
            jumps.append(len(quadruples)-1)
        else:
            print 'se esperaba valor booleano!'
            exit(1)

def p_endwhile_quadruple(p):
    '''endwhile_quadruple :'''
    if jumps:
        false = jumps.pop()
        init = jumps.pop()
        add_quadruple('GOTO', init, -1, -1, -1, mem_temps, mem_global_temps)
        quadruples[false][3] = len(quadruples)
        print_quadruples()


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
    '''forloop : FOR '(' assign ';' init_while hyperexpression for_quadruple ';' hyperexpression for_expression ')' block endfor_quadruple '''

# <for_quadruple>
def p_for_quadruple(p):
    '''for_quadruple :'''
    if types:
        type1 = types.pop() if types else -1
        if type1 == 'bool':
            op1 = operands.pop()
            add_quadruple('GOTOF', op1, -1, -1, -1, mem_temps, mem_global_temps)
            jumps.append(len(quadruples)-1)
            add_quadruple('GOTO', -1, -1, -1, -1, mem_temps, mem_global_temps)
            jumps.append(len(quadruples)-1)
        else:
            print 'se esperaba valor booleano!'
            exit(1)

# <for_expression>
def p_for_expression(p):
    '''for_expression :'''
    if jumps:
        skip_forexpression = jumps.pop()
        false = jumps.pop()
        init = jumps.pop()
        jumps.append(len(quadruples)-1)
        add_quadruple('GOTO', init, -1, -1, -1, mem_temps, mem_global_temps)
        quadruples[skip_forexpression][3] = len(quadruples)
        jumps.append(false)
        print_quadruples()

def p_endfor_quadruple(p):
    '''endfor_quadruple :'''
    if jumps:
        false = jumps.pop()
        expression = jumps.pop()
        add_quadruple('GOTO', expression, -1, -1, -1, mem_temps, mem_global_temps)
        quadruples[false][3] = len(quadruples)
        print_quadruples()

# <read>
def p_read(p):
    """read : READ '(' validate_id push_operand read_quadruple readB ')' """

def p_validate_id(p):
    '''validate_id : ID'''
    if ( var_exists_in_dict(current['scope'], p[1]) ):
        p[0] = p[1]
    else:
        print errors['UNDECLARED_VARIABLE'].format(p[1], p.lineno(1))
        exit(1)

def p_read_quadruple(p):
    '''read_quadruple :'''
    if operands:
        op1 = operands.pop()
        types.pop()
        add_quadruple('READ', op1, -1, -1, -1, mem_temps, mem_global_temps)

def p_readB(p):
    '''readB : ',' validate_id push_operand read_quadruple readB
              | empty'''
# <output>
def p_output(p):
    '''output : PRINT '(' outputB '''

def p_outputB(p):
    '''outputB : hyperexpression print_quadruple outputC'''

def p_print_quadruple(p):
    '''print_quadruple :'''
    if operands:
        print_operands()
        print_types()
        op1 = operands.pop()
        types.pop()
        add_quadruple('PRINT', op1, -1, -1, -1, mem_temps, mem_global_temps)

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
    #clear_current()
    current['params'] = []

def p_funccallB(p):
    '''funccallB : hyperexpression seen_param
                 | empty '''

def p_seen_param(p):
    '''seen_param :'''
    if types and operands:
        type1 = types.pop()
        op1 = operands.pop()

    current['params'].append({'id': op1, 'type': type1})

    add_quadruple('PARAMETER', op1, type1, len(current['params']) - 1, -1, mem_temps, mem_global_temps)
    ## here I should be assigning the operand address to the corresponding parameter, and checking if there is a type match
    #called_function = func_dict[ current['id'] ]
    #if ( len(current['params']) <= len(called_function['params']) ):
        #expected_type = called_function['params'][ len(current['params']) - 1 ]['type']
        #if ( not ( expected_type == type1 ) ):
            #print errors['PARAMETER_TYPE_MISMATCH'].format(current['id'], expected_type, type1, len(current['params']) - 1)



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
    '''return : RETURN hyperexpression return_quadruple'''

# <return_quadruple>
def p_return_quadruple(p):
    '''return_quadruple :'''
    if operands and types:

        print_operands()
        print_types()

        op1 = operands.pop()
        type1 = types.pop()

        print_current()

        if (type1 == func_dict[ current['id'] ]['type']):
            add_quadruple('RETURN', op1, type1, -1, -1, mem_temps, mem_global_temps)
        else:
            print 'Error en return type'
            exit(1)

# <params>
def p_params(p):
    '''params : type ID '''
    current['params'].append({ 'type': current['type'], 'id': p[2]})
    if var_exists_in_dict('local', p[2]):
        print errors['REPEATED_DECLARATION'].format(p[2], p.lineno(2))
        exit(1)
    else:
        add_var_to_dict('local', p[2], p[1], 0, 0, mem_local)

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
