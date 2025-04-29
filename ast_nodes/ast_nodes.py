class Node:
    pass

class Program(Node):
    def __init__(self, statements):
        self.statements = statements

class Declaration(Node):
    def __init__(self, var_type, identifier, expr=None):
        self.var_type  = var_type
        self.identifier= identifier
        self.expr      = expr

class Assignment(Node):
    def __init__(self, identifier, expr):
        self.identifier = identifier
        self.expr       = expr

class If(Node):
    def __init__(self, condition, then_stmt, else_stmt=None):
        self.condition = condition
        self.then_stmt = then_stmt
        self.else_stmt = else_stmt

class While(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body      = body

class Block(Node):
    def __init__(self, statements):
        self.statements = statements

class BinaryOp(Node):
    def __init__(self, op, left, right):
        self.op    = op
        self.left  = left
        self.right = right

class Number(Node):
    def __init__(self, value):
        self.value = value

class Identifier(Node):
    def __init__(self, name):
        self.name = name
