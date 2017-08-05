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
f_sampl = 900e6 		# sampling frequency in Hz
T_int = 0.001 			# entire signal length in s

##################### Simulation BASEBAND ######################
t = np.arange(0,T_int,1/f_sampl)	# time axis
#f = ut.freq_fr_time (t)				# frequency axis
#cd = np.array([1,1,1,0,1,1,1,1,0,1,0,0,1,0,1]) # code
cd = prn.gold_seq(2,6,1)
Ts = 1/1023							# Nyquist's symbol interval
tau = 0.3							# time acceleration factor
Tstr = Ts * tau						# transmitted symbol interval
bitrate  = 1/Tstr
td = 0.0							# initial delay of the sequence (time offset)

# baseband signals
a1 = mod.rcos_bpsk_map(t,cd,bitrate,pw = Ts,alpha = 1.0,td=Tstr/2)
#a2 = mod.rcos_bpsk_map(t,cd,bitrate,pw = Ts,alpha = 0.5)
#a3 = mod.rcos_bpsk_map(t,cd,bitrate,pw = Ts,alpha = 0.0)
c  = gen.rect_tr(t,Tstr,0,td,cd)


##################### Plots ###########################
#plt.figure(1,figsize=(10, 8), dpi=300)

#  Time domain

#ax1 = plt.subplot(311)
#plt.plot(t, np.real(a1),'-r', label='$h_{rcos}(t), \\beta = 1.0$')
#plt.plot(t, np.real(a2),'-b', label='$h_{rcos}(t), \\beta = 0.5$')
#plt.plot(t, np.real(a3),'-g', label='$h_{rcos}(t), \\beta = 0.0$')
#plt.plot(t,  c,'-k', label='$x_{rect}(t)$')
#plt.grid(True)
#plt.legend(loc='upper left', bbox_to_anchor=(1.12,1.35))
#plt.title('Pulse-shaped baseband signal')
#plt.ylabel('$h(t)$')
#plt.xlabel('Time')
#plt.axis([0, 1, -1.6, 1.5])

#plt.savefig('gold_2_6_tau1_bb.eps',format='eps')

#plt.show()

##################### Simulation PASSBAND ######################

fc = 60e6			# carrier frequency in Hz


a1_fc = upcon.quad_mod(a1,t,fc,0,0,0)
#a2_fc = upcon.quad_mod(a2,t,fc,0,0,0)
#a3_fc = upcon.quad_mod(a3,t,fc,0,0,0)
c_fc  = upcon.quad_mod( c,t,fc,0,0,0)


a1_fc.tofile("data_a1_gold.txt",format='%.5f',sep=',')
##################### Plots ###########################
plt.figure(2,figsize=(10, 8), dpi=300)

#  Time domain

#ax1 = plt.subplot(311)
#plt.plot(t, a1_fc,'-r', label='$s_{m,rcos}(t), \\beta = 1.0$')
#plt.plot(t, np.real(a1),'-b', label='$h_{rcos}(t), \\beta = 1.0$')
#plt.plot(t, np.imag(a1),'-g', label='$h_{rcos}(t), \\beta = 1.0$')
#plt.plot(t, a1_fc,'-b', label='$s_{m,rcos}(t), \\beta = 0.5$')
#plt.plot(t, a1_fc,'-g', label='$s_{m,rcos}(t), \\beta = 0.0$')
#plt.plot(t,  c,'-k', label='$x_{m,rect}(t)$')
#plt.grid(True)
#plt.legend(loc='upper left', bbox_to_anchor=(1.12,1.35))
#plt.title('Pulse-shaped baseband signal')
#plt.ylabel('$s_{m}(t)$')
#plt.xlabel('Time')
#plt.axis([0, 0.01, -1.6, 1.5])

#plt.savefig('seq_tau04_pb.eps',format='eps')

#plt.show()

