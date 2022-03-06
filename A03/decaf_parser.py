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

block = 0
scope = {}

def p_program(p):
    """program : class_decl
               | """

def p_class_decl(p):
    """class_decl : CLASS ID superclass LBRACE new_block class_body_decl exit_block RBRACE
                  | CLASS ID superclass LBRACE new_block class_body_decl exit_block RBRACE class_decl"""
    
def p_superclass(p):
    """superclass : EXTENDS ID
                  | """

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
    i = 1
    for var in p[2][1]:
        if p[1] == None:
            p[0] = Field(var, i, None, "private", "instance", p[2][0])
        elif "private" in p[1]:
            if "static" in p[1]:
                p[0] = Field(var, i, None)
            else:
                p[0] = Field()
        else:
            if "static" in p[1]:
                p[0] = Field()
            else:
                p[0] = Field()
        i += 1


def p_method_decl(p):
    """method_decl : modifier type ID LPAREN formal_param RPAREN block
                   | modifier VOID ID LPAREN formal_param RPAREN block"""
    p[0] = "method"

def p_constructor_decl(p):
    "constructor_decl : modifier ID LPAREN formal_param RPAREN block"
    p[0] = "constructor"

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
        pass

def p_var_decl(p):
    "var_decl : type variables SEMICOLON"
    p[0] = [Type(p[1]),flatten(p[2])]

def p_type(p):
    """type : INT
            | FLOAT
            | BOOLEAN
            | ID"""
    p[0] = p[1]

def p_variables(p):
    """variables : variable additional_variables
                 | """
    try: 
        p[0] = [p[1], p[3]]
    except:
        p[0] = [p[1]]

def p_additional_variables(p):
    """additional_variables : COMMA variables additional_variables
                            | """

def p_variable(p):
    "variable : ID"
    p[0] = p[1]

def p_formal_param(p):
    """formal_param : param formals
                    | """
                    
def p_formals(p):
    """formals : COMMA param formals
               | """

def p_param(p):
    "param : type variable"

def p_block(p):
    "block : LBRACE new_block stmts exit_block RBRACE"

def p_stmts(p):
    """stmts : stmt additional_stmts
             | """

def p_additional_stmts(p):
    """additional_stmts : stmt additional_stmts
                        | """

def p_stmt(p):
    """stmt : IF LPAREN expr RPAREN stmt
            | IF LPAREN expr RPAREN stmt ELSE stmt
            | WHILE LPAREN expr RPAREN stmt
            | FOR LPAREN stmt_expr SEMICOLON expr SEMICOLON stmt_expr RPAREN stmt
            | FOR LPAREN           SEMICOLON      SEMICOLON           RPAREN stmt
            | RETURN expr SEMICOLON
            | RETURN SEMICOLON
            | stmt_expr SEMICOLON
            | BREAK SEMICOLON
            | CONTINUE SEMICOLON
            | block
            | var_decl
            | SEMICOLON"""

def p_stmt_expr(p):
    """stmt_expr : assign
                 | method_invocation"""

def p_expr(p):
    """expr : primary
            | assign
            | expr_arith_op
            | expr_bool_op
            | expr_unary_op"""

def p_primary(p):
    """primary : literal
               | THIS
               | SUPER
               | LPAREN expr RPAREN
               | NEW ID LPAREN arguments RPAREN
               | lhs
               | method_invocation"""
    if (p[1]) == "this":
        p[0] = This(p.lineno)
    if (p[1]) == "super":
        p[0] = Super(p.lineno)

def p_assign(p):
    """assign : lhs EQUALS expr
              | lhs INCREMENT
              | INCREMENT lhs
              | lhs DECREMENT
              | DECREMENT lhs"""

def p_lhs(p):
    "lhs : field_access"

def p_field_access(p):
    """field_access : primary DOT ID
                    | ID"""

def p_arguments(p):
    """arguments : expr additional_arguments
                 | """

def p_additional_arguments(p):
    """additional_arguments : COMMA expr additional_arguments
                            | """

def p_method_invocation(p):
    "method_invocation : field_access LPAREN arguments RPAREN"

def p_expr_arith_op(p):
    "expr_arith_op : expr arith_op expr"
    # if   p[2] == "+" : p[0] = p[1] + p[3]
    # elif p[2] == "-" : p[0] = p[1] - p[3]
    # elif p[2] == "*" : p[0] = p[1] * p[3]
    # elif p[2] == "/" : p[0] = p[1] / p[3]

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

def p_expr_unary_op(p):
    """expr_unary_op : PLUS expr %prec UPLUS
                     | MINUS expr %prec UMINUS
                     | NOT expr"""
    # if   p[1] == "+" : p[0] = +p[2]
    # elif p[1] == "-" : p[0] = -p[2]
    # elif p[1] == "!" : p[0] = not p[2]


def p_literal(p):
    """literal : INT_CONST
               | FLOAT_CONST
               | STRING_CONST
               | NULL
               | TRUE
               | FALSE"""
    p[0] = p[1]

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

def p_exit_block(p):
    "exit_block : "
    global block
    block -= 1

def p_error(p):
    print("Syntax error in input: %s [%d,%d]" % (repr(p.value), p.lineno, p.lexpos))
    import sys
    sys.exit()

def flatten(outer):
    flat = []
    for element in outer:
        if not isinstance(element, list):
            flat.append(element)
        else:
            flat.extend(flatten(element))
    return flat

parser = yacc.yacc()
