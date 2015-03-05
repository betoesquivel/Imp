import lexer

f = open("test.imp")
program = f.readlines()

for l in program:
    lexer.lexer.input(l)
    print [x.lineno for x in lexer.lexer]
