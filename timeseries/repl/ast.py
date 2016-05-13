class AST_insert():
    def __init__(self, pk, timestamps, values):
        """
        Parameters
        ----------
        pk: AST_ID
        timestamps: AST_numlist
        values: AST_numlist
        """
        self.pk = pk
        self.timestamps = timestamps
        self.values = values

    def __str__(self):
        return '{%r %r %r}' % (self.pk, self.timestamps, self.values)

class AST_numlist():
    def __init__(self, elements):
        """
        Parameters
        ----------
        elements: list of int or float
        """
        self.elements = elements

    def __len__(self):
        """
        returns the length of elements
        """
        return len(self.elements)


class AST_ID():
    def __init__(self, id):
        """
        Parameters
        ----------
        id: str
        """
        self.id = id


class AST_select():
    def __init__(self, pk=None, selector=None, orderby=None, ascending=True, limit=None):
        """
        Parameters
        ----------
        pk: AST_ID node
        selector: AST_proc node or list of AST_ID nodes
            optional argument
        orderby: AST_ID
            optional argument
            field name to sort results by
        ascending: bool
            optional argument
            ignored when orderby is None
            descending if False; default is True
        limit: int
            optional argument
            limits number of rows returned
        """
        self.pk = pk
        self.selector = selector or []
        self.orderby = orderby
        self.ascending = ascending
        self.limit = limit


class AST_proc():
    def __init__(self, id, targets):
        """
        for stored procedure calls

        Parameters
        ----------
        id: AST_ID
            proc name from procs directory
        targets: list of AST_ID
            names of fields that the results of the proc will be assigned to
        """
        self.id = id
        self.targets = targets


class AST_simsearch():
    def __init__(self, k, pk):
        """
        for similarity search

        Parameters
        ----------
        k: int
            k_nearest, number of closest timeseries
        pk: AST_ID
            timeseries to compare against
        """
        self.k = k
        self.pk = pk
