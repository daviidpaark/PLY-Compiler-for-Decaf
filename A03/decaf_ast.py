# David Park
# dappark
# 109582425


class AST:
    def __init__(self, classes):
        self.classes = classes

    def printAST(self):
        for entry in self.classes:
            print("-" * 80)
            entry.tree()
        print("-" * 80)


class Class:
    def __init__(self, name, superclass, fields, methods, constructors):
        self.name = name
        self.superclass = superclass
        self.fields = fields
        self.methods = methods
        self.constructors = constructors

    def tree(self):
        print("Class Name: %s" % self.name)
        if self.superclass is not None:
            print("Superclass Name: %s" % self.superclass)
        else:
            print("Superclass Name: ")
        print("Fields: ")
        for field in self.fields:
            field.tree()
        print("Constructors: ")
        for constructor in self.constructors:
            constructor.tree()
        print("Methods: ")
        for method in self.methods:
            method.tree()


class Field:
    def __init__(self, name, id, cclass, visibility, applicability, type):
        self.name = name
        self.id = id
        self.cclass = cclass
        self.visibility = visibility
        self.applicability = applicability
        self.type = type

    def tree(self):
        type = self.type.name
        if type not in ("int", "float", "boolean"):
            type = "user(%s)" % type
        print(
            "FIELD: %d, %s, %s, %s, %s, %s"
            % (
                self.id,
                self.name,
                self.cclass,
                self.visibility,
                self.applicability,
                type,
            )
        )


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

    def tree(self):
        type = self.type.name
        if type not in ("int", "float", "boolean", "void"):
            type = "user(%s)" % type
        print(
            "METHOD: %d, %s, %s, %s, %s, %s"
            % (
                self.id,
                self.name,
                self.cclass,
                self.visibility,
                self.applicability,
                type,
            )
        )
        params = []
        try:
            for parameter in self.parameters:
                params.append(str(parameter.id))
        except:
            pass
        print("Method Parameters:", ", ".join(params))
        print("Variable Table: ")
        for variable in self.variables:
            variable.tree()
        print("Method Body: ")
        print("Block([")
        stmts = []
        try:
            for stmt in self.body.statements:
                stmts.append(stmt.tree())
        except:
            pass
        if stmts:
            print(", \n".join(filter(None, stmts)))
        print("])")


class Constructor:
    def __init__(self, id, visibility, parameters, variables, body):
        self.id = id
        self.visibility = visibility
        self.parameters = parameters
        self.variables = variables
        self.body = body

    def tree(self):
        print("CONSTRUCTOR: %d, %s" % (self.id, self.visibility))
        params = []
        try:
            for parameter in self.parameters:
                params.append(str(parameter.id))
        except:
            pass
        print("Constructor Parameters:", ", ".join(params))
        print("Variable Table: ")
        for variable in self.variables:
            variable.tree()
        print("Constructor Body: ")
        print("Block([")
        stmts = []
        try:
            for stmt in self.body.statements:
                stmts.append(stmt.tree())
        except:
            pass
        if stmts:
            print(", \n".join(filter(None, stmts)))
        print("])")


class Variable:
    def __init__(self, name, id, kind, type):
        self.name = name
        self.id = id
        self.kind = kind
        self.type = type

    def tree(self):
        type = self.type.name
        if type not in ("int", "float", "boolean"):
            type = "user(%s)" % type
        print(
            "VARIABLE: %d, %s, %s, %s"
            % (
                self.id,
                self.name,
                self.kind,
                type,
            )
        )


class Type:
    def __init__(self, name):
        self.name = name


class If:
    def __init__(self, condition, then, elsee, line):
        self.condition = condition
        self.then = then
        self.elsee = elsee
        self.line = line

    def tree(self):
        return "If( %s,\n%s,\n%s )" % (
            self.condition.tree(),
            self.then.tree(),
            self.elsee.tree(),
        )


class While:
    def __init__(self, condition, body, line):
        self.condition = condition
        self.body = body
        self.line = line

    def tree(self):
        stmts = []
        try:
            for stmt in self.body.statements:
                stmts.append(stmt.tree())
        except:
            pass
        return "While( %s,\n%s )" % (
            self.condition.tree(),
            ",\n".join(filter(None, stmts)),
        )


class For:
    def __init__(self, initializer, condition, update, body, line):
        self.initializer = initializer
        self.condition = condition
        self.update = update
        self.body = body
        self.line = line

    def tree(self):
        stmts = []
        try:
            for stmt in self.body.statements:
                stmts.append(stmt.tree())
        except:
            pass
        return "For( %s,\n%s,\n%s,\n%s )" % (
            self.initializer.tree(),
            self.condition.tree(),
            self.update.tree(),
            ",\n".join(filter(None, stmts)),
        )


class Return:
    def __init__(self, value, line):
        self.value = value
        self.line = line

    def tree(self):
        return "Return( %s )" % self.value.tree()


class Expr:
    def __init__(self, expr, line):
        self.expr = expr
        self.line = line

    def tree(self):
        return "Expr( %s )" % self.expr.tree()


class Block:
    def __init__(self, statements, line):
        self.statements = statements
        self.line = line


