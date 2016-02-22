class LazyOperation(object):
    """
    A class which is a "thunk" to represent the result from a computation to be
    lazily evaluated at a later time.
    """

    def __init__(self, function, *args, **kwargs):
        self.function = function
        self.args = args
        self.kwargs = kwargs


def lazy(func):
    def inner(*args, **kwargs):
        ins = LazyOperation(func, *args, **kwargs)
        return ins
    return inner


@lazy
def lazy_add(a, b):
    return a+b

print (isinstance( lazy_add(1,2), LazyOperation ) == True)
