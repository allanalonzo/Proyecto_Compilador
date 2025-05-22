from ast_nodes import Program, Declaration, Assignment, BinaryOp, Identifier, Literal

class Generador3AC:
    def __init__(self):
        self.temp_count = 0
        self.codigo = []
        self.simbolos = {}  # Tabla de símbolos para almacenar valores de variables

    def new_temp(self):
        temp = f"t{self.temp_count}"
        self.temp_count += 1
        return temp

    def generar(self, node):
        if isinstance(node, Program):
            for stmt in node.statements:
                self.generar(stmt)

        elif isinstance(node, Declaration):
            if node.expression is not None:
                temp = self.generar(node.expression)
                self.simbolos[node.identifier.name] = temp
                self.codigo.append(f"{node.identifier.name} = {temp}")
            else:
                self.simbolos[node.identifier.name] = 0
                self.codigo.append(f"{node.identifier.name} = 0")

        elif isinstance(node, Assignment):
            temp = self.generar(node.expression)
            self.simbolos[node.identifier.name] = temp
            self.codigo.append(f"{node.identifier.name} = {temp}")

        elif isinstance(node, BinaryOp):
            left = self.generar(node.left)
            right = self.generar(node.right)
            temp = self.new_temp()
            self.codigo.append(f"{temp} = {left} {node.operator} {right}")
            return temp

        elif isinstance(node, Literal):
            temp = self.new_temp()
            self.codigo.append(f"{temp} = {node.value}")
            return temp


        elif isinstance(node, Identifier):
            return self.simbolos.get(node.name, node.name)  # Devuelve valor o nombre

    def get_code(self):
        return "\n".join(self.codigo)
