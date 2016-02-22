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
    TypeError: __init__() missing 2 required positional arguments: 'times' and 'values'
    >>> B = TimeSeries(1)
    Traceback (most recent call last):
        ...
    TypeError: __init__() missing 1 required positional argument: 'values'
    >>> C = TimeSeries('hello')
    Traceback (most recent call last):
        ...
    TypeError: __init__() missing 1 required positional argument: 'values'
    >>> D = TimeSeries([1, 2, 3], ['h', 'e', 'l'])
    Traceback (most recent call last):
        ...
    TypeError: iterable must contain numerical types
    >>> E = TimeSeries([1, 2], [4, 5, 6])
    >>> print(len(E))
    Traceback (most recent call last):
        ...
    AssertionError: lengths of times and values arrays not equal
    >>> a = TimeSeries([1, 2, 3], [4, 5.5, 6.5])
    >>> print(a)
    TimeSeries[(1, 4.0), (2, 5.5), (3, 6.5)]
    >>> len(a)
    3
    >>> a[6]
    Traceback (most recent call last):
        ...
    IndexError: The index you are providing does not exist. Please enter a valid time index.
    >>> a[2]
    5.5
    >>> a[2] = 10
    >>> a[2]
    10.0
    >>> [v for v in TimeSeries([0,1,2],[1,3,5])]
    [1, 3, 5]
    >>> a.times()
    array([1, 2, 3])
    >>> a.values()
    array([  4. ,  10. ,   6.5])
    >>> print([x for x in a.items()])
    [(1, 4.0), (2, 10.0), (3, 6.5)]
    >>> b = TimeSeries([1, 1.5, 2, 2.5, 10], [0, 2, -1, 0.5, 0])
    >>> print(b)
    TimeSeries[(1.0, 0.0), (1.5, 2.0), (2.0, -1.0), (2.5, 0.5), (10.0, 0.0)]
    >>> b.values()
    array([ 0. ,  2. , -1. ,  0.5,  0. ])
    >>> a = TimeSeries([0,5,10], [1,2,3])
    >>> b = TimeSeries([2.5,7.5], [100, -100])
    >>> print(a.interpolate([1]))
    TimeSeries[(1, 1.2)]
    >>> print(a.interpolate(b.times()))
    TimeSeries[(2.5, 1.5), (7.5, 2.5)]
    >>> print(a.interpolate([-100, 100]))
    TimeSeries[(-100, 1.0), (100, 3.0)]
    """

    def __init__(self, times, values):
        """
        Constructor for the TimeSeries class.

        Parameters
        ----------
        times: sequence
            Monotonically increasing sequence of times the values were collected
        values: sequence
            The ordered sequence of data points.

        Raises
        ------
        TypeError
            Raises the error if the input data is not an iterable or if it contains any type that is not numerical

        Notes
        -----
        PRE: times is sorted in monotonically increasing order and has matching indices to values
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

        Raises
        ------
        AssertionError
            Raises the error if the values and times arrays are not of equal length

        Returns
        -------
        int
        """
        assert len(self._times) == len(self._values), "lengths of times and values arrays not equal"

        return len(self._times)

    def __getitem__(self, time):
        """
        Getter for the class - used to retrieve individual values in the TimeSeries based on the time provided

        Parameters
        ----------
        time: int or float

        Returns
        -------
        float
            Returns the value at the given time point

        Raises
        ------
        IndexError
            Raises the error if the time does not exist in the times array

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
        time : int or float
            time to change

        value : int or float
            value to change to

        Raises
        ------
        IndexError
            Raises the error if the time does not exist in the times array
        """

        position = self.binary_search(time)

        if position is None:
            msg = "The index you are providing does not exist. Please enter a valid time index."
            raise IndexError(msg)
        else:
            self._values[position] = value

    def __contains__(self, time):
        """
        Setter for the class - used to modify individual values in the TimeSeries given a particular time point

        Parameters
        ----------
        time : int or float
            time to check for

        Returns
        ----------
        bool:
            True if time exists in self._times. False otherwise.
        """
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
            A string representation of the sequence of time series times and values.
            Truncates longer sequences using the reprlib library.
        """
        return str("TimeSeries" + reprlib.repr(list(zip(self._times, self._values))))

    def __str__(self):
        """
        Returns
        -------
        string
            A string representation of the sequence of time series times and values.
            Truncates longer sequences using the reprlib library.
        """
        return repr(self)

    def values(self):
        """
        Returns
        -------
        ndarray
            a numpy array of the time series values
        """
        return self._values

    def times(self):
        """
        Returns
        -------
        ndarray
            a numpy array of the time series times
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

    def interpolate(self, interp_times):
        """
        creates new TimeSeries object by interpolating interp_times in piece-wise linear fashion from self
        Uses stationary boundary conditions if points are smaller than first time point or larger than last.

        Parameters
        ----------
        interp_times : sequence
            list of times to interpolate from self

        Returns
        -------
        TimeSeries object
            new TimesSeries object with interp_times as times and interpolated values
        """
        new_values = [np.interp(it, self._times, self._values) for it in interp_times]
        return TimeSeries(interp_times, new_values)

    @property
    def lazy(self):
        return lz.lazy(lambda x: x)(self)


if __name__ == '__main__':
    dtest(TimeSeries, globals(), verbose=True)