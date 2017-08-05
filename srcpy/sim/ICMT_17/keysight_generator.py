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
T_int = 0.005115 			# entire signal length in s

##################### Simulation BASEBAND ######################
t = np.arange(0,T_int,1/f_sampl)	# time axis
#f = ut.freq_fr_time (t)				# frequency axis
#cd = np.array([1,1,1,0,1,1,1,1,0,1,0,0,1,0,1]) # code
x1 = 2				# tap 1 to generate G2 in goldcode generator
x2 = 6				# tap 2 to generate G2 in goldcode generator
cd = prn.gold_seq(x1,x2,1)
Tstr = 5e-6						# Nyquist's symbol interval
tau = 0.35							# time acceleration factor
Ts = Tstr / tau						# transmitted symbol interval
bitrate  = 1/Tstr
td = 0.0							# initial delay of the sequence (time offset)

# baseband signals
a1 = mod.rcos_bpsk_map(t,cd,bitrate,pw = Ts,alpha = 1.0,td=Tstr/2)
a2 = mod.rcos_bpsk_map(t,cd,bitrate,pw = Ts,alpha = 0.5,td=Tstr/2)
a3 = mod.rcos_bpsk_map(t,cd,bitrate,pw = Ts,alpha = 0.0,td=Tstr/2)
c  = gen.rect_tr(t,Tstr,0,td,cd)

##################### Simulation PASSBAND ######################

fc = 60e6			# carrier frequency in Hz


a1_fc = upcon.quad_mod(a1,t,fc,0,0,0)
a2_fc = upcon.quad_mod(a2,t,fc,0,0,0)
a3_fc = upcon.quad_mod(a3,t,fc,0,0,0)
c_fc  = upcon.quad_mod( c,t,fc,0,0,0)

##################### files ######################
filename = "ts5_prn{0:1}{1:1}_tau{2:6.2}_a1.dat".format(x1,x2,tau)
a1_fc.tofile(filename,format='%.5f',sep=',')

filename = "ts5_prn{0:1}{1:1}_tau{2:6.2}_a2.dat".format(x1,x2,tau)
a2_fc.tofile(filename,format='%.5f',sep=',')

filename = "ts5_prn{0:1}{1:1}_tau{2:6.2}_a3.dat".format(x1,x2,tau)
a3_fc.tofile(filename,format='%.5f',sep=',')

filename = "ts5_prn{0:1}{1:1}_tau{2:6.2}_rec.dat".format(x1,x2,tau)
c_fc.tofile(filename,format='%.5f',sep=',')


