class LazyOperation(object):
    """
    A class which is a "thunk" to represent the result from a computation to be
    lazily evaluated at a later time.
    """

    def __init__(self, function, *args, **kwargs):
        self.function = function
        self.args = list(args)
        self.kwargs = kwargs

    def getFinalEval(self, curEval):
        while isinstance(curEval, LazyOperation):
            curEval = curEval.eval()
        return curEval

    def eval(self):
        for i in range(len(self.args)):
            self.args[i] = self.getFinalEval(self.args[i])

        for k, v in self.kwargs.iteritems():
            self.kwargs[k] = self.getFinalEval(v)

        return self.function(*self.args, **self.kwargs)  # http://stackoverflow.com/questions/3394835/args-and-kwargs

def lazy(func):
    def inner(*args, **kwargs):
        ins = LazyOperation(func, *args, **kwargs)
        return ins
    return inner

@lazy
def lazy_add(a, b):
    return a+b

lazy_ins = lazy_add(1, lazy_add(3, 17))
print (isinstance( lazy_ins, LazyOperation ) == True)
print lazy_ins.eval()
