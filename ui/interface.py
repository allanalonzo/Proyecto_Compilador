from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(__file__),'templates'),
            static_folder=os.path.join(os.path.dirname(__file__),'static'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/compile', methods=['POST'])
def compile_code():
    code = request.json.get('code','')
    # poner la wea del lexer/parser reales aquí despues 
    tokens = [{'type':'ID','value':'foo','line':1,'column':1}]
    errors = []
    return jsonify(tokens=tokens, errors=errors)

if __name__ == '__main__':
    app.run(debug=True)
