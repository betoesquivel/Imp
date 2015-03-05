import lexer

f = open("test.imp")
program = f.readlines()

for l in program:
    lexer.lexer.input(l)
    print [x.type for x in lexer.lexer]
