from flask import Flask, render_template, request, jsonify
import os
from lexer.lexer import lexer, lex_errors
from parser.parser import parser
import ast_nodes
from semantic.semantic import SemanticAnalyzer
from codegen.intermedio import Generador3AC

app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), 'static'))

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
            'type': tok.type,
            'value': tok.value,
            'line': tok.lineno,
            'column': tok.lexpos
        })

    errors = lex_errors.copy()
    ast_root = None
    semantic_errors = []
    intermediate_code = []

    try:
        ast_root = parser.parse(code, lexer=lexer)
    except SyntaxError as e:
        errors.append(f"Error de sintaxis: {str(e)}")

    if ast_root and not errors:
        analyzer = SemanticAnalyzer()
        semantic_errors = analyzer.analyze(ast_root)
        errors.extend(semantic_errors)

        if not semantic_errors:
            generador = Generador3AC()
            generador.generar(ast_root)
            intermediate_code = generador.get_code()

    return jsonify({
        'tokens': tokens,
        'errors': errors,
        'has_semantic_errors': len(semantic_errors) > 0,
        'intermediate_code': intermediate_code
    })

def ast_to_dot(node, lines=None, counter=None, parent_id=None):
    if lines is None:
        lines = []
    if counter is None:
        counter = {'n': 0}

    node_id = f"n{counter['n']}"
    counter['n'] += 1

    lines.append(f'{node_id} [label="{type(node).__name__}"];')

    if parent_id:
        lines.append(f'{parent_id} -> {node_id};')

    for attr, val in vars(node).items():
        if isinstance(val, ast_nodes.Node):
            ast_to_dot(val, lines, counter, node_id)
        elif isinstance(val, list):
            for child in val:
                if isinstance(child, ast_nodes.Node):
                    ast_to_dot(child, lines, counter, node_id)
    return lines

@app.route('/api/ast', methods=['POST'])
def get_ast():
    data = request.get_json() or {}
    code = data.get('code', '')

    lexer.input(code)

    try:
        ast_root = parser.parse(code, lexer=lexer)
    except Exception as e:
        return jsonify(error=str(e)), 400

    analyzer = SemanticAnalyzer()
    semantic_errors = analyzer.analyze(ast_root)
    if semantic_errors:
        return jsonify(error="\n".join(semantic_errors)), 400

    lines = ['digraph AST {', 'node [shape=box];']
    lines += ast_to_dot(ast_root)
    lines.append('}')

    return jsonify(dot="\n".join(lines))

if __name__ == '__main__':
    app.run(debug=True)
