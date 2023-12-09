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
from gnuradio import blocks, gr
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation



class set_var_test(gr.top_block, Qt.QWidget):

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

        self.settings = Qt.QSettings("GNU Radio", "set_var_test")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.variable_qtgui_toggle_button_msg_0 = variable_qtgui_toggle_button_msg_0 = 0
        self.freq_offset = freq_offset = 32000

        ##################################################
        # Blocks
        ##################################################

        self._variable_qtgui_toggle_button_msg_0_choices = {'Pressed': 1, 'Released': 0}

        _variable_qtgui_toggle_button_msg_0_toggle_button = qtgui.ToggleButton(self.set_variable_qtgui_toggle_button_msg_0, 'variable_qtgui_toggle_button_msg_0', self._variable_qtgui_toggle_button_msg_0_choices, False, 'value')
        _variable_qtgui_toggle_button_msg_0_toggle_button.setColors("default", "default", "default", "default")
        self.variable_qtgui_toggle_button_msg_0 = _variable_qtgui_toggle_button_msg_0_toggle_button

        self.top_layout.addWidget(_variable_qtgui_toggle_button_msg_0_toggle_button)
        self.blocks_msgpair_to_var_0 = blocks.msg_pair_to_var(self.set_freq_offset)
        self.blocks_message_debug_0 = blocks.message_debug(True, gr.log_levels.info)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.variable_qtgui_toggle_button_msg_0, 'state'), (self.blocks_message_debug_0, 'log'))
        self.msg_connect((self.variable_qtgui_toggle_button_msg_0, 'state'), (self.blocks_msgpair_to_var_0, 'inpair'))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "set_var_test")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_variable_qtgui_toggle_button_msg_0(self):
        return self.variable_qtgui_toggle_button_msg_0

    def set_variable_qtgui_toggle_button_msg_0(self, variable_qtgui_toggle_button_msg_0):
        self.variable_qtgui_toggle_button_msg_0 = variable_qtgui_toggle_button_msg_0

    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset




def main(top_block_cls=set_var_test, options=None):

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
