import ply.yacc
from .lexer import tokens, reserved
from .ast import *


def p_insert_command(p):
    r'''command : INSERT bracketed_number_list AT bracketed_number_list INTO ID'''
    p[0] = AST_insert(p[6], p[4], p[2])


def p_select_command(p):
    r'''command : SELECT FROM ID
                | SELECT expr_list FROM ID'''
    if len(p) == 4:
        p[0] = AST_select(p[3])
    elif len(p) == 5:
        p[0] = AST_select(p[4], exprs=p[2])
    else:
        raise SyntaxError


def p_bracketed_number_list(p):
    r'''bracketed_number_list : LBRACK number_list RBRACK'''
    p[0] = p[2]


# TODO convert these to ints?
def p_number_list(p):
    r'''number_list : number_list COMMA NUMBER
                    | NUMBER'''
    if len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = [p[1]]


def p_expr_list(p):
    r'''expr_list : expr_list COMMA ID
                    | ID'''
    # left recursive on expr_list, or case just with ID
    if len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = [p[1]]


def p_error(p):
    """
    error handling function that prints out line number and column numbers of error location
    """
    if p is None:
        print('Unexpected, EOF!')
    else:
        # p is a token
        print("Parse Error: %r" % p)


start = 'command'


def new_parser():
    return ply.yacc.yacc() # To get more information, add debug=True
