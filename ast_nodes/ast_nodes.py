class Node:
    pass

class Program(Node):
    def __init__(self, statements):
        self.statements = statements

class Declaration(Node):
    def __init__(self, type, identifier, expression):
        self.type = type
        self.identifier = identifier
        self.expression = expression

class Assignment(Node):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

class If(Node):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class While(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class Block(Node):
    def __init__(self, statements):
        self.statements = statements

class BinaryOp(Node):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

class Number(Node):
    def __init__(self, value):
        self.value = value

class Boolean(Node):
    def __init__(self, value):
        self.value = value

class String(Node):
    def __init__(self, value):
        self.value = value

class Identifier(Node):
    def __init__(self, name):
        self.name = name

class Literal(Node):
    def __init__(self, value):
        self.value = value
