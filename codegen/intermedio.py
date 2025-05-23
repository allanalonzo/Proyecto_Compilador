from ast_nodes import Program, Declaration, Assignment, BinaryOp, Identifier, Literal, Number, If, While

class Generador3AC:
    def __init__(self, modo_debug=False):
        self.temp_count = 0
        self.label_count = 0
        self.codigo = []
        self.simbolos = {}  # Tabla de símbolos para valores
        self.debug = modo_debug

    def nueva_temporal(self):
        temp = f"t{self.temp_count}"
        self.temp_count += 1
        return temp

    def nueva_etiqueta(self):
        label = f"L{self.label_count}"
        self.label_count += 1
        return label

    def emitir(self, instruccion):
        self.codigo.append(instruccion)
        if self.debug:
            print(f"[DEBUG] {instruccion}")

    def generar(self, node):
        if isinstance(node, Program):
            for stmt in node.statements:
                self.generar(stmt)

        elif isinstance(node, Declaration):
            valor = self.generar(node.expression) if node.expression else "0"
            self.simbolos[node.identifier.name] = valor
            self.emitir(f"{node.identifier.name} = {valor}")

        elif isinstance(node, Assignment):
            valor = self.generar(node.expression)
            self.simbolos[node.identifier.name] = valor
            self.emitir(f"{node.identifier.name} = {valor}")

        elif isinstance(node, BinaryOp):
            izq = self.generar(node.left)
            der = self.generar(node.right)
            temp = self.nueva_temporal()
            self.emitir(f"{temp} = {izq} {node.operator} {der}")
            return temp

        elif isinstance(node, Literal) or isinstance(node, Number):
            temp = self.nueva_temporal()
            self.emitir(f"{temp} = {node.value}")
            return temp

        elif isinstance(node, Identifier):
            return self.simbolos.get(node.name, node.name)

        elif isinstance(node, If):
            cond = self.generar(node.condition)
            etiqueta_si = self.nueva_etiqueta()
            etiqueta_fin = self.nueva_etiqueta()

            self.emitir(f"if {cond} goto {etiqueta_si}")
            self.emitir(f"goto {etiqueta_fin}")
            self.emitir(f"{etiqueta_si}:")
            for stmt in node.then_body:
                self.generar(stmt)
            self.emitir(f"{etiqueta_fin}:")

        elif isinstance(node, While):
            etiqueta_inicio = self.nueva_etiqueta()
            etiqueta_cuerpo = self.nueva_etiqueta()
            etiqueta_salida = self.nueva_etiqueta()

            self.emitir(f"{etiqueta_inicio}:")
            cond = self.generar(node.condition)
            self.emitir(f"if {cond} goto {etiqueta_cuerpo}")
            self.emitir(f"goto {etiqueta_salida}")
            self.emitir(f"{etiqueta_cuerpo}:")
            for stmt in node.body:
                self.generar(stmt)
            self.emitir(f"goto {etiqueta_inicio}")
            self.emitir(f"{etiqueta_salida}:")

        else:
            raise Exception(f"Tipo de nodo no soportado: {type(node)}")

    def get_code(self):
        return "\n".join(self.codigo)
