import ply.yacc
from .lexer import tokens, reserved
from .ast import *


# Here's an example production rule which constructs an AST node
def p_command(p):
    r'''command : insert_command'''
            #   | select_command
            #   | ...
    p[0] = p[1]


def p_insert_command(p):
    r'''insert_command : INSERT bracketed_number_list AT bracketed_number_list INTO ID'''
    p[0] = AST_insert(p[6], p[4], p[2])


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


start = 'command'

def new_parser():
    return ply.yacc.yacc() # To get more information, add debug=True
