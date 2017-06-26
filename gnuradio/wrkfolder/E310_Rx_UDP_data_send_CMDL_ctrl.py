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
from gnuradio import uhd
try:
    from uhd_app import UHDApp
except ImportError:
    from gnuradio.uhd.uhd_app import UHDApp
import numpy



##########################################################
# Global Variables
##########################################################
IP_loopback = '127.0.0.1'
IP_remote_server = '192.168.21.1'
IP_local_eth = '192.168.21.10'
UDP_data_port = 12345
TCP_ctrl_port = 22345


class E310_Rx_UDP_data_send(gr.top_block, UHDApp):
    def __init__(self, args):
        gr.top_block.__init__(self, "E310 Rx remote")

        ##################################################
        # Parameters
        ##################################################
        self.args = args

        self.verbose = args.verbose
        self.prefix = args.prefix = None
        self.sample_rate = args.samp_rate


        #    UHD Radio Receiver Parameters
        self.antenna = args.antenna
        self.freq = args.freq
        self.gain = args.gain_type
        self.gain_type = args.gain_type
        self.spec = args.spec
        self.stream_args = args.stream_args
        self.wire_format = args.otw_format

        #    Network Connections Parameters
        self.UDP_data_port = args.UDP_data_port
        self.TCP_ctrl_port = args.TCP_ctrl_port
        self.ip_address = args.ip_address
        if args.network:
            self.ip_address = args.ip_address
        elif args.loopback:
            self.ip_address = IP_loopback

        ##################################################
        # Variables
        ##################################################

        self.usrp_device_info = "[No USRP Device Info Found!]"
        self.uhd_version_info = uhd.get_version_string()



        ##################################################
        # Blocks
        ##################################################
        self.setup_usrp(uhd.usrp_source, args)
        self._ant_options = self.usrp.get_antennas(self.channels[0])
        for c in self.channels:
            self.usrp.set_bandwidth(self.sample_rate, c)
            tr = uhd.tune_request(self.freq)
            self.usrp.set_center_freq  (tr, c)
        self.usrp_device_info = self.get_usrp_info_string(compact=True, tx_or_rx='rx')
        self.bandwidth = self.usrp.get_bandwidth (0)

        self.blocks_udp_sink_0 = blocks.udp_sink(gr.sizeof_gr_complex * 1, self.ip_address, self.UDP_data_port, 1472, True)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.usrp, 0), (self.blocks_udp_sink_0, 0))


    def get_sample_rate(self):
        return self.sample_rate

    def set_sample_rate(self, sample_rate):
        self.sample_rate = sample_rate
        self.usrp.set_samp_rate(self.samp_rate)
        self.usrp.set_bandwidth(self.samp_rate, 0)

    def get_UDP_data_port(self):
        return self.UDP_data_port

    def set_UDP_data_port(self, UDP_data_port):
        self.UDP_data_port = UDP_data_port
        self.blocks_udp_sink_0.disconnect()
        self.blocks_udp_sink_0.connect(self.ip_address, self.UDP_data_port)

    def get_TCP_ctrl_port(self):
        return self.TCP_ctrl_port

    def set_TCP_port(self, TCP_ctrl_port):
        self.TCP_port = TCP_ctrl_port

    def get_ip_address(self):
        return self.ip_address

    def set_antenna(self, antenna):
        self.antenna = antenna
        self.set_ant(self.antenna)

    def set_args(self, args):
        self.args = args

    def get_usrp_device_info(self):
        return self.usrp_device_info

    def get_uhd_version_info(self):
        return self.uhd_version_info

    def get_lo_names(self):
        return self.usrp.get_lo_names(0)

    def get_lo_freq_range(self):
        return self.usrp.get_lo_freq_range('',0)

    def get_center_freq (self):
        return self.usrp.get_center_freq (0)

    def get_bandwidth (self):
        return self.usrp.get_bandwidth (0)

    def get_bandwidth_range (self):
        return self.usrp.get_bandwidth_range (0)

    def get_gain_range(self):
        return self.usrp.get_gain_range('',0)

    def get_gain (self):
        return self.usrp.get_gain (0)

    def get_normalized_gain (self):
        return self.usrp.get_normalized_gain (0)

    def set_center_freq (self,freq):
        self.usrp.set_center_freq (freq, 0)
        self.freq = self.usrp.get_center_freq (0)

    def set_bandwidth (self,bw):
        self.usrp.set_bandwidth (bw, 0)
        self.bandwidth = self.usrp.get_bandwidth (0)

    def set_gain (self,gain):
        self.usrp.set_gain (gain, 0)
        self.gain = self.usrp.get_gain (0)

def setup_argparser():
    # Parses a set of input arguments coming from a command line
    parser = UHDApp.setup_argparser(
            description="UHD Receiver",
            tx_or_rx="Rx")

    group_network = parser.add_argument_group('Network Connection Parameters')

    group_network.add_argument("-i", "--ip-address", dest="ip_address", default=IP_remote_server,
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

    tb = E310_Rx_UDP_data_send(args)
    tb.start()


    # Print a nice banner with information on what the current signal generator
    # parameters are
    print "-" * 60
    print "Parameters of the USRP radio:"
    print "USRP device info: " , tb.get_usrp_device_info()
    print "UHD driver info: " , tb.get_uhd_version_info()
    print "sample rate is" , tb.get_sample_rate() / 1e3, "kSps"

    print "Available LO stages: " , tb.get_lo_names()
    print "Available LO frequency range: " , tb.get_lo_freq_range(), "in Hz"
    print "Current center frequency: " , tb.get_center_freq ()/1e6, "MHz"
    print "Available RF bandpass filter bandwidth range: " , tb.get_bandwidth_range (), "in Hz"
    print "Current RF bandpass filter setting: " , tb.get_bandwidth ()/1e6, "MHz"
    print "Available gain range: " , tb.get_gain_range(), "in dB"
    print "Current RF gain: " , tb.get_gain (), "dB, normalized gain: ", tb.get_normalized_gain ()

    print "-" * 60
    print "Parameters of the network connections:"
    print "IP address is " , tb.get_ip_address()
    print "UDP data port" , tb.get_UDP_data_port()
    print "TCP ctrl port" , tb.get_TCP_ctrl_port()
    print "-" * 60

    while True:
        try:
            # Ask for input
            print "Receiver is on now, you can switch it off by pressing CTRL+C."
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
    print 'The receiver went off.'

    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
