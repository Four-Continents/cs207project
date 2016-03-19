import pype
import pytest

# to run, type in command line: ```PYTHONPATH=. py.test -vv tests/test_lexer.py```


def pprint_str(ast, indent=''):
    '''Recursively prints a formatted string representation of the AST.'''
    result = ''
    result += indent+ast.__class__.__name__+'\n'
    for child in ast.children:
        result += pprint_str(child, indent+'  ')

    return result


def test_example0():
    lexer = pype.lexer.new_lexer()

    data = open('samples/example0.ppl').read()

    ast = pype.parser.parser.parse(data, lexer=lexer)

    ast_strs = pprint_str(ast).strip().split('\n')

    parsed_data = open('samples/example0.ast').read().strip().split('\n')

    print('\n'.join(ast_strs))
    for i, line in enumerate(parsed_data):
        assert line == ast_strs[i]

    assert len(parsed_data) == len(ast_strs)


def test_example1():
    lexer = pype.lexer.new_lexer()

    data = open('samples/example1.ppl').read()

    ast = pype.parser.parser.parse(data, lexer=lexer)

    ast_strs = pprint_str(ast).strip().split('\n')

    parsed_data = open('samples/example1.ast').read().strip().split('\n')

    print('\n'.join(ast_strs))
    for i, line in enumerate(parsed_data):
        assert line == ast_strs[i]

    assert len(parsed_data) == len(ast_strs)