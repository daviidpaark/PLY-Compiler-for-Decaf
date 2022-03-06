# David Park
# dappark
# 109582425


class Class:
    def __init__(self, name, superclass, fields, constructors, methods):
        self.name = name
        self.superclass = superclass
        self.fields = fields
        self.constructors = constructors
        self.methods = methods


class Field:
    def __init__(self, name, id, cclass, visibility, applicability, type):
        self.name = name
        self.id = id
        self.cclass = cclass
        self.visibility = visibility
        self.applicability = applicability
        self.type = type


class Constructor:
    def __init__(self, id, visibility, parameters, variables, body):
        self.id = id
        self.visibility = visibility
        self.parameters = parameters
        self.variables = variables
        self.body = body


class Method:
    def __init__(
        self,
        name,
        id,
        cclass,
        visibility,
        applicability,
        parameters,
        type,
        variables,
        body,
    ):
        self.name = name
        self.id = id
        self.cclass = cclass
        self.visibility = visibility
        self.applicability = applicability
        self.parameters = parameters
        self.type = type
        self.variables = variables
        self.body = body


class Variable:
    def __init__(self, name, id, kind, type):
        self.name = name
        self.id = id
        self.kind = kind
        self.type = type


class Type:
    def __init__(self, name):
        self.name = name


class If:
    def __init__(self, condition, then, elsee, line):
        self.condition = condition
        self.then = then
        self.elsee = elsee
        self.line = line


class While:
    def __init__(self, condition, body, line):
        self.condition = condition
        self.body = body
        self.line = line


class For:
    def __init__(self, initializer, condition, update, body, line):
        self.initializer = initializer
        self.condition = condition
        self.update = update
        self.body = body
        self.line = line


class Return:
    def __init__(self, value, line):
        self.value = value
        self.line = line


class Expr:
    def __init__(self, expr, line):
        self.expr = expr
        self.line = line


class Block:
    def __init__(self, statements, line):
        self.statements = statements
        self.line = line


class Break:
    def __init__(self, line):
        self.line = line


class Continue:
    def __init__(self, line):
        self.line = line


class Skip:
    def __init__(self, line):
        self.line = line


class Constant:
    def __init__(self, value, line):
        self.value = value
        self.line = line


class VariableExpr:
    def __init__(self, id, line):
        self.id = id
        self.line = line


class Unary:
    def __init__(self, operator, operand, line):
        self.operator = operator
        self.operand = operand
        self.line = line


class Binary:
    def __init__(self, left, operator, right, line):
        self.left = left
        self.operator = operator
        self.right = right
        self.line = line


class Assign:
    def __init__(self, lhs, rhs, line):
        self.lhs = lhs
        self.rhs = rhs
        self.line = line


class Auto:
    def __init__(self, operator, operand, placement, line):
        self.operator = operator
        self.operand = operand
        self.placement = placement
        self.line = line


class FieldAccess:
    def __init__(self, base, field, line):
        self.base = base
        self.field = field
        self.line = line


class MethodCall:
    def __init__(self, base, method, arguments, line):
        self.base = base
        self.method = method
        self.arguments = arguments
        self.line = line


class Object:
    def __init__(self, base, arguments, line):
        self.base = base
        self.arguments = arguments
        self.line = line


class This:
    def __init__(self, line):
        self.line = line


class Super:
    def __init__(self, line):
        self.line = line


class Reference:
    def __init__(self, name, line):
        self.name = name
        self.line = line
