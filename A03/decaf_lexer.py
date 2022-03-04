# David Park
# dappark
# 109582425

import sys
import ply.lex as lex

reserved = {
    "boolean": "BOOLEAN",
    "break": "BREAK",
    "continue": "CONTINUE",
    "class": "CLASS",
    "else": "ELSE",
    "extends": "EXTENDS",
    "false": "FALSE",
    "float": "FLOAT",
    "for": "FOR",
    "if": "IF",
    "int": "INT",
    "new": "NEW",
    "null": "NULL",
    "private": "PRIVATE",
    "public": "PUBLIC",
    "return": "RETURN",
    "static": "STATIC",
    "super": "SUPER",
    "this": "THIS",
    "true": "TRUE",
    "void": "VOID",
    "while": "WHILE",
}


tokens = (
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "LPAREN",
    "RPAREN",
    "LBRACE",
    "RBRACE",
    "SEMICOLON",
    "INT_CONST",
    "FLOAT_CONST",
    "STRING_CONST",
    "ID",
    "DOT",
    "COMMA",
    "EQUALS",
    "AND",
    "OR",
    "EQ",
    "NE",
    "LT",
    "GT",
    "LE",
    "GE",
    "NOT",
    "INCREMENT",
    "DECREMENT",
) + tuple(reserved.values())

t_ignore = " \t"

t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_SEMICOLON = r";"
t_DOT = r"\."
t_COMMA = r","
t_EQUALS = r"="

t_AND = r"&&"
t_OR = r"\|\|"
t_EQ = r"=="
t_NE = r"!="
t_LT = r"<"
t_GT = r">"
t_LE = r"<="
t_GE = r">="
t_NOT = r"!"

t_INCREMENT = r"\+\+"
t_DECREMENT = r"--"


def t_newline(t):
    r"\n+"
    t.lexer.lineno += t.value.count("\n")


def t_COMMENTBLOCK(t):
    r"\/\*(.|\n)*?\*\/"
    t.lexer.lineno += t.value.count("\n")


def t_COMMENT(t):
    r"\/\/.*"
    t.lexer.lineno += t.value.count("\n")


def t_FLOAT_CONST(t):
    r"\d+\.\d+"
    t.value = float(t.value)
    return t


def t_INT_CONST(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_STRING_CONST(t):
    r"\".*\""
    return t


def t_ID(t):
    r"[a-zA-Z][a-zA-Z_0-9]*"
    t.type = reserved.get(t.value, "ID")
    return t


def t_error(t):
    print("Illegal character: %s [%d,%d]" % (repr(t.value[0]), t.lineno, t.lexpos))
    sys.exit()


lexer = lex.lex()

if __name__ == "__main__":
    lex.runmain(lexer)
