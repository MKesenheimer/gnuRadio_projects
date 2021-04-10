#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: kesenheimer
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

from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
import inspector
from gnuradio import qtgui
import sip
import osmosdr
import time

from gnuradio import qtgui

class ofdm_analyze(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
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

        self.settings = Qt.QSettings("GNU Radio", "ofdm_analyze")

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
        self.thres = thres = -75
        self.samp_rate = samp_rate = 500e3
        self.freq = freq = 4345e5
        self.fft_length = fft_length = 1024*4

        ##################################################
        # Blocks
        ##################################################
        self._thres_range = Range(-120, 50, 1, -75, 200)
        self._thres_win = RangeWidget(self._thres_range, self.set_thres, 'Threshold', "counter_slider", float)
        self.top_grid_layout.addWidget(self._thres_win)
        self.rtlsdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ''
        )
        self.rtlsdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(freq, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(40, 0)
        self.rtlsdr_source_0.set_if_gain(40, 0)
        self.rtlsdr_source_0.set_bb_gain(40, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
        self.inspector_signal_detector_cvf_0 = inspector.signal_detector_cvf(samp_rate, fft_length, firdes.WIN_BLACKMAN_hARRIS, thres,  0.2, False, 0.2, 0.001, 5000, '')
        self.inspector_qtgui_sink_vf_0 = inspector.qtgui_inspector_sink_vf(
          samp_rate,
          fft_length,
          freq,
          1,
          1,
          False
        )
        self._inspector_qtgui_sink_vf_0_win = sip.wrapinstance(self.inspector_qtgui_sink_vf_0.pyqwidget(), Qt.QWidget)

        self.top_grid_layout.addWidget(self._inspector_qtgui_sink_vf_0_win)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.inspector_signal_detector_cvf_0, 'map_out'), (self.inspector_qtgui_sink_vf_0, 'map_in'))
        self.connect((self.inspector_signal_detector_cvf_0, 0), (self.inspector_qtgui_sink_vf_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.inspector_signal_detector_cvf_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ofdm_analyze")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_thres(self):
        return self.thres

    def set_thres(self, thres):
        self.thres = thres
        self.inspector_signal_detector_cvf_0.set_threshold(self.thres)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.inspector_qtgui_sink_vf_0.set_samp_rate(self.samp_rate)
        self.inspector_signal_detector_cvf_0.set_samp_rate(self.samp_rate)
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.inspector_qtgui_sink_vf_0.set_cfreq(self.freq)
        self.rtlsdr_source_0.set_center_freq(self.freq, 0)

    def get_fft_length(self):
        return self.fft_length

    def set_fft_length(self, fft_length):
        self.fft_length = fft_length
        self.inspector_signal_detector_cvf_0.set_fft_len(self.fft_length)





def main(top_block_cls=ofdm_analyze, options=None):

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
