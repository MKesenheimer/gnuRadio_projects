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
from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import gr, pdu
from gnuradio import pdu
from xmlrpc.server import SimpleXMLRPCServer
import threading
import ford_tx_freq_epy_block_0 as epy_block_0  # embedded python block
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
        self.samp_rate = samp_rate = 10000000
        self.payload = payload = str("\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x35\x55\x4c\xb5\x2b\x34\xb4\xb3\x2d\x4b\x2b\x53\x4a\xab\x32\xaa\xb2\xb5\x2c\xd2\xd3\x54\xab\x52\xb5\x4b\x41\xff")
        self.freq_offset = freq_offset = 330000
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
        self.pdu_tagged_stream_to_pdu_0_0 = pdu.tagged_stream_to_pdu(gr.types.complex_t, 'packet_len')
        self.pdu_tagged_stream_to_pdu_0 = pdu.tagged_stream_to_pdu(gr.types.complex_t, 'packet_len')
        self.pdu_pdu_to_tagged_stream_1 = pdu.pdu_to_tagged_stream(gr.types.complex_t, 'packet_len')
        self.pdu_pdu_to_stream_x_0_0 = pdu.pdu_to_stream_b(pdu.EARLY_BURST_APPEND, 64)
        self.pdu_pdu_to_stream_x_0 = pdu.pdu_to_stream_b(pdu.EARLY_BURST_APPEND, 64)
        self.epy_block_0 = epy_block_0.fsk_message_sync_block(payload=payload, period=5000, pause=1000)
        self.blocks_vco_c_0_0 = blocks.vco_c(samp_rate, sensitivity		, 1)
        self.blocks_vco_c_0 = blocks.vco_c(samp_rate, sensitivity		, 1)
        self.blocks_unpack_k_bits_bb_0_0 = blocks.unpack_k_bits_bb(8)
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(8)
        self.blocks_uchar_to_float_0_0 = blocks.uchar_to_float()
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_stream_to_tagged_stream_1_0 = blocks.stream_to_tagged_stream(gr.sizeof_gr_complex, 1, (int(samp_rate/bits_per_second) * 8), "packet_len")
        self.blocks_stream_to_tagged_stream_1 = blocks.stream_to_tagged_stream(gr.sizeof_gr_complex, 1, (int(samp_rate/bits_per_second) * 8), "packet_len")
        self.blocks_repeat_0_0 = blocks.repeat(gr.sizeof_float*1, (int(samp_rate/bits_per_second)))
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_float*1, (int(samp_rate/bits_per_second)))
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_ff((2 * math.pi * freq_spread / sensitivity))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff((2 * math.pi * freq_spread / sensitivity))
        self.blocks_add_const_vxx_0_0 = blocks.add_const_ff((2 * math.pi * (- freq_spread / 2) / sensitivity))
        self.blocks_add_const_vxx_0 = blocks.add_const_ff((2 * math.pi * (- freq_spread / 2) / sensitivity))
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, (-freq_offset), 1, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, freq_offset, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.epy_block_0, 'chan0'), (self.pdu_pdu_to_stream_x_0, 'pdus'))
        self.msg_connect((self.epy_block_0, 'chan1'), (self.pdu_pdu_to_stream_x_0_0, 'pdus'))
        self.msg_connect((self.pdu_tagged_stream_to_pdu_0, 'pdus'), (self.pdu_pdu_to_tagged_stream_1, 'pdus'))
        self.msg_connect((self.pdu_tagged_stream_to_pdu_0_0, 'pdus'), (self.pdu_pdu_to_tagged_stream_1, 'pdus'))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.blocks_add_const_vxx_0_0, 0), (self.blocks_repeat_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_add_const_vxx_0_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_stream_to_tagged_stream_1, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.blocks_stream_to_tagged_stream_1_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_vco_c_0, 0))
        self.connect((self.blocks_repeat_0_0, 0), (self.blocks_vco_c_0_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_1, 0), (self.pdu_tagged_stream_to_pdu_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_1_0, 0), (self.pdu_tagged_stream_to_pdu_0_0, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_uchar_to_float_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.blocks_uchar_to_float_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0_0, 0), (self.blocks_uchar_to_float_0_0, 0))
        self.connect((self.blocks_vco_c_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_vco_c_0_0, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.pdu_pdu_to_stream_x_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))
        self.connect((self.pdu_pdu_to_stream_x_0_0, 0), (self.blocks_unpack_k_bits_bb_0_0, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_1, 0), (self.qtgui_sink_x_0, 0))


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
        self.blocks_add_const_vxx_0.set_k((2 * math.pi * (- self.freq_spread / 2) / self.sensitivity))
        self.blocks_add_const_vxx_0_0.set_k((2 * math.pi * (- self.freq_spread / 2) / self.sensitivity))
        self.blocks_multiply_const_vxx_0.set_k((2 * math.pi * self.freq_spread / self.sensitivity))
        self.blocks_multiply_const_vxx_0_0.set_k((2 * math.pi * self.freq_spread / self.sensitivity))

    def get_sensitivity(self):
        return self.sensitivity

    def set_sensitivity(self, sensitivity):
        self.sensitivity = sensitivity
        self.blocks_add_const_vxx_0.set_k((2 * math.pi * (- self.freq_spread / 2) / self.sensitivity))
        self.blocks_add_const_vxx_0_0.set_k((2 * math.pi * (- self.freq_spread / 2) / self.sensitivity))
        self.blocks_multiply_const_vxx_0.set_k((2 * math.pi * self.freq_spread / self.sensitivity))
        self.blocks_multiply_const_vxx_0_0.set_k((2 * math.pi * self.freq_spread / self.sensitivity))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.blocks_repeat_0.set_interpolation((int(self.samp_rate/self.bits_per_second)))
        self.blocks_repeat_0_0.set_interpolation((int(self.samp_rate/self.bits_per_second)))
        self.blocks_stream_to_tagged_stream_1.set_packet_len((int(self.samp_rate/self.bits_per_second) * 8))
        self.blocks_stream_to_tagged_stream_1.set_packet_len_pmt((int(self.samp_rate/self.bits_per_second) * 8))
        self.blocks_stream_to_tagged_stream_1_0.set_packet_len((int(self.samp_rate/self.bits_per_second) * 8))
        self.blocks_stream_to_tagged_stream_1_0.set_packet_len_pmt((int(self.samp_rate/self.bits_per_second) * 8))
        self.qtgui_sink_x_0.set_frequency_range(self.freq, self.samp_rate)

    def get_payload(self):
        return self.payload

    def set_payload(self, payload):
        self.payload = payload
        self.epy_block_0.payload = self.payload

    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset
        self.analog_sig_source_x_0.set_frequency(self.freq_offset)
        self.analog_sig_source_x_0_0.set_frequency((-self.freq_offset))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.qtgui_sink_x_0.set_frequency_range(self.freq, self.samp_rate)

    def get_bits_per_second(self):
        return self.bits_per_second

    def set_bits_per_second(self, bits_per_second):
        self.bits_per_second = bits_per_second
        self.blocks_repeat_0.set_interpolation((int(self.samp_rate/self.bits_per_second)))
        self.blocks_repeat_0_0.set_interpolation((int(self.samp_rate/self.bits_per_second)))
        self.blocks_stream_to_tagged_stream_1.set_packet_len((int(self.samp_rate/self.bits_per_second) * 8))
        self.blocks_stream_to_tagged_stream_1.set_packet_len_pmt((int(self.samp_rate/self.bits_per_second) * 8))
        self.blocks_stream_to_tagged_stream_1_0.set_packet_len((int(self.samp_rate/self.bits_per_second) * 8))
        self.blocks_stream_to_tagged_stream_1_0.set_packet_len_pmt((int(self.samp_rate/self.bits_per_second) * 8))




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
