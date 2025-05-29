# codegen/optimizer_dce.py

class DeadCodeElimOptimizer:
    """
    Eliminación de código muerto: quita instrucciones
    cuyo resultado nunca se usa después.
    Entrada: lista de instrucciones (tuplas op, a, b, res o any).
    Salida: lista sin las cuádruplas muertas.
    """
    def optimize(self, code):
        # 1) Primero, recopilar todos los temps/variables que se usan
        used = set()
        for instr in code:
            if isinstance(instr, (tuple, list)) and len(instr) == 4:
                _, a, b, _ = instr
                if isinstance(a, str): used.add(a)
                if isinstance(b, str): used.add(b)

        # 2) Recorremos de nuevo y sólo mantenemos las defs cuyo res está en 'used'
        optimized = []
        for instr in code:
            if isinstance(instr, (tuple, list)) and len(instr) == 4:
                op, a, b, res = instr
                # Si 'res' nunca se usa y no es una variable destino en última línea, lo quitamos
                if isinstance(res, str) and res not in used:
                    continue
            optimized.append(instr)

        return optimized