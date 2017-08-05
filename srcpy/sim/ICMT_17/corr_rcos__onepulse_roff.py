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
from siggens import one_pulse as gen
from siggens import PRN_bitstreams as prn
from utils import freqaxis_shape as ut

##################### Parameters ######################
f_sampl = 50e3 		# sampling frequency in kHz
T_int = 0.2			# entire signal length in ms

##################### Simulation ######################
t = np.arange(0,T_int,1/f_sampl)	# time axis
f = ut.freq_fr_time (t)				# frequency axis
tc = ut.corr_fr_time (t)			# correlation time axis
Ts = 20e-3							# Nyquist's symbol interval
tau = 1							# time acceleration factor
Tstr = Ts * tau						# transmitted symbol interval
td = 0.05							# initial delay of the pulse (time offset)

# Time Domain
a1 = gen.rcos_p(t,td + Tstr/2,Ts,1.0)
a2 = gen.rcos_p(t,td + Tstr/2,Ts,0.5)
a3 = gen.rcos_p(t,td + Tstr/2,Ts,0.0)
c  = gen.rect_p(t,td,td + Tstr)


# Correlate processor
A1_c = signal.correlate(a1,a1,'full')
A2_c = signal.correlate(a2,a2,'full')
A3_c = signal.correlate(a3,a3,'full')
C1_c = signal.correlate( c,a1,'full')
C2_c = signal.correlate( c,a2,'full')
C3_c = signal.correlate( c,a3,'full')

CC_c = signal.correlate( c, c,'full')

##################### Plots ###########################
plt.figure(1,figsize=(8, 6), dpi=200)

#  Time domain

#ax1 = plt.subplot(311)
plt.plot(t, a1,'-g', label='$h_{rcos}(t), \\beta = 1.0$')
plt.plot(t, a2,'-b', label='$h_{rcos}(t), \\beta = 0.5$')
plt.plot(t, a3,'-r', label='$h_{rcos}(t), \\beta = 0.0$')
plt.plot(t,  c,'-k', label='$h_{rect}(t)$')
plt.grid(True)
plt.legend(loc='upper right', bbox_to_anchor=(1.12,1.1))
plt.title('Pulse-shaped baseband signal $\\tau = 1.0$', loc='left')
plt.ylabel('Baseband - voltage')
plt.xlabel('Time')
plt.axis([0.03,0.15, -0.3, 1.1])
#plt.show()

# Frequency domain - spectrum of sinc pulse
#ax2 = plt.subplot(312)
#plt.plot(tc, A1_c,'-g', label="$X_{sinc}(f)$")
#plt.plot(tc, A2_c,'-b', label='$X_{rcos}(f)$')
#plt.plot(tc, A3_c,'-r', label='$X_{rcos}(f)$')
#plt.grid(True)

# Frequency domain - spectrum of square pulse
#ax3 = plt.subplot(313,sharex=ax2)
#plt.plot(tc, C1_c,'-g', label="$X_{sinc}(f)$")
#plt.plot(tc, C2_c,'-b', label='$X_{rcos}(f)$')
#plt.plot(tc, C3_c,'-r', label='$X_{rcos}(f)$')
#plt.plot(tc, CC_c,'-k', label='$X_{rcos}(f)$')
#plt.grid(True)
plt.savefig('Pulse_shaping_1.eps',format='eps')
plt.show()


