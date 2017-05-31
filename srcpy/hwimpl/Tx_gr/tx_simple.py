#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Tx Simple
# Generated: Wed May 31 18:22:18 2017
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import numpy
import subprocess
from datetime import datetime


class tx_simple(gr.top_block):

	def __init__(self):
		gr.top_block.__init__(self, "Tx Simple")

		##################################################
		# Variables
		##################################################
 		self.sps = sps = 2
		self.samp_rate = samp_rate = 32000
		self.qpsk_const = qpsk_const = digital.constellation_rect(([-1-1j, -1+1j, 1+1j, 1-1j]), ([0, 1, 3, 2]), 4, 2, 2, 1, 1).base()
		self.f0 = f0 = 1.06e9
		self.Gain_dB = Gain_dB = 30

		##################################################
		# Blocks
		##################################################
		self.uhd_usrp_sink_0 = uhd.usrp_sink(
			",".join(("", "")),
			uhd.stream_args(
				cpu_format="fc32",
			channels=range(1),
			),
		)
		self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
		self.uhd_usrp_sink_0.set_center_freq(f0, 0)
		self.uhd_usrp_sink_0.set_gain(Gain_dB, 0)
		self.uhd_usrp_sink_0.set_antenna('TX0', 0)
		self.digital_constellation_modulator_0 = digital.generic_mod(
			constellation=qpsk_const,
			differential=True,
			samples_per_symbol=sps,
			pre_diff_code=True,
			excess_bw=0.10,
			verbose=False,
			log=False,
			)
		self.analog_random_source_x_0 = blocks.vector_source_b(map(int, numpy.random.randint(0, 2, 1000)), True)

		##################################################
		# Connections
		##################################################
		self.connect((self.analog_random_source_x_0, 0), (self.digital_constellation_modulator_0, 0))       
		self.connect((self.digital_constellation_modulator_0, 0), (self.uhd_usrp_sink_0, 0))    

	def get_sps(self):
		return self.sps

	def set_sps(self, sps):
		self.sps = sps

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

	def get_qpsk_const(self):
		return self.qpsk_const

	def set_qpsk_const(self, qpsk_const):
		self.qpsk_const = qpsk_const

	def get_f0(self):
		return self.f0

	def set_f0(self, f0):
		self.f0 = f0
		self.uhd_usrp_sink_0.set_center_freq(self.f0, 0)

	def get_Gain_dB(self):
		return self.Gain_dB

	def set_Gain_dB(self, Gain_dB):
		self.Gain_dB = Gain_dB
		self.uhd_usrp_sink_0.set_gain(self.Gain_dB, 0)
        	


def main(top_block_cls=tx_simple, options=None):
	# Clear the screen
	subprocess.call('clear', shell=True)

	# Check what time the scan started
	t1 = datetime.now()

	tb = top_block_cls()
	tb.start()
	
	freq = tb.get_Gain_dB()
	gain = tb.get_f0()

	# Print a nice banner with information on which host we are about to scan
	print "-" * 60
	print "Please wait, processing the keyboard input"
	print "frequency is" , freq, "Hz"
	print "gain is" , gain, "dB"
	print "-" * 60	

	while True:
		try:
			# Ask for input
			parameter_change    = raw_input("transmitting now .. >> ")	
			param = parameter_change.split()
			if len(param) == 2:
				if param[0] == "f": 
					freq = float(param[1])
					tb.set_f0(freq)
					print "Frequency changed to:", freq
				elif param[0] == "g":
					gain = int(param[1])
					tb.set_Gain_dB(gain)
					print "Gain changed to:", gain
				else:
					print "Can't recognize received", param[0], "parameter."
			else:
				print "Received", len(param), "parameters. Can't parse, try again."
			pass			
		except ValueError:
			print "Value", param[1], "not valid, Try again."
			pass

		except KeyboardInterrupt:
			print "You have pressed Ctrl+C, it is right time to finish ..."
			break

	print "Received was:", parameter_change
	print "frequency is" , freq, "Hz"
	print "gain is" , gain, "dB"
	# Checking the time again


	# Checking the time again
	t2 = datetime.now()

	# Calculates the difference of time, to see how long it took to run the script
	total =  t2 - t1

	# Printing the information to screen
	print 'Transmission Completed in: ', total


	tb.stop()
	tb.wait()


if __name__ == '__main__':
	main()
