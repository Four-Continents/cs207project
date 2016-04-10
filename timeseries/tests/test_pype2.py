import pytest
import pype
from pype import *

# to run, type in command line: ```PYTHONPATH=. py.test -vv tests/test_pype2.py```

# samples_dir = os.path.join(os.path.dirname(__file__), '../samples')


# def read_sample(filename):
#     return open(os.path.join(samples_dir, filename)).read()

def test_samples():

    # lexer = pype.lexer.new_lexer()

    # data = read_sample('example1.ppl')

    # ast = pype.parser.parser.parse(data, lexer=lexer)

    #  # Semantic analysis
    # # Check to see if something in a component is assigned twice
    # ast.walk( CheckSingleAssignment() )
    # # Translation
    # syms = ast.walk( SymbolTableVisitor() )
    # return syms, ast

     # two (more complicated) functions
    

    Pipeline(source='tests/samples/example0.ppl')
    Pipeline(source='tests/samples/example1.ppl')


   