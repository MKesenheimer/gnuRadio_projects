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
import math
from gnuradio import blocks
from gnuradio import blocks, gr
from gnuradio import digital
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
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import extract_payload
import osmosdr
import time
import sip



class ford_rx(gr.top_block, Qt.QWidget):

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

        self.settings = Qt.QSettings("GNU Radio", "ford_rx")

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
        self.squelch_threshold = squelch_threshold = -40
        self.samp_rate = samp_rate = 1000000
        self.fsk_deviation = fsk_deviation = freq_spread*2
        self.freq_offset_chan1 = freq_offset_chan1 = 330000
        self.freq_offset_chan0 = freq_offset_chan0 = -330000
        self.freq = freq = 433930000

        ##################################################
        # Blocks
        ##################################################

        self._squelch_threshold_range = Range(-90, -10, 1, -40, 200)
        self._squelch_threshold_win = RangeWidget(self._squelch_threshold_range, self.set_squelch_threshold, "'squelch_threshold'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._squelch_threshold_win)
        self.rtlsdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )
        self.rtlsdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(freq, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(10, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(samp_rate, 0)
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_fff(
                interpolation=2,
                decimation=4,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=2,
                decimation=4,
                taps=[],
                fractional_bw=0)
        self.qtgui_waterfall_sink_x_0_0 = qtgui.waterfall_sink_c(
            4096, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            freq, #fc
            samp_rate, #bw
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0_0.qwidget(), Qt.QWidget)

        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_0_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            int(samp_rate/2), #samp_rate
            "", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-20, 20)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_AUTO, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.pdu_tagged_stream_to_pdu_0_0 = pdu.tagged_stream_to_pdu(gr.types.byte_t, 'packet_len')
        self.pdu_tagged_stream_to_pdu_0 = pdu.tagged_stream_to_pdu(gr.types.byte_t, 'packet_len')
        self.freq_xlating_fir_filter_xxx_0_0 = filter.freq_xlating_fir_filter_ccf(8, firdes.band_pass(1.0, samp_rate, 0.1, freq_spread/2, freq_spread), freq_offset_chan1, samp_rate)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccf(8, firdes.band_pass(1.0, samp_rate, 0.1, freq_spread/2, freq_spread), freq_offset_chan0, samp_rate)
        self.extract_payload_0_0 = extract_payload.extract_payload((0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,0,1,1,0,1), 218, 200, True, 'packet_len')
        self.extract_payload_0 = extract_payload.extract_payload((0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,0,1,1,0,1), 218, 200, True, 'packet_len')
        self.digital_symbol_sync_xx_0_0 = digital.symbol_sync_ff(
            digital.TED_GARDNER,
            15,
            0.045,
            1.0,
            1.0,
            1.5,
            1,
            digital.constellation_bpsk().base(),
            digital.IR_MMSE_8TAP,
            128,
            [])
        self.digital_symbol_sync_xx_0 = digital.symbol_sync_ff(
            digital.TED_GARDNER,
            15,
            0.045,
            1.0,
            1.0,
            1.5,
            1,
            digital.constellation_bpsk().base(),
            digital.IR_MMSE_8TAP,
            128,
            [])
        self.digital_binary_slicer_fb_0_0 = digital.binary_slicer_fb()
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink(
            'demod.wav',
            2,
            (int(samp_rate/2)),
            blocks.FORMAT_WAV,
            blocks.FORMAT_FLOAT,
            False
            )
        self.blocks_repack_bits_bb_0_2 = blocks.repack_bits_bb(1, 8, "", False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0_1_0 = blocks.repack_bits_bb(1, 8, 'packet_len', False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0_1 = blocks.repack_bits_bb(1, 8, 'packet_len', False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0_0_0 = blocks.repack_bits_bb(1, 8, "", False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0_0 = blocks.repack_bits_bb(1, 8, "", False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(1, 8, "", False, gr.GR_MSB_FIRST)
        self.blocks_message_debug_0 = blocks.message_debug(True, gr.log_levels.info)
        self.blocks_file_sink_0_0_0_0_0_1 = blocks.file_sink(gr.sizeof_char*1, 'payload_chan1.bin', False)
        self.blocks_file_sink_0_0_0_0_0_1.set_unbuffered(True)
        self.blocks_file_sink_0_0_0_0_0_0_0 = blocks.file_sink(gr.sizeof_char*1, 'decoded_chan1.bin', False)
        self.blocks_file_sink_0_0_0_0_0_0_0.set_unbuffered(True)
        self.blocks_file_sink_0_0_0_0_0_0 = blocks.file_sink(gr.sizeof_char*1, 'decoded_chan0.bin', False)
        self.blocks_file_sink_0_0_0_0_0_0.set_unbuffered(True)
        self.blocks_file_sink_0_0_0_0_0 = blocks.file_sink(gr.sizeof_char*1, 'payload_chan0.bin', False)
        self.blocks_file_sink_0_0_0_0_0.set_unbuffered(True)
        self.analog_simple_squelch_cc_0_0 = analog.simple_squelch_cc(squelch_threshold, 1)
        self.analog_simple_squelch_cc_0 = analog.simple_squelch_cc(squelch_threshold, 1)
        self.analog_quadrature_demod_cf_0_0 = analog.quadrature_demod_cf((samp_rate/(2*math.pi*fsk_deviation)))
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf((samp_rate/(2*math.pi*fsk_deviation)))


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.pdu_tagged_stream_to_pdu_0, 'pdus'), (self.blocks_message_debug_0, 'log'))
        self.msg_connect((self.pdu_tagged_stream_to_pdu_0_0, 'pdus'), (self.blocks_message_debug_0, 'log'))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0_0, 0), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.analog_simple_squelch_cc_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.analog_simple_squelch_cc_0_0, 0), (self.analog_quadrature_demod_cf_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.blocks_file_sink_0_0_0_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_0, 0), (self.blocks_file_sink_0_0_0_0_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_0_0, 0), (self.blocks_file_sink_0_0_0_0_0_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_1, 0), (self.pdu_tagged_stream_to_pdu_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_1_0, 0), (self.pdu_tagged_stream_to_pdu_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_2, 0), (self.blocks_file_sink_0_0_0_0_0_1, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.blocks_repack_bits_bb_0_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.extract_payload_0, 0))
        self.connect((self.digital_binary_slicer_fb_0_0, 0), (self.blocks_repack_bits_bb_0_0_0, 0))
        self.connect((self.digital_binary_slicer_fb_0_0, 0), (self.extract_payload_0_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.digital_symbol_sync_xx_0_0, 0), (self.digital_binary_slicer_fb_0_0, 0))
        self.connect((self.digital_symbol_sync_xx_0_0, 0), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.extract_payload_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.extract_payload_0, 1), (self.blocks_repack_bits_bb_0_1, 0))
        self.connect((self.extract_payload_0_0, 1), (self.blocks_repack_bits_bb_0_1_0, 0))
        self.connect((self.extract_payload_0_0, 0), (self.blocks_repack_bits_bb_0_2, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_simple_squelch_cc_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.analog_simple_squelch_cc_0_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_wavfile_sink_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.digital_symbol_sync_xx_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.blocks_wavfile_sink_0, 1))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.digital_symbol_sync_xx_0_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.qtgui_waterfall_sink_x_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ford_rx")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_freq_spread(self):
        return self.freq_spread

    def set_freq_spread(self, freq_spread):
        self.freq_spread = freq_spread
        self.set_fsk_deviation(self.freq_spread*2)
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.band_pass(1.0, self.samp_rate, 0.1, self.freq_spread/2, self.freq_spread))
        self.freq_xlating_fir_filter_xxx_0_0.set_taps(firdes.band_pass(1.0, self.samp_rate, 0.1, self.freq_spread/2, self.freq_spread))

    def get_squelch_threshold(self):
        return self.squelch_threshold

    def set_squelch_threshold(self, squelch_threshold):
        self.squelch_threshold = squelch_threshold
        self.analog_simple_squelch_cc_0.set_threshold(self.squelch_threshold)
        self.analog_simple_squelch_cc_0_0.set_threshold(self.squelch_threshold)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_quadrature_demod_cf_0.set_gain((self.samp_rate/(2*math.pi*self.fsk_deviation)))
        self.analog_quadrature_demod_cf_0_0.set_gain((self.samp_rate/(2*math.pi*self.fsk_deviation)))
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.band_pass(1.0, self.samp_rate, 0.1, self.freq_spread/2, self.freq_spread))
        self.freq_xlating_fir_filter_xxx_0_0.set_taps(firdes.band_pass(1.0, self.samp_rate, 0.1, self.freq_spread/2, self.freq_spread))
        self.qtgui_time_sink_x_0.set_samp_rate(int(self.samp_rate/2))
        self.qtgui_waterfall_sink_x_0_0.set_frequency_range(self.freq, self.samp_rate)
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)
        self.rtlsdr_source_0.set_bandwidth(self.samp_rate, 0)

    def get_fsk_deviation(self):
        return self.fsk_deviation

    def set_fsk_deviation(self, fsk_deviation):
        self.fsk_deviation = fsk_deviation
        self.analog_quadrature_demod_cf_0.set_gain((self.samp_rate/(2*math.pi*self.fsk_deviation)))
        self.analog_quadrature_demod_cf_0_0.set_gain((self.samp_rate/(2*math.pi*self.fsk_deviation)))

    def get_freq_offset_chan1(self):
        return self.freq_offset_chan1

    def set_freq_offset_chan1(self, freq_offset_chan1):
        self.freq_offset_chan1 = freq_offset_chan1
        self.freq_xlating_fir_filter_xxx_0_0.set_center_freq(self.freq_offset_chan1)

    def get_freq_offset_chan0(self):
        return self.freq_offset_chan0

    def set_freq_offset_chan0(self, freq_offset_chan0):
        self.freq_offset_chan0 = freq_offset_chan0
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.freq_offset_chan0)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.qtgui_waterfall_sink_x_0_0.set_frequency_range(self.freq, self.samp_rate)
        self.rtlsdr_source_0.set_center_freq(self.freq, 0)




def main(top_block_cls=ford_rx, options=None):

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
