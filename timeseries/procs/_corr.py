import numpy.fft as nfft
import numpy as np
import timeseries as ts
from scipy.stats import norm


def tsmaker(m, s, j):
    meta = {}
    meta['order'] = int(np.random.choice([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]))
    meta['blarg'] = int(np.random.choice([1, 2]))
    t = np.arange(0.0, 1.0, 0.01)
    v = norm.pdf(t, m, s) + j*np.random.randn(100)
    return meta, ts.TimeSeries(t, v)


def random_ts(a):
    t = np.arange(0.0, 1.0, 0.01)
    v = a*np.random.random(100)
    return ts.TimeSeries(t, v)


def stand(x, m, s):
    return (x-m)/s


def ccor(ts1, ts2):
    "given two standardized time series, compute their cross-correlation using FFT"
    # your code here
    # Ref: http://dsp.stackexchange.com/questions/736/how-do-i-implement-cross-correlation-to-prove-two-audio-files-are-similar

    # assert len(ts1) == len(ts2) # Make sure they are equal length time series

    # Get the values of the time series into a list
    ts1_p, ts2_p = list(ts1), list(ts2)
    # N = len(ts1_p) + len(ts2_p) - 1

    # Pad with zeros
    # ts1_p.extend([0.] * (N-len(ts1_p)))
    # ts2_p.extend([0.] * (N-len(ts2_p)))

    # print (ts1_p)
    # print (ts2_p)
    # Reverse the second time series
    # ts2_p = np.array(ts2_p[::-1])
    ts2_p = np.array(ts2_p)
    ts1_p = np.array(ts1_p)

    # print (ts2_p)

    # corr(a, b) = ifft(fft(a_and_zeros) * fft(b_and_zeros[reversed]))
    # print (type(nfft.fft(ts1_p) ))
    # print (type(nfft.fft(ts2_p)))
    inter = nfft.fft(ts1_p) * np.conjugate(nfft.fft(ts2_p))
    res = nfft.ifft( inter )
    # res = res[len(ts1)-1:]
    # print ((res))
    # print(type(res))
    return res


def max_corr_at_phase(ts1, ts2):
    ccorts = ccor(ts1, ts2)
    idx = np.argmax(ccorts)
    # print ('Cand:', ccorts)
    # print ('Size:', len(ccorts))
    npc = np.correlate(ts1, ts2, 'same')
    # print ('NPCorr:', npc, 'Max:', max(npc), 'Len:', len(npc), 'Arg:', np.argmax(npc))
    maxcorr = ccorts[idx]
    return idx, maxcorr


# Ref: http://stackoverflow.com/questions/9457832/python-list-rotation
def rotate(l, x):
    x = x%len(l)
    return l[-x:] + l[:-x]

def calcK(ts1, ts2, mult):
    # N = len(ts1)
    ret_c = np.sum( np.exp( mult * ccor(ts1, ts2) ) )

    # res = 0.
    # for i in range(1, N+1):
    #     y = np.array(rotate(list(ts2), i))
    #     x = np.array(ts1)
    #     res += np.exp( mult * np.inner(x, y) )

    return ret_c

#The equation for the kernelized cross correlation is given at
#http://www.cs.tufts.edu/~roni/PUB/ecml09-tskernels.pdf
#normalize the kernel there by np.sqrt(K(x,x)K(y,y)) so that the correlation
# of a time series with itself is 1.
def kernel_corr(ts1, ts2, mult=1):
    "compute a kernelized correlation so that we can get a real distance"
    # your code here.
    Kx, Ky = calcK(ts1, ts1, mult), calcK(ts2, ts2, mult)
    # print (ts1)
    # print ('KxKy:', Kx, Ky)
    cX = ccor(ts1, ts1)
    # cX = np.correlate(ts1, ts1, 'full')
    # print ('XX', cX, 'Len:', len(cX), 'Argmax:', np.argmax(cX), 'Max:', max(cX))
    ret = calcK(ts1, ts2, mult)
    return np.linalg.norm(ret) / np.linalg.norm((np.sqrt(Kx * Ky)))





#this is for a quick and dirty test of these functions
# you might need to add procs to pythonpath for this to work
if __name__ == "__main__":
    print("HI")
    _, t1 = tsmaker(0.5, 0.1, 0.01)
    _, t2 = tsmaker(0.5, 0.1, 0.01)
    print(t1.mean(), t1.std(), t2.mean(), t2.std())

    import matplotlib
    matplotlib.use('qt4agg')
    import matplotlib.pyplot as plt

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
    t3 = random_ts(2)
    t4 = random_ts(3)
    plt.plot(t3)
    plt.plot(t4)
    plt.show()
    standts3 = stand(t3, t3.mean(), t3.std())
    standts4 = stand(t4, t4.mean(), t4.std())
    idx, mcorr = max_corr_at_phase(standts3, standts4)
    print(idx, mcorr)
    sumcorr = kernel_corr(standts3, standts4, mult=1)
    print(sumcorr)
