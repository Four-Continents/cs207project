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

        for k, v in self.kwargs.items():
            self.kwargs[k] = self.getFinalEval(v)
        # http://stackoverflow.com/questions/3394835/args-and-kwargs
        return self.function(*self.args, **self.kwargs)


def lazy(func):
    def inner(*args, **kwargs):
        ins = LazyOperation(func, *args, **kwargs)
        return ins
    return inner
