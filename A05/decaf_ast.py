# David Park
# dappark
# 109582425

import decaf_typecheck as typeCheck

global table
global hierachy
global args
global temp
global registers
global localVars
global branch
branch = 0


class AST:
    def __init__(self, classes, classTable, classHierarchy):
        self.classes = classes
        self.table = classTable
        global table
        table = classTable
        self.hierarchy = classHierarchy
        global hierachy
        hierachy = classHierarchy

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
            params = ""
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

    def getType(self):
        return self.type.getType()

    def gen(self):
        global temp
        temp = 0
        global localVars
        localVars = {}
        global registers
        registers = {}


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

    def getType(self):
        return self.type.getType()


class Type:
    def __init__(self, name):
        self.name = name

    def getType(self):
        return self.name


class If:
    def __init__(self, condition, then, elsee, line):
        self.condition = condition
        self.then = then
        self.elsee = elsee
        self.line = line

    def tree(self):
        if isinstance(self.elsee, Skip):
            return "If( (%s),\n(%s) )" % (self.condition.tree(), self.then.tree())
        else:
            return "If( (%s),\n(%s),\nElse(%s) )" % (
                self.condition.tree(),
                self.then.tree(),
                self.elsee.tree(),
            )

    def getType(self):
        if self.condition.getType() == "boolean":
            try:
                for stmt in self.then.statements:
                    if stmt.getType() == "error":
                        return "error"
            except:
                if self.then.getType() == "error":
                    return "error"
            try:
                for stmt in self.elsee:
                    if stmt.getType() == "error":
                        return "error"
            except:
                if self.elsee.getType() == "error":
                    return "error"


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

    def getType(self):
        if self.condition.getType() == "boolean":
            for stmt in self.body:
                if stmt.getType() == "error":
                    return "error"


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

    def getType(self):
        if self.condition.getType() == "boolean":
            for stmt in self.body:
                if stmt.getType() == "error":
                    return "error"


class Return:
    def __init__(self, value, line):
        self.value = value
        self.line = line

    def tree(self):
        return "Return( %s )" % self.value.tree()

    def getType(self):
        return self.value.getType()


class Expr:
    def __init__(self, expr, line):
        self.expr = expr
        self.line = line

    def tree(self):
        return "Expr( %s )" % self.expr.tree()

    def getType(self):
        return self.expr.getType()

    def gen(self):
        return self.expr.gen()


class Block:
    def __init__(self, statements, line):
        self.statements = statements
        self.line = line

    def tree(self):
        stmts = []
        try:
            for stmt in self.statements:
                stmts.append(stmt.tree())
        except:
            pass
        if stmts:
            stmts = ", \n".join(filter(None, stmts))
        else:
            stmts = ""
        return stmts

    def getType(self):
        for stmt in self.statements:
            if stmt.getType() == "error":
                return "error"
        return "block"


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

    def getType(self):
        if self.value in ("true", "false"):
            return "boolean"
        elif self.value == "null":
            return "null"
        elif isinstance(self.value, int):
            return "int"
        elif isinstance(self.value, float):
            return "float"
        elif isinstance(self.value, str):
            return "string"

    def gen(self, lhs):
        global temp
        global localVars
        if self.value == "true":
            code = "move_immed_i t%d, 1" % temp
            registers[lhs.variable.name] = temp
            temp += 1
            localVars[lhs.variable.name] = 1
            return code
        elif self.value == "false":
            code = "move_immed_i t%d, 0" % temp
            registers[lhs.variable.name] = temp
            temp += 1
            localVars[lhs.variable.name] = 0
            return code
        elif isinstance(self.value, int):
            code = "move_immed_i t%d, %d" % (temp, self.value)
            registers[lhs.variable.name] = temp
            temp += 1
            localVars[lhs.variable.name] = self.value
            return code
        elif isinstance(self.value, float):
            code = "move_immed_f t%d, %f" % (temp, self.value)
            registers[lhs.variable.name] = temp
            temp += 1
            localVars[lhs.variable.name] = self.value
            return code


