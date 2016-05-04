import timeseries as ts

def f():
    return 1

l = ts.LazyOperation(f)
print(isinstance("abc", str))
