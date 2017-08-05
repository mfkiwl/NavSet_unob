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
from utils import freqaxis_shape as ut

##################### Parameters ######################
f_sampl = 50e3 		# sampling frequency in kHz
T_int = 0.2 			# entire signal length in ms

##################### Simulation ######################
t = np.arange(0,T_int,1/f_sampl)	# time axis
f = ut.freq_fr_time (t)				# frequency axis
tc = ut.corr_fr_time (t)			# correlation time axis
cd = np.array([1,1,1,0,1,1,1,1,0,1,0,0,1,0,1])	# code
Ts = 10e-3							# Nyquist's symbol interval
tau = 0.8							# time acceleration factor
Tstr = Ts * tau						# transmitted symbol interval
td = 0.01							# initial delay of the sequence (time offset)

# Time Domain
a1 = gen.rcos_tr(t,Tstr,td + Tstr/2,cd,Ts,1.0)
a2 = gen.rcos_tr(t,Tstr,td + Tstr/2,cd,Ts,0.5)
a3 = gen.rcos_tr(t,Tstr,td + Tstr/2,cd,Ts,0.0)
c  = gen.rect_tr(t,Tstr,0,td,cd)


# Correlate processor
A1_c = signal.correlate(a1,a1,'full')
A2_c = signal.correlate(a2,a2,'full')
A3_c = signal.correlate(a3,a3,'full')
C1_c = signal.correlate( c,a1,'full')
C2_c = signal.correlate( c,a2,'full')
C3_c = signal.correlate( c,a3,'full')

CC_c = signal.correlate( c, c,'full')


##################### Plots ###########################
plt.figure(1,figsize=(10, 12), dpi=200)

#  Time domain

ax1 = plt.subplot(311)
plt.plot(t, a1,'-g', label='$x_{rcos}(t), \\beta = 1.0$')
plt.plot(t, a2,'-b', label='$x_{rcos}(t), \\beta = 0.5$')
plt.plot(t, a3,'-r', label='$x_{rcos}(t), \\beta = 0.0$')
plt.plot(t,  c,'-k', label='$x_{rect}(t)$')
plt.grid(True)
lgd = ax1.legend(loc='upper right', bbox_to_anchor=(1.12,1.2))
plt.title('Pulse-shaped baseband signal, $\\tau = 1.0$', loc='left')
plt.ylabel('Voltage')
plt.xlabel('Time')
plt.axis([0, 0.2, -0.3, 1.3])
#plt.show()

# Frequency domain - spectrum of sinc pulse
ax2 = plt.subplot(312)
plt.plot(tc, A1_c,'-g', label="$X_{sinc}(f)$")
plt.plot(tc, A2_c,'-b', label='$X_{rcos}(f)$')
plt.plot(tc, A3_c,'-r', label='$X_{rcos}(f)$')
plt.grid(True)

# Frequency domain - spectrum of square pulse
ax3 = plt.subplot(313,sharex=ax2)
plt.plot(tc, C1_c,'-g', label="$X_{sinc}(f)$")
plt.plot(tc, C2_c,'-b', label='$X_{rcos}(f)$')
plt.plot(tc, C3_c,'-r', label='$X_{rcos}(f)$')
plt.plot(tc, CC_c,'-k', label='$X_{rcos}(f)$')
plt.grid(True)
plt.savefig('sequence_accelerated.eps',format='eps')
plt.show()


