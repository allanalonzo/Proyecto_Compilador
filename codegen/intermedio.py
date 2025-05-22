from ast_nodes import Program, Declaration, Assignment, BinaryOp, Identifier, Constant

class Generador3AC:
    def __init__(self):
        self.code = []
        self.temp_counter = 0

    def get_code(self):
        return self.code

    def new_temp(self):
        t = f"t{self.temp_counter}"
        self.temp_counter += 1
        return t

    def generar(self, node):
        if isinstance(node, Program):
            for stmt in node.statements:
                self.generar(stmt)

        elif isinstance(node, Declaration):
            self.code.append(f"{node.identifier.name} = 0")

        elif isinstance(node, Assignment):
            expr_result = self.generar(node.expression)
            self.code.append(f"{node.identifier.name} = {expr_result}")

        elif isinstance(node, BinaryOp):
            left = self.generar(node.left)
            right = self.generar(node.right)
            temp = self.new_temp()
            self.code.append(f"{temp} = {left} {node.operator} {right}")
            return temp

        elif isinstance(node, Identifier):
            return node.name

        elif isinstance(node, Constant):
            return str(node.value)

        else:
            self.code.append(f"# Nodo no soportado: {type(node).__name__}")

