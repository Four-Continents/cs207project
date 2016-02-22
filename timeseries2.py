import reprlib
import numpy as np
from doctest import run_docstring_examples as dtest
import numbers
import lazy as lz


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
    [0, 1, 2, 3, 4, 5, ..g.]
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
    # TODO should be monotonically increasing (you don't need to enforce this right now)v
    def __init__(self, times, values):
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
        def convert_to_np_array(data):

            if not hasattr(data, '__len__') and not hasattr(data, '__getitem__') and not \
                    hasattr(data, '__array_interface__') and not hasattr(data, '__array__'):
                msg = 'Passed in parameter must be an array, any object exposing the array interface, an object whose ' \
                  '__array__ method returns an array, or any (nested) sequence.'
                raise TypeError(msg)

            for item in data:
                if not isinstance(item, numbers.Number):
                    msg = 'iterable must contain numerical types'
                    raise TypeError(msg)

            return np.array(data)

        self._times = convert_to_np_array(times)
        self._values = convert_to_np_array(values)

    def __iter__(self):
        """
        Yields a generator for the entire iterable

        Returns
        -------
        Generator
        """
        for x in self._values:
            yield x

    def __len__(self):
        """
        Returns the length of the iterable or sequence

        Returns
        -------
        int
        """
        assert len(self._times) == len(self._values),  "lengths of times and values arrays not equal"

        return len(self._times)

    def __getitem__(self, time):
        """
        Getter for the class - used to retrieve individual values in the TimeSeries based on the time provided

        Parameters
        ----------
        index : int

        Returns
        -------
        float
            Returns the value at the given time point
        """

        position = self.binary_search(time)

        if position is None:
            msg = "The index you are providing does not exist. Please enter a valid time index."
            raise IndexError(msg)
        else:
            return self._values[position]

    def __setitem__(self, time, value):
        """
        Setter for the class - used to modify individual values in the TimeSeries given a particular time point

        Parameters
        ----------
        index : int

        value : float
        """

        position = self.binary_search(time)

        if position is None:
            msg = "The index you are providing does not exist. Please enter a valid time index."
            raise IndexError(msg)
        else:
            self._values[position] = value

    def __contains__(self, time):

        position = self.binary_search(time)

        if position is None:
            return False
        else:
            return True

    def binary_search(self, time):
        position = np.searchsorted(self._times, time)

        if position == len(self._times) or self._times[position] != time:
            return None
        else:
            return position

    def __repr__(self):
        """
        Returns
        -------
        string
            A string representation of the sequence time series values. Truncates longer sequences using the reprlib library.
        """
        return str("TimeSeries" + reprlib.repr(list(zip(self._times, self._values))))

    def __str__(self):
        """
        Returns
        -------
        string
            A string representation of the sequence of time series values. Truncates longer sequences using the reprlib library.
        """
        return repr(self)

    def values(self):
        """
        Returns
        -------
        sequence
            a sequence of the time series values
        """
        return self._values

    def times(self):
        """
        Returns
        -------
        sequence
            a sequence of the time series times
        """

        return self._times

    def items(self):
        """
        Returns
        -------
        sequence
            a sequence of of (time, value) tuples
        """
        return zip(self._times, self._values)

    def interpolate(self):
        pass

    @property
    def lazy(self):
        return lz.lazy(lambda x: x)(self)


if __name__ == '__main__':
    # dtest(TimeSeries, globals(), verbose = True)

    #[v for v in TimeSeries([0,1,2],[1,3,5
    # [1,3,5]

    a = TimeSeries([1, 2, 3], [4, 5, 6])
    print(str(a))
    # TimeSeries[(1, 4), (2, 5), (3, 6)]
    # print(len(a))
    # 3

    # print(a.binary_search(4))
    # print(np.searchsorted([0, 2, 3], 1))

    # a = TimeSeries([1, 2], [4, 5, 6])
    # print(len(a)) # AssertionError: lengths of times and values arrays not equal
