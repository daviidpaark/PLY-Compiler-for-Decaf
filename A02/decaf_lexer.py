# David Park
# dappark
# 109582425

from ply.lex import lex

reserved = (
    "boolean",
    "break",
    "continue",
    "class",
    "do",
    "else",
    "extends",
    "false",
    "float",
    "for",
    "if",
    "int",
    "new",
    "null",
    "private",
    "public",
    "return",
    "static",
    "super",
    "this",
    "true",
    "void",
    "while",
)

t_ignore = " \t"


def t_NEWLINE(t):
    r"\n+"
    t.lexer.lineno += t.value.count("\n")
