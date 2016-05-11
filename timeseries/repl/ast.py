class AST_insert():
    """
    create class for every node in the language, just abstract syntax tree, can ignore "into"

    identifier primary key
    2 number lists
    """
    def __init__(self, pk, timestamps, values):
        self.pk = pk
        self.timestamps = timestamps
        self.values = values

    def __str__(self):
        return '{%r %r %r}' % (self.pk, self.timestamps, self.values)

class AST_numlist():
    """
    """
    def __init__(self, elements):
        self.elements = elements


class AST_ID():
    """
    """
    def __init__(self, id):
        self.id = id


class AST_select():
    """
    """
    def __init__(self, pk, exprs=None):
        self.pk = pk
        self.exprs = exprs or []