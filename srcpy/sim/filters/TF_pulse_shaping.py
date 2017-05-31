"""
Part of the signal-generator library.
File contains set of functions helping to produce a signal and to process it.
    - freq_fr_time :: shapes frequency axis from a given time vector

"""
import numpy as np

def root_raised_cosine(f, pw, **args):
    """
    Computes a transfer function of the filter RR-Cos

    :param f: frequency axis
    :param pw: pulse width measured at the sinc's main lobe
    :param args:
    :return: transfer function
    """
    if 'alpha' in args:
        alpha = args['alpha']
    else:
        alpha = .8  # roll-off factor

    ## Transfer Function creator
    beta = alpha / pw

    f1 = np.pi * (1 - alpha) / (2 * pw)
    f2 = np.pi * (1 + alpha) / (2 * pw)

    print(f1)
    print(f2)

    edge = np.sqrt(pw / 2 * (1 + np.cos(np.pi * pw / alpha * (abs(f) - f1))))

    tf1 = np.sqrt(pw) * (((f >= 0) & (f < f1)) * 1 + ((f < 0) & (f > (-f1))) * 1)
    tf2 = edge * (((f > f1) & (f < f2)) * 1 + ((f < (-f1)) & (f > (-f2))) * 1)

    tfc = np.zeros(np.size(f))
    tf = tf1 + tf2 + tfc * 1j

    return (tf)
