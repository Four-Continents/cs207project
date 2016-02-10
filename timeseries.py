import reprlib


class TimeSeries(object):
    """
    TODO Document: We'd like you to add docstrings to some of the components you've built. Specifically, please document: the
    TimeSeries class, its constructor, and the __str__ function. Try to include meaningful notes, instead of "this is a
    time series class" or "this returns a string". For the constructor, maybe describe its argument and what values it
    can take; for the string function, maybe describe how it abbreviates the output.

    stores a single, ordered set of numerical data. You can store this data as a Python list.
    """

    def __init__(self, data):
        self.data = data
        assert type(data) == list, "Please enter a list."  # TODO: sequence base class

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        assert index < self.__len__() and index >= 0, "Please enter a valid index."
        return self.data[index]

    def __setitem__(self, index, value):
        assert index <= self.__len__() and index >= 0, "Please enter a valid index."
        self.data[index] = value
        return 1

    def __repr__(self):
        return reprlib.repr(self.data)

    def __str__(self):
        return reprlib.repr(self.data)


if __name__ == '__main__':
    # print(TimeSeries(list(range(0, 1000000))))

    # a = TimeSeries(list(range(0, 1000000)))
    # print(a[5])
    #     if i in threes or i in fives:

    threes = TimeSeries(list(range(0, 1000, 3)))
    fives = TimeSeries(list(range(0, 1000, 5)))

    s = 0
    for i in range(0, 1000):
            s += i

    print("sum", s)
