#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph - highly modified script
# Title: E310_sim_UDP_data_send
# Generated: Sat Jun 17 19:07:24 2017
# Modified: Sat Jun 24 2017
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
import argparse
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes

import numpy

import subprocess
from datetime import datetime

##########################################################
# Global Variables
##########################################################
IP_loopback = '127.0.0.1'
IP_remote_server = '192.168.21.1'
IP_local_eth = '192.168.21.10'
UDP_port = 12345


class E310_sim_UDP_data_send(gr.top_block):
    def __init__(self, args):
        gr.top_block.__init__(self, "E310 UDP Signal Generator")

        ##################################################
        # Variables
        ##################################################
        #    Signal Parameters
        self.sample_rate = args.sample_rate
        self.c_pts = args.c_pts
        self.samples_per_symbols = args.samples_per_symbols
        self.excess_bw = args.excess_bw
        #    Network Connections Parameters
        self.UDP_port = args.UDP_port
        self.ip_address = args.ip_address
        if args.network:
            self.ip_address = args.ip_address
        elif args.loopback:
            self.ip_address = IP_loopback

        ##################################################
        # Blocks
        ##################################################
        self.digital_psk_mod_0 = digital.psk.psk_mod(
            constellation_points=self.c_pts,
            mod_code="none",
            differential=False,
            samples_per_symbol=self.samples_per_symbols,
            excess_bw=self.excess_bw,
            verbose=False,
            log=False,
        )
        self.blocks_udp_sink_0 = blocks.udp_sink(gr.sizeof_gr_complex * 1, self.ip_address, self.UDP_port, 1472, True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex * 1, self.sample_rate, True)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((0.5,))
        self.analog_random_source_x_0 = blocks.vector_source_b(map(int, numpy.random.randint(0, 255, 10000000)), True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_source_x_0, 0), (self.digital_psk_mod_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_udp_sink_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.digital_psk_mod_0, 0), (self.blocks_throttle_0, 0))

    def get_sample_rate(self):
        return self.sample_rate

    def set_sample_rate(self, sample_rate):
        self.sample_rate = sample_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_c_pts(self):
        return self.c_pts

    def set_c_pts(self, c_pts):
        self.c_pts = c_pts

    def get_samples_per_symbols(self):
        return self.samples_per_symbols

    def set_samples_per_symbols(self, samples_per_symbols):
        self.samples_per_symbols = samples_per_symbols

    def get_excess_bw(self):
        return self.excess_bw

    def set_excess_bw(self, excess_bw):
        self.excess_bw = excess_bw

    def get_UDP_port(self):
        return self.UDP_port

    def set_UDP_port(self, UDP_port):
        self.UDP_port = UDP_port

    def get_ip_address(self):
        return self.ip_address

    def set_ip_address(self, ip_address):
        self.ip_address = ip_address


def setup_argparser():
    # Parses a set of input arguments coming from a command line
    parser = argparse.ArgumentParser(
        description='''
                            Script generates a PSK baseband signal and
                            transmits it via UDP protocol to the remote computer (server)''')

    group_signal = parser.add_argument_group('Signal Parameters')

    group_signal.add_argument("-r", "--sampling-rate", dest="sample_rate", type=float, default=2e6,
                              help='''Sets a sampling rate of the generator''')
    group_signal.add_argument("-c", "--constellation", dest="c_pts", type=int, default=4,
                              help="Sets number of constellation points of the PSK modulation")
    group_signal.add_argument("-s", "--samples-per-sym", dest="samples_per_symbols", type=int, default=2,
                              help="Sets number of bits per one data symbol")
    group_signal.add_argument("-e", "--excess-bandwidth", dest="excess_bw", type=float, default=500e-3,
                              help="Sets number of bits per one data symbol")

    group_network = parser.add_argument_group('UDP Connection Parameters')

    group_network.add_argument("-a", "--ip-address", dest="ip_address", default=IP_remote_server,
                               help="Sets remote ip address to send the data stream to")
    group_network.add_argument("-p", "--UDP-port", dest="UDP_port", type=int, default=UDP_port,
                               help="Sets an UDP port")
    group_network.add_argument("-l", "--loopback", action="store_true",
                               help="Sets a default loopback configuration")
    group_network.add_argument("-n", "--network", action="store_true",
                               help="Sets a default network configuration with a remote server ")

    return (parser)


def main():
    args = setup_argparser().parse_args()

    tb = E310_sim_UDP_data_send(args)
    tb.start()

    # Print a nice banner with information on what are the current transmission
	# parameters values and how to change them
    print "-" * 60
    print "Parameters of the signal generator:"
    print "modulation PSK with " , tb.get_c_pts(), " constellation points"
    print "samples per symbol" , tb.get_samples_per_symbols()
    print "excess bandwidth is ", tb.get_excess_bw()
    print "sample rate is" , tb.get_sample_rate()

    print "Parameters of the UDP connection:"
    print "IP address is " , tb.get_ip_address()
    print "UDP port" , tb.get_UDP_port()
    print "-" * 60
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