class VariableExpr:
    def __init__(self, id, line, variable):
        self.id = id
        self.line = line
        self.variable = variable

    def tree(self):
        return "Variable(%d)" % self.id

    def getType(self):
        return self.variable.getType()

    def getValue(self):
        return localVars[self.variable.name]

    def gen(self, lhs):
        global temp
        code = "move t%d, t%d" % (temp, registers[self.variable.name])
        registers[lhs.variable.name] = temp
        temp += 1
        localVars[lhs.variable.name] = localVars[self.variable.name]
        return code


class Unary:
    def __init__(self, operator, operand, line):
        self.operator = operator
        self.operand = operand
        self.line = line

    def tree(self):
        return "Unary('%s', %s)" % (self.operator, self.operand.tree())

    def getType(self):
        if self.operator == "-" or self.operator == "+":
            if self.operand.getType() in ("int", "float"):
                return self.operand.getType()
            else:
                return "error"
        elif self.operator == "!":
            if self.operand.getType() == "boolean":
                return self.operand.getType()
            else:
                return "error"

    def gen(self, lhs):
        global temp
        if isinstance(self.operand, VariableExpr):
            if self.operator == "+":
                if isinstance(self.operand.getValue(), int):
                    code = "move_immed_i t%d, %d" % (temp, self.operand.getValue())
                    registers[lhs.variable.name] = temp
                    temp += 1
                    localVars[lhs.variable.name] = self.operand.getValue()
                    return code
                else:
                    code = "move_immed_f t%d, %f" % (temp, self.operand.getValue())
                    registers[lhs.variable.name] = temp
                    temp += 1
                    localVars[lhs.variable.name] = self.operand.getValue()
                    return code
            elif self.operator == "-":
                if isinstance(self.operand.getValue(), int):
                    code = "move_immed_i t%d, %d" % (temp, self.operand.getValue() * -1)
                    registers[lhs.variable.name] = temp
                    temp += 1
                    localVars[lhs.variable.name] = self.operand.getValue()
                    return code
                else:
                    code = "move_immed_f t%d, %f" % (temp, self.operand.getValue() * -1)
                    registers[lhs.variable.name] = temp
                    temp += 1
                    localVars[lhs.variable.name] = self.operand.getValue()
                    return code
            elif self.operator == "!":
                if self.operand.getValue() == 0:
                    code = "move_immed_i t%d, 1" % temp
                    registers[lhs.variable.name] = temp
                    temp += 1
                    localVars[lhs.variable.name] = 1
                    return code
                else:
                    code = "move_immed_i t%d, 0" % temp
                    registers[lhs.variable.name] = temp
                    temp += 1
                    localVars[lhs.variable.name] = 0
                    return code
        elif isinstance(self.operand, Constant):
            if self.operator == "+":
                code = "move_immed_i t%d, %d" % (temp, self.operand.value)
                registers[lhs.variable.name] = temp
                temp += 1
                localVars[lhs.variable.name] = self.operand.value
                return code
            elif self.operator == "-":
                code = "move_immed_i t%d, %d" % (temp, self.operand.value * -1)
                registers[lhs.variable.name] = temp
                temp += 1
                localVars[lhs.variable.name] = self.operand.value
                return code


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

    def getType(self):
        if self.operator in ("+", "-", "*", "/"):
            if (
                self.left.getType() == self.right.getType()
            ) and self.left.getType() in (
                "int",
                "float",
            ):
                return self.left.getType()
            elif self.left.getType() in (
                "int",
                "float",
            ) and self.right.getType() in ("int", "float"):
                return "float"
            else:
                return "error"
        elif self.operator in ("&&", "||"):
            if self.left.getType() == "boolean" and self.right.getType() == "boolean":
                return "boolean"
            else:
                return "error"
        elif self.operator in ("<", "<=", ">", ">="):
            if self.left.getType() in (
                "int",
                "float",
            ) and self.right.getType() in ("int", "float"):
                return "boolean"
            else:
                return "error"
        elif self.operator in ("==", "!="):
            if typeCheck.isSubType(
                self.left.getType(), self.right.getType()
            ) or typeCheck.isSubType(self.right.getType(), self.left.getType()):
                return "boolean"
            else:
                return "error"

    def gen(self, lhs):
        global temp, branch
        code = self.left.gen(lhs) + "\n\t" + self.right.gen(lhs)
        if self.operator == "+":
            if lhs.getType() == "int":
                code += "\n\tiadd t%d, t%d, t%d" % (temp, temp - 2, temp - 1)
                localVars[lhs.variable.name] = "iadd"
            elif lhs.getType() == "float":
                code += "\n\tfadd t%d, t%d, t%d" % (temp, temp - 2, temp - 1)
                localVars[lhs.variable.name] = "fadd"
        elif self.operator == "-":
            if lhs.getType() == "int":
                code += "\n\tisub t%d, t%d, t%d" % (temp, temp - 2, temp - 1)
                localVars[lhs.variable.name] = "isub"
            elif lhs.getType() == "float":
                code += "\n\tfsub t%d, t%d, t%d" % (temp, temp - 2, temp - 1)
                localVars[lhs.variable.name] = "fsub"
        elif self.operator == "*":
            if lhs.getType() == "int":
                code += "\n\timul t%d, t%d, t%d" % (temp, temp - 2, temp - 1)
                localVars[lhs.variable.name] = "imul"
            elif lhs.getType() == "float":
                code += "\n\tfmul t%d, t%d, t%d" % (temp, temp - 2, temp - 1)
                localVars[lhs.variable.name] = "fmul"
        elif self.operator == "/":
            if lhs.getType() == "int":
                code += "\n\tidiv t%d, t%d, t%d" % (temp, temp - 2, temp - 1)
                localVars[lhs.variable.name] = "idiv"
            elif lhs.getType() == "float":
                code += "\n\tfdiv t%d, t%d, t%d" % (temp, temp - 2, temp - 1)
                localVars[lhs.variable.name] = "fdiv"
        elif self.operator == "<":
            if self.left.getType() == "float" or self.right.getType() == "float":
                code += "\n\tflt t%d, t%d, t%d" % (temp, temp - 2, temp - 1)
                localVars[lhs.variable.name] = "flt"
            else:
                code += "\n\tilt t%d, t%d, t%d" % (temp, temp - 2, temp - 1)
                localVars[lhs.variable.name] = "ilt"
        elif self.operator == "<=":
            if self.left.getType() == "float" or self.right.getType() == "float":
                code += "\n\tfleq t%d, t%d, t%d" % (temp, temp - 2, temp - 1)
                localVars[lhs.variable.name] = "fleq"
            else:
                code += "\n\tileq t%d, t%d, t%d" % (temp, temp - 2, temp - 1)
                localVars[lhs.variable.name] = "ileq"
        elif self.operator == ">":
            if self.left.getType() == "float" or self.right.getType() == "float":
                code += "\n\tfgt t%d, t%d, t%d" % (temp, temp - 2, temp - 1)
                localVars[lhs.variable.name] = "fgt"
            else:
                code += "\n\tigt t%d, t%d, t%d" % (temp, temp - 2, temp - 1)
                localVars[lhs.variable.name] = "igt"
        elif self.operator == ">=":
            if self.left.getType() == "float" or self.right.getType() == "float":
                code += "\n\tfgeq t%d, t%d, t%d" % (temp, temp - 2, temp - 1)
                localVars[lhs.variable.name] = "fgeq"
            else:
                code += "\n\tigeq t%d, t%d, t%d" % (temp, temp - 2, temp - 1)
                localVars[lhs.variable.name] = "igeq"
        elif self.operator == "==":
            if self.left.getType() == "float" or self.right.getType() == "float":
                code += "\n\tfsub t%d, t%d, t%d" % (temp, temp - 2, temp - 1)
                localVars[lhs.variable.name] = "feq"
            else:
                code += "\n\tisub t%d, t%d, t%d" % (temp, temp - 2, temp - 1)
                localVars[lhs.variable.name] = "ieq"
            label = "L%d" % branch
            branch += 1
            code += "\n\tbz t%d, %s" % (temp, label)
            code += "\n\tmove_immed_i t%d, 0" % temp
            code += "\n\tjmp L%d" % branch
            code += "\n%s:" % label
            code += "\n\tmove_immed_i t%d, 1" % temp
            code += "\nL%d:" % branch
            branch += 1
        elif self.operator == "!=":
            if self.left.getType() == "float" or self.right.getType() == "float":
                code += "\n\tfsub t%d, t%d, t%d" % (temp, temp - 2, temp - 1)
                localVars[lhs.variable.name] = "fneq"
            else:
                code += "\n\tisub t%d, t%d, t%d" % (temp, temp - 2, temp - 1)
                localVars[lhs.variable.name] = "ineq"
            label = "L%d" % branch
            branch += 1
            code += "\n\tbnz t%d, %s" % (temp, label)
            code += "\n\tmove_immed_i t%d, 0" % temp
            code += "\n\tjmp L%d" % branch
            code += "\n%s:" % label
            code += "\n\tmove_immed_i t%d, 1" % temp
            code += "\nL%d:" % branch
            branch += 1
        elif self.operator == "&&":
            localVars[lhs.variable.name] = "and"
            label = "L%d" % branch
            branch += 1
            code += "\n\tbz t%d, %s" % (temp - 2, label)
            code += "\n\tbz t%d, %s" % (temp - 1, label)
            code += "\n\tmove_immed_i t%d, 1" % temp
            code += "\n\tjmp L%d" % branch
            code += "\n%s:" % label
            code += "\n\tmove_immed_i t%d, 0" % temp
            code += "\nL%d:" % branch
            branch += 1
        elif self.operator == "||":
            localVars[lhs.variable.name] = "or"
            label = "L%d" % branch
            branch += 1
            code += "\n\tbnz t%d, %s" % (temp - 2, label)
            code += "\n\tbnz t%d, %s" % (temp - 1, label)
            code += "\n\tmove_immed_i t%d, 0" % temp
            code += "\n\tjmp L%d" % branch
            code += "\n%s:" % label
            code += "\n\tmove_immed_i t%d, 1" % temp
            code += "\nL%d:" % branch
            branch += 1
        registers[lhs.variable.name] = temp
        temp += 1
        return code


