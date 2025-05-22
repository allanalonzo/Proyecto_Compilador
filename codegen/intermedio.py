# codegen/intermedio.py

class Generador3AC:
    def __init__(self):
        self.temp_count = 0
        self.code = []

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def generar(self, node):
        if node['type'] == 'assign':
            temp = self.generar(node['expr'])
            self.code.append(f"{node['id']} = {temp}")
            return node['id']
        
        elif node['type'] == 'binop':
            left = self.generar(node['left'])
            right = self.generar(node['right'])
            temp = self.new_temp()
            self.code.append(f"{temp} = {left} {node['op']} {right}")
            return temp
        
        elif node['type'] == 'number':
            return str(node['value'])

    def get_code(self):
        return self.code
