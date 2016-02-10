import reprlib


class TimeSeries(object):
    """
    TODO Document: We'd like you to add docstrings to some of the components you've built. Specifically, please document: the
    TimeSeries class, its constructor, and the __str__ function. Try to include meaningful notes, instead of "this is a
    time series class" or "this returns a string". For the constructor, maybe describe its argument and what values it
    can take; for the string function, maybe describe how it abbreviates the output.

    stores a single, ordered set of numerical data. You can store this data as a Python list.

    TODO add doctests
    TODO implement __iter__
    """

    def __init__(self, data):
        self._data = data

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, index, value):
        self._data[index] = value

    def __repr__(self):
        return reprlib.repr(self._data)

    def __str__(self):
        return reprlib.repr(self._data)


if __name__ == '__main__':
    print(TimeSeries(list(range(0, 1000000))))

    a = TimeSeries(list(range(0, 1000000)))
    print(a[5])

    threes = TimeSeries(range(0, 1000, 3))
    fives = TimeSeries(range(0, 1000, 5))

    # threes = TimeSeries(list(range(0, 1000, 3)))
    # fives = TimeSeries(list(range(0, 1000, 5)))
    #
    # s = 0
    # for i in range(0, 1000):
    #     if i in threes or i in fives:
    #         s += i
    #
    # print("sum", s)
