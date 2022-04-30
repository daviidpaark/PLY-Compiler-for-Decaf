# David Park
# dappark
# 109582425

import decaf_lexer
from decaf_ast import *
import ply.yacc as yacc

tokens = decaf_lexer.tokens

precedence = (
    ("right", "EQUALS"),
    ("left", "OR"),
    ("left", "AND"),
    ("nonassoc", "EQ", "NE"),
    ("nonassoc", "LT", "GT", "LE", "GE"),
    ("left", "PLUS", "MINUS"),
    ("left", "TIMES", "DIVIDE"),
    ("right", "UPLUS", "UMINUS"),
    ("right", "NOT"),
)

classTable = {}
classHierarchy = {}
fieldID = 1
methodID = 1
constructorID = 1

block = -1
varID = 1

currentScope = Scope(None)
classTable["In"] = []
classTable["Out"] = []
currentScope.addMethod(Method("scan_int", 0, "In", "public", "static", None, Type("int"), None, None))
currentScope.addMethod(Method("scan_float", 0, "In", "public", "static", None, Type("float"), None, None))
currentScope.addMethod(Method("print", 0, "Out", "public", "static", Variable("i", 0 , "formal", Type("int")), None, None, None))
currentScope.addMethod(Method("print", 0, "Out", "public", "static", Variable("i", 0 , "formal", Type("float")), None, None, None))
currentScope.addMethod(Method("print", 0, "Out", "public", "static", Variable("i", 0 , "formal", Type("boolean")), None, None, None))
currentScope.addMethod(Method("print", 0, "Out", "public", "static", Variable("i", 0 , "formal", Type("string")), None, None, None))

classHierarchy["int"] = ["float"]
classHierarchy["float"] = []
classHierarchy["string"] = []
classHierarchy["boolean"] = []

def p_program(p):
    """program : class_decl
               | """
    try:
        p[0] = AST(flatten(p[1]), classTable, classHierarchy)
    except:
        pass
        
def p_class_decl(p):
    "class_decl : classname superclass LBRACE new_block class_body_decl exit_block RBRACE next_class_decl"
    fields = []
    methods = []
    constructors = []
    for decl in flatten(p[5]):
        if isinstance(decl, Field):
            decl.cclass = p[1]
            fields.append(decl)
        if isinstance(decl, Method):
            decl.cclass = p[1]
            methods.append(decl)
        if isinstance(decl, Constructor):
            constructors.append(decl)
    try:
        p[0] = [Class(p[1], p[2], fields, methods, constructors), p[8]]
    except:
        p[0] = [Class(p[1], p[2], fields, methods, constructors)]

def p_next_class_decl(p):
    """next_class_decl : classname superclass LBRACE new_block class_body_decl exit_block RBRACE next_class_decl
                       | """
    try:
        fields = []
        methods = []
        constructors = []
        for decl in flatten(p[5]):
            if isinstance(decl, Field):
                decl.cclass = p[1]
                fields.append(decl)
            if isinstance(decl, Method):
                decl.cclass = p[1]
                methods.append(decl)
            if isinstance(decl, Constructor):
                constructors.append(decl)
        try:
            p[0] = [Class(p[1], p[2], fields, methods, constructors), p[8]]
        except:
            p[0] = [Class(p[1], p[2], fields, methods, constructors)]
    except:
        pass

def p_classname(p):
    "classname : CLASS ID"
    if p[2] in classTable.keys():
        print("Duplicate class name: %s" % p[2])
        import sys
        sys.exit()
    classTable[p[2]] = []
    classHierarchy[p[2]] = []
    currentScope.className = p[2]
    p[0] = p[2]

def p_superclass(p):
    """superclass : EXTENDS ID
                  | """
    try:
        classHierarchy[currentScope.getClass()].append(p[2])
    except:
        pass

def p_class_body_decl(p):
    """class_body_decl : field_decl
                       | method_decl
                       | constructor_decl
                       | field_decl       class_body_decl
                       | method_decl      class_body_decl
                       | constructor_decl class_body_decl"""
    try: 
        p[0] = [p[1], p[2]]
    except:
        p[0] = [p[1]]

def p_field_decl(p):
    "field_decl : modifier var_decl"
    global fieldID
    fields = []
    for var in p[2][1]:
        if "public" in p[1]:
            if "static" in p[1]:
                fields.append(Field(var, fieldID, None, "public", "static", p[2][0]))
            else:
                fields.append(Field(var, fieldID, None, "public", "instance", p[2][0]))
        else:
            if "static" in p[1]:
                fields.append(Field(var, fieldID, None, "private", "static", p[2][0]))
            else:
                fields.append(Field(var, fieldID, None, "private", "instance", p[2][0]))
        fieldID += 1
    p[0] = fields
    for field in fields:
        currentScope.addField(field)
        classTable[currentScope.getClass()].append(field)

