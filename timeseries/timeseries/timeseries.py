import reprlib
import numpy as np
from doctest import run_docstring_examples as dtest
import numbers
import operator
#import pype


class TimeSeriesIterator:
    def __init__(self, values): 
        self._values = values
        self.index = 0

    def __next__(self):
        try:
            value = self._values[self.index]
        except IndexError:
            raise StopIteration()
        self.index += 1
        return value

    def __iter__(self):
        return self


class TimeSeries(object):
    """
    A class which stores a single ordered sequence of numerical data, and \
    supports lookup and modification operations on the data.

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
    >>> [v for v in TimeSeries([0,1,2],[1,3,5])]
    [1, 3, 5]
    >>> a.times
    array([1, 2, 3])
    >>> a.values
    array([  4. ,  5.5 ,   6.5])
    >>> print([x for x in a.items()])
    [(1, 4.0), (2, 10.0), (3, 6.5)]
    >>> x = TimeSeries([1,2,3,4],[1,4,9,16])
    >>> print(x)
    TimeSeries[(1, 1), (2, 4), (3, 9), (4, 16)]
    >>> x = TimeSeries([1,2,3,4],[1,4,9,16])
    >>> [v for v in x]
    [1, 4, 9, 16]
    >>> [v for v in x.times]
    [1, 2, 3, 4]
    >>> [v for v in x.values]
    [1, 4, 9, 16]
    >>> #Test for overloaded operators
    >>> x = TimeSeries([1,2,3,4],[1,4,9,16])
    >>> y = TimeSeries([1,2,3,4],[2,4.5,-1,20])
    >>> z = TimeSeries([1,2], [0,0.5])
    >>> z_ts = TimeSeries([1,2,3], [0,0,0])
    >>> x * [1, 2, 3, 4]
    Traceback (most recent call last):
        ...
    NotImplementedError
    >>> x == [1, 2, 3, 4]
    Traceback (most recent call last):
        ...
    NotImplementedError
    >>> not x
    False
    >>> x2 = +x
    >>> x2 is x
    False
    >>> z + x
    Traceback (most recent call last):
        ...
    ValueError: TimeSeries[(1, 0.0), (2, 0.5)] and TimeSeries[(1, 1), (2, 4), (3, 9), (4, 16)] must have the same length
    >>> -z
    TimeSeries[(1, -0.0), (2, -0.5)]
    """
    def __init__(self, times, values):
        """
        Constructor for the TimeSeries class.

        Parameters
        ----------
        times: sequence
            Monotonically increasing sequence of times at which the values \
            were collected
        values: sequence
            The ordered sequence of data points

        Raises
        ------
        TypeError
            Raises the error if the input data is not an iterable or if it \
            contains any type that is not numerical

        Notes
        -----
        PRE: times is sorted in monotonically increasing order and has \
        matching indices to values
        """

        def convert_to_np_array(data):

            if not hasattr(data, '__len__') and \
               not hasattr(data, '__getitem__') and \
               not hasattr(data, '__array_interface__') and \
               not hasattr(data, '__array__'):
                msg = 'Passed in parameter must be an array, any object \
                       exposing the array interface, an object whose __array__\
                       method returns an array, or any (nested) sequence.'
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
        Returns
        -------
        iterator
            a sequence of values in the series
        """
         return TimeSeriesIterator(self.values)

    def itertimes(self):
         """
        Returns
        -------
        iterator
            an iterator of time points in the series
        """
         return TimeSeriesIterator(self.times)

    def itervalues(self):
         """
        Returns
        -------
        iterator
            an iterator of values in the series
        """
         return TimeSeriesIterator(self.values)

    def iteritems(self):
         """
        Returns
        -------
        iterator
            an iterator of (time,values) tuples in the series
        """
         time_value = []
         for i in range(len(self.times)):
            time_value.append((self.times[i], self.values[i]))
         return TimeSeriesIterator(time_value)

    def __len__(self):
        """
        Returns the length of the iterable or sequence

        Raises
        ------
        AssertionError
            Raises the error if the values and times arrays are not of equal \
            length

        Returns
        -------
        int
        """
        assert len(self.times) == len(self.values), "lengths of times and values arrays not equal"

        return len(self.times)

    def __getitem__(self, time):
        """
        Getter for the class - used to retrieve individual values in the \
        TimeSeries based on the time provided

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

        position = self._binary_search(time)

        if position is None:
            msg = "The index you are providing does not exist. Please enter a valid time index."
            raise IndexError(msg)
        else:
            return self.values[position]

    def __setitem__(self, time, value):
        """
        Setter for the class - used to modify individual values in the \
        TimeSeries given a particular time point

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

        position = self._binary_search(time)

        if position is None:
            msg = "The index you are providing does not exist. Please enter a valid time index."
            raise IndexError(msg)
        else:
            self.values[position] = value

    def __contains__(self, time):
        """
        Function to check if given index exists in the TimeSeries

        Parameters
        ----------
        time : int or float
            time to check for

        Returns
        ----------
        bool:
            True if time exists in self.times. False otherwise.
        """
        position = self._binary_search(time)

        if position is None:
            return False
        else:
            return True

    def _binary_search(self, time):
        """
        Utility function for internal usage - performs binary search

        Parameters
        ----------
        time : int or float
            time to search for

        Returns
        ----------
        bool:
            Position if it exists in self.times. 'None' otherwise.
        """

        position = np.searchsorted(self.times, time)

        if position == len(self.times) or self.times[position] != time:
            return None
        else:
            return position

    def __repr__(self):
        """
        Returns
        -------
        string
            A string representation of the sequence of time series times and \
            values. Truncates longer sequences using the reprlib library.
        """
        return str("TimeSeries" +
                   reprlib.repr(list(zip(self.times, self.values))))

    def __str__(self):
        """
        Returns
        -------
        string
            A string representation of the sequence of time series times and \
            values. Truncates longer sequences using the reprlib library.
        """
        return repr(self)

    @property
    def values(self):
        """
        Returns
        -------
        ndarray
            a numpy array of the time series values
        """
        return self._values

    @property
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
        return zip(self.times, self.values)

    def interpolate(self, interp_times):
        """
        Creates new TimeSeries object by interpolating interp_times in \
        piece-wise linear fashion from self. \
        Uses stationary boundary conditions if points are smaller than first \
        time point or larger than last.

        Parameters
        ----------
        interp_times : sequence
            list of times to interpolate from self

        Returns
        -------
        TimeSeries object
            new TimesSeries object with interp_times as times and interpolated\
            values
        """
        new_values = [np.interp(it,
                                self.times,
                                self.values) for it in interp_times]
        return TimeSeries(interp_times, new_values)

    #@pype.lib_import.component
    def mean(self):
        """
        Computes mean of values in TimesSeries

        Returns
        -------
        float
            Mean of values in TimesSeries

        Raises
        ------
        ValueError
            Raises the error if there are no values in the TimesSeries
        """
        if len(self._values) == 0:
            msg = "Cannot take mean of TimesSeries with no values"
            raise ValueError(msg)
        else:
            return np.mean(self._values)

    #@component
    def std(self):

        """
        Computes standard deviation of values in TimesSeries

        Returns
        -------
        float
            Standard deviation of values in TimesSeries

        Raises
        ------
        ValueError
            Raises the error if there are no values in the TimesSeries
        """
        if len(self._values) == 0:
            msg = "Cannot take standard deviation of TimesSeries with no values"
            raise ValueError(msg)
        else:
            return np.std(self._values)

    def median(self):
        """
        Computes median of values in TimesSeries

        Returns
        -------
        float
            Median of values in TimesSeries

        Raises
        ------
        ValueError
            Raises the error if there are no values in the TimesSeries
        """
        if len(self._values) == 0:
            msg = "Cannot take median of TimesSeries with no values"
            raise ValueError(msg)
        else:
            return np.median(self._values)

    def _seq_equal(self, seqA, seqB):
        """
        Helper function that returns whether two sequences have all elements equal

        Returns
        -------
        bool
            Whether all elements in the sequence are equal
        """
        return all(a == b for a, b in zip(seqA, seqB))

    def _seq_equal_len(self, seqA, seqB):
        """
        Helper function to determine whether two sequences have an equal number of elements

        Returns
        -------
        bool
            Whether the sequence length is the same
        """
        return len(seqA) == len(seqB)

    def _check_length_helper(self , rhs):
        """
        Helper function to determine whether two sequences have an equal number of elements

        Returns
        -------
        None

        Raises
        ------
        ValueError
            Raises the error if the lengths are unequal
        """
        if not self._seq_equal_len(self, rhs):
            raise ValueError(str(self)+' and '+str(rhs)+' must have the same length')

    def _check_times_helper(self, rhs):
        """
        Helper function to determine whether two TimeSeries have the same time points

        Returns
        -------
        None

        Raises
        ------
        ValueError
            Raises the error if the time points are different
        """
        if not self._seq_equal(self.times, rhs.times):
            raise ValueError(str(self)+' and '+str(rhs)+' must have the same time points')

    def _elem_op(self, rhs, op):
        """
        Helper function to apply the operator `op` to the values and `rhs`. `rhs` can be a real number or
        another TimeSeries object.

        Returns
        -------
        Float or
            The result of applying the operation to self.values and `rhs`.

        Raises
        -------
        NotImplementedError
            NotImplementedError is raised if the operation cannot be applied.
        """
        try:
            if isinstance(rhs, numbers.Real):
                return TimeSeries(self.times, [op(a, rhs) for a in self.values])
            elif isinstance(rhs, TimeSeries):
                self._check_length_helper(rhs)
                self._check_times_helper(rhs)
                pairs = zip(self, rhs)
                return TimeSeries( self.times, [op(a, b) for a, b in pairs] )
            else:
                raise NotImplementedError
        except TypeError:
            raise NotImplementedError

    def __add__(self, rhs):
        """
        Addition operator between the values of `self` and `rhs`. Operations are element-wise.

        Returns
        -------
        TimeSeries
            Result of adding `rhs` to the values of `self`.

        Raises
        -------
        NotImplementedError
            NotImplementedError is raised if the operation cannot be applied.
        """
        return self._elem_op(rhs, operator.add)

    def __radd__(self, other):
        """
        Reverses the addition order if the regular order is not implemented.

        Returns
        -------
        TimeSeries
            Result of adding `self` to the values of `rhs`.
        """
        return self + other

    def __mul__(self, rhs):
        """
        Multiplication operator between the values of `self` and `rhs`. Operations are element-wise.

        Returns
        -------
        TimeSeries
            Result of multiplying the values of `rhs` to the values of `self`.

        Raises
        -------
        NotImplementedError
            NotImplementedError is raised if the operation cannot be applied.
        """
        return self._elem_op(rhs, operator.mul)

    def __rmul__(self, other):
        """
        Reverses the multiplication order if the regular order is not implemented.

        Returns
        -------
        TimeSeries
            Result of multiplying the values of `self` to the values of `rhs`.

        Raises
        -------
        NotImplementedError
            NotImplementedError is raised if the operation cannot be applied.
        """
        return self * other

    def __sub__(self, rhs):
        """
        Subtraction operator between the values of `self` and `rhs`. Operations are element-wise.

        Returns
        -------
        TimeSeries
            Result of subtracting `rhs` from the values of `self`.

        Raises
        -------
        NotImplementedError
            NotImplementedError is raised if the operation cannot be applied.
        """
        return self._elem_op(rhs, operator.sub)

    def __eq__(self, rhs):
        """
        Equality operator between the values of `self` and `rhs`. Operations are element-wise.

        Returns
        -------
        bool
           True if the values from `rhs` are equal to the values from `self`.

        Raises
        -------
        NotImplementedError
            NotImplementedError is raised if the operation cannot be applied.
        """
        if not isinstance(rhs, TimeSeries):
            raise NotImplementedError
        return self._seq_equal_len(self.times, rhs.times) and self._seq_equal_len(self.values, rhs.values) and \
               self._seq_equal(self.times, rhs.times) and self._seq_equal(self.values, rhs.values)

    def __abs__(self):
        """
        Returns
        -------
        float
           L2 norm of the values of `self`.
        """
        return np.sqrt(sum(x * x for x in self.values))

    def __bool__(self):
        """
        Returns
        -------
        bool
           Boolean value after taking the L2 norm of the values of `self`
        """
        return bool(abs(self))

    def __neg__(self):
        """
        Returns
        -------
        TimeSeries
           A copy of `self` with each value multiplied by -1.
        """
        return TimeSeries(self.times, -self.values)

    def __pos__(self):
        """
        Returns
        -------
        TimeSeries
           A copy of `self`.
        """
        return TimeSeries(self.times, self.values)

    @property
    def lazy(self):
        return lz.lazy(lambda x: x)(self)


if __name__ == '__main__':
    import lazy as lz
    dtest(TimeSeries, globals(), verbose=True)

else:
     import timeseries.lazy as lz


