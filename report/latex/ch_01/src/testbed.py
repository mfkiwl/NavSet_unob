#!/usr/bin/env python

"""
This is a test bed script to plot imported signals in both time and frequency domain.
"""

import numpy as np
import matplotlib.pyplot as plt
from siggens import one_pulse as gen

# simulation parameters
f_sampl = 100e3 	# sampling frequency in kHz
T_int = 1 			# entire signal length in ms
f_IF = 10.7e3 		# IF frequency in kHz

chr = 1.023e3 		# chip rate in kbps
#	fs = 10e3
#	N = 1e5
amp = 2*np.sqrt(2)
#	freq = 1270.0
noise_power = 0.001 * f_sampl / 2
#	time = np.arange(N) / fs

t = np.arange(0,T_int,1/f_sampl)


y = gen.square_p(t,.1,.2)


plt.plot(t, y)
plt.grid(True)
plt.show()


