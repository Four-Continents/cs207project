import importlib
import inspect
import functools

from .symtab import *

ATTRIB_COMPONENT = '_pype_component'

def component(func):
    'Marks a functions as compatible for exposing as a component in PyPE.'
    def ext_func(*args, **kwargs):
        return func(*args, **kwargs)
    ext_func._attributes = {ATTRIB_COMPONENT: True}
    return ext_func

def is_component(func):
    'Checks whether the @component decorator was applied to a function.'
    try:
        return func._attributes[ATTRIB_COMPONENT]
    except AttributeError:
        return False

class LibraryImporter(object):
  def __init__(self, modname=None, package=None):
    self.package = package
    self.mod = None
    if modname is not None:
      self.import_module(modname)

  def import_module(self, modname):
    if self.package is None:
        self.mod = importlib.import_module(modname)
    else:
        # dot makes it a relative instead of absolute import
        self.mod = importlib.import_module('.'+modname, package=self.package)

  def add_symbols(self, symtab):
    assert self.mod is not None, 'No module specified or loaded'
    for (name,obj) in inspect.getmembers(self.mod):
      # print('   '+name)
      if inspect.isroutine(obj) and is_component(obj):
        # DONE: add a symbol to symtab
        #       it should be named name
        #       its type should be a libraryfunction SymbolType
        #       its ref should be the object itself (obj)
        # print('++ function: ' + name)
        symtab.addsym( Symbol(name, SymbolType.libraryfunction, obj) )
      elif inspect.isclass(obj):
        for (methodname,method) in inspect.getmembers(obj):
           # DONE:
           #   check if method was decorated like before
           #   add a symbol like before, but with type librarymethod
           #   (the ref should be the method, not obj)
           if is_component(method):
              # print('++ method: ' + methodname)
              symtab.addsym( Symbol(methodname, SymbolType.librarymethod, method) )

    return symtab
