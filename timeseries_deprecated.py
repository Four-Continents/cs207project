import reprlib
import numpy as np
from doctest import run_docstring_examples as dtest
import numbers


class TimeSeries(object):
    """
    A class which stores a single ordered sequence of numerical data, and supports lookup and modification operations
    on the data.

    Examples
    --------
    >>> A = TimeSeries()
    Traceback (most recent call last):
        ...
    TypeError: __init__() missing 1 required positional argument: 'data'
    >>> B = TimeSeries(1)
    Traceback (most recent call last):
        ...
    TypeError: parameter must be a sequence
    >>> C = TimeSeries('hello')
    Traceback (most recent call last):
        ...
    TypeError: iterable must contain numerical types
    >>> a = TimeSeries(range(0,1000000))
    >>> a
    [0, 1, 2, 3, 4, 5, ...]
    >>> print(a)
    [0, 1, 2, 3, 4, 5, ...]
    >>> len(a)
    1000000
    >>> a[6] = 100
    >>> a[6]
    100
    >>> a[0:3]
    [0, 1, 2]
    """
    def __init__(self, data):
        """
        Constructor for the TimeSeries class.

        Parameters
        ----------
        data: sequence
            The ordered sequence of data points.

        Raises
        ------
        TypeError
            Raises the error if the input data is not a sequence or if it contains any type that is not numerical
        """
        if not hasattr(data, '__len__') and not hasattr(data, '__getitem__'):
            msg = 'parameter must be a sequence'
            raise TypeError(msg)

        for item in data:
            if not isinstance(item, numbers.Integral):
                msg = 'iterable must contain numerical types'
                raise TypeError(msg)

        if not hasattr(data, '__setitem__'):
            self._data = list(data)
        else:
            self._data = data

    def __iter__(self):
        """
        Yields a generator for the entire iterable

        Returns
        -------
        Generator
        """
        for x in self._data:
            yield x



    def __len__(self):
        """
        Returns the length of the iterable or sequence

        Returns
        -------
        int
        """
        return len(self._data)



    def __getitem__(self, index):
        """
        Getter for the class - used to retrieve individual values in the TimeSeries based on the index provided

        Parameters
        ----------
        index : int

        Returns
        -------
        float
            Returns the value at the given index
        """
        return self._data[index]



    def __setitem__(self, index, value):
        """
        Setter for the class - used to modify individual values in the TimeSeries

        Parameters
        ----------
        index : int

        value : float
        """
        self._data[index] = value

    def __repr__(self):
        """
        Returns
        -------
        string
            A string representation of the sequence data. Truncates longer sequences using the reprlib library.
        """
        return reprlib.repr(self._data)

    def __str__(self):
        """
        Returns
        -------
        string
            A string representation of the sequence data. Truncates longer sequences using the reprlib library.
        """
        return reprlib.repr(self._data)


class ArrayTimeSeries(TimeSeries):
    """
    Examples
    --------
    >>> C = ArrayTimeSeries('hello')
    Traceback (most recent call last):
        ...
    TypeError: iterable must contain numerical types
    >>> A = ArrayTimeSeries()
    Traceback (most recent call last):
    ...
    TypeError: __init__() missing 1 required positional argument: 'data'
    >>> B = ArrayTimeSeries(1)
    Traceback (most recent call last):
        ...
    TypeError: parameter must be a sequence
    >>> a = ArrayTimeSeries(range(0,1000000))
    >>> a
    array([     0...9998, 999999])
    >>> print(a)
    array([     0...9998, 999999])
    >>> len(a)
    1000000
    >>> a[6] = 100
    >>> a[6]
    100
    """
    def __init__(self, data):
        """
        Constructor for the ArrayTimeSeries class.

        Parameters
        ----------
        data: iterable
            The ordered sequence of data points.

        Raises
        ------
        TypeError
            Raises the error if the input data is not an iterable
        """
        super().__init__(data)

        if not hasattr(self._data, '__len__') and not hasattr(self._data, '__array_interface__') and not \
                hasattr(self._data, '__array__'):
            msg = 'Passed in parameter must be an array, any object exposing the array interface, an object whose ' \
                  '__array__ method returns an array, or any (nested) sequence.'
            raise TypeError(msg)

        self._data = np.array(self._data)


if __name__ == '__main__':
    dtest(TimeSeries, globals(), verbose = True)
    dtest(ArrayTimeSeries, globals(), verbose = True)
