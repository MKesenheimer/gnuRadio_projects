#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: FSK 2-channel TX
# Author: kesenheimer
# GNU Radio version: 3.10.8.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import analog
from gnuradio import blocks
import pmt
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import pdu
from gnuradio import soapy
from xmlrpc.server import SimpleXMLRPCServer
import threading
import FSK_epy_block_0 as epy_block_0  # embedded python block
import math
import numpy as np
import sip



class FSK(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "FSK 2-channel TX", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("FSK 2-channel TX")
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

        self.settings = Qt.QSettings("GNU Radio", "FSK")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 10000000
        self.payload = payload = str("\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x35\x55\x4c\xb5\x2b\x34\xb4\xb3\x2d\x4b\x2b\x53\x4a\xab\x32\xaa\xb2\xb5\x2c\xd2\xd3\x54\xab\x52\xb5\x4b\x41\xff")
        self.padding = padding = 16 * "\xff"
        self.freq_spread = freq_spread = 20000
        self.bits_per_second = bits_per_second = 4166
        self.sensitivity = sensitivity = 2 * math.pi * freq_spread
        self.samples_per_padding = samples_per_padding = int(samp_rate/bits_per_second) * 8 * len(padding)
        self.samples_per_packet = samples_per_packet = int(samp_rate/bits_per_second) * 8 * len(payload)
        self.freq_offset = freq_offset = 330000
        self.freq = freq = 433930000

        ##################################################
        # Blocks
        ##################################################

        self.xmlrpc_server_0 = SimpleXMLRPCServer(('localhost', 8080), allow_none=True)
        self.xmlrpc_server_0.register_instance(self)
        self.xmlrpc_server_0_thread = threading.Thread(target=self.xmlrpc_server_0.serve_forever)
        self.xmlrpc_server_0_thread.daemon = True
        self.xmlrpc_server_0_thread.start()
        self.soapy_hackrf_sink_0 = None
        dev = 'driver=hackrf'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_hackrf_sink_0 = soapy.sink(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_hackrf_sink_0.set_sample_rate(0, samp_rate)
        self.soapy_hackrf_sink_0.set_bandwidth(0, samp_rate)
        self.soapy_hackrf_sink_0.set_frequency(0, freq)
        self.soapy_hackrf_sink_0.set_gain(0, 'AMP', False)
        self.soapy_hackrf_sink_0.set_gain(0, 'VGA', min(max(30, 0.0), 47.0))
        self.qtgui_sink_x_0 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            freq, #fc
            samp_rate, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(False)

        self.top_layout.addWidget(self._qtgui_sink_x_0_win)
        self.pdu_pdu_to_stream_x_0 = pdu.pdu_to_stream_b(pdu.EARLY_BURST_APPEND, len(payload))
        self.epy_block_0 = epy_block_0.fsk_message_sync_block(freq_offset=freq_offset, pause=250)
        self.blocks_vco_c_0 = blocks.vco_c(samp_rate, sensitivity		, 1)
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(8)
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_gr_complex, 1, samples_per_packet, "packet_len")
        self.blocks_stream_mux_0_0 = blocks.stream_mux(gr.sizeof_gr_complex*1, (samples_per_padding, samples_per_packet))
        self.blocks_stream_mux_0 = blocks.stream_mux(gr.sizeof_gr_complex*1, (samples_per_packet + samples_per_padding, samples_per_padding))
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_float*1, (int(samp_rate/bits_per_second)))
        self.blocks_null_source_0_0 = blocks.null_source(gr.sizeof_gr_complex*1)
        self.blocks_null_source_0 = blocks.null_source(gr.sizeof_gr_complex*1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff((2 * math.pi * freq_spread / sensitivity))
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.string_to_symbol(payload), 5000)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff((2 * math.pi * (- freq_spread / 2) / sensitivity))
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 0, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.epy_block_0, 'trigger'))
        self.msg_connect((self.epy_block_0, 'freq'), (self.analog_sig_source_x_0, 'cmd'))
        self.msg_connect((self.epy_block_0, 'payload'), (self.pdu_pdu_to_stream_x_0, 'pdus'))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.blocks_null_source_0, 0), (self.blocks_stream_mux_0, 1))
        self.connect((self.blocks_null_source_0_0, 0), (self.blocks_stream_mux_0_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_vco_c_0, 0))
        self.connect((self.blocks_stream_mux_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.blocks_stream_mux_0, 0), (self.soapy_hackrf_sink_0, 0))
        self.connect((self.blocks_stream_mux_0_0, 0), (self.blocks_stream_mux_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.blocks_stream_mux_0_0, 1))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.blocks_uchar_to_float_0, 0))
        self.connect((self.blocks_vco_c_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.pdu_pdu_to_stream_x_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "FSK")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_samples_per_packet(int(self.samp_rate/self.bits_per_second) * 8 * len(self.payload))
        self.set_samples_per_padding(int(self.samp_rate/self.bits_per_second) * 8 * len(self.padding))
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.blocks_repeat_0.set_interpolation((int(self.samp_rate/self.bits_per_second)))
        self.qtgui_sink_x_0.set_frequency_range(self.freq, self.samp_rate)
        self.soapy_hackrf_sink_0.set_sample_rate(0, self.samp_rate)
        self.soapy_hackrf_sink_0.set_bandwidth(0, self.samp_rate)

    def get_payload(self):
        return self.payload

    def set_payload(self, payload):
        self.payload = payload
        self.set_samples_per_packet(int(self.samp_rate/self.bits_per_second) * 8 * len(self.payload))
        self.blocks_message_strobe_0.set_msg(pmt.string_to_symbol(self.payload))
        self.pdu_pdu_to_stream_x_0.set_max_queue_size(len(self.payload))

    def get_padding(self):
        return self.padding

    def set_padding(self, padding):
        self.padding = padding
        self.set_samples_per_padding(int(self.samp_rate/self.bits_per_second) * 8 * len(self.padding))

    def get_freq_spread(self):
        return self.freq_spread

    def set_freq_spread(self, freq_spread):
        self.freq_spread = freq_spread
        self.set_sensitivity(2 * math.pi * self.freq_spread)
        self.blocks_add_const_vxx_0.set_k((2 * math.pi * (- self.freq_spread / 2) / self.sensitivity))
        self.blocks_multiply_const_vxx_0.set_k((2 * math.pi * self.freq_spread / self.sensitivity))

    def get_bits_per_second(self):
        return self.bits_per_second

    def set_bits_per_second(self, bits_per_second):
        self.bits_per_second = bits_per_second
        self.set_samples_per_packet(int(self.samp_rate/self.bits_per_second) * 8 * len(self.payload))
        self.set_samples_per_padding(int(self.samp_rate/self.bits_per_second) * 8 * len(self.padding))
        self.blocks_repeat_0.set_interpolation((int(self.samp_rate/self.bits_per_second)))

    def get_sensitivity(self):
        return self.sensitivity

    def set_sensitivity(self, sensitivity):
        self.sensitivity = sensitivity
        self.blocks_add_const_vxx_0.set_k((2 * math.pi * (- self.freq_spread / 2) / self.sensitivity))
        self.blocks_multiply_const_vxx_0.set_k((2 * math.pi * self.freq_spread / self.sensitivity))

    def get_samples_per_padding(self):
        return self.samples_per_padding

    def set_samples_per_padding(self, samples_per_padding):
        self.samples_per_padding = samples_per_padding

    def get_samples_per_packet(self):
        return self.samples_per_packet

    def set_samples_per_packet(self, samples_per_packet):
        self.samples_per_packet = samples_per_packet
        self.blocks_stream_to_tagged_stream_0.set_packet_len(self.samples_per_packet)
        self.blocks_stream_to_tagged_stream_0.set_packet_len_pmt(self.samples_per_packet)

    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset
        self.epy_block_0.freq_offset = self.freq_offset

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.qtgui_sink_x_0.set_frequency_range(self.freq, self.samp_rate)
        self.soapy_hackrf_sink_0.set_frequency(0, self.freq)




def main(top_block_cls=FSK, options=None):

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
