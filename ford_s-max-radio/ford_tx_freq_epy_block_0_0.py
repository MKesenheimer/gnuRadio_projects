"""
Synchronized fsk message block
"""

#  epy_block_0.py
#  created 10/17/2019

import numpy as np
from gnuradio import gr
import pmt
import threading
import time

class fsk_message_sync_block(gr.sync_block):
    """
    For example:
    payload: Payload string to send
    freq_offset: 
    bits_per_second:
    period: [ms]
    pause: [ms]
    """
    def __init__(self, payload: str = "", freq_offset: int = 0, 
                 bits_per_second: int = 0, period: int = 1000, pause: int = 50):
        gr.sync_block.__init__(self,
            name = "Synchronized FSK message block",
            in_sig = None,
            out_sig = [np.byte])
        self.message_port_register_in(pmt.intern('msg_in'))
        self.message_port_register_out(pmt.intern('freq'))
        self.set_msg_handler(pmt.intern('msg_in'), self.handle_msg)
        self.payload = payload
        self.freq_offset = freq_offset
        self.bits_per_second = bits_per_second
        self.period = period
        self.pause = pause

    def handle_msg(self, msg):
        print(msg)
    
    def set_payload(self, output_items, payload, freq_offset):
        freq_msg = pmt.dict_add(pmt.make_dict(), pmt.intern("freq"), pmt.from_double(freq_offset))
        self.message_port_pub(pmt.intern('freq'), freq_msg)
        _len = len(payload)
        if _len > 0:
            for x in range(_len):
                output_items[0][x] = ord(payload[x])
                return _len
        else:
            return 0
        

    def work(self, input_items, output_items):
        nitems = self.set_payload(output_items, self.payload, self.freq_offset)
        nbytes_padding = int(self.bits_per_second * self.period / 1000 / 8)
        padding = str(nbytes_padding * "\x00")
        nitems += self.set_payload(output_items, padding, -self.freq_offset)
        return nitems