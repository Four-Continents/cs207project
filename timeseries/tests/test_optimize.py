import os
from pytest import raises
import pype
from pype.lexer import lexer
from pype.semantic_analysis import CheckSingleAssignment, CheckSingleIOExpression, CheckUndefinedVariables
from pype.translate import SymbolTableVisitor, LoweringVisitor
from pype.optimize import *
from pype import fgir
import timeseries

# to run, type in command line: ```PYTHONPATH=. py.test -vv tests/test_optimize.py```

samples_dir = os.path.join(os.path.dirname(__file__), '../samples')


def read_sample(filename):
    return open(os.path.join(samples_dir, filename)).read()


def run_pipeline(fName):
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

    ir.topological_flowgraph_pass( InlineComponents() )

    return ir


def test_visit():
    """
    tests the visit() method of InlineComponents

    Prove that the version we gave you in optimize.py does what we say it does. In other words, we'd like you to write
    test cases (with 100% coverage) for the visit() method of InlineComponents.

    There's two main invariants to check: first, that the function behavior isn't broken (all the inputs and outputs
    are still there, etc.), and second, that there are no component nodes in the graph anymore. If there are, you know
    that the inliner didn't complete its task.
    """
    ir = run_pipeline('inlining.ppl')
    # for c in ir:
    #     print(ir[c].dotfile())

    # map component to input
    input_nodes = {}
    output_nodes = {}
    components = []
    for c in ir:
        # print(c)
        fg = ir[c]
        if input_nodes.get(fg.name) is not None:
            assert False
        else:
            input_nodes[fg.name] = []
            output_nodes[fg.name] = []
        for nodeid, node in fg.nodes.items():
            if node.type == fgir.FGNodeType.input:
                input_nodes[fg.name].append(nodeid)
            elif node.type == fgir.FGNodeType.output:
                output_nodes[fg.name].append(nodeid)
            # iterate through each node in ir[c] and check the type is not component
            elif node.type == fgir.FGNodeType.component:
                components.append((fg.name, nodeid, node))

    for c in ir:
        fg = ir[c]

        fgin = input_nodes[fg.name]
        assert sorted(fgin) == sorted(fg.inputs)

        fgout = output_nodes[fg.name]
        assert sorted(fgout) == sorted(fg.outputs)

    assert len(components) == 0