def p_method_decl(p):
    """method_decl : modifier type ID LPAREN formal_param RPAREN block
                   | modifier VOID ID LPAREN formal_param RPAREN block"""
    variables = []
    try:
        if p[5]:
            for param in filter(None, p[5]):
                variables.append(param)
        for stmt in filter(None, (p[7].statements)):
            if isinstance(stmt, Variable):
                variables.append(stmt)
    except:
        pass
    try:
        p[7].statements = [stmt for stmt in p[7].statements if not isinstance(stmt, Variable)]
    except:
        pass
    variables = flatten(variables)
    global methodID
    if p[2] == "void":
        p[2] = Type("void")
    if "public" in p[1]:
        if "static" in p[1]:
            p[0] = Method(p[3], methodID, None, "public", "static", p[5], p[2], variables, p[7])
        else:
            p[0] = Method(p[3], methodID, None, "public", "instance", p[5], p[2], variables, p[7])
    else:
        if "static" in p[1]:
            p[0] = Method(p[3], methodID, None, "private", "static", p[5], p[2], variables, p[7])
        else:
            p[0] = Method(p[3], methodID, None, "private", "instance", p[5], p[2], variables, p[7])
    methodID += 1


def p_constructor_decl(p):
    "constructor_decl : modifier ID LPAREN formal_param RPAREN block"
    variables = []
    try:
        if p[4]:
            for param in filter(None, p[4]):
                variables.append(param)
        for stmt in filter(None, (p[6].statements)):
            if isinstance(stmt, Variable):
                variables.append(stmt)
    except:
        pass
    try:
        p[6].statements = [stmt for stmt in p[6].statements if not isinstance(stmt, Variable)]
    except:
        pass
    variables = flatten(variables)
    global constructorID
    if "public" in p[1]:
        p[0] = Constructor(constructorID, "public", p[4], variables, p[6])
    else:
        p[0] = Constructor(constructorID, "private", p[4], variables, p[6])
    constructorID += 1

def p_modifier(p):
    """modifier : PUBLIC STATIC
                | PRIVATE STATIC
                | PUBLIC
                | PRIVATE
                | STATIC
                | """
    try:
        try:
            p[0] = [p[1], p[2]]
        except:
            p[0] = [p[1]]
    except:
        p[0] = "private"

def p_var_decl(p):
    "var_decl : type variables SEMICOLON"
    p[0] = [p[1], flatten(p[2])]

def p_type(p):
    """type : INT
            | FLOAT
            | BOOLEAN
            | ID"""
    p[0] = Type(p[1])

def p_variables(p):
    """variables : variable additional_variables
                 | """
    try:
        try: 
            p[0] = [p[1], p[2]]
        except:
            p[0] = [p[1]]       
    except:
        pass

def p_additional_variables(p):
    """additional_variables : COMMA variables additional_variables
                            | """
    try:
        try: 
            p[0] = [p[2], p[3]]
        except:
            p[0] = [p[2]]
    except:
        pass

def p_variable(p):
    "variable : ID"
    p[0] = p[1]

def p_formal_param(p):
    """formal_param : param formals
                    | """
    try:
        try: 
            p[0] = flatten([p[1], p[2]])
        except:
            p[0] = flatten(p[1])       
    except:
        pass

def p_formals(p):
    """formals : COMMA param formals
               | """
    try:
        try: 
            p[0] = [p[2], p[3]]
        except:
            p[0] = [p[2]]
    except:
        pass

def p_param(p):
    "param : type variable"
    global varID
    p[0] = Variable(p[2], varID, "formal", p[1])
    currentScope.add(p[0])
    varID += 1

def p_block(p):
    "block : LBRACE new_block stmts exit_block RBRACE"
    p[0] = Block(flatten(p[3]), p.lineno(3))

def p_stmts(p):
    """stmts : stmt additional_stmts
             | """
    try:
        try: 
            p[0] = [p[1], p[2]]
        except:
            p[0] = [p[1]]
    except:
        pass
    
def p_additional_stmts(p):
    """additional_stmts : stmt additional_stmts
                        | """
    try:
        try:
            p[0] = [p[1],p[2]]
        except:
            p[0] = [p[1]]
    except:
        pass

