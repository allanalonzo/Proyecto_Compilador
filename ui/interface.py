from flask import Flask, render_template, request, jsonify
import os
from lexer.lexer import lexer, lex_errors
from parser.parser import parser
import ast_nodes


app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(__file__),'templates'),
            static_folder=os.path.join(os.path.dirname(__file__),'static'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/compile', methods=['POST'])
def compile_code():
    data = request.get_json() or {}
    code = data.get('code', '')

    lex_errors.clear()
    lexer.input(code)

    tokens = []
    for tok in lexer:
        tokens.append({
            'type':   tok.type,
            'value':  tok.value,
            'line':   tok.lineno,
            'column': tok.lexpos
        })

    errors = lex_errors.copy()

    try:
        ast_root = parser.parse(code, lexer=lexer)
    except SyntaxError as e:
        errors.append(str(e))
        
    return jsonify(tokens=tokens, errors=errors)
if __name__ == '__main__':
    app.run(debug=True)
    
def ast_to_dot(node, lines=None, counter=None, parent_id=None):
    """
    Recorre recursivamente tu AST y genera las líneas DOT.
    """
    if lines is None:   lines = []
    if counter is None: counter = {'n': 0}

    node_id = f"n{counter['n']}"
    counter['n'] += 1

    # Etiqueta con el nombre de la clase, ej "If" o "BinaryOp"
    lines.append(f'{node_id} [label="{type(node).__name__}"];')

    if parent_id:
        lines.append(f'{parent_id} -> {node_id};')

    # Para cada atributo del nodo
    for attr, val in vars(node).items():
        # Si es un subnodo AST
        if isinstance(val, ast_nodes.Node):
            ast_to_dot(val, lines, counter, node_id)
        # Si es lista de subnodos
        elif isinstance(val, list):
            for child in val:
                if isinstance(child, ast_nodes.Node):
                    ast_to_dot(child, lines, counter, node_id)
    return lines

@app.route('/api/ast', methods=['POST'])
def get_ast():
    data = request.get_json() or {}
    code = data.get('code', '')

    # 1) Tokeniza (limpio errores léxicos)
    lexer.input(code)

    # 2) Parseo
    try:
        ast_root = parser.parse(code, lexer=lexer)
    except Exception as e:
        # Devuelve 400 con mensaje de error
        return jsonify(error=str(e)), 400

    # 3) Genera DOT
    lines = ['digraph AST {', 'node [shape=box];']
    lines += ast_to_dot(ast_root)
    lines.append('}')

    return jsonify(dot="\n".join(lines))

