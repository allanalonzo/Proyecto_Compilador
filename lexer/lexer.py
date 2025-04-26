import ply.lex as lex

tokens = [
    'ID',
    'INT_CONST',
    'FLOAT_CONST',
    'SUMA',
    'RESTA',
    'MULT',
    'DIV',
    'MOD',
    'EQ',
    'NEQ',
    'LT',
    'GT',
    'LE',
    'GE',
    'AND',
    'OR',
    'NOT',
    'IZQ_PAREN',
    'DER_PAREN',
    'IZQ_BRACE',
    'DER_BRACE',
    'PUNTO_COMA',
    'COMA',
    'COMILLAS_S',
    'ASIGNACION',
    'COMILLAS'
    
]

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'return': 'RETURN',
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
}

tokens += list(reserved.values())

t_SUMA    = r'\+'
t_RESTA   = r'-'
t_MULT    = r'\*'
t_DIV     = r'/'
t_MOD     = r'%'
t_EQ      = r'=='
t_NEQ     = r'!='
t_LT      = r'<'
t_GT      = r'>'
t_LE      = r'<='
t_GE      = r'>='
t_AND     = r'&&'
t_OR      = r'\|\|'
t_NOT     = r'!'
t_IZQ_PAREN  = r'\('
t_DER_PAREN  = r'\)'
t_IZQ_BRACE  = r'\{'
t_DER_BRACE  = r'\}'
t_PUNTO_COMA    = r';'
t_COMA   = r','
t_COMILLAS_S = r'\''
t_ASIGNACION = r'='
t_COMILLAS = r'\"'


def t_FLOAT_CONST(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT_CONST(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  
    return t

def t_COMMENT_LINE(t):
    r'//.*'
    pass 

def t_COMMENT_BLOCK(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass  

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

lex_errors = []                 
def t_error(t):
    lex_errors.append(
        f"Error léxico: carácter ilegal '{t.value[0]}' "
        f"en línea {t.lineno}, posición {t.lexpos}"
    )
    t.lexer.skip(1)

lexer = lex.lex()