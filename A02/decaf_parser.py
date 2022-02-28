# David Park
# dappark
# 109582425

import decaf_lexer
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

id = { }

methods = { }

def p_program(p):
	"""program : class_decl
			   | """

def p_class_decl(p):
    """class_decl : CLASS ID            LBRACE class_body_decl RBRACE
                  | CLASS ID EXTENDS ID LBRACE class_body_decl RBRACE
				  | CLASS ID            LBRACE class_body_decl RBRACE class_decl
				  | CLASS ID EXTENDS ID LBRACE class_body_decl RBRACE class_decl"""
                  
def p_class_body_decl(p):
	"""class_body_decl : field_decl
					   | method_decl
					   | constructor_decl
					   | field_decl       class_body_decl
					   | method_decl      class_body_decl
					   | constructor_decl class_body_decl"""

def p_field_decl(p):
	"field_decl : modifier var_decl"

def p_method_decl(p):
	"""method_decl : modifier type ID LPAREN formals RPAREN block
				   | modifier type ID LPAREN         RPAREN block
				   | modifier VOID ID LPAREN formals RPAREN block
				   | modifier VOID ID LPAREN         RPAREN block"""

def p_constructor_decl(p):
	"""constructor_decl : modifier ID LPAREN formals RPAREN block
						| modifier ID LPAREN         RPAREN block"""

def p_modifier(p):
	"""modifier : PUBLIC STATIC
				| PRIVATE STATIC
				| PUBLIC
				| PRIVATE
				| STATIC
				| """

def p_var_decl(p):
	"var_decl : type variables SEMICOLON"

def p_type(p):
	"""type : INT
			| FLOAT
			| BOOLEAN
			| ID"""	
			
def p_variables(p):
	"""variables : variable
				 | variable COMMA variables"""

def p_variable(p):
	"variable : ID"

def p_formals(p):
	"""formals : formal_param
			   | formal_param COMMA formals"""

def p_formal_param(p):
	"formal_param : type variable"
	
def p_block(p):
	"block : LBRACE stmts RBRACE"


def p_stmts(p):
	"""stmts : stmt
			 | stmt stmts"""

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
	"""arguments : expr
				 | expr COMMA arguments 
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
	# elif p[2] == "||" : p[0] = p[1] or p[3]
	# elif p[2] == "==" : p[0] = p[1] == p[3]
	# elif p[2] == "!=" : p[0] = p[1] != p[3]
	# elif p[2] == "<" : p[0] = p[1] < p[3]
	# elif p[2] == ">" : p[0] = p[1] > p[3]
	# elif p[2] == "<=" : p[0] = p[1] <= p[3]
	# elif p[2] == ">=" : p[0] = p[1] >= p[3]

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

def p_arith_op(p):
	"""arith_op : PLUS
				| MINUS
				| TIMES
				| DIVIDE"""

def p_bool_op(p):
	"""bool_op : AND
			   | OR
			   | EQ
			   | NE
			   | LT
			   | GT
			   | LE
			   | GE"""

def p_error(p):
	print("Syntax error in input: %s [%d,%d]" % (repr(p.value), p.lineno, p.lexpos))
	import sys
	sys.exit()

parser = yacc.yacc()
