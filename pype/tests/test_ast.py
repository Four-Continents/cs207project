import pype
import pytest
import os

# to run, type in command line: ```PYTHONPATH=. py.test -vv tests/test_lexer.py```

samples_dir = os.path.join(os.path.dirname(__file__), '../samples')


def read_sample(filename):
    return open(os.path.join(samples_dir, filename)).read()


def pprint_str(ast, indent=''):
    '''Recursively prints a formatted string representation of the AST.'''
    result = ''
    result += indent+ast.__class__.__name__+'\n'
    for child in ast.children:
        result += pprint_str(child, indent+'  ')

    return result


def test_example0():
    lexer = pype.lexer.new_lexer()

    data = read_sample('example0.ppl')

    ast = pype.parser.parser.parse(data, lexer=lexer)

    ast_strs = pprint_str(ast).strip().split('\n')

    parsed_data = read_sample('example0.ast').strip().split('\n')

    print('\n'.join(ast_strs))
    for i, line in enumerate(parsed_data):
        assert line == ast_strs[i]

    assert len(parsed_data) == len(ast_strs)


def test_example1():
    lexer = pype.lexer.new_lexer()

    data = read_sample('example1.ppl')

    ast = pype.parser.parser.parse(data, lexer=lexer)

    ast_strs = pprint_str(ast).strip().split('\n')

    parsed_data = read_sample('example1.ast').strip().split('\n')

    # Semantic analysis
    # Check to see if something in a component is assigned twice
    ast.walk( CheckSingleAssignment() )
    # Translation
    syms = ast.walk( SymbolTableVisitor() )
    return syms, ast

    print('\n'.join(ast_strs))
    for i, line in enumerate(parsed_data):
        assert line == ast_strs[i]

    assert len(parsed_data) == len(ast_strs)