#!/usr/bin/env python

"""
This is a test bed script to plot a bitsteam with its
symbols shaped. 
"""
import sys
sys.path.append("../../sim")

import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
from siggens import train_pulse as gen
from siggens import PRN_bitstreams as prn
from utils import freqaxis_shape as ut
from modulators import constallation_mappers as mod
from modulators import up_convertors as upcon

##################### Parameters ######################
f_sampl = 900e3  # sampling frequency in kHz
T_int = 1  # entire signal length in ms

##################### Simulation ######################
t = np.arange(0, T_int, 1 / f_sampl)  # time axis
# f = ut.freq_fr_time (t)				# frequency axis
cd = prn.gold_seq(2, 6, 1)  # code
Ts = 1 / 1023  # Nyquist's symbol interval
tau = 1  # time acceleration factor
Tstr = Ts * tau  # transmitted symbol interval
bitrate = 1 / Tstr
td = 0.0  # initial delay of the sequence (time offset)

# baseband signals
a1 = mod.rcos_bpsk_map(t, cd, bitrate, pw=Ts, alpha=1.0)
a2 = mod.rcos_bpsk_map(t, cd, bitrate, pw=Ts, alpha=0.5)
a3 = mod.rcos_bpsk_map(t, cd, bitrate, pw=Ts, alpha=0.0)
c = mod.rect_tr(t, Tstr, 0, td, cd)

##################### Plots ###########################
plt.figure(1, figsize=(10, 15), dpi=300)

#  Time domain

ax1 = plt.subplot(311)
plt.plot(t, np.real(a1), '-r', label='$x_{rcos}(t), \\beta = 1.0$')
plt.plot(t, np.real(a2), '-b', label='$x_{rcos}(t), \\beta = 0.5$')
plt.plot(t, np.real(a3), '-g', label='$x_{rcos}(t), \\beta = 0.0$')
plt.plot(t, c, '-k', label='$x_{rect}(t)$')
plt.grid(True)
plt.legend(loc='upper left', bbox_to_anchor=(1.12, 1.35))
plt.title('Pulse-shaped baseband signal')
plt.ylabel('Voltage')
plt.xlabel('Time')
plt.axis([0, 10, -0.3, 1.3])

plt.show()
