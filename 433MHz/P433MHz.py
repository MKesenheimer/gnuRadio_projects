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

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from set_variable import set_variable
import find_max_channel
import iio

from gnuradio import qtgui

class P433MHz(gr.top_block, Qt.QWidget):

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

        self.settings = Qt.QSettings("GNU Radio", "P433MHz")

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
        self.samp_rate = samp_rate = 2.5e6
        self.samp_per_sym = samp_per_sym = 1596
        self.samp_decimation = samp_decimation = 32
        self.npoints = npoints = 1024
        self.gain = gain = 10
        self.freq_0 = freq_0 = 0
        self.band_width = band_width = 2500000

        ##################################################
        # Blocks
        ##################################################
        self._gain_range = Range(1, 1000, 1, 10, 200)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, 'gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._gain_win)
        self.set_variable_0 = set_variable(self.set_freq_0)
        self.qtgui_sink_x_0 = qtgui.sink_c(
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
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                10e3,
                2e3,
                firdes.WIN_HAMMING,
                6.76))
        self.iio_pluto_source_0 = iio.pluto_source('', 433430000, int(samp_rate), 20000000, 32768, True, True, True, 'manual', 64, '', True)
        self.find_max_channel_0 = find_max_channel.find_max_channel(npoints, 80)
        self.fft_vxx_0 = fft.fft_vcc(npoints, True, window.blackmanharris(npoints), True, 1)
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff(samp_per_sym*(1+0.0), 0.25*0.175*0.175, 0.5, 0.175, 0.005)
        self.blocks_threshold_ff_0 = blocks.threshold_ff(0.1, 0.25, 0)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, 1024)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(1, 8, "", False, gr.GR_LSB_FIRST)
        self.blocks_null_sink_1 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_ff(-band_width/npoints)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(gain)
        self.blocks_float_to_char_0 = blocks.float_to_char(1, 1)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, '/Users/kesenheimer/Documents/Basteln/SDR/gnuRadio_projects/433MHz/stdout', False)
        self.blocks_file_sink_0.set_unbuffered(True)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, 4*npoints)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(npoints)
        self.blocks_add_const_vxx_1 = blocks.add_const_ff(-npoints/2)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff(0.5)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, freq_0, 1, 0, 0)
        self.analog_am_demod_cf_0 = analog.am_demod_cf(
        	channel_rate=samp_rate/samp_decimation,
        	audio_decim=1,
        	audio_pass=5000,
        	audio_stop=5500,
        )



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_am_demod_cf_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_threshold_ff_0, 0))
        self.connect((self.blocks_add_const_vxx_1, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.find_max_channel_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_float_to_char_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.analog_am_demod_cf_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.set_variable_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_threshold_ff_0, 0), (self.digital_clock_recovery_mm_xx_0, 0))
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.blocks_float_to_char_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.find_max_channel_0, 0), (self.blocks_add_const_vxx_1, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.set_variable_0, 0), (self.blocks_null_sink_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "P433MHz")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.iio_pluto_source_0.set_params(433430000, int(self.samp_rate), 20000000, True, True, True, 'manual', 64, '', True)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 10e3, 2e3, firdes.WIN_HAMMING, 6.76))
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_samp_per_sym(self):
        return self.samp_per_sym

    def set_samp_per_sym(self, samp_per_sym):
        self.samp_per_sym = samp_per_sym
        self.digital_clock_recovery_mm_xx_0.set_omega(self.samp_per_sym*(1+0.0))

    def get_samp_decimation(self):
        return self.samp_decimation

    def set_samp_decimation(self, samp_decimation):
        self.samp_decimation = samp_decimation

    def get_npoints(self):
        return self.npoints

    def set_npoints(self, npoints):
        self.npoints = npoints
        self.blocks_add_const_vxx_1.set_k(-self.npoints/2)
        self.blocks_delay_0.set_dly(4*self.npoints)
        self.blocks_multiply_const_vxx_1.set_k(-self.band_width/self.npoints)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.blocks_multiply_const_vxx_0.set_k(self.gain)

    def get_freq_0(self):
        return self.freq_0

    def set_freq_0(self, freq_0):
        self.freq_0 = freq_0
        self.analog_sig_source_x_0.set_frequency(self.freq_0)

    def get_band_width(self):
        return self.band_width

    def set_band_width(self, band_width):
        self.band_width = band_width
        self.blocks_multiply_const_vxx_1.set_k(-self.band_width/self.npoints)





def main(top_block_cls=P433MHz, options=None):

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
