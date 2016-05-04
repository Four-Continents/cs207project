import timeseries as ts
import numpy as np
import time
import matplotlib
matplotlib.use('qt4agg')
import matplotlib.pyplot as plt

from procs._corr import *

EPS = 1e-8

def test_vp_random():
    _, t1 = tsmaker(0.5, 0.1, 0.01)
    _, t2 = tsmaker(0.5, 0.1, 0.01)
    print(t1.mean(), t1.std(), t2.mean(), t2.std())

    print(t1.times)
    print(t1.values)
    plt.plot(t1.times, t1.values)
    plt.plot(t2.times, t2.values)
    # plt.plot([1, 3, 5], [10, 12, 18])
    # plt.show()
    standts1 = stand(t1, t1.mean(), t1.std())
    standts2 = stand(t2, t2.mean(), t2.std())

    idx, mcorr = max_corr_at_phase(standts1, standts2)
    print(idx, mcorr)
    sumcorr = kernel_corr(standts1, standts2, mult=1)
    print(sumcorr)

def test_vp_random2():
    t3 = random_ts(2)
    t4 = random_ts(3)
    plt.plot(t3)
    plt.plot(t4)
    # plt.show()
    standts3 = stand(t3, t3.mean(), t3.std())
    standts4 = stand(t4, t4.mean(), t4.std())
    idx, mcorr = max_corr_at_phase(standts3, standts4)
    print(idx, mcorr)
    sumcorr = kernel_corr(standts3, standts4, mult=1)
    print(sumcorr)
    # print (np.inner(list(standts1)[:10], list(standts1)[:10]))
    # print (np.sum(np.array(standts1)*np.array(standts1)))
    # print ('SD:', np.std(list(standts1)))

    # assert 0

def test_vp_shifted():
    t1 = random_ts(2)
    standts1 = stand(t1, t1.mean(), t1.std())

    # Rotate ts1 by k positions and call it ts2
    disp = 15
    standts2 = rotate(list(standts1), disp)

    idx, mcorr = max_corr_at_phase(standts1, standts2)
    print(idx, mcorr)

    # Check that we get the right answer
    assert idx == len(t1) - disp
    assert np.abs(mcorr - 100.0) < EPS

    sumcorr = kernel_corr(standts1, standts2, mult=1)
    print(sumcorr)
    assert np.abs(sumcorr - 1.0) < EPS

    # assert 0


