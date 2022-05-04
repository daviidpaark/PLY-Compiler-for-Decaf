# David Park
# dappark
# 109582425

import decaf_ast as AST
import decaf_absmc as ABSMC

global f
global static
static = 0


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
        if method.name == "main":
            genMethod(method)
            ABSMC.writeFile("")
    for method in entry.methods:
        if method.name != "main":
            genMethod(method)
            ABSMC.writeFile("")


def genField(field):
    pass


def genConstructor(constructor):
    pass


def genMethod(method):
    label = "M_%s_%d" % (method.name, method.id)
    ABSMC.newLabel(label)
    method.gen()
    for stmt in method.body.statements:
        ABSMC.writeFile(stmt.gen())
