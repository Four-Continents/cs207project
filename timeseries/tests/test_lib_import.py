from pype import lib_import as li
from pype import symtab as st
import pype
import pytest
import os
from samples import lib_import_testmodule

# to run, type in command line: ```PYTHONPATH=. py.test -vv tests/test_lib_import.py```


def test_LibraryImporter():
    table = st.SymbolTable()

    libimporter = li.LibraryImporter()

    libimporter.import_module('samples.lib_import_testmodule')

    libimporter.add_symbols(table)

    s = table.lookupsym('external_function')

    assert s == st.Symbol('external_function', st.SymbolType.libraryfunction, lib_import_testmodule.external_function)

    # check to make sure not decorated function returns None
    ns = table.lookupsym('not_decorated_function')

    assert ns is None
