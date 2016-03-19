import ply.lex

# LEXING phase: emits pairs of types and contents
# TODO test these regexes, write more tests for error cases

reserved = { # pattern : token-name
  'input' : 'INPUT',
  'output' : 'OUTPUT',
  'import' : 'IMPORT',
}
# 'tokens' is a special word in ply's lexers.
# TODO implement production rules for each token, Many of these will be simple literals (for instance, LPAREN, RPAREN, etc),
tokens = [ 
  'LPAREN','RPAREN', # Individual parentheses
  'LBRACE','RBRACE', # Individual braces
  'OP_ADD','OP_SUB','OP_MUL','OP_DIV', # the four basic arithmetic symbols
  'STRING', # Anything enclosed by double quotes
  'ASSIGN', # The two characters :=
  'NUMBER', # An arbitrary number of digits
  'ID', # a sequence of letters, numbers, and underscores. Must not start with a number.
] + list(reserved.values())

# TODO You'll need a list of token specifications here.
# TODO Here's an example:
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_OP_ADD = r'\+'
t_OP_SUB = r'-'
t_OP_MUL = r'\*'
t_OP_DIV = r'/'
t_STRING = r'"[^"]*"'
t_ASSIGN = r':='
t_NUMBER = r'[0-9]+'

# TODO Ignore whitespace.
t_ignore = '\t '


# TODO Write one rule for IDs and reserved keywords. Section 4.3 has an example.
# used to lex/match identifiers and reserved words
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, t.type)    # Check for reserved words
    return t


# TODO Ignore comments. Comments in PyPE are just like in Python. Section 4.5.
t_ignore_COMMENT = r'\#.*'


# TODO Write a rule for newlines that track line numbers. Section 4.6.
# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(input, token):
    last_cr = input.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (token.lexpos - last_cr)
    return column


# TODO Write an error-handling routine. It should print both line and column numbers.
# Error handling rule
def t_error(t):
    print("Error at line #: %r, column #: %r" % (t.lexer.lineno, find_column(t.lexer.lexdata, t)))

# This actually builds the lexer.
lexer = ply.lex.lex(
  #debug=True
  )

def new_lexer():
    return ply.lex.lex()