class Assign:
    def __init__(self, lhs, rhs, line):
        self.lhs = lhs
        self.rhs = rhs
        self.line = line

    def tree(self):
        return "Assign(%s, %s), %s, %s" % (
            self.lhs.tree(),
            self.rhs.tree(),
            self.lhs.getType(),
            self.rhs.getType(),
        )

    def getType(self):
        if typeCheck.isSubType(self.rhs.getType(), self.lhs.getType()):
            return self.lhs.getType()
        else:
            print(
                "Invalid assignment from %s to %s (line %d)"
                % (self.rhs.getType(), self.lhs.getType(), self.line)
            )
            return "error"

    def gen(self):
        return self.rhs.gen(self.lhs)


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

    def getType(self):
        if self.operand.getType() in ("int", "float"):
            return self.operand.getType()
        else:
            return "error"


class FieldAccess:
    def __init__(self, base, field, line, id, type):
        self.base = base
        self.field = field
        self.line = line
        self.id = id
        self.type = type

    def tree(self):
        if isinstance(self.base, str):
            if isinstance(self.field, str):
                return "Field-access(%s, %s, %d)" % (self.base, self.field, self.id)
            return "Field-access(%s, %s, %d)" % (self.base, self.field.tree(), self.id)
        elif isinstance(self.field, str):
            return "Field-access(%s, %s, %d)" % (self.base.tree(), self.field, self.id)
        return "Field-access(%s, %s, %d)" % (
            self.base.tree(),
            self.field.tree(),
            self.id,
        )

    def getType(self):
        if isinstance(self.base, Reference):
            if self.base.name in table.keys():
                for field in table[self.base.name]:
                    if field.name == self.field:
                        self.id = field.id
                        self.type = field.type
        return self.type.getType()


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

    def getType(self):
        pass


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

    def getType(self):
        return self.base


class This:
    def __init__(self, line):
        self.line = line

    def tree(self):
        return "This"

    def getType(self):
        pass


class Super:
    def __init__(self, line):
        self.line = line

    def tree(self):
        return "Super"

    def getType(self):
        pass


class Reference:
    def __init__(self, name, line):
        self.name = name
        self.line = line

    def tree(self):
        return "Class-reference(%s)" % self.name

    def getType(self):
        pass


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

    def getClass(self):
        try:
            return self.className
        except:
            return self.parent.getClass()