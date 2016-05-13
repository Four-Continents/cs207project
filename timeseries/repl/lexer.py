import ply.lex


reserved = { # pattern : token-name
             'insert': 'INSERT',
             'into': 'INTO',
             'select': 'SELECT',
             'from': 'FROM',
             'order': 'ORDER',
             'by': 'BY',
             'asc': 'ASC',
             'desc': 'DESC',
             'limit': 'LIMIT',
             'as': 'AS',
             'like': 'LIKE',
             'simsearch': 'SIMSEARCH',
             }

# 'tokens' is a special word in ply's lexers.
tokens = [
             'LBRACK','RBRACK', # Individual parentheses
             'NUMBER', # An arbitrary number of digits
             'ID', # a sequence of letters, numbers, and underscores. Must not start with a number.
             'AT', # for timeseries timestamps associated with values
             'COMMA', # to separate items in lists
             'LPAREN',
             'RPAREN',
         ] + list(reserved.values())

t_LBRACK = r'\['
t_RBRACK = r'\]'
# floats and ints
t_NUMBER = r'[0-9]+(?:\.[0-9]+)?'
t_AT = r'@'
t_COMMA = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'

t_ignore = '\t '


# used to lex/match identifiers and reserved words
def t_ID(t):
    r'[-a-zA-Z_][-a-zA-Z_0-9]*'
    # lower to make reserved words case insensitive
    t.type = reserved.get(t.value.lower(), t.type)    # Check for reserved words
    return t


# Error handling rule
def t_error(t):
    print("Error: %r" % t)


def new_lexer():
    return ply.lex.lex()
