from flask import Flask, render_template, request, jsonify
import os
import importlib
import ply.lex as lex
import ply.yacc as yacc

class CompilerServer:
    def __init__(self):
        # Inicializa la aplicación Flask con rutas a UI
        base_dir = os.path.dirname(__file__)
        self.app = Flask(
            __name__,
            template_folder=os.path.join(base_dir, 'ui', 'templates'),
            static_folder=os.path.join(base_dir, 'ui', 'static')
        )
        self._configure_routes()

    def _configure_routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/api/compile', methods=['POST'])
        def compile_code():
            data = request.get_json() or {}
            code = data.get('code', '')

            # Reconstruye lexer para reiniciar completamente su estado
            lex_mod = importlib.import_module('lexer.lexer')
            lex_mod.lex_errors.clear()
            lexer = lex.lex(module=lex_mod)
            lexer.lineno = 1
            lexer.input(code)

            # Recolecta tokens
            tokens = []
            for tok in lexer:
                tokens.append({
                    'type': tok.type,
                    'value': tok.value,
                    'line': tok.lineno,
                    'column': tok.lexpos
                })
            errors = lex_mod.lex_errors.copy()

            # Reconstruye parser para limpiar estado interno
            parser_mod = importlib.import_module('parser.parser')
            parser_obj = yacc.yacc(module=parser_mod)

            ast_root = None
            semantic_errors = []
            intermediate_code = []

            # Genera AST
            try:
                ast_root = parser_obj.parse(code, lexer=lexer)
            except SyntaxError as e:
                errors.append(f"Error de sintaxis: {e}")

            # Análisis semántico y 3AC si no hay errores
            if ast_root and not errors:
                from semantic.semantic import SemanticAnalyzer
                from codegen.intermedio import Generador3AC
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
                'has_semantic_errors': bool(semantic_errors),
                'intermediate_code': intermediate_code
            })

        @self.app.route('/api/ast', methods=['POST'])
        def get_ast():
            data = request.get_json() or {}
            code = data.get('code', '')

            # Reconstruye lexer y parser para AST
            lex_mod = importlib.import_module('lexer.lexer')
            lex_mod.lex_errors.clear()
            lexer = lex.lex(module=lex_mod)
            lexer.lineno = 1
            lexer.input(code)

            parser_mod = importlib.import_module('parser.parser')
            parser_obj = yacc.yacc(module=parser_mod)

            try:
                ast_root = parser_obj.parse(code, lexer=lexer)
            except Exception as e:
                return jsonify(error=str(e)), 400

            from semantic.semantic import SemanticAnalyzer
            analyzer = SemanticAnalyzer()
            semantic_errors = analyzer.analyze(ast_root)
            if semantic_errors:
                return jsonify(error="\n".join(semantic_errors)), 400

            # Convierte AST a formato DOT
            lines = ['digraph AST {', 'node [shape=box];']
            lines += self._ast_to_dot(ast_root)
            lines.append('}')

            return jsonify(dot="\n".join(lines))

    def _ast_to_dot(self, node, lines=None, counter=None, parent_id=None):
        if lines is None:
            lines = []
        if counter is None:
            counter = {'n': 0}
        node_id = f"n{counter['n']}"
        counter['n'] += 1
        lines.append(f'{node_id} [label="{type(node).__name__}"];')
        if parent_id:
            lines.append(f'{parent_id} -> {node_id};')
        import ast_nodes
        for attr, val in vars(node).items():
            if isinstance(val, ast_nodes.Node):
                self._ast_to_dot(val, lines, counter, node_id)
            elif isinstance(val, list):
                for child in val:
                    if isinstance(child, ast_nodes.Node):
                        self._ast_to_dot(child, lines, counter, node_id)
        return lines

    def run(self, host='0.0.0.0', port=5000, debug=True):
        self.app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    server = CompilerServer()
    server.run()
