
import numpy as np
import accelerate.mkl.blas as blas
import accelerate.mkl.fftpack as ftpck

def corr_td_single (x1,x2):

    c_12 = blas.dot(x1,x2)
    return c_12


def corr_FD(x1,x2):

    X1 = ftpck.rfft(x1)
    X2 = ftpck.rfft(x2)

    C = X1 * np.conjugate(X2)

    c = ftpck.ifft(C)

    return c
