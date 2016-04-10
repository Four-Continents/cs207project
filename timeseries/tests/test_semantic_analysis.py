from pype import semantic_analysis as sa
import pype
import pytest
import os

# to run, type in command line: ```PYTHONPATH=. py.test -vv tests/test_semantic_analysis.py```

samples_dir = os.path.join(os.path.dirname(__file__), '../samples')


def read_sample(filename):
    return open(os.path.join(samples_dir, filename)).read()


def test_PrettyPrint():
    """
    walk implements recursive depth first pre-order traversal once
    leaves it up to visitor what it does by calling .visit()
    """
    printed = []

    # stub out printing so we can capture print output
    def stub_print(*out):
        printed.extend(out)
    try:
        # override print in semantic_analysis module context
        sa.print = stub_print

        pp = sa.PrettyPrint()

        data = read_sample('example1.ppl')

        # get a lexer
        lexer = pype.lexer.new_lexer()

        ast = pype.parser.parser.parse(data, lexer=lexer)

        return_values = ast.walk(pp)

        # ASTVisitor has None, not overridden by PrettyPrint()
        assert return_values is None

        # make sure this matches example1.ast in exact order
        expected = ['ASTProgram', 'ASTImport', 'ASTComponent', 'ASTID', 'ASTAssignmentExpr', 'ASTID', 'ASTEvalExpr',
                    'ASTID', 'ASTEvalExpr', 'ASTID', 'ASTID', 'ASTID', 'ASTID', 'ASTAssignmentExpr', 'ASTID',
                    'ASTEvalExpr', 'ASTID', 'ASTID', 'ASTAssignmentExpr', 'ASTID', 'ASTEvalExpr', 'ASTID', 'ASTID',
                    'ASTInputExpr', 'ASTID', 'ASTOutputExpr', 'ASTID']

        assert printed == expected

    # restore sa to behave with builtin print
    finally:
        del sa.__dict__['print']


def test_CheckSingleAssignment_same_var():
    lexer = pype.lexer.new_lexer()

    data = read_sample('doubleassignment.ppl')

    ast = pype.parser.parser.parse(data, lexer=lexer)

    check = sa.CheckSingleAssignment()

    try:
        ast.walk(check)
        assert False, 'expected error from double assignment'
    except:
        pass

def test_CheckSingleAssignment_dual_comp():
    lexer = pype.lexer.new_lexer()

    data = read_sample('doubleassignment_ok.ppl')

    ast = pype.parser.parser.parse(data, lexer=lexer)

    check = sa.CheckSingleAssignment()

    try:
        ast.walk(check)
    except:
        assert False