def p_stmt(p):
    """stmt : ifelse
            | while
            | for
            | return_stmt
            | stmt_expr SEMICOLON
            | BREAK SEMICOLON
            | CONTINUE SEMICOLON
            | block
            | var_decl_stmt
            | SEMICOLON"""
    if p[1] == "break":
        p[0] = Break(p.lineno(1))
    elif p[1] == "continue":
        p[0] = Continue(p.lineno(1))
    elif p[1] == ";":
        p[0] = Skip(p.lineno(1))
    else:
        p[0] = p[1]
        
def p_ifelse(p):
    """ifelse : IF LPAREN expr RPAREN stmt ELSE stmt
              | IF LPAREN expr RPAREN stmt"""
    try:
        p[0] = If(p[3], p[5], p[7], p.lineno(3))
    except:
        p[0] = If(p[3], p[5], Skip(p.lineno(3)), p.lineno(3))

def p_while(p):
    "while : WHILE LPAREN expr RPAREN stmt"
    p[0] = While(p[3], p[5], p.lineno(3))

def p_for(p):
    "for : FOR LPAREN opt_stmt_expr SEMICOLON opt_expr SEMICOLON opt_stmt_expr RPAREN stmt"
    p[0] = For(p[3], p[5], p[7], p[9], p.lineno(3))

def p_return_stmt(p):
    "return_stmt : RETURN opt_expr SEMICOLON"
    p[0] = Return(p[2], p.lineno(2))

def p_var_decl_stmt(p):
    "var_decl_stmt : var_decl"
    global varID
    vars = []
    for var in p[1][1]:
        variable = Variable(var, varID, "local", p[1][0])
        vars.append(variable)
        currentScope.add(variable)
        varID += 1
    p[0] = vars

def p_opt_stmt_expr(p):
    """opt_stmt_expr : stmt_expr
                     | """
    try:
        p[0] = p[1]
    except:
        p[0] = Skip(p.lineno(1))

def p_opt_expr(p):
    """opt_expr : expr
                | """
    try:
        p[0] = p[1]
    except:
        p[0] = Skip(p.lineno(0))

def p_stmt_expr(p):
    """stmt_expr : assign
                 | method_invocation"""
    p[0] = Expr(p[1], p.lineno(1))

def p_expr(p):
    """expr : primary
            | assign
            | expr_arith_op
            | expr_bool_op
            | expr_unary_op"""
    p[0] = p[1]

def p_primary(p):
    """primary : literal
               | THIS
               | SUPER
               | grouped_expr
               | new_object
               | field_access
               | method_invocation"""
    if p[1] == "this":
        p[0] = This(p.lineno(1))
    elif p[1] == "super":
        p[0] = Super(p.lineno(1))
    else:
        p[0] = p[1]

def p_literal(p):
    """literal : INT_CONST
               | FLOAT_CONST
               | STRING_CONST
               | NULL
               | TRUE
               | FALSE"""
    p[0] = Constant(p[1], p.lineno(1))

def p_grouped_expr(p):
    "grouped_expr : LPAREN expr RPAREN"
    p[0] = p[2]

def p_new_object(p):
    "new_object : NEW ID LPAREN arguments RPAREN"
    p[0] = Object(p[2], flatten(p[4]), p.lineno(2))

def p_assign(p):
    """assign : field_access EQUALS expr
              | auto_expr_post
              | auto_expr_pre"""
    try: 
        p[0] = Assign(p[1], p[3], p.lineno(2))
    except:
        p[0] = p[1]

def p_auto_expr_post(p):
    """auto_expr_post : field_access INCREMENT
                      | field_access DECREMENT"""
    p[0] = Auto(p[2], p[1], "post", p.lineno(1))

def p_auto_expr_pre(p):
    """auto_expr_pre : INCREMENT field_access
                     | DECREMENT field_access"""
    p[0] = Auto(p[1], p[2], "pre", p.lineno(2))

def p_field_access(p):
    """field_access : explicit_field
                    | implicit_access"""
    p[0] = p[1]
    
