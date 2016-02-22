# import timeseries2

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

        return self.function(*self.args, **self.kwargs)  # http://stackoverflow.com/questions/3394835/args-and-kwargs


def lazy(func):
    def inner(*args, **kwargs):
        ins = LazyOperation(func, *args, **kwargs)
        return ins
    return inner

# @lazy
# def lazy_add(a, b):
#     return a+b
#
# lazy_ins = lazy_add(1, lazy_add(3, 17))
# print (isinstance( lazy_ins, LazyOperation ) == True)
# print lazy_ins.eval()

# @lazy
# def check_length(a,b):
#   return len(a)==len(b)
#
# print (dir(timeseries2))
# thunk = check_length(timeseries2.TimeSeries(range(0,4),range(1,5)), timeseries2.TimeSeries(range(1,5),range(2,6)))
# assert thunk.eval()==True
