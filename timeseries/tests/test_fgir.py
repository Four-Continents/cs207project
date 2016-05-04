import pype
import pytest
import os
from pype.semantic_analysis import CheckSingleAssignment, CheckSingleIOExpression, CheckUndefinedVariables
from pype.translate import SymbolTableVisitor, LoweringVisitor
from pype.optimize import *
import timeseries

# to run, type in command line: ```PYTHONPATH=. py.test -vv tests/test_fgir.py```

samples_dir = os.path.join(os.path.dirname(__file__), '../samples')


def read_sample(filename):
    return open(os.path.join(samples_dir, filename)).read()


def generate_ir(fName):
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

    return ir


def optimize_file(fName):
    ir = generate_ir(fName)

    for c in ir:
        print(ir[c].dotfile())

    ir.flowgraph_pass( AssignmentEllision() )

    for c in ir:
        print(ir[c].dotfile())
    ir.flowgraph_pass( DeadCodeElimination() )

    for c in ir:
        print(ir[c].dotfile())


def test_optimize_example0():
    optimize_file('example0.ppl')


def test_optimize_example1():
    optimize_file('example1.ppl')

# def test_optimize_example1():
#     optimize_file('six.ppl')


def topsort_validate(componentir, res):
    # Test whether top sorted list is correctly formed
    # There are multiple possible valid lists (which are not deterministically generated)
    # node ids are not globally unique, only unique within a component

    seen = {}

    for nodeid in res:
        if nodeid not in componentir.nodes:
            continue
        for inp_nid in componentir.nodes[nodeid].inputs:
            assert inp_nid in seen

        seen[nodeid] = True


def generate_topsort(fName):
    ir = generate_ir(fName)

    # Topologically sort each component and validate it is a valid ordering
    for c in ir:
        # print(ir[c].dotfile())
        ts = ir[c].topological_sort()
        # print(ts)
        topsort_validate(ir[c], ts)


def test_topsort_example0():
    generate_topsort('example0.ppl')


def test_topsort_example1():
    generate_topsort('example1.ppl')

def test_topsort_six():
    generate_topsort('six.ppl')