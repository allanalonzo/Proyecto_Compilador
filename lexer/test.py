from lexer import lexer

codigo = '''
// Este es un comentario de línea

if (a < b) {
    return a + b;
}
'''

lexer.input(codigo)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)

