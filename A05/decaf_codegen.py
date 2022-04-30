# David Park
# dappark
# 109582425

import decaf_ast as AST
import decaf_absmc as ABSMC

global f


def codeGen(AST, file):
    global f
    f = ABSMC.openFile(file)
    for entry in AST.classes:
        genClass(entry)
    ABSMC.closeFile(f)


def genClass(entry):
    for field in entry.fields:
        genField(field)
    for constructor in entry.constructors:
        genConstructor(constructor)
    for method in entry.methods:
        genMethod(method)


def genField(field):
    pass


def genConstructor(constructor):
    pass


def genMethod(method):
    ABSMC.newLabel(method.name)
    method.gen()
    for stmt in method.body.statements:
        ABSMC.writeFile(stmt.gen())
