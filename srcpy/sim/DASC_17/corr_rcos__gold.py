#!/usr/bin/env python

"""
This is a test bed script to plot a bitsteam with its
symbols shaped. 
"""
import sys
sys.path.append("../../sim")

from timeit import default_timer as timer
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
from siggens import train_pulse as gen
from siggens import PRN_bitstreams as prn
from utils import freqaxis_shape as ut

##################### Parameters ######################
f_sampl = 50e3 		# sampling frequency in kHz
T_int = 30 			# entire signal length in ms

##################### Simulation ######################
t = np.arange(0,T_int,1/f_sampl)	# time axis
f = ut.freq_fr_time (t)				# frequency axis
tc = ut.corr_fr_time (t)			# correlation time axis
cd = prn.gold_seq(3,5,no_periods = 3)	# code
Ts = 10e-3							# Nyquist's symbol interval
tau = 0.3							# time acceleration factor
Tstr = Ts * tau						# transmitted symbol interval
td = 0.05							# initial delay of the sequence (time offset)

# Time Domain
a1 = gen.rcos_tr(t,Tstr,td + Tstr/2,cd,Ts,1.0)
#c  = gen.rect_tr(t,Tstr,0,td,cd)

print ("Length of the signal", np.size(a1))

# Correlate processor
#ts = timer()
#A1_c = signal.correlate(a1,a1,'full')
#C1_c = signal.correlate( c,a1,'full')
#CC_c = signal.correlate( c, c,'full')
#te = timer()
#print('CPU: %.2fs' % (te - ts))

##################### Plots ###########################
#plt.figure(1,figsize=(10, 15), dpi=300)

#  Time domain

#ax1 = plt.subplot(211)
#plt.plot(t, a1,'-r', label='$x_{rcos}(t)$')
#plt.plot(t,  c,'-k', label='$x_{rect}(t)$')
#plt.legend(loc='upper right', bbox_to_anchor=(1.12,1.1))
#plt.grid(True)

#plt.title('Pulse-shaped baseband signal')
#plt.ylabel('Voltage')
#plt.xlabel('Time')
#plt.axis([0, 10, -0.3, 1.3])


# Frequency domain - spectrum of sinc pulse
#ax2 = plt.subplot(212)
#plt.plot(tc, A1_c,'-r', label="autocorr rcos")
#plt.plot(tc, C1_c,'-r', label="cross-corr")
#plt.plot(tc, CC_c,'-k', label='autocorr rect')
#plt.grid(True)
#plt.savefig('corr_fnc.eps',format='eps')
#plt.show()

