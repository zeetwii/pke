#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: PKE Transmit
# Author: ZeeTulsa
# GNU Radio version: v3.10.0.0git-316-gb6851218

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import soapy
from xmlrpc.server import SimpleXMLRPCServer
import threading
import pke




class pke_transmit(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "PKE Transmit", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2e6
        self.offset_freq = offset_freq = 125e6
        self.msg_freq = msg_freq = 134e3
        self.bit_period = bit_period = 200e-6
        self.rate_mul = rate_mul = samp_rate / (1/bit_period)
        self.center_freq = center_freq = msg_freq + offset_freq

        ##################################################
        # Blocks
        ##################################################
        self.xmlrpc_server_0 = SimpleXMLRPCServer(('127.0.0.1', 8080), allow_none=True)
        self.xmlrpc_server_0.register_instance(self)
        self.xmlrpc_server_0_thread = threading.Thread(target=self.xmlrpc_server_0.serve_forever)
        self.xmlrpc_server_0_thread.daemon = True
        self.xmlrpc_server_0_thread.start()
        self.soapy_hackrf_sink_0 = None
        dev = 'driver=hackrf'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_hackrf_sink_0 = soapy.sink(dev, "fc32", 1, 'hackrf=0',
                                  stream_args, tune_args, settings)
        self.soapy_hackrf_sink_0.set_sample_rate(0, samp_rate)
        self.soapy_hackrf_sink_0.set_bandwidth(0, 0)
        self.soapy_hackrf_sink_0.set_frequency(0, center_freq)
        self.soapy_hackrf_sink_0.set_gain(0, 'AMP', 14)
        self.soapy_hackrf_sink_0.set_gain(0, 'VGA', min(max(47, 0.0), 47.0))
        self.pke_pkeGenerator_0 = pke.pkeGenerator('0.0.0.0', 7331, int(rate_mul))
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_float_to_complex_0, 0), (self.soapy_hackrf_sink_0, 0))
        self.connect((self.pke_pkeGenerator_0, 0), (self.blocks_float_to_complex_0, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_rate_mul(self.samp_rate / (1/self.bit_period))
        self.soapy_hackrf_sink_0.set_sample_rate(0, self.samp_rate)

    def get_offset_freq(self):
        return self.offset_freq

    def set_offset_freq(self, offset_freq):
        self.offset_freq = offset_freq
        self.set_center_freq(self.msg_freq + self.offset_freq)

    def get_msg_freq(self):
        return self.msg_freq

    def set_msg_freq(self, msg_freq):
        self.msg_freq = msg_freq
        self.set_center_freq(self.msg_freq + self.offset_freq)

    def get_bit_period(self):
        return self.bit_period

    def set_bit_period(self, bit_period):
        self.bit_period = bit_period
        self.set_rate_mul(self.samp_rate / (1/self.bit_period))

    def get_rate_mul(self):
        return self.rate_mul

    def set_rate_mul(self, rate_mul):
        self.rate_mul = rate_mul

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.soapy_hackrf_sink_0.set_frequency(0, self.center_freq)




def main(top_block_cls=pke_transmit, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