class Break:
    def __init__(self, line):
        self.line = line

    def tree(self):
        return "Break"


class Continue:
    def __init__(self, line):
        self.line = line

    def tree(self):
        return "Continue"


class Skip:
    def __init__(self, line):
        self.line = line

    def tree(self):
        return "Skip"


class Constant:
    def __init__(self, value, line):
        self.value = value
        self.line = line

    def tree(self):
        if self.value in ("true", "false"):
            type = "Boolean-constant"
        elif self.value == "null":
            type = "Null-constant"
        elif isinstance(self.value, int):
            type = "Int-constant"
        elif isinstance(self.value, float):
            type = "Float-constant"
        elif isinstance(self.value, str):
            type = "String-constant"
        return "Constant(%s(%s))" % (type, str(self.value))


class VariableExpr:
    def __init__(self, id, line):
        self.id = id
        self.line = line

    def tree(self):
        return "Variable(%d)" % self.id


class Unary:
    def __init__(self, operator, operand, line):
        self.operator = operator
        self.operand = operand
        self.line = line

    def tree(self):
        return "Unary('%s', %s)" % (self.operator, self.operand.tree())


class Binary:
    def __init__(self, left, operator, right, line):
        self.left = left
        self.operator = operator
        self.right = right
        self.line = line

    def tree(self):
        return "Binary('%s', %s, %s)" % (
            self.operator,
            self.left.tree(),
            self.right.tree(),
        )


class Assign:
    def __init__(self, lhs, rhs, line):
        self.lhs = lhs
        self.rhs = rhs
        self.line = line

    def tree(self):
        return "Assign(%s, %s)" % (self.lhs.tree(), self.rhs.tree())


class Auto:
    def __init__(self, operator, operand, placement, line):
        self.operator = operator
        self.operand = operand
        self.placement = placement
        self.line = line

    def tree(self):
        return "Auto('%s', %s, %s)" % (
            self.operator,
            self.operand.tree(),
            self.placement,
        )


class FieldAccess:
    def __init__(self, base, field, line):
        self.base = base
        self.field = field
        self.line = line

    def tree(self):
        if isinstance(self.base, str):
            if isinstance(self.field, str):
                return "Field-access(%s, %s)" % (self.base, self.field)
            return "Field-access(%s, %s)" % (self.base, self.field.tree())
        elif isinstance(self.field, str):
            return "Field-access(%s, %s)" % (self.base.tree(), self.field)
        return "Field-access(%s, %s)" % (self.base.tree(), self.field.tree())


class MethodCall:
    def __init__(self, base, method, arguments, line):
        self.base = base
        self.method = method
        self.arguments = arguments
        self.line = line

    def tree(self):
        args = []
        try:
            for arg in self.arguments:
                args.append(arg.tree())
            args = ", ".join(args)
        except:
            args = ""
        if isinstance(self.base, str):
            if isinstance(self.method, str):
                return "Method-call(%s, %s, [%s])" % (self.base, self.method, args)
            return "Method-call(%s, %s, [%s])" % (self.base, self.method.tree(), args)
        elif isinstance(self.method, str):
            return "Method-call(%s, %s, [%s])" % (self.base.tree(), self.method, args)
        return "Method-call(%s, %s, [%s])" % (
            self.base.tree(),
            self.method.tree(),
            args,
        )


class Object:
    def __init__(self, base, arguments, line):
        self.base = base
        self.arguments = arguments
        self.line = line

    def tree(self):
        args = []
        try:
            for arg in self.arguments:
                args.append(arg.tree())
            args = ", ".join(args)
        except:
            args = ""
        return "New-object(%s, [%s])" % (self.base, args)


class This:
    def __init__(self, line):
        self.line = line

    def tree(self):
        return "This"


class Super:
    def __init__(self, line):
        self.line = line

    def tree(self):
        return "Super"


class Reference:
    def __init__(self, name, line):
        self.name = name
        self.line = line

    def tree(self):
        return "Class-reference(%s)" % self.name


class Scope:
    def __init__(self, parent):
        self.varTable = {}
        self.fieldTable = {}
        self.methodTable = {}
        self.constructorTable = {}
        self.parent = parent

    def add(self, variable):
        if self.varTable.__contains__(variable.name):
            return False
        self.varTable[variable.name] = variable
        return True

    def get(self, name):
        if self.varTable.__contains__(name):
            return self.varTable[name]
        elif self.parent:
            return self.parent.get(name)
        return None

    def addField(self, field):
        if self.fieldTable.__contains__(field.name):
            return False
        self.fieldTable[field.name] = field
        return True

    def getField(self, name):
        if self.fieldTable.__contains__(name):
            return self.fieldTable[name]
        elif self.parent:
            return self.parent.getField(name)
        return None

    def addMethod(self, method):
        if self.methodTable.__contains__(method.name):
            return False
        self.methodTable[method.name] = method
        return True

    def getMethod(self, name):
        if self.methodTable.__contains__(name):
            return self.methodTable[name]
        elif self.parent:
            return self.parent.getMethod(name)
        return None

    def setClass(self, className):
        self.className = className
