# codegen/optimizer.py

class CSEOptimizer:
    """
    Optimización por eliminación de subexpresiones comunes (CSE).
    Entrada: lista de instrucciones; las que sean tuplas/lists de 4 elementos 
             se tratan como (op, a, b, res). Las demás se copian tal cual.
    Salida: lista optimizada, sin duplicados de expresiones idénticas.
    """
    def optimize(self, code):
        expr_table = {}      # (op, a, b) -> primer_temp
        temp_mapping = {}    # temp_nueva -> temp_canonical
        optimized = []

        for instr in code:
            # Paso 1: si no es una cuádrupla, la dejo pasar
            if not (isinstance(instr, (tuple, list)) and len(instr) == 4):
                optimized.append(instr)
                continue

            op, a, b, res = instr

            # Aplico mapeo previo a los operandos
            a_eff = temp_mapping.get(a, a)
            b_eff = temp_mapping.get(b, b) if b is not None else None

            # Solo optimizo operaciones puras
            key = (op, a_eff, b_eff)
            if key in expr_table:
                # Ya existía: reapunto la nueva temp a la antigua
                temp_mapping[res] = expr_table[key]
                # omitimos añadir esta cuádrupla
                continue

            # Primera vez que aparece: la guardo
            expr_table[key] = res
            optimized.append((op, a_eff, b_eff, res))

        return optimized
