class ConstantFoldingOptimizer:
    """
    Plegado de constantes: evalúa operaciones aritméticas y lógicas
    cuyo operando(s) son literales, sustituyéndolas por el resultado.
    Entrada: lista de instrucciones (tuplas op, a, b, res o cualquier otro).
    Salida: lista donde las instrucciones constantes ya están plegadas.
    """
    def optimize(self, code):
        optimized = []
        for instr in code:
            # Solo plegamos cuádruplas (op, a, b, res)
            if isinstance(instr, (tuple, list)) and len(instr) == 4:
                op, a, b, res = instr
                # Si ambos operandos son literales numéricos, lo evaluamos
                if op in ('+', '-', '*', '/', '%', '<', '<=', '>', '>=', '==', '!=') \
                   and isinstance(a, (int, float)) \
                   and isinstance(b, (int, float)):
                    # Ejemplo: ('+', 2, 3, 't1') → ('assign', 5, None, 't1')
                    result = None
                    if op == '+':   result = a + b
                    elif op == '-': result = a - b
                    elif op == '*': result = a * b
                    elif op == '/': result = a / b
                    elif op == '%': result = a % b
                    elif op == '<': result = a < b
                    elif op == '<=':result = a <= b
                    elif op == '>': result = a > b
                    elif op == '>=':result = a >= b
                    elif op == '==':result = a == b
                    elif op == '!=':result = a != b

                    # Reemplazamos la cuádrupla original por una asignación directa
                    optimized.append(('assign', result, None, res))
                    continue
            # En cualquier otro caso, la instrucción queda igual
            optimized.append(instr)
        return optimized