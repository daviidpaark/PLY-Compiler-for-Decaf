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


tokens = reserved + (
    "NUMBER",
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
)

t_ignore = " \t"

t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACE = r"{"
t_RBRACE = r"}"
t_SEMICOLON = r";"


def t_NEWLINE(t):
    r"\n+"
    t.lexer.lineno += t.value.count("\n")


def t_COMMENTBLOCK(t):
    r"\/\*(.|\n)*\*\/"
    t.lexer.lineno += t.value.count("\n")


def t_COMMENT(t):
    r"\/\/.*"
    t.lexer.lineno += t.value.count("\n")


t_INT_CONST = r"-?+\d+"
t_FLOAT_CONST = r"-?\d+\.\d+"
t_STRING_CONST = r"\".*\""

lexer = lex()

if __name__ == "__main__":
    lex.runmain(lexer)
