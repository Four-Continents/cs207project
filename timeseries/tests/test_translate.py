from pype import translate as tr
from pype import lib_import as li
from pype import symtab as st
import pype
import pytest
import os
import timeseries

# to run, type in command line: ```PYTHONPATH=. py.test -vv tests/test_translate.py```

samples_dir = os.path.join(os.path.dirname(__file__), '../samples')


def read_sample(filename):
    return open(os.path.join(samples_dir, filename)).read()


def test_SymbolTableVisitor():
    """
    { standardize
    (input (TimeSeries t))
    (:= mu (mean t))
    (:= sig (std t))
    (:= new_t (/ (- t mu) sig))
    (output new_t)
    }

    should have two scopes: global and standardize
    should have 4 symbols: new_t, sig, mu, standardize
    """
    # parse the 0 ppl file
    data = read_sample('example0.ppl')

    lexer = pype.lexer.new_lexer()

    ast = pype.parser.parser.parse(data, lexer=lexer)

    # walk with SymbolTableVisitor
    sv = tr.SymbolTableVisitor(import_package='timeseries')

    # walk calls visit
    ast.walk(sv)

    # sv.symbol_table.pprint()

    assert sv.symbol_table.lookupsym('new_t', 'standardize') == st.Symbol('new_t', st.SymbolType.var, ref=None)
    assert sv.symbol_table.lookupsym('mu', 'standardize') == st.Symbol('mu', st.SymbolType.var, ref=None)
    assert sv.symbol_table.lookupsym('sig', 'standardize') == st.Symbol('sig', st.SymbolType.var, ref=None)
    assert sv.symbol_table.lookupsym('t', 'standardize') == st.Symbol('t', st.SymbolType.input, ref=None)

    assert sv.symbol_table.lookupsym('standardize') == st.Symbol('standardize', st.SymbolType.component, ref=None)

    # these have addresses that will change, so I am checking the attribute separately
    mean = sv.symbol_table.lookupsym('mean')
    assert mean.name == 'mean'
    assert mean.type == st.SymbolType.librarymethod

    mean = sv.symbol_table.lookupsym('std')
    assert mean.name == 'std'
    assert mean.type == st.SymbolType.librarymethod

