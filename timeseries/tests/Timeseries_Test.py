import unittest
from timeseries.timeseries import TimeSeries
import numpy as np

class TimeSeriesTest(unittest.TestCase):

    def test_init(self):
        b = TimeSeries([1, 1.5, 2, 2.5, 10], [0, 2, -1, 0.5, 0])
        assert isinstance(b, TimeSeries)
        self.assertTrue( TimeSeries([1, 1.5, 2, 2.5, 10], [0, 2, -1, 0.5, 0]) )

    def test_setter(self):
        b = TimeSeries([1, 1.5, 2, 2.5, 10], [0, 2, -1, 0.5, 0])
        self.assertTrue ( b[2]== -1 )
        b[2] = 10
        self.assertTrue ( b[2]== 10 )

    def test_len(self):
        b = TimeSeries([1, 1.5, 2, 2.5, 10], [0, 2, -1, 0.5, 0])
        self.assertTrue( len(b) == 5)

# Test Operators
    def test_add(self):
        x = TimeSeries([1, 2, 3, 4],[1, 4, 9, 16])
        y = TimeSeries([1, 2, 3, 4],[2, 4.5, -1, 20])
        self.assertTrue( x+y == TimeSeries([1, 2, 3, 4], [3.0, 8.5, 8.0, 36.0]) )
        self.assertTrue ( x+2 == TimeSeries([1.0, 2.0, 3.0, 4.0], [3.0, 6.0, 11.0, 18.0]) )
        self.assertTrue ( 2+x == TimeSeries([1.0, 2.0, 3.0, 4.0], [3.0, 6.0, 11.0, 18.0]) )

    def test_sub(self):
        x = TimeSeries([1,2,3,4],[1,4,9,16])
        y = TimeSeries([1,2,3,4],[2,4.5,-1,20])
        self.assertTrue( y-x == TimeSeries([1, 2, 3, 4], [1.0, 0.5, -10.0, 4.0]))

    def test_mul(self):
        x = TimeSeries([1, 2, 3, 4],[1, 4, 9, 16])
        y = TimeSeries([1, 2, 3, 4],[2, 4.5, -1, 20])
        self.assertTrue( x*y == TimeSeries([1, 2, 3, 4], [2.0, 18.0, -9.0, 320.0]) ) 
        self.assertTrue( 5.0*x == TimeSeries([1, 2, 3, 4],[5.0, 20.0, 45.0, 80.0]) )

# Lazy Evaluation
    def test_lazy(self):
        x = TimeSeries([1,2,3,4],[1,4,9,16])
        self.assertTrue ( x == x.lazy.eval() )

# Test mean and Standard Deviation
    def test_mean(self):
        x = TimeSeries([1, 2, 3, 4],[1, 4, 9, 16])  
        self.assertTrue ( x.mean() == 7.5)
    
    def test_median(self):
        x = TimeSeries([1,2,3,4],[4,5,6,7])
        self.assertTrue (x.median()==5.5)

    def test_interpolate(self):
        a = TimeSeries([0, 5, 10], [ 1, 2, 3])
        b = TimeSeries([2.5,7.5], [100, -100])
        self.assertTrue ( a.interpolate([1]) == TimeSeries([1],[1.2]) )
        self.assertTrue ( a.interpolate(b.times) == TimeSeries([2.5,7.5], [1.5, 2.5]))
        self.assertTrue ( a.interpolate([-100, 100]) == TimeSeries([-100,100], [1,3]))

    def test_bool(self):
        x = TimeSeries([1, 2, 3, 4],[1, 4, 9, 16])
        y = TimeSeries([1,2,3,4],[2,4.5,-1,20])
        z_ts = TimeSeries([1,2,3], [0,0,0])
        x2 = +x
        self.assertTrue ( abs(x) == 18.814887722226779 )
        self.assertTrue ( bool(z_ts) == False )
        self.assertTrue ( ( x2==x ) == True)
        self.assertTrue ( (x==y) == False)

    def test_iter(self):
        x = TimeSeries([1, 2, 3, 4],[1, 4, 9, 16])
        i = iter(x)
        nextt = next(i)
        self.assertTrue ( nextt == 1 )
        nextt = next(i)
        self.assertTrue ( nextt == 4 )
        self.assertTrue (nextt.dtype == np.int64)

    def test_itertimes(self):
        x = TimeSeries([1, 2, 3, 4],[1, 4, 9, 16])
        i = x.itertimes()
        nextt = next(i)
        self.assertTrue ( nextt == 1 )
        nextt = next(i)
        self.assertTrue ( nextt == 2 )
        self.assertTrue (nextt.dtype == np.int64)

    def test_itervalues(self):
        x = TimeSeries([1, 2, 3, 4],[1, 4, 9, 16])
        i = x.itervalues()
        nextt = next(i)
        self.assertTrue ( nextt == 1 )
        nextt = next(i)
        self.assertTrue ( nextt == 4 )
        self.assertTrue (nextt.dtype == np.int64)

    def test_iteritems(self):
        x = TimeSeries([1, 2, 3, 4],[1, 4, 9, 16])
        i = x.iteritems()
        nextt = next(i)
        self.assertTrue ( nextt == (1, 1) )
        nextt = next(i)
        self.assertTrue ( nextt == (2, 4) )
        self.assertTrue (len(nextt) ==2 )


if __name__=='__main__':
    unittest.main()

