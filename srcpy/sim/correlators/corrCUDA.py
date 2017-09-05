
import numpy as np
import accelerate.cuda.blas as blas
import accelerate.cuda.fft as ft
from numba import cuda

def corr_td_single (x1,x2):
    c_12 = blas.dot(x1,x2)
    return c_12

def best_grid_size(size, tpb):
    bpg = np.ceil(np.array(size, dtype=np.float) / tpb).astype(np.int).tolist()
    return tuple(bpg)


@cuda.jit('void(float32[:], float32[:])')
def mult_inplace(img, resp):
    i = cuda.grid(1)
    img[i] *= resp[i]


def corr_FD(x1,x2):
    threadperblock = 32, 8
    blockpergrid = best_grid_size(tuple(reversed(x1.shape)), threadperblock)
    print('kernel config: %s x %s' % (blockpergrid, threadperblock))

    # Trigger initialization the cuFFT system.
    # This takes significant time for small dataset.
    # We should not be including the time wasted here



    #ft.FFTPlan(shape=x1.shape, itype=np.float32, otype=np.complex64)

    X1 = x1.astype(np.float32)
    X2 = x2.astype(np.float32)


    stream1 = cuda.stream()
    stream2 = cuda.stream()

    fftplan1 = ft.FFTPlan(shape=x1.shape, itype=np.float32,
                       otype=np.complex64, stream=stream1)
    fftplan2 = ft.FFTPlan(shape=x2.shape, itype=np.float32,
                       otype=np.complex64, stream=stream2)

    # pagelock memory
    with cuda.pinned(X1, X2):

        # We can overlap the transfer of response_complex with the forward FFT
        # on image_complex.
        d_X1 = cuda.to_device(X1, stream=stream1)
        d_X2 = cuda.to_device(X2, stream=stream2)

        fftplan1.forward(d_X1, out=d_X1)
        fftplan2.forward(d_X2, out=d_X2)
        print ('d_X1 is ',np.shape(d_X1),type(d_X1),np.max(d_X1))
        print ('d_X2 is ',np.shape(d_X2),type(d_X2),np.max(d_X2))

        stream2.synchronize()

        mult_inplace[blockpergrid, threadperblock, stream1](d_X1, d_X2)
        fftplan1.inverse(d_X1, out=d_X1)

        # implicitly synchronizes the streams
        c = d_X1.copy_to_host().real / np.prod(x1.shape)

    return c
