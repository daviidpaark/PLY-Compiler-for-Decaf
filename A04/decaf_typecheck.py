# David Park
# dappark
# 109582425

import decaf_ast as AST

global hierarchy

def typeCheck(AST):
    global hierarchy
    hierarchy = AST.hierarchy
    for entry in AST.classes:
        if not typeCheckClass(entry):
            return False
    return True


def typeCheckClass(entry):
    for constructor in entry.constructors:
        if not typeCheckConstructor(constructor):
            return False
    for method in entry.methods:
        if not typeCheckMethod(method):
            return False
    return True


def typeCheckConstructor(constructor):
    for stmt in constructor.body.statements:
        if stmt.getType() == "error":
            return False
    return True


def typeCheckMethod(method):
    for stmt in method.body.statements:
        if stmt.getType() == "error":
            return False
    return True


def isSubType(lower, upper):
    if lower == upper:
        return True
    elif lower == "null" and upper not in ("int", "float", "string", "boolean"):
        return True
    elif hierarchy[lower].__contains__(upper):
        return True
    return False
