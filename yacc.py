import ply.yacc as yacc
import lex
import sys

tokens = lex.tokens

# sintaxis rules

# <program>
def p_program(p):
    '''program : config body'''

# <config>
def p_config(p):
    '''config : configdirective configB
              | empty'''

def p_configB(p):
    '''configB : config
               | empty'''

# <configdirective>
def p_configdirective(p):
    '''configdirective : HASHTAG VARS EQUAL options
                       | HASHTAG DECISIONS EQUAL options
                       | HASHTAG COMPLEXITY EQUAL optionsyesno'''

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
    '''declarations : type declarationsB SEMI declarations
                    | empty'''

def p_declarationsB(p):
    '''declarationsB : ID dimensionB constantB declarationsC'''

def p_declarationsC(p):
    '''declarationsC : COMMA declarationsB
                     | empty'''

def p_dimensionB(p):
    '''dimensionB : dimension
                  | empty'''

def p_constantB(p):
    '''constantB : EQUAL constant
                 | empty'''

# <main>
def p_main(p):
    '''main : main LPAREN RPAREN block'''

# <func>
def p_func(p):
    '''func : returntype ID LPAREN paramsB RPAREN block
            | empty'''

def p_paramsB(p):
    '''paramsB : params
               | empty'''

# <block>
def p_block(p):
    '''block : LBRACE instruction RBRACE'''

# <asign>
def p_asign(p):
    '''asign : ID dimensionB EQUAL superexpression'''

# <condition>
def p_condition(p):
    '''condition : IF LPAREN superexression RPAREN block else'''

# <else>
def p_else(p):
    '''else : ELSE block
            | empty'''

# <instruction>
def p_instruction(p):
    '''instruction : asign SEMI instructionB
                   | condition SEMI instructionB
                   | output SEMI instructionB
                   | whileloop SEMI instructionB
                   | forloop SEMI instructionB
                   | input SEMI instructionB
                   | funccall SEMI instructionB
                   | return SEMI instructionB
                   | localdirective instructionB
                   | declarations instructionB'''

def p_instructionB(p):
    '''instructionB : instruction
                    | empty'''

# <localdirective>
def p_localdirective(p):
    '''localdirective : localvardirective
                      | localdecisiondirective
                      | lcoalmsgdirective'''

# <superexpression>
def p_superexpression(p):
    '''superexpression : expression superexpressionB'''

def p_superexpressionB(p):
    '''superexpressionB : AND superexpression
                        | OR superexpression
                        | empty'''

# <expression>
def p_expression(p):
    '''expression : exp expressionB'''

def p_expressionB(p):
    '''expressionB : LESSTHAN exp
                   | GREATHAN exp
                   | DIFFERENT exp
                   | TWOEQUAL exp
                   | GREATEQUAL exp
                   | LESSEQUAL exp
                   | empty'''

# <exp>
def p_exp(p):
    '''exp : term expB'''

def p_expB(p):
    '''expB : MINUS exp
            | PLUS exp
            | empty'''

# <term>
def p_term(p):
    '''term : factor termB'''

def p_termB(p):
    '''termB : DIVIDE term
             | TIMES term
             | empty'''

# <factor>
def p_factor(p):
    '''factor : signB constant
              | LPAREN superexpression RPAREN
              | funccall
              | ID dimensionB'''

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
    '''sign : PLUS
            | MINUS'''

# <whileloop>
def p_whileloop(p):
    '''whileloop : WHILE LPAREN superexpression RPAREN block'''

# <type>
def p_type(p):
    '''type : INT
            | FLOAT
            | STRING'''

# <returntype>
def p_returntype(p):
    '''returntype : VOID
                  | type'''

# <foorloop>
def p_foorloop(p):
    '''foorloop : FOR LPAREN asign SEMI superexpression SEMI superexpression RPAREN block'''

# <input>
def p_input(p):
    '''input : INPUT LPAREN inputB RPAREN'''

def p_inputB(p):
    '''inputB : ID inputC'''

def p_inputC(p):
    '''inputC : COMMA inputB
              | empty'''


# <output>
# <localvardirective>
# <localmsgdirective>
# <localdecisiondirective>
# <funccall>
# <dimension>
# <return>
# <params>

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
