import ply.yacc as yacc
from lexer.lexer import lexer, tokens
from ast_nodes import (
    Program, Declaration, Assignment,
    If, While, Block, BinaryOp,
    Number, Identifier, Boolean, String
)

# Precedencia de operadores
precedence = (
    ('nonassoc', 'IFX'),
    ('nonassoc', 'ELSE'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'NEQ'),
    ('left', 'LT', 'GT', 'LE', 'GE'),
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULT', 'DIV', 'MOD'),
)

# Programa principal
def p_program(p):
    'program : lista_sentencias'
    p[0] = Program(p[1])

# Lista de sentencias
def p_lista_sentencias_multiple(p):
    'lista_sentencias : lista_sentencias sentencia'
    p[0] = p[1] + [p[2]]

def p_lista_sentencias_simple(p):
    'lista_sentencias : sentencia'
    p[0] = [p[1]]

# Declaraciones con o sin inicialización
def p_sentencia_declaracion(p):
    '''sentencia : INT ID PUNTO_COMA
                 | FLOAT ID PUNTO_COMA
                 | BOOL ID PUNTO_COMA
                 | STRING ID PUNTO_COMA
                 | INT ID ASIGNACION expr PUNTO_COMA
                 | FLOAT ID ASIGNACION expr PUNTO_COMA
                 | BOOL ID ASIGNACION expr PUNTO_COMA
                 | STRING ID ASIGNACION expr PUNTO_COMA'''
    if len(p) == 4:
        p[0] = Declaration(p[1], Identifier(p[2]), None)
    else:
        p[0] = Declaration(p[1], Identifier(p[2]), p[4])

# Asignación simple
def p_sentencia_asignacion(p):
    'sentencia : ID ASIGNACION expr PUNTO_COMA'
    p[0] = Assignment(Identifier(p[1]), p[3])

# Estructura de control if / else
def p_sentencia_if(p):
    """sentencia : IF IZQ_PAREN expr DER_PAREN sentencia %prec IFX
                 | IF IZQ_PAREN expr DER_PAREN sentencia ELSE sentencia"""
    if len(p) == 6:
        p[0] = If(p[3], p[5], None)
    else:
        p[0] = If(p[3], p[5], p[7])

# Bucle while
def p_sentencia_while(p):
    'sentencia : WHILE IZQ_PAREN expr DER_PAREN sentencia'
    p[0] = While(p[3], p[5])

# Bloques de código
def p_sentencia_bloque(p):
    'sentencia : IZQ_BRACE lista_sentencias DER_BRACE'
    p[0] = Block(p[2])

# Expresiones binarias
def p_expr_binaria(p):
    '''expr : expr SUMA expr
            | expr RESTA expr
            | expr MULT expr
            | expr DIV expr
            | expr MOD expr
            | expr EQ expr
            | expr NEQ expr
            | expr LT expr
            | expr GT expr
            | expr LE expr
            | expr GE expr
            | expr AND expr
            | expr OR expr'''
    p[0] = BinaryOp(p[2], p[1], p[3])

# Expresión unaria
def p_expr_unaria(p):
    'expr : NOT expr'
    p[0] = BinaryOp(p[1], p[2], None)

# Agrupación de expresiones
def p_expr_group(p):
    'expr : IZQ_PAREN expr DER_PAREN'
    p[0] = p[2]

# Constantes y variables
def p_expr_atom(p):
    '''expr : INT_CONST
            | FLOAT_CONST
            | BOOL_CONST
            | STRING_CONST
            | ID'''
    if isinstance(p[1], bool):
        p[0] = Boolean(p[1])
    elif p.slice[1].type == 'STRING_CONST':
        p[0] = String(p[1][1:-1])  # Elimina las comillas dobles
    elif isinstance(p[1], (int, float)):
        p[0] = Number(p[1])
    else:
        p[0] = Identifier(p[1])

# Manejo de errores
def p_error(p):
    if p:
        raise SyntaxError(f"Error sintáctico en token '{p.value}' (línea {p.lineno})")
    else:
        raise SyntaxError("Error sintáctico al final del archivo")

parser = yacc.yacc()
