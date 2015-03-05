import ply.yacc as yacc
import lexer
import sys

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
    '''configdirective : '#' VARS '=' options
                       | '#' DECISIONS '=' options
                       | '#' COMPLEXITY '=' optionsyesno'''

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
    '''body : declarations func funcB main func funcB'''

def p_funcB(p):
    '''funcB : func
             | empty'''

# <declarations>
def p_declarations(p):
    '''declarations : type declarationsB ';' declarations
                    | empty'''

def p_declarationsB(p):
    '''declarationsB : ID dimensionB constantB declarationsC'''

def p_declarationsC(p):
    '''declarationsC : ',' declarationsB
                     | empty'''

def p_dimensionB(p):
    '''dimensionB : dimension
                  | empty'''

def p_constantB(p):
    '''constantB : '=' constant
                 | empty'''

# <main>
def p_main(p):
    '''main : MAIN '(' ')' block'''

# <func>
def p_func(p):
    '''func : returntype ID '(' optionalparams ')' block
            | empty'''

def p_optionalparams(p):
    '''optionalparams : params
                      | empty'''

# <block>
def p_block(p):
    '''block : '{' instruction '}' '''

# <asign>
def p_asign(p):
    '''asign : ID dimensionB '=' superexpression'''

# <condition>
def p_condition(p):
    '''condition : IF '(' superexpression ')' block else'''

# <else>
def p_else(p):
    '''else : ELSE block
            | empty'''

# question: Does the whileloop and forloops end with a ';'?
# <instruction>
def p_instruction(p):
    '''instruction : asign ';' instructionB
                   | condition ';' instructionB
                   | output ';' instructionB
                   | whileloop instructionB
                   | forloop instructionB
                   | input ';' instructionB
                   | funccall ';' instructionB
                   | return ';' instructionB
                   | localdirective instructionB
                   | declarations instructionB'''

def p_instructionB(p):
    '''instructionB : instruction
                    | empty'''

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
# <factor>
def p_factor(p):
    '''factor : constant
              | '(' superexpression ')'
              | funccall
              | ID dimensionB'''

#def p_signB(p):
#    '''signB : sign
#             | empty'''

# <constant>
def p_constant(p):
    '''constant : FCONST
                | ICONST
                | TRUE
                | FALSE'''

# <sign>
#def p_sign(p):
#    """sign : '+'
#            | '-' """

# <whileloop>
def p_whileloop(p):
    '''whileloop : WHILE '(' superexpression ')' block'''

# <type>
def p_type(p):
    '''type : INT
            | FLOAT
            | STRING'''

# <returntype>
def p_returntype(p):
    '''returntype : VOID
                  | type'''

# <forloop>
def p_forloop(p):
    '''forloop : FOR '(' asign ';' superexpression ';' superexpression ')' block'''

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
    '''outputB : STRING outputC
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
    '''localmsgdirective : '#' SHOW STRING'''

# <localdecisiondirective>
def p_localdecisiondirective(p):
    '''localdecisiondirective : '#' localdecisiondirectiveB DECISION
                              | empty'''

def p_localdecisiondirectiveB(p):
    '''localdecisiondirectiveB : TRACK
                               | FORGET'''

# <funccall>
def p_funccall(p):
    '''funccall : ID '(' funccallB ')' '''

def p_funccallB(p):
    '''funccallB : superexpression funccallC
                 | empty'''

def p_funccallC(p):
    '''funccallC : ',' superexpression funccallC
                 | empty'''

# <dimension>
def p_dimension(p):
    '''dimension : '[' superexpression ']' dimensionB '''

# <return>
def p_return(p):
    '''return : RETURN superexpression'''

# <params>
def p_params(p):
    '''params : type ID paramsB'''

def p_paramsB(p):
    '''paramsB : ',' type ID paramsB
               | empty'''

def p_empty(p):
    '''empty : '''

def p_error(p):
    print "Syntax error in input!", p.type

parser = yacc.yacc()

if(len(sys.argv) > 1):
    if sys.argv[1] == "-f":
        f = open(sys.argv[2], "r")
        s = f.readlines()
    string = ""
    for line in s:
        string += line
    print string
    result = parser.parse(string)
else:
    print "Error"
