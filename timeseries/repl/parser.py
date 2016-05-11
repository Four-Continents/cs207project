import ply.yacc
from .lexer import tokens, reserved
from .ast import *

# production rules and grammars below

def p_insert_command(p):
    r'''command : INSERT bracketed_number_list AT bracketed_number_list INTO ID'''
    p[0] = AST_insert(p[6], p[4], p[2])


def p_select_from(p):
    r'''command : SELECT FROM ID
                | SELECT selector FROM ID'''
    if len(p) == 4:
        p[0] = AST_select(pk=p[3])
    elif len(p) == 5:
        p[0] = AST_select(pk=p[4], selector=p[2])
    else:
        raise SyntaxError


def p_select_multi(p):
    r'''command : SELECT selector
                | SELECT selector LIMIT NUMBER
                | SELECT selector ORDER BY ID
                | SELECT selector ORDER BY ID order_direction
                | SELECT selector ORDER BY ID LIMIT NUMBER
                | SELECT selector ORDER BY ID order_direction LIMIT NUMBER'''

    if len(p) == 3:
        p[0] = AST_select(selector=p[2])
    elif len(p) == 5:
        p[0] = AST_select(selector=p[2], limit=int(p[4]))
    elif len(p) == 6:
        p[0] = AST_select(selector=p[2], orderby=p[5])
    elif len(p) == 7:
        p[0] = AST_select(selector=p[2], orderby=p[5], ascending=(p[6]=='ASC'))
    elif len(p) == 8:
        p[0] = AST_select(selector=p[2], orderby=p[5], limit=int(p[7]))
    elif len(p) == 9:
        p[0] = AST_select(selector=p[2], orderby=p[5], ascending=(p[6]=='ASC'), limit=int(p[8]))
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

# can only do proc() or field list
# selector will either be a field_list (list of strings) or an AST_proc
def p_selector(p):
    r'''selector : field_list
                 | ID LPAREN RPAREN AS field_list'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = AST_proc(p[1], p[5])


def p_field_list(p):
    r'''field_list : field_list COMMA ID
                    | ID'''
    # left recursive on field_list, or case just with ID
    if len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = [p[1]]


def p_order_direction(p):
    r'''order_direction : ASC
                        | DESC'''
    p[0] = p[1]


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
