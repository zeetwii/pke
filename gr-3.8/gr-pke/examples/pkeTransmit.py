#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: PKE Transmit
# Author: ZeeTulsa
# Description: Flowgraph tha transmits PKE messages
# GNU Radio version: 3.8.2.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import pke

from gnuradio import qtgui

class pkeTransmit(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "PKE Transmit")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("PKE Transmit")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "pkeTransmit")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2e6
        self.pulse_size = pulse_size = 200e-6
        self.offset_freq = offset_freq = 125e6
        self.msg_freq = msg_freq = -134e3
        self.rate_mul = rate_mul = pulse_size / (1/samp_rate)
        self.decodeMul = decodeMul = 4
        self.center_freq = center_freq = msg_freq + offset_freq

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_sink_x_0 = qtgui.sink_f(
            1024, #fftsize
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(False)

        self.top_grid_layout.addWidget(self._qtgui_sink_x_0_win)
        self.pke_pkeGenerator_0 = pke.pkeGenerator('0.0.0.0', 7331, round(rate_mul))
        self.pke_pkeDecoder_0 = pke.pkeDecoder('0.0.0.0', 7331, decodeMul)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_threshold_ff_0 = blocks.threshold_ff(.015, 0.015, 0)
        self.blocks_rms_xx_0 = blocks.rms_cf(1)
        self.blocks_multiply_const_xx_0 = blocks.multiply_const_cc(1, 1)
        self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_float*1, int(int(rate_mul) / decodeMul))
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_multiply_const_xx_0, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.blocks_threshold_ff_0, 0))
        self.connect((self.blocks_multiply_const_xx_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_rms_xx_0, 0), (self.blocks_keep_one_in_n_0, 0))
        self.connect((self.blocks_threshold_ff_0, 0), (self.pke_pkeDecoder_0, 0))
        self.connect((self.blocks_threshold_ff_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_rms_xx_0, 0))
        self.connect((self.pke_pkeGenerator_0, 0), (self.blocks_float_to_complex_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "pkeTransmit")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_rate_mul(self.pulse_size / (1/self.samp_rate))
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_pulse_size(self):
        return self.pulse_size

    def set_pulse_size(self, pulse_size):
        self.pulse_size = pulse_size
        self.set_rate_mul(self.pulse_size / (1/self.samp_rate))

    def get_offset_freq(self):
        return self.offset_freq

    def set_offset_freq(self, offset_freq):
        self.offset_freq = offset_freq
        self.set_center_freq(self.msg_freq + self.offset_freq )

    def get_msg_freq(self):
        return self.msg_freq

    def set_msg_freq(self, msg_freq):
        self.msg_freq = msg_freq
        self.set_center_freq(self.msg_freq + self.offset_freq )

    def get_rate_mul(self):
        return self.rate_mul

    def set_rate_mul(self, rate_mul):
        self.rate_mul = rate_mul
        self.blocks_keep_one_in_n_0.set_n(int(int(self.rate_mul) / self.decodeMul))

    def get_decodeMul(self):
        return self.decodeMul

    def set_decodeMul(self, decodeMul):
        self.decodeMul = decodeMul
        self.blocks_keep_one_in_n_0.set_n(int(int(self.rate_mul) / self.decodeMul))

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq





def main(top_block_cls=pkeTransmit, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
