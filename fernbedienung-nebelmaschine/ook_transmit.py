#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Ook Transmit
# GNU Radio version: 3.10.8.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import blocks
import pmt
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
from gnuradio import iio
from gnuradio import pdu
import sip



class ook_transmit(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Ook Transmit", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Ook Transmit")
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

        self.settings = Qt.QSettings("GNU Radio", "ook_transmit")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.payload = payload = str("\x84\x21\x08\x42\x10\x84\x21\x08\x42\x10\xee\x84\x21\x08\x42")
        self.padding = padding = 400*"\x00"
        self.samples_per_symbol = samples_per_symbol = 1000
        self.samp_rate = samp_rate = 10e6
        self.payload_bytes = payload_bytes = [ord(i) for i in payload]
        self.padding_bytes = padding_bytes = [ord(i) for i in padding]
        self.carrier_freq = carrier_freq = 314980000
        self.bits_per_pack = bits_per_pack = 2

        ##################################################
        # Blocks
        ##################################################

        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=int(samples_per_symbol),
                decimation=1,
                taps=[1],
                fractional_bw=0)
        self.qtgui_sink_x_0 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            carrier_freq, #fc
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

        self.qtgui_sink_x_0.enable_rf_freq(True)

        self.top_layout.addWidget(self._qtgui_sink_x_0_win)
        self.pdu_pdu_to_stream_x_0 = pdu.pdu_to_stream_b(pdu.EARLY_BURST_APPEND, (len(payload)+len(padding)))
        self.iio_pluto_sink_0 = iio.fmcomms2_sink_fc32('' if '' else iio.get_pluto_uri(), [True, True], 32768, False)
        self.iio_pluto_sink_0.set_len_tag_key('')
        self.iio_pluto_sink_0.set_bandwidth(20000000)
        self.iio_pluto_sink_0.set_frequency(carrier_freq)
        self.iio_pluto_sink_0.set_samplerate(int(samp_rate))
        self.iio_pluto_sink_0.set_attenuation(0, 0.0)
        self.iio_pluto_sink_0.set_filter_params('Auto', '', 0, 0)
        self.blocks_unpack_k_bits_bb_0_0 = blocks.unpack_k_bits_bb(8)
        self.blocks_uchar_to_float_0_0 = blocks.uchar_to_float()
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(int(samples_per_symbol), 1, 4000, 1)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(payload_bytes) + len(padding_bytes), payload_bytes + padding_bytes)), 1000)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.pdu_pdu_to_stream_x_0, 'pdus'))
        self.connect((self.blocks_float_to_complex_0, 0), (self.iio_pluto_sink_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_uchar_to_float_0_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0_0, 0), (self.blocks_uchar_to_float_0_0, 0))
        self.connect((self.pdu_pdu_to_stream_x_0, 0), (self.blocks_unpack_k_bits_bb_0_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_moving_average_xx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ook_transmit")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_payload(self):
        return self.payload

    def set_payload(self, payload):
        self.payload = payload
        self.set_payload_bytes([ord(i) for i in self.payload])
        self.pdu_pdu_to_stream_x_0.set_max_queue_size((len(self.payload)+len(self.padding)))

    def get_padding(self):
        return self.padding

    def set_padding(self, padding):
        self.padding = padding
        self.set_padding_bytes([ord(i) for i in self.padding])
        self.pdu_pdu_to_stream_x_0.set_max_queue_size((len(self.payload)+len(self.padding)))

    def get_samples_per_symbol(self):
        return self.samples_per_symbol

    def set_samples_per_symbol(self, samples_per_symbol):
        self.samples_per_symbol = samples_per_symbol
        self.blocks_moving_average_xx_0.set_length_and_scale(int(self.samples_per_symbol), 1)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.iio_pluto_sink_0.set_samplerate(int(self.samp_rate))
        self.qtgui_sink_x_0.set_frequency_range(self.carrier_freq, self.samp_rate)

    def get_payload_bytes(self):
        return self.payload_bytes

    def set_payload_bytes(self, payload_bytes):
        self.payload_bytes = payload_bytes
        self.blocks_message_strobe_0.set_msg(pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(self.payload_bytes) + len(self.padding_bytes), self.payload_bytes + self.padding_bytes)))

    def get_padding_bytes(self):
        return self.padding_bytes

    def set_padding_bytes(self, padding_bytes):
        self.padding_bytes = padding_bytes
        self.blocks_message_strobe_0.set_msg(pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(self.payload_bytes) + len(self.padding_bytes), self.payload_bytes + self.padding_bytes)))

    def get_carrier_freq(self):
        return self.carrier_freq

    def set_carrier_freq(self, carrier_freq):
        self.carrier_freq = carrier_freq
        self.iio_pluto_sink_0.set_frequency(self.carrier_freq)
        self.qtgui_sink_x_0.set_frequency_range(self.carrier_freq, self.samp_rate)

    def get_bits_per_pack(self):
        return self.bits_per_pack

    def set_bits_per_pack(self, bits_per_pack):
        self.bits_per_pack = bits_per_pack




def main(top_block_cls=ook_transmit, options=None):

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
