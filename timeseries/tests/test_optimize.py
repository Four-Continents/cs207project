import pype
import pytest
import os
import timeseries
from pype.semantic_analysis import CheckSingleAssignment, CheckSingleIOExpression, CheckUndefinedVariables
from pype.translate import SymbolTableVisitor, LoweringVisitor
from pype.optimize import *

# to run, type in command line: ```PYTHONPATH=. py.test -vv tests/test_optimize.py```

samples_dir = os.path.join(os.path.dirname(__file__), '../samples')


def read_sample(filename):
    return open(os.path.join(samples_dir, filename)).read()


# Writing an inliner is a little tricky, and we have other things for you to write. So instead, we'd like you to prove
# that the version we gave you in optimize.py does what we say it does. In other words, we'd like you to write test
# cases (with 100% coverage) for the visit() method of InlineComponents.
#
# There's two main invariants to check: first, that the function behavior isn't broken (all the inputs and outputs
# are still there, etc.), and second, that there are no component nodes in the graph anymore. If there are, you know
# that the inliner didn't complete its task.

def run_pipeline(fName):
    lexer = pype.lexer.new_lexer()

    data = read_sample(fName)

    ast = pype.parser.parser.parse(data, lexer=lexer)

    # Semantic analysis
    ast.walk( CheckSingleAssignment() )
    ast.walk( CheckSingleIOExpression() )
    syms = ast.walk( SymbolTableVisitor(import_package='timeseries') )
    ast.walk( CheckUndefinedVariables(syms) )

    # Translation
    ir = ast.mod_walk( LoweringVisitor(syms) )

    # for c in ir:
    #     print(ir[c].dotfile())

    # Optimization
    ir.flowgraph_pass( AssignmentEllision() )

    # for c in ir:
    #     print(ir[c].dotfile())
    ir.flowgraph_pass( DeadCodeElimination() )

    # for c in ir:
    #     print(ir[c].dotfile())
    ir.topological_flowgraph_pass( InlineComponents() )

    return ir

def test_visit():
    """
    tests the visit() method of InlineComponents
    """
    ir = run_pipeline('inlining.ppl')
    for c in ir:
        print(ir[c].dotfile())

    assert False