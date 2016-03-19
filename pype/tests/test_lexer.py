import pype
import pytest
from ply.lex import LexError
import os

# to run, type in command line: ```PYTHONPATH=. py.test -vv tests/test_lexer.py```

samples_dir = os.path.join(os.path.dirname(__file__), '../samples')


def read_sample(filename):
    return open(os.path.join(samples_dir, filename)).read()


def test_regexes():

    expected = ["LexToken(NUMBER,'3',2,5)", "LexToken(OP_ADD,'+',2,7)", "LexToken(NUMBER,'4',2,9)",
                "LexToken(OP_MUL,'*',2,11)",
                "LexToken(NUMBER,'10',2,13)", "LexToken(ID,'abc',2,16)", "LexToken(IMPORT,'import',2,20)",
                "LexToken(OP_ADD,'+',3,33)", "LexToken(OP_SUB,'-',3,35)", "LexToken(NUMBER,'20',3,36)",
                "LexToken(OP_MUL,'*',3,39)", "LexToken(NUMBER,'2',3,40)"]

    lexer = pype.lexer.new_lexer()

    # Test it out
    data = '''
    3 + 4 * 10 abc import
      + -20 *2
    '''

    # Give the lexer some input
    lexer.input(data)

    # Tokenize
    results = []
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        results.append(tok)

    for i in range(len(expected)):
        assert str(results[i]) == expected[i]

    assert len(expected) == len(results)


def test_error():
    lexer = pype.lexer.new_lexer()

    data = '''
    %
    '''

    lexer.input(data)

    try:
        lexer.token()
        assert False
    except LexError:
        pass


def test_example0():
    lexer = pype.lexer.new_lexer()

    data = read_sample('example0.ppl')

    lexer.input(data)

    tok_strs = []
    while True:
        tok = lexer.token()
        if tok is None:
            break
        tok_strs.append(str(tok))

    lexed_data = read_sample('example0.tokens').strip().split('\n')

    for i, line in enumerate(lexed_data):
        assert line == tok_strs[i]

    assert len(lexed_data) == len(tok_strs)


def test_example1():
    lexer = pype.lexer.new_lexer()

    data = read_sample('example1.ppl')

    lexer.input(data)

    tok_strs = []
    while True:
        tok = lexer.token()
        if tok is None:
            break
        tok_strs.append(str(tok))

    lexed_data = read_sample('example1.tokens').strip().split('\n')

    for i, line in enumerate(lexed_data):
        assert line == tok_strs[i]

    assert len(lexed_data) == len(tok_strs)