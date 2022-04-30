# David Park
# dappark
# 109582425

import sys
import ply.lex as lex
import ply.yacc as yacc


def just_scan():
    fn = sys.argv[1] if len(sys.argv) > 1 else ""
    if fn == "":
        print("Missing file name for source program.")
        print("USAGE: python3 decaf_compiler.py <decaf_source_file_name>")
        sys.exit()
    import decaf_lexer

    lexer = lex.lex(module=decaf_lexer, debug=0)

    fh = open(fn, "r")
    source = fh.read()
    lexer.input(source)
    next_token = lexer.token()
    while next_token != None:
        print(next_token)
        next_token = lexer.token()


# end def just_scan()


def main():
    fn = sys.argv[1] if len(sys.argv) > 1 else ""
    if fn == "":
        print("Missing file name for source program.")
        print("USAGE: python3 decaf_compiler.py <decaf_source_file_name>")
        sys.exit()
    import decaf_lexer
    import decaf_parser

    lexer = lex.lex(module=decaf_lexer, debug=0)
    parser = yacc.yacc(module=decaf_parser, debug=0)

    fh = open(fn, "r")
    source = fh.read()
    fh.close()
    ast = parser.parse(source, lexer=lexer, debug=0)
    import decaf_typecheck

    if decaf_typecheck.typeCheck(ast):
        # ast.printAST()
        import decaf_codegen
        decaf_codegen.codeGen(ast, sys.argv[1][0 : sys.argv[1].index(".decaf")])


if __name__ == "__main__":
    # just_scan()
    main()