def p_explicit_field(p):
    "explicit_field : primary DOT ID"
    for value in classHierarchy[currentScope.getClass()]:
        for field in classTable[value]:
            if field.name == p[3]:
                p[0] = FieldAccess(p[1], p[3], p.lineno(3), field.id, field.type)
                return
    if (isinstance(p[1],This) and not currentScope.getField(p[3])) and (isinstance(p[1],This) and not currentScope.get(p[3])):
        print("Invalid/undeclared field access: %s [%d,%d]" % (p[3], p.lineno(3), p.lexpos(3)))
        import sys
        sys.exit()
    if (currentScope.get(p[3])):
        id = currentScope.get(p[3]).id
        type = currentScope.get(p[3]).type
    elif (currentScope.getField(p[3])):
        id = currentScope.getField(p[3]).id
        type = currentScope.getField(p[3]).type
    else:
        id = 1
        type = Type("%s.%s" % (p[1], p[3]))

    if p[1] in classTable.keys():
        p[0] = FieldAccess(Reference(p[1], p.lineno(3)), p[3], p.lineno(3), id, type)
    else:
        p[0] = FieldAccess(p[1], p[3], p.lineno(3), id, type)

def p_implicit_access(p):
    "implicit_access : ID"
    variable = currentScope.get(p[1])
    if variable:
        p[0] = VariableExpr(variable.id, p.lineno(1), variable)
    elif p[1] in classTable.keys():
        p[0] = p[1]
    else:
        print("Error accessing undeclared/implicit variable: %s [%d,%d]" % (p[1], p.lineno(1), p.lexpos(1)))
        import sys
        sys.exit()

def p_arguments(p):
    """arguments : expr additional_arguments
                 | """
    try:
        try: 
            p[0] = [p[1], p[2]]
        except:
            p[0] = [p[1]]
    except:
        pass

def p_additional_arguments(p):
    """additional_arguments : COMMA expr additional_arguments
                            | """
    try:
        try:
            p[0] = [p[2],p[3]]
        except:
            p[0] = p[2]
    except:
        pass

def p_method_invocation(p):
    "method_invocation : primary DOT ID LPAREN arguments RPAREN"
    p[0] = MethodCall(p[1], p[3], flatten(p[5]), p.lineno(3))

def p_expr_arith_op(p):
    "expr_arith_op : expr arith_op expr"
    # if   p[2] == "+" : p[0] = p[1] + p[3]
    # elif p[2] == "-" : p[0] = p[1] - p[3]
    # elif p[2] == "*" : p[0] = p[1] * p[3]
    # elif p[2] == "/" : p[0] = p[1] / p[3]
    p[0] = Binary(p[1], p[2], p[3], p.lineno(2))

def p_expr_bool_op(p):
    "expr_bool_op : expr bool_op expr"
    # if   p[2] == "&&" : p[0] = p[1] and p[3]
    # elif p[2] == "||" : p[0] = p[1] or  p[3]
    # elif p[2] == "==" : p[0] = p[1] ==  p[3]
    # elif p[2] == "!=" : p[0] = p[1] !=  p[3]
    # elif p[2] == "<"  : p[0] = p[1] <   p[3]
    # elif p[2] == ">"  : p[0] = p[1] >   p[3]
    # elif p[2] == "<=" : p[0] = p[1] <=  p[3]
    # elif p[2] == ">=" : p[0] = p[1] >=  p[3]
    p[0] = Binary(p[1], p[2], p[3], p.lineno(2))

def p_expr_unary_op(p):
    """expr_unary_op : PLUS expr %prec UPLUS
                     | MINUS expr %prec UMINUS
                     | NOT expr"""
    # if   p[1] == "+" : p[0] = +p[2]
    # elif p[1] == "-" : p[0] = -p[2]
    # elif p[1] == "!" : p[0] = not p[2]
    p[0] = Unary(p[1], p[2], p.lineno(1))

def p_arith_op(p):
    """arith_op : PLUS
                | MINUS
                | TIMES
                | DIVIDE"""
    p[0] = p[1]

def p_bool_op(p):
    """bool_op : AND
               | OR
               | EQ
               | NE
               | LT
               | GT
               | LE
               | GE"""
    p[0] = p[1]

def p_new_block(p):
    "new_block : "
    global block
    block += 1
    global currentScope
    currentScope = Scope(currentScope)

def p_exit_block(p):
    "exit_block : "
    global currentScope
    currentScope = currentScope.parent
    global varID
    varID = 1

def p_error(p):
    try:
        print("Syntax error in input: %s [%d,%d]" % (repr(p.value), p.lineno, p.lexpos))
    except:
        print("Syntax error in input")
    import sys
    sys.exit()

def flatten(outer):
    flat = []
    if outer == None:
        return
    for element in outer:
        if element == None:
            continue
        if not isinstance(element, list):
            flat.append(element)
        else:
            flat.extend(flatten(element))
    return flat

parser = yacc.yacc()
