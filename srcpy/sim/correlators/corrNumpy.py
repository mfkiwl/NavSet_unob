
import numpy as np
import numpy.fft as npfft
import scipy.signal as signal


def corr_td_single (x1,x2):

    c_12 = np.dot(x1,x2)
    return c_12


def corr_FD(x1,x2):

    X1 = npfft.fft(x1)
    X2 = npfft.fft(x2)
    #print ('X1 is ',np.shape(X1),type(X1),np.max(X1))
    #print ('X2 is ',np.shape(X2),type(X2),np.max(X2))

    C = X1 * np.conjugate(X2)
    #print ('C is ',np.shape(C),type(C),np.max(C))

    c = npfft.ifft(C)
    #print ('c is ',np.shape(c),type(c),np.max(c))
    return c

def corr_CORR(x1,x2):
    c = signal.correlate(x1,x2,'full')
    return c
