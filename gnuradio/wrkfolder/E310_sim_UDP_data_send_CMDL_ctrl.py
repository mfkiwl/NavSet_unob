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
from gnuradio import gr
import argparse
import socket, sys
import numpy



##########################################################
# Global Variables
##########################################################
IP_loopback = '127.0.0.1'
IP_remote_server = '192.168.21.1'
IP_local_eth = '192.168.21.10'
UDP_data_port = 12345
TCP_ctrl_port = 22345


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
        self.UDP_data_port = args.UDP_data_port
        self.TCP_ctrl_port = args.TCP_ctrl_port
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
        self.blocks_udp_sink_0 = blocks.udp_sink(gr.sizeof_gr_complex * 1, self.ip_address, self.UDP_data_port, 1472, True)
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
        self.blocks_throttle_0.set_sample_rate(self.sample_rate)

    def get_c_pts(self):
        return self.c_pts

    def set_c_pts(self, c_pts):
        self.c_pts = c_pts
        self.digital_psk_mod_0.constellation_points = c_pts

    def get_samples_per_symbols(self):
        return self.samples_per_symbols

    def set_samples_per_symbols(self, samples_per_symbols):
        self.samples_per_symbols = samples_per_symbols

    def get_excess_bw(self):
        return self.excess_bw

    def set_excess_bw(self, excess_bw):
        self.excess_bw = excess_bw

    def get_UDP_data_port(self):
        return self.UDP_data_port

    def set_UDP_data_port(self, UDP_data_port):
        self.UDP_data_port = UDP_data_port

    def get_TCP_ctrl_port(self):
        return self.TCP_ctrl_port

    def set_TCP_port(self, TCP_ctrl_port):
        self.TCP_port = TCP_ctrl_port

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

    group_network = parser.add_argument_group('Network Connection Parameters')

    group_network.add_argument("-a", "--ip-address", dest="ip_address", default=IP_remote_server,
                               help="Sets remote ip address to send the data stream to")
    group_network.add_argument("-d", "--UDP-data-port", dest="UDP_data_port", type=int, default=UDP_data_port,
                               help="Sets an UDP port through which the data are sent")
    group_network.add_argument("-p", "--TCP-ctrl-port", dest="TCP_ctrl_port", type=int, default=TCP_ctrl_port,
                               help="Sets an TCP port through which the control commands are received")
    group_network.add_argument("-l", "--loopback", action="store_true",
                               help="Sets a default loopback configuration")
    group_network.add_argument("-n", "--network", action="store_true",
                               help="Sets a default network configuration with a remote server ")

    return (parser)


def main():
    args = setup_argparser().parse_args()

    tb = E310_sim_UDP_data_send(args)
    tb.start()

    c_pts = tb.get_c_pts()
    samples_per_symbols = tb.get_samples_per_symbols()
    excess_bw = tb.get_excess_bw()
    sample_rate = tb.get_sample_rate()

    # Print a nice banner with information on what the current signal generator
    # parameters are
    print "-" * 60
    print "Parameters of the signal generator:"
    print "modulation PSK with " , tb.get_c_pts(), " constellation points"
    print "samples per symbol" , tb.get_samples_per_symbols()
    print "excess bandwidth is ", tb.get_excess_bw()
    print "sample rate is" , tb.get_sample_rate()

    print "Parameters of the network connections:"
    print "IP address is " , tb.get_ip_address()
    print "UDP data port" , tb.get_UDP_data_port()
    print "TCP ctrl port" , tb.get_TCP_ctrl_port()
    print "-" * 60

    while True:
        try:
            # Ask for input
            print "Generator is on now, you can switch it off by pressing CTRL+C."
            print "Please, feel free to change any signal parameter by pressing c, s, r or e followed by an appropriate value."
            parameter_change    = raw_input("Signaling now .. >> ")
            param = parameter_change.split()
            if len(param) == 2:
                if param[0] == "c":
                    c_pts = int(param[1])
                    print "Attempting to change current constellation points to: ", c_pts
                    #tb.set_c_pts(c_pts)
                    c_pts = tb.get_c_pts()
                    print "Number of constellation points is now: ", c_pts
                    print "This parameter can't be changed on runtime"
                elif param[0] == "s":
                    samples_per_symbols = int(param[1])
                    print "Attempting to change current number of samples per symbol to: ", samples_per_symbols
                    #tb.set_samples_per_symbols(samples_per_symbols)
                    samples_per_symbols = tb.get_samples_per_symbols()
                    print "There is ", samples_per_symbols, "samples per symbol being generated now"
                    print "This parameter can't be changed on runtime"
                elif param[0] == "r":
                    sample_rate = float(param[1])
                    print "Attempting to change current sampling rate to: ", sample_rate
                    #tb.set_sample_rate(sample_rate)
                    sample_rate = tb.get_sample_rate()
                    print "Sampling rate is now: ", sample_rate
                    print "This parameter can't be changed on runtime"
                elif param[0] == "e":
                    excess_bw = float(param[1])
                    print "Attempting to change current excess bandwidth to: ", excess_bw
                    #tb.set_excess_bw(excess_bw)
                    excess_bw = tb.get_excess_bw()
                    print "The excess bandwidth is now ", excess_bw
                    print "This parameter can't be changed on runtime"
                else:
                    print "Can't recognize received ", param[0], "parameter."
            elif len(param) == 1:
                if param[0] == "c":
                    c_pts = tb.get_c_pts()
                    print "Current number of constellation points is: ", c_pts
                elif param[0] == "s":
                    samples_per_symbols = tb.get_samples_per_symbols()
                    print "Currently is being generated ", samples_per_symbols, " samples per one symbol."
                elif param[0] == "r":
                    sample_rate = tb.get_sample_rate()
                    print "Current sampling rate is ", sample_rate/1e3, " kSps."
                elif param[0] == "e":
                    excess_bw = tb.get_excess_bw()
                    print "Current excess bandwidth is ", excess_bw
                elif param[0] == "l":
                    # Print a nice banner with information on what the current signal generator
                    # parameters are
                    print "-" * 60
                    print "Parameters of the signal generator:"
                    print "modulation PSK with " , tb.get_c_pts(), " constellation points"
                    print "samples per symbol" , tb.get_samples_per_symbols()
                    print "excess bandwidth is ", tb.get_excess_bw()
                    print "sample rate is" , tb.get_sample_rate()
                elif param[0] == "n":
                    # Print a nice banner with information on what the current network
                    # parameters are
                    print "-" * 60
                    print "Parameters of the network connections:"
                    print "IP address is " , tb.get_ip_address()
                    print "UDP data port" , tb.get_UDP_data_port()
                    print "TCP ctrl port" , tb.get_TCP_ctrl_port()
                    print "-" * 60
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

    # Printing the information to screen
    print 'Signal Generator went off.'

    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
