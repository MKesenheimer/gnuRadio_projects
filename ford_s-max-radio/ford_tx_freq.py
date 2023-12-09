#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: kesenheimer
# GNU Radio version: 3.10.8.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import gr, pdu
from gnuradio import network
from xmlrpc.server import SimpleXMLRPCServer
import threading
import math
import sip



class ford_tx_freq(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
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

        self.settings = Qt.QSettings("GNU Radio", "ford_tx_freq")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.freq_spread = freq_spread = 20000
        self.sensitivity = sensitivity = 2 * math.pi * freq_spread
        self.samp_rate = samp_rate = 1000000
        self.freq_offset = freq_offset = -330000
        self.freq = freq = 433930000
        self.bits_per_second = bits_per_second = 4166

        ##################################################
        # Blocks
        ##################################################

        self.xmlrpc_server_0 = SimpleXMLRPCServer(('localhost', 8080), allow_none=True)
        self.xmlrpc_server_0.register_instance(self)
        self.xmlrpc_server_0_thread = threading.Thread(target=self.xmlrpc_server_0.serve_forever)
        self.xmlrpc_server_0_thread.daemon = True
        self.xmlrpc_server_0_thread.start()
        self.qtgui_waterfall_sink_x_1 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            freq, #fc
            samp_rate, #bw
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_1.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_1.enable_grid(False)
        self.qtgui_waterfall_sink_x_1.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_1.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_1.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_1.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_1_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_1.qwidget(), Qt.QWidget)

        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_1_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            freq, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.pdu_pdu_to_tagged_stream_0 = pdu.pdu_to_tagged_stream(gr.types.byte_t, 'packet_len')
        self.network_socket_pdu_0 = network.socket_pdu('TCP_SERVER', '127.0.0.1', '2000', 100, True)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_fcc(1, firdes.complex_band_pass(1, samp_rate, freq_offset - freq_spread/2, freq_offset + freq_spread/2, freq_spread), 0, samp_rate)
        self.blocks_vco_f_0 = blocks.vco_f(samp_rate, sensitivity, 1)
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(8)
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_char*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_char*1, (int(samp_rate/bits_per_second)))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff((2 * math.pi * freq_spread/sensitivity))
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, 'Simulation_Ford_433.93MHz_1Msps.raw', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff((2 * math.pi * (freq_offset - freq_spread / 2)/sensitivity))


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.network_socket_pdu_0, 'pdus'), (self.pdu_pdu_to_tagged_stream_0, 'pdus'))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_vco_f_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_uchar_to_float_0, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.blocks_vco_f_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.qtgui_waterfall_sink_x_1, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ford_tx_freq")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_freq_spread(self):
        return self.freq_spread

    def set_freq_spread(self, freq_spread):
        self.freq_spread = freq_spread
        self.set_sensitivity(2 * math.pi * self.freq_spread)
        self.blocks_add_const_vxx_0.set_k((2 * math.pi * (self.freq_offset - self.freq_spread / 2)/self.sensitivity))
        self.blocks_multiply_const_vxx_0.set_k((2 * math.pi * self.freq_spread/self.sensitivity))
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.complex_band_pass(1, self.samp_rate, self.freq_offset - self.freq_spread/2, self.freq_offset + self.freq_spread/2, self.freq_spread))

    def get_sensitivity(self):
        return self.sensitivity

    def set_sensitivity(self, sensitivity):
        self.sensitivity = sensitivity
        self.blocks_add_const_vxx_0.set_k((2 * math.pi * (self.freq_offset - self.freq_spread / 2)/self.sensitivity))
        self.blocks_multiply_const_vxx_0.set_k((2 * math.pi * self.freq_spread/self.sensitivity))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_repeat_0.set_interpolation((int(self.samp_rate/self.bits_per_second)))
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.complex_band_pass(1, self.samp_rate, self.freq_offset - self.freq_spread/2, self.freq_offset + self.freq_spread/2, self.freq_spread))
        self.qtgui_freq_sink_x_0.set_frequency_range(self.freq, self.samp_rate)
        self.qtgui_waterfall_sink_x_1.set_frequency_range(self.freq, self.samp_rate)

    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset
        self.blocks_add_const_vxx_0.set_k((2 * math.pi * (self.freq_offset - self.freq_spread / 2)/self.sensitivity))
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.complex_band_pass(1, self.samp_rate, self.freq_offset - self.freq_spread/2, self.freq_offset + self.freq_spread/2, self.freq_spread))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.qtgui_freq_sink_x_0.set_frequency_range(self.freq, self.samp_rate)
        self.qtgui_waterfall_sink_x_1.set_frequency_range(self.freq, self.samp_rate)

    def get_bits_per_second(self):
        return self.bits_per_second

    def set_bits_per_second(self, bits_per_second):
        self.bits_per_second = bits_per_second
        self.blocks_repeat_0.set_interpolation((int(self.samp_rate/self.bits_per_second)))




def main(top_block_cls=ford_tx_freq, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
