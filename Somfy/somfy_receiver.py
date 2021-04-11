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

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from OOK_demodulator_improved import OOK_demodulator_improved  # grc-generated hier_block
from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
import pmt
from gnuradio import gr
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation

from gnuradio import qtgui

class somfy_receiver(gr.top_block, Qt.QWidget):

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

        self.settings = Qt.QSettings("GNU Radio", "somfy_receiver")

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
        self.samp_rate = samp_rate = 2.4e6
        self.fmid = fmid = 868.949e6
        self.dfctr3 = dfctr3 = 0
        self.dfctr2 = dfctr2 = -19.2e3
        self.dfctr1 = dfctr1 = 19.2e3
        self.baud_rate = baud_rate = 4800*4

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_freq_sink_x_1 = qtgui.freq_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            3
        )
        self.qtgui_freq_sink_x_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_1.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_1.enable_grid(False)
        self.qtgui_freq_sink_x_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1.enable_control_panel(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(3):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_1_win)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_null_sink_0_0_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/Users/kesenheimer/Documents/Basteln/SDR/gnuRadio_projects/io-home/somfy_868.949MHz_2.4Mss.complex', False, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.OOK_demodulator_improved_0_1 = OOK_demodulator_improved(
            fbaud=baud_rate,
            freq=dfctr2,
            offset=0.5,
            re_samp_rate=96000,
            samp_rate=samp_rate,
        )
        self.OOK_demodulator_improved_0_0 = OOK_demodulator_improved(
            fbaud=baud_rate,
            freq=dfctr3,
            offset=0,
            re_samp_rate=96000,
            samp_rate=samp_rate,
        )
        self.OOK_demodulator_improved_0 = OOK_demodulator_improved(
            fbaud=baud_rate,
            freq=dfctr1,
            offset=-0.5,
            re_samp_rate=96000,
            samp_rate=samp_rate,
        )



        ##################################################
        # Connections
        ##################################################
        self.connect((self.OOK_demodulator_improved_0, 1), (self.blocks_null_sink_0, 0))
        self.connect((self.OOK_demodulator_improved_0, 2), (self.qtgui_freq_sink_x_1, 0))
        self.connect((self.OOK_demodulator_improved_0_0, 1), (self.blocks_null_sink_0_0_0, 0))
        self.connect((self.OOK_demodulator_improved_0_0, 2), (self.qtgui_freq_sink_x_1, 1))
        self.connect((self.OOK_demodulator_improved_0_1, 1), (self.blocks_null_sink_0_0, 0))
        self.connect((self.OOK_demodulator_improved_0_1, 2), (self.qtgui_freq_sink_x_1, 2))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.OOK_demodulator_improved_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.OOK_demodulator_improved_0_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.OOK_demodulator_improved_0_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "somfy_receiver")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.OOK_demodulator_improved_0.set_samp_rate(self.samp_rate)
        self.OOK_demodulator_improved_0_0.set_samp_rate(self.samp_rate)
        self.OOK_demodulator_improved_0_1.set_samp_rate(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.qtgui_freq_sink_x_1.set_frequency_range(0, self.samp_rate)

    def get_fmid(self):
        return self.fmid

    def set_fmid(self, fmid):
        self.fmid = fmid

    def get_dfctr3(self):
        return self.dfctr3

    def set_dfctr3(self, dfctr3):
        self.dfctr3 = dfctr3
        self.OOK_demodulator_improved_0_0.set_freq(self.dfctr3)

    def get_dfctr2(self):
        return self.dfctr2

    def set_dfctr2(self, dfctr2):
        self.dfctr2 = dfctr2
        self.OOK_demodulator_improved_0_1.set_freq(self.dfctr2)

    def get_dfctr1(self):
        return self.dfctr1

    def set_dfctr1(self, dfctr1):
        self.dfctr1 = dfctr1
        self.OOK_demodulator_improved_0.set_freq(self.dfctr1)

    def get_baud_rate(self):
        return self.baud_rate

    def set_baud_rate(self, baud_rate):
        self.baud_rate = baud_rate
        self.OOK_demodulator_improved_0.set_fbaud(self.baud_rate)
        self.OOK_demodulator_improved_0_0.set_fbaud(self.baud_rate)
        self.OOK_demodulator_improved_0_1.set_fbaud(self.baud_rate)





def main(top_block_cls=somfy_receiver, options=None):

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
