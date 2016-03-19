import pype
import pytest

# to run, type in command line: ```PYTHONPATH=. py.test -vv tests/test_lexer.py```


def test_example0():
    lexer = pype.lexer.new_lexer()

    data = open('samples/example0.ppl').read()

    lexer.input(data)

    tok_strs = []
    while True:
        tok = lexer.token()
        if tok is None:
            break
        tok_strs.append(str(tok))

    lexed_data = open('samples/example0.tokens').read().strip()

    for i, line in enumerate(lexed_data.split('\n')):
        assert line == tok_strs[i]


def test_example1():
    lexer = pype.lexer.new_lexer()

    data = open('samples/example1.ppl').read()

    lexer.input(data)

    tok_strs = []
    while True:
        tok = lexer.token()
        if tok is None:
            break
        tok_strs.append(str(tok))

    lexed_data = open('samples/example1.tokens').read().strip()

    for i, line in enumerate(lexed_data.split('\n')):
        assert line == tok_strs[i]