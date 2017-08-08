
import numpy as np
import scipy.signal as signal


def corr_td_single (x1,x2):

    c_12 = np.dot(x1,x2)
    return c_12


def corr_FD(x1,x2):

    X1 = np.fft(x1)
    X2 = np.fft(x2)


    C = np.dot(X1,np.conjugate(X2))

    c = np.rfft(C)

    return c

def corr_CORR(x1,x2):
    c = signal.correlate(x1,x2,'full')
    return c
