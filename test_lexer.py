import lexer

f = open("test.imp")
program = f.readlines()

i = 0
pos = 0
for l in program:
    lexer.lexer.input(l)
    print i," ",  [ (x.type, pos + x.lexpos) for x in lexer.lexer]
    i += 1
