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
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
import extract_payload
import math
import osmosdr
import time

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
        self.zeta = zeta = 1.0
        self.ted_gain = ted_gain = 1
        self.samp_rate = samp_rate = 2.4e6
        self.samp_per_sym = samp_per_sym = 5
        self.omega_n_norm = omega_n_norm = 0.045
        self.ofile = ofile = "/Users/kesenheimer/Documents/Basteln/SDR/gnuRadio_projects/Somfy/payloads/out"
        self.ifile = ifile = "/Users/kesenheimer/Documents/Basteln/SDR/gnuRadio_projects/Somfy/records/somfy_868.949MHz_2.4Mss.complex"
        self.fmid = fmid = 868.949e6
        self.dfctr3 = dfctr3 = 0
        self.dfctr2 = dfctr2 = -19.2e3
        self.dfctr1 = dfctr1 = 19.2e3
        self.baud_rate = baud_rate = 4800*4

        ##################################################
        # Blocks
        ##################################################
        self._zeta_range = Range(0.1, 5.0, 0.1, 1.0, 200)
        self._zeta_win = RangeWidget(self._zeta_range, self.set_zeta, 'Damping Factor', "counter_slider", float)
        self.top_grid_layout.addWidget(self._zeta_win, 0, 0, 1, 2)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._ted_gain_range = Range(0.05, 5.0, 0.01, 1, 200)
        self._ted_gain_win = RangeWidget(self._ted_gain_range, self.set_ted_gain, 'Expected TED Gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._ted_gain_win, 2, 0, 1, 2)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._omega_n_norm_range = Range(0.0, 2.0*math.pi*0.25, 0.001, 0.045, 200)
        self._omega_n_norm_win = RangeWidget(self._omega_n_norm_range, self.set_omega_n_norm, 'Normalized Bandwidth', "counter_slider", float)
        self.top_grid_layout.addWidget(self._omega_n_norm_win, 1, 0, 1, 2)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.rtlsdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ''
        )
        self.rtlsdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(fmid, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(True, 0)
        self.rtlsdr_source_0.set_gain(10, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
        self.qtgui_time_sink_x_0_0_0_0_0 = qtgui.time_sink_f(
            256, #size
            baud_rate, #samp_rate
            'Symbol Synced Output and Debug', #name
            4 #number of inputs
        )
        self.qtgui_time_sink_x_0_0_0_0_0.set_update_time(0.1)
        self.qtgui_time_sink_x_0_0_0_0_0.set_y_axis(-1.5, samp_per_sym+2)

        self.qtgui_time_sink_x_0_0_0_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_0_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_NORM, qtgui.TRIG_SLOPE_POS, 0.1, 0.01, 0, "time_est")
        self.qtgui_time_sink_x_0_0_0_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_0_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_0_0_0.enable_stem_plot(False)


        labels = ['Soft Bits', 'Error', 'Instantaneous Period', 'Average Period', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [0, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(4):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_0_0_0_win, 3, 1, 1, 2)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
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
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_1_win, 3, 0, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.fir_filter_xxx_0_1_0_0_0_0_0 = filter.fir_filter_fff(1, [1.0/float(samp_per_sym)]*samp_per_sym)
        self.fir_filter_xxx_0_1_0_0_0_0_0.declare_sample_delay(int((samp_per_sym-1.0)/2.0)+4)
        self.fir_filter_xxx_0_1_0_0_0_0 = filter.fir_filter_fff(1, [1.0/float(samp_per_sym)]*samp_per_sym)
        self.fir_filter_xxx_0_1_0_0_0_0.declare_sample_delay(int((samp_per_sym-1.0)/2.0)+4)
        self.fir_filter_xxx_0_1_0_0_0 = filter.fir_filter_fff(1, [1.0/float(samp_per_sym)]*samp_per_sym)
        self.fir_filter_xxx_0_1_0_0_0.declare_sample_delay(int((samp_per_sym-1.0)/2.0)+4)
        self.extract_payload_0_0_0 = extract_payload.extract_payload((1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1), 40*8, 40*8)
        self.extract_payload_0_0 = extract_payload.extract_payload((1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1), 40*8, 40*8)
        self.extract_payload_0 = extract_payload.extract_payload((1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1), 40*8, 40*8)
        self.digital_symbol_sync_xx_0_0_0_0 = digital.symbol_sync_ff(
            digital.TED_GARDNER,
            samp_per_sym,
            omega_n_norm,
            zeta,
            ted_gain,
            1.5,
            1,
            digital.constellation_bpsk().base(),
            digital.IR_MMSE_8TAP,
            128,
            [])
        self.digital_symbol_sync_xx_0_0_0 = digital.symbol_sync_ff(
            digital.TED_GARDNER,
            samp_per_sym,
            omega_n_norm,
            zeta,
            ted_gain,
            1.5,
            1,
            digital.constellation_bpsk().base(),
            digital.IR_MMSE_8TAP,
            128,
            [])
        self.digital_symbol_sync_xx_0_0 = digital.symbol_sync_ff(
            digital.TED_GARDNER,
            samp_per_sym,
            omega_n_norm,
            zeta,
            ted_gain,
            1.5,
            1,
            digital.constellation_bpsk().base(),
            digital.IR_MMSE_8TAP,
            128,
            [])
        self.blocks_threshold_ff_0_0_0 = blocks.threshold_ff(-0.2, 0.2, 0)
        self.blocks_threshold_ff_0_0 = blocks.threshold_ff(-0.2, 0.2, 0)
        self.blocks_threshold_ff_0 = blocks.threshold_ff(-0.2, 0.2, 0)
        self.blocks_repack_bits_bb_0_0_0 = blocks.repack_bits_bb(1, 8, "", False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0_0 = blocks.repack_bits_bb(1, 8, "", False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(1, 8, "", False, gr.GR_MSB_FIRST)
        self.blocks_float_to_char_0_0_0 = blocks.float_to_char(1, 1)
        self.blocks_float_to_char_0_0 = blocks.float_to_char(1, 1)
        self.blocks_float_to_char_0 = blocks.float_to_char(1, 1)
        self.blocks_file_sink_0_0_0_0_0_1_0 = blocks.file_sink(gr.sizeof_char*1, ofile+"_chn2.bin", False)
        self.blocks_file_sink_0_0_0_0_0_1_0.set_unbuffered(True)
        self.blocks_file_sink_0_0_0_0_0_1 = blocks.file_sink(gr.sizeof_char*1, ofile+"_chn3.bin", False)
        self.blocks_file_sink_0_0_0_0_0_1.set_unbuffered(True)
        self.blocks_file_sink_0_0_0_0_0 = blocks.file_sink(gr.sizeof_char*1, ofile+"_chn1.bin", False)
        self.blocks_file_sink_0_0_0_0_0.set_unbuffered(True)
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
            offset=-0.01,
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
        self.connect((self.OOK_demodulator_improved_0, 0), (self.fir_filter_xxx_0_1_0_0_0, 0))
        self.connect((self.OOK_demodulator_improved_0, 2), (self.qtgui_freq_sink_x_1, 0))
        self.connect((self.OOK_demodulator_improved_0_0, 0), (self.fir_filter_xxx_0_1_0_0_0_0, 0))
        self.connect((self.OOK_demodulator_improved_0_0, 2), (self.qtgui_freq_sink_x_1, 1))
        self.connect((self.OOK_demodulator_improved_0_1, 0), (self.fir_filter_xxx_0_1_0_0_0_0_0, 0))
        self.connect((self.OOK_demodulator_improved_0_1, 2), (self.qtgui_freq_sink_x_1, 2))
        self.connect((self.blocks_float_to_char_0, 0), (self.extract_payload_0, 0))
        self.connect((self.blocks_float_to_char_0_0, 0), (self.extract_payload_0_0, 0))
        self.connect((self.blocks_float_to_char_0_0_0, 0), (self.extract_payload_0_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.blocks_file_sink_0_0_0_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_0, 0), (self.blocks_file_sink_0_0_0_0_0_1, 0))
        self.connect((self.blocks_repack_bits_bb_0_0_0, 0), (self.blocks_file_sink_0_0_0_0_0_1_0, 0))
        self.connect((self.blocks_threshold_ff_0, 0), (self.blocks_float_to_char_0, 0))
        self.connect((self.blocks_threshold_ff_0_0, 0), (self.blocks_float_to_char_0_0, 0))
        self.connect((self.blocks_threshold_ff_0_0_0, 0), (self.blocks_float_to_char_0_0_0, 0))
        self.connect((self.digital_symbol_sync_xx_0_0, 0), (self.blocks_threshold_ff_0, 0))
        self.connect((self.digital_symbol_sync_xx_0_0, 2), (self.qtgui_time_sink_x_0_0_0_0_0, 2))
        self.connect((self.digital_symbol_sync_xx_0_0, 0), (self.qtgui_time_sink_x_0_0_0_0_0, 0))
        self.connect((self.digital_symbol_sync_xx_0_0, 1), (self.qtgui_time_sink_x_0_0_0_0_0, 1))
        self.connect((self.digital_symbol_sync_xx_0_0, 3), (self.qtgui_time_sink_x_0_0_0_0_0, 3))
        self.connect((self.digital_symbol_sync_xx_0_0_0, 0), (self.blocks_threshold_ff_0_0, 0))
        self.connect((self.digital_symbol_sync_xx_0_0_0_0, 0), (self.blocks_threshold_ff_0_0_0, 0))
        self.connect((self.extract_payload_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.extract_payload_0_0, 0), (self.blocks_repack_bits_bb_0_0, 0))
        self.connect((self.extract_payload_0_0_0, 0), (self.blocks_repack_bits_bb_0_0_0, 0))
        self.connect((self.fir_filter_xxx_0_1_0_0_0, 0), (self.digital_symbol_sync_xx_0_0, 0))
        self.connect((self.fir_filter_xxx_0_1_0_0_0_0, 0), (self.digital_symbol_sync_xx_0_0_0, 0))
        self.connect((self.fir_filter_xxx_0_1_0_0_0_0_0, 0), (self.digital_symbol_sync_xx_0_0_0_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.OOK_demodulator_improved_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.OOK_demodulator_improved_0_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.OOK_demodulator_improved_0_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "somfy_receiver")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_zeta(self):
        return self.zeta

    def set_zeta(self, zeta):
        self.zeta = zeta
        self.digital_symbol_sync_xx_0_0.set_damping_factor(self.zeta)
        self.digital_symbol_sync_xx_0_0_0.set_damping_factor(self.zeta)
        self.digital_symbol_sync_xx_0_0_0_0.set_damping_factor(self.zeta)

    def get_ted_gain(self):
        return self.ted_gain

    def set_ted_gain(self, ted_gain):
        self.ted_gain = ted_gain
        self.digital_symbol_sync_xx_0_0.set_ted_gain(self.ted_gain)
        self.digital_symbol_sync_xx_0_0_0.set_ted_gain(self.ted_gain)
        self.digital_symbol_sync_xx_0_0_0_0.set_ted_gain(self.ted_gain)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.OOK_demodulator_improved_0.set_samp_rate(self.samp_rate)
        self.OOK_demodulator_improved_0_0.set_samp_rate(self.samp_rate)
        self.OOK_demodulator_improved_0_1.set_samp_rate(self.samp_rate)
        self.qtgui_freq_sink_x_1.set_frequency_range(0, self.samp_rate)
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    def get_samp_per_sym(self):
        return self.samp_per_sym

    def set_samp_per_sym(self, samp_per_sym):
        self.samp_per_sym = samp_per_sym
        self.fir_filter_xxx_0_1_0_0_0.set_taps([1.0/float(self.samp_per_sym)]*self.samp_per_sym)
        self.fir_filter_xxx_0_1_0_0_0_0.set_taps([1.0/float(self.samp_per_sym)]*self.samp_per_sym)
        self.fir_filter_xxx_0_1_0_0_0_0_0.set_taps([1.0/float(self.samp_per_sym)]*self.samp_per_sym)
        self.qtgui_time_sink_x_0_0_0_0_0.set_y_axis(-1.5, self.samp_per_sym+2)

    def get_omega_n_norm(self):
        return self.omega_n_norm

    def set_omega_n_norm(self, omega_n_norm):
        self.omega_n_norm = omega_n_norm
        self.digital_symbol_sync_xx_0_0.set_loop_bandwidth(self.omega_n_norm)
        self.digital_symbol_sync_xx_0_0_0.set_loop_bandwidth(self.omega_n_norm)
        self.digital_symbol_sync_xx_0_0_0_0.set_loop_bandwidth(self.omega_n_norm)

    def get_ofile(self):
        return self.ofile

    def set_ofile(self, ofile):
        self.ofile = ofile
        self.blocks_file_sink_0_0_0_0_0.open(self.ofile+"_chn1.bin")
        self.blocks_file_sink_0_0_0_0_0_1.open(self.ofile+"_chn3.bin")
        self.blocks_file_sink_0_0_0_0_0_1_0.open(self.ofile+"_chn2.bin")

    def get_ifile(self):
        return self.ifile

    def set_ifile(self, ifile):
        self.ifile = ifile

    def get_fmid(self):
        return self.fmid

    def set_fmid(self, fmid):
        self.fmid = fmid
        self.rtlsdr_source_0.set_center_freq(self.fmid, 0)

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
        self.qtgui_time_sink_x_0_0_0_0_0.set_samp_rate(self.baud_rate)





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
