from pype import symtab as st
import pype
import pytest
import os

# to run, type in command line: ```PYTHONPATH=. py.test -vv tests/test_symtab.py```

samples_dir = os.path.join(os.path.dirname(__file__), '../samples')

def test_addsym():
    table = st.SymbolTable()

    # try local context
    table.addsym(st.Symbol('foo', st.SymbolType.var, None), 'standardize')

    assert table.lookupsym('foo', 'standardize') == st.Symbol('foo', st.SymbolType.var, None)

    # try global context, make sure it's the right thing
    table.addsym(st.Symbol('foo', st.SymbolType.input, None))

    assert table.lookupsym('foo', 'global') == st.Symbol('foo', st.SymbolType.input, None)

    # check to see if not in local, that it falls back to global scope
    table.addsym(st.Symbol('bar', st.SymbolType.librarymethod, None))

    assert table.lookupsym('bar', 'standardize') == st.Symbol('bar', st.SymbolType.librarymethod, None)

    # now try defining in local and looking up in local updates appropriately
    table.addsym(st.Symbol('bar', st.SymbolType.component, None), 'standardize')

    assert table.lookupsym('bar', 'standardize') == st.Symbol('bar', st.SymbolType.component, None)