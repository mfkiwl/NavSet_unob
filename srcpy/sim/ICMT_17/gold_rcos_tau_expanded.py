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

##################### Parameters ######################
f_sampl = 50e3 		# sampling frequency in kHz
T_int = 10.23 		# entire signal length in ms

##################### Simulation TAU = 1 ######################
t = np.arange(0,T_int,1/f_sampl)	# time axis
f = ut.freq_fr_time (t)				# frequency axis
tc = ut.corr_fr_time (t)			# correlation time axis
cd = prn.gold_seq(2,6,1)	# code

tau = 1								# time acceleration factor
Tstr = 10e-3						# transmitted symbol interval
Ts = Tstr/tau						# Nyquist's symbol interval
td = 0								# initial delay of the sequence (time offset)

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

# Frequency Spectrum 
#A1_fft = np.fft.fft(np.real(a1))
#A2_fft = np.fft.fft(np.real(a2))
#A3_fft = np.fft.fft(np.real(a3))
#C_fft = np.fft.fft(np.real( c))

##################### Plots ###########################
f1 = plt.figure(1,figsize=(10, 15), dpi=300)

#  Time domain
f1ax1 = f1.add_subplot(311)
f1ax1.plot(t, a1,'-g', label='$h_{rcos}(t), \\beta = 1.0$')
f1ax1.plot(t, a2,'-b', label='$h_{rcos}(t), \\beta = 0.5$')
f1ax1.plot(t, a3,'-r', label='$h_{rcos}(t), \\beta = 0.0$')
f1ax1.plot(t,  c,'-k', label='$h_{rect}(t)$')
f1ax1.grid(True)
lgd = f1ax1.legend(loc='upper right', bbox_to_anchor=(1.12,1.35))
plt.title('Pulse-shaped baseband signal, $\\tau_A = 1.0$, $\\tau_B = 0.6$, $\\tau_C = 0.3$', loc='left')
f1ax1.set_ylabel('Baseband - voltage')
f1ax1.axis([0, 0.15, -0.3, 1.3])


f2 = plt.figure(2,figsize=(10, 15), dpi=300)

#  Autocorrelated
f2ax1 = f2.add_subplot(311)
f2ax1.plot(tc, A1_c,'-g', label='$h_{rcos}(t), \\beta = 1.0$')
f2ax1.plot(tc, A2_c,'-b', label='$h_{rcos}(t), \\beta = 0.5$')
f2ax1.plot(tc, A3_c,'-r', label='$h_{rcos}(t), \\beta = 0.0$')
f2ax1.plot(tc, CC_c,'-k', label='$h_{rect}(t)$')
f2ax1.grid(True)
lgd = f2ax1.legend(loc='upper right', bbox_to_anchor=(1.05,1.15))
plt.title('Pulse-shaped Autocorrelated, $\\tau_A = 1.0$, $\\tau_B = 0.6$, $\\tau_C = 0.3$', loc='left')
f2ax1.set_ylabel('Baseband - voltage')
f2ax1.axis([-0.25, 0.25, -100, 253000])


f3 = plt.figure(3,figsize=(10, 15), dpi=300)

#  Crossorrelated
f3ax1 = f3.add_subplot(311)
f3ax1.plot(tc, C1_c,'-g', label='$h_{rcos}(t), \\beta = 1.0$')
f3ax1.plot(tc, C2_c,'-b', label='$h_{rcos}(t), \\beta = 0.5$')
f3ax1.plot(tc, C3_c,'-r', label='$h_{rcos}(t), \\beta = 0.0$')
f3ax1.plot(tc, CC_c,'-k', label='$h_{rect}(t)$')
f3ax1.grid(True)
lgd = f3ax1.legend(loc='upper right', bbox_to_anchor=(1.05,1.15))
plt.title('Pulse-shaped Cross-Correlated, $\\tau_A = 1.0$, $\\tau_B = 0.6$, $\\tau_C = 0.3$', loc='left')
f3ax1.set_ylabel('Baseband - voltage')
f3ax1.axis([-0.25, 0.25, 30000, 253000])


#f4 = plt.figure(4,figsize=(10, 15), dpi=300)

#  Frequency Domain
#f4ax1 = f4.add_subplot(311)
#f4ax1.plot(f,  C_fft,'-k', label='$H_{rect}(f)$')

#f4ax1.plot(f, A1_fft,'-g', label='$H_{rcos}(f), \\beta = 1.0$')
#f4ax1.plot(f, A2_fft,'-b', label='$H_{rcos}(f), \\beta = 0.5$')
#f4ax1.plot(f, A3_fft,'-r', label='$H_{rcos}(f), \\beta = 0.0$')

#f4ax1.grid(True)
#lgd = f4ax1.legend(loc='upper right', bbox_to_anchor=(1.05,1.15))
#plt.title('Pulse-shaped Frequency Spectrum, $\\tau_A = 1.0$, $\\tau_B = 0.6$, $\\tau_C = 0.3$', loc='left')
#f4ax1.set_ylabel('$H^A(f)$')
#f4ax1.axis([-500, 1000, -1400, 2500])


##################### Simulation TAU = 0.6 ######################

tau = 0.6							# time acceleration factor
Tstr = 10e-3						# transmitted symbol interval
Ts = Tstr/tau						# Nyquist's symbol interval
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

# Frequency Spectrum 
#A1_fft = np.fft.fft(np.real(a1))
#A2_fft = np.fft.fft(np.real(a2))
#A3_fft = np.fft.fft(np.real(a3))
#C_fft = np.fft.fft(np.real( c))

##################### Plots ###########################

#  Time domain
f1ax2 = f1.add_subplot(312,sharex=f1ax1)
f1ax2.plot(t, a1,'-g', label='$h_{rcos}(t), \\beta = 1.0$')
f1ax2.plot(t, a2,'-b', label='$h_{rcos}(t), \\beta = 0.5$')
f1ax2.plot(t, a3,'-r', label='$h_{rcos}(t), \\beta = 0.0$')
f1ax2.plot(t,  c,'-k', label='$h_{rect}(t)$')
f1ax2.grid(True)
f1ax2.set_ylabel('Baseband - voltage')
f1ax2.axis([0, 0.15, -0.3, 1.3])
#plt.show()

#  Autocorrelated
f2ax2 = f2.add_subplot(312)
f2ax2.plot(tc, A1_c,'-g', label='$h_{rcos}(t), \\beta = 1.0$')
f2ax2.plot(tc, A2_c,'-b', label='$h_{rcos}(t), \\beta = 0.5$')
f2ax2.plot(tc, A3_c,'-r', label='$h_{rcos}(t), \\beta = 0.0$')
f2ax2.plot(tc, CC_c,'-k', label='$h_{rect}(t)$')
f2ax2.grid(True)
f2ax2.set_ylabel('Baseband - voltage')
f2ax2.axis([-0.25, 0.25, 30000, 253000])


#  Crossorrelated
f3ax2 = f3.add_subplot(312)
f3ax2.plot(tc, C1_c,'-g', label='$h_{rcos}(t), \\beta = 1.0$')
f3ax2.plot(tc, C2_c,'-b', label='$h_{rcos}(t), \\beta = 0.5$')
f3ax2.plot(tc, C3_c,'-r', label='$h_{rcos}(t), \\beta = 0.0$')
f3ax2.plot(tc, CC_c,'-k', label='$h_{rect}(t)$')
f3ax2.grid(True)
f3ax2.set_ylabel('Baseband - voltage')
f3ax2.axis([-0.25, 0.25, 70000, 253000])

#  Frequency Domain
#f4ax2 = f4.add_subplot(312)
#f4ax2.plot(f,  C_fft,'-k', label='$H_{rect}(f)$')

#f4ax2.plot(f, A1_fft,'-g', label='$H_{rcos}(f), \\beta = 1.0$')
#f4ax2.plot(f, A2_fft,'-b', label='$H_{rcos}(f), \\beta = 0.5$')
#f4ax2.plot(f, A3_fft,'-r', label='$H_{rcos}(f), \\beta = 0.0$')

#f4ax2.grid(True)
#f4ax2.set_ylabel('$H^B(f)$')
#f4ax2.axis([-500, 1000, -1400, 2500])

##################### Simulation TAU = 0.3 ######################

tau = 0.3								# time acceleration factor
Tstr = 10e-3						# transmitted symbol interval
Ts = Tstr/tau						# Nyquist's symbol interval
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

# Frequency Spectrum 
#A1_fft = np.fft.fft(np.real(a1))
#A2_fft = np.fft.fft(np.real(a2))
#A3_fft = np.fft.fft(np.real(a3))
#C_fft = np.fft.fft(np.real( c))

##################### Plots ###########################

#  Time domain

f1ax3 = f1.add_subplot(313,sharex=f1ax1)
f1ax3.plot(t, a1,'-g', label='$x_{rcos}(t), \\beta = 1.0$')
f1ax3.plot(t, a2,'-b', label='$x_{rcos}(t), \\beta = 0.5$')
f1ax3.plot(t, a3,'-r', label='$x_{rcos}(t), \\beta = 0.0$')
f1ax3.plot(t,  c,'-k', label='$x_{rect}(t)$')
f1ax3.grid(True)
f1ax3.set_ylabel('Baseband - voltage')
f1ax3.set_xlabel('Time')
f1ax3.axis([0, 0.15, -0.3, 1.3])

#  Correlated
f2ax3 = f2.add_subplot(313)
f2ax3.plot(tc, A1_c,'-g', label='$h_{rcos}(t), \\beta = 1.0$')
f2ax3.plot(tc, A2_c,'-b', label='$h_{rcos}(t), \\beta = 0.5$')
f2ax3.plot(tc, A3_c,'-r', label='$h_{rcos}(t), \\beta = 0.0$')
f2ax3.plot(tc, CC_c,'-k', label='transmitted $T_{str}$')
f2ax3.grid(True)
f2ax3.set_ylabel('Baseband - voltage')
f2ax3.set_xlabel('Time')
f2ax3.axis([-0.25, 0.25, 120000, 253000])

#  Crossorrelated
f3ax3 = f3.add_subplot(313)
f3ax3.plot(tc, C1_c,'-g', label='$h_{rcos}(t), \\beta = 1.0$')
f3ax3.plot(tc, C2_c,'-b', label='$h_{rcos}(t), \\beta = 0.5$')
f3ax3.plot(tc, C3_c,'-r', label='$h_{rcos}(t), \\beta = 0.0$')
f3ax3.plot(tc, CC_c,'-k', label='transmitted $T_{str}$')
f3ax3.grid(True)
f3ax3.set_ylabel('Baseband - voltage')
f3ax3.set_xlabel('Time')
f3ax3.axis([-0.25, 0.25, 120000, 253000])

#  Frequency Domain
#f4ax3 = f4.add_subplot(313)
#f4ax3.plot(f,  C_fft,'-k', label='$H_{rect}(f)$')

#f4ax3.plot(f, A1_fft,'-g', label='$H_{rcos}(f), \\beta = 1.0$')
#f4ax3.plot(f, A2_fft,'-b', label='$H_{rcos}(f), \\beta = 0.5$')
#f4ax3.plot(f, A3_fft,'-r', label='$H_{rcos}(f), \\beta = 0.0$')

#f4ax3.grid(True)
#f4ax3.set_ylabel('$H^C(f)$')
#f4ax3.set_xlabel('Frequency')
#f4ax3.axis([-500, 1000, -1400, 2500])


f1.savefig('gold_expanded.eps',format='eps')
f2.savefig('gold_expanded_autocorr.eps',format='eps')
f3.savefig('gold_expanded_crosscorr.eps',format='eps')
#f4.savefig('gold_expanded_fft.eps',format='eps')
plt.show()


