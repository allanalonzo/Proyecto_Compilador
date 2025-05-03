class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}  # Tabla de símbolos: {nombre: {'type': tipo, 'scope': ámbito}}
        self.current_scope = "global"
        self.errors = []
    
    def analyze(self, ast):
        """Método principal para iniciar el análisis semántico"""
        self.visit(ast)
        return self.errors
    
    def visit(self, node):
        """Método de despacho para visitar los nodos del AST"""
        method_name = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        """Método genérico para nodos no implementados"""
        raise Exception(f'No existe método visit_{node.__class__.__name__}')
    
    def visit_Program(self, node):
        """Visita el nodo Program (raíz del AST)"""
        for statement in node.statements:
            self.visit(statement)
    
    def visit_Declaration(self, node):
        var_name = node.identifier.name
        var_type = node.type

        # Verificar redeclaración
        if var_name in self.symbol_table and self.symbol_table[var_name]['scope'] == self.current_scope:
            self.errors.append(f"Error semántico: Variable '{var_name}' ya declarada")
            return

        # Verificar inicialización si existe
        if node.expression:
            expr_type = self.visit(node.expression)
            self.check_type_compatibility(var_type, expr_type, var_name)

        # Registrar variable
        self.symbol_table[var_name] = {
            'type': var_type,
            'scope': self.current_scope
        }
    
    def visit_Assignment(self, node):
        var_name = node.identifier.name
        
        # Verificar existencia
        if var_name not in self.symbol_table:
            self.errors.append(f"Error semántico: Variable '{var_name}' no declarada")
            return
        
        # Verificar tipos
        var_type = self.symbol_table[var_name]['type']
        expr_type = self.visit(node.expression)
        self.check_type_compatibility(var_type, expr_type, var_name)
    
    def visit_If(self, node):
        """Visita sentencias if"""
        cond_type = self.visit(node.condition)
        if cond_type != 'bool':
            self.errors.append(f"Error semántico: La condición del if debe ser booleana (tipo {cond_type} encontrado)")
        
        self.visit(node.then_branch)
        if node.else_branch:
            self.visit(node.else_branch)
    
    def visit_While(self, node):
        """Visita sentencias while"""
        cond_type = self.visit(node.condition)
        if cond_type != 'bool':
            self.errors.append(f"Error semántico: La condición del while debe ser booleana (tipo {cond_type} encontrado)")
        
        self.visit(node.body)
    
    def visit_Block(self, node):
        """Visita bloques de código (ámbitos nuevos)"""
        previous_scope = self.current_scope
        self.current_scope = f"block_{id(node)}"  # Crear un nuevo ámbito
        
        for statement in node.statements:
            self.visit(statement)
        
        self.current_scope = previous_scope  # Restaurar ámbito anterior
    
    def visit_BinaryOp(self, node):
        """Visita operaciones binarias"""
        left_type = self.visit(node.left)
        right_type = self.visit(node.right) if node.right else None
        
        # Operadores aritméticos
        if node.operator in ['+', '-', '*', '/', '%']:
            if left_type not in ['int', 'float'] or (right_type and right_type not in ['int', 'float']):
                self.errors.append(f"Error semántico: Operador '{node.operator}' no soportado para {left_type} y {right_type}")
                return 'error'
            
            # Promoción de tipos: si alguno es float, el resultado es float
            return 'float' if 'float' in [left_type, right_type] else 'int'
        
        # Operadores de comparación
        elif node.operator in ['<', '>', '<=', '>=']:
            if left_type not in ['int', 'float'] or right_type not in ['int', 'float']:
                self.errors.append(f"Error semántico: Comparación '{node.operator}' no soportada para {left_type} y {right_type}")
            return 'bool'
        
        # Operadores de igualdad
        elif node.operator in ['==', '!=']:
            if left_type != right_type:
                self.errors.append(f"Error semántico: No se pueden comparar {left_type} y {right_type} con '{node.operator}'")
            return 'bool'
        
        # Operadores lógicos
        elif node.operator in ['&&', '||']:
            if left_type != 'bool' or right_type != 'bool':
                self.errors.append(f"Error semántico: Operador lógico '{node.operator}' requiere operandos booleanos")
            return 'bool'
        
        # Operador unario NOT
        elif node.operator == '!':
            if left_type != 'bool':
                self.errors.append(f"Error semántico: Operador '!' requiere operando booleano")
            return 'bool'
        
        return 'error'
    
    def visit_Number(self, node):
        """Visita literales numéricos"""
        return 'float' if isinstance(node.value, float) else 'int'
    
    def visit_Boolean(self, node):
        """Visita literales booleanos"""
        return 'bool'
    
    def visit_String(self, node):
        """Visita literales de cadena"""
        return 'string'
    
    def visit_Identifier(self, node):
        """Visita identificadores (variables)"""
        var_name = node.name
        
        if var_name not in self.symbol_table:
            self.errors.append(f"Error semántico: Variable '{var_name}' no declarada")
            return 'error'
        
        return self.symbol_table[var_name]['type']
    
    def check_type_compatibility(self, target_type, source_type, var_name):
        """Verifica compatibilidad de tipos en asignaciones"""
        if source_type == 'error':
            return  # Ya se reportó un error
        
        # Reglas de compatibilidad mejoradas
        compatible = False
        if target_type == 'int':
            compatible = source_type in ['int']
        elif target_type == 'float':
            compatible = source_type in ['int', 'float']
        elif target_type == 'bool':
            compatible = source_type == 'bool'
        elif target_type == 'string':
            # Solo permitir asignación de otro string
            compatible = source_type == 'string'
        else:
            compatible = False  # Tipo objetivo desconocido
        
        if not compatible:
            self.errors.append(
                f"Error semántico: No se puede asignar {source_type} a {target_type} "
                f"(variable '{var_name}')"
            )