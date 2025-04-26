from flask import Flask, render_template, request, jsonify
import os
from lexer.lexer import lexer, lex_errors

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

    return jsonify(tokens=tokens, errors=errors)
if __name__ == '__main__':
    app.run(debug=True)
