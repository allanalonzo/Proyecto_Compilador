import ply.yacc as yacc
from lexer.lexer import lexer, tokens      
from ast_nodes import (
    Program, Declaration, Assignment,
    If, While, Block, BinaryOp,
    Number, Identifier
)

precedence = (
    ('nonassoc', 'IFX'),          
    ('nonassoc', 'ELSE'),
    ('left',    'SUMA', 'RESTA'),
    ('left',    'MULT', 'DIV'),
)

def p_program(p):
    'program : lista_sentencias'
    p[0] = Program(p[1])

def p_lista_sentencias_multiple(p):
    'lista_sentencias : lista_sentencias sentencia'
    p[0] = p[1] + [p[2]]

def p_lista_sentencias_simple(p):
    'lista_sentencias : sentencia'
    p[0] = [p[1]]

def p_sentencia_declaracion(p):
    '''sentencia : INT ID PUNTO_COMA
                | INT ID ASIGNACION expr PUNTO_COMA'''
    if len(p) == 4:
        p[0] = Declaration('int', Identifier(p[2]), None)
    else:
        p[0] = Declaration('int', Identifier(p[2]), p[4])

def p_sentencia_asignacion(p):
    'sentencia : ID ASIGNACION expr PUNTO_COMA'
    p[0] = Assignment(Identifier(p[1]), p[3])

def p_sentencia_if(p):
    """sentencia : IF IZQ_PAREN expr DER_PAREN sentencia %prec IFX
                 | IF IZQ_PAREN expr DER_PAREN sentencia ELSE sentencia"""
    if len(p) == 6:
        p[0] = If(p[3], p[5], None)
    elif len(p) == 8:
        p[0] = If(p[3], p[5], p[7])

def p_sentencia_while(p):
    'sentencia : WHILE IZQ_PAREN expr DER_PAREN sentencia'
    p[0] = While(p[3], p[5])

def p_sentencia_bloque(p):
    'sentencia : IZQ_BRACE lista_sentencias DER_BRACE'
    p[0] = Block(p[2])

def p_expr_binaria(p):
    '''expr : expr SUMA termino
            | expr RESTA termino'''
    p[0] = BinaryOp(p[2], p[1], p[3])

def p_termino_binario(p):
    '''termino : termino MULT factor
            | termino DIV factor'''
    p[0] = BinaryOp(p[2], p[1], p[3])

def p_expr_termino(p):
    'expr : termino'
    p[0] = p[1]

def p_termino_factor(p):
    'termino : factor'
    p[0] = p[1]

def p_factor_numero(p):
    '''factor : INT_CONST
              | FLOAT_CONST'''
    p[0] = Number(p[1])

def p_factor_id(p):
    'factor : ID'
    p[0] = Identifier(p[1])

def p_factor_expr(p):
    'factor : IZQ_PAREN expr DER_PAREN'
    p[0] = p[2]

def p_error(p):
    if p:
        raise SyntaxError(f"Error sintactico en token '{p.value}' (línea {p.lineno})")
    else:
        raise SyntaxError("Error sintactico ")

parser = yacc.yacc()
