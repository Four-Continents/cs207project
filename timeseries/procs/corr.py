import timeseries as ts
import numpy as np
import time

from ._corr import stand, kernel_corr
import asyncio


# this function is directly used for augmented selects
def proc_main(pk, row, arg):
    # The argument is a time series. But due to serialization it does
    # not come out as the "instance", and must be cast
    argts = ts.TimeSeries(**arg)
    # compute a standardized time series
    stand_argts = stand(argts, argts.mean(), argts.std())
    # for each row in our select/etc, standardize the time series
    mean = ts.TimeSeries(row['ts']['times'], row['ts']['values']).mean()
    std = ts.TimeSeries(row['ts']['times'], row['ts']['values']).std()
    stand_rowts = stand(ts.TimeSeries(row['ts']['times'], row['ts']['values']), mean, std)
    # compute the normalozed kernelized cross-correlation
    kerncorr = kernel_corr(stand_rowts, stand_argts, 1)
    # compute a distance from it.
    # The distance is given by np.sqrt(K(x,x) + K(y,y) - 2*K(x,y))
    # since we are normalized the autocorrs are 1
    kerndist = np.sqrt(2*(1-kerncorr))
    return [kerndist]

# the function is wrapped in a coroutine for triggers
async def main(pk, row, arg):
    return proc_main(pk, row, arg)
