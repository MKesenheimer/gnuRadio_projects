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

run = 1

class fsk_message_sync_block(gr.sync_block):
    def __init__(self, payload: str = "", freq_offset: int = 0, period: int = 1000, pause: int = 50):
        gr.sync_block.__init__(self,
            name = "Synchronized FSK message block",
            in_sig = None,
            out_sig = None) # [np.byte]
        self.message_port_register_in(pmt.intern('msg_in'))
        self.message_port_register_out(pmt.intern('freq'))
        self.message_port_register_out(pmt.intern('payload'))
        self.set_msg_handler(pmt.intern('msg_in'), self.handle_msg)
        self.payload = payload
        self.freq_offset = freq_offset
        self.period = period
        self.pause = pause

    def start(self):
        self.x = threading.Thread(target=self.run, args=())
        print("Starting FSK payload generation thread")
        self.x.start()

    def stop(self):
        print("Stopping FSK payload generation thread")
        global run
        run = 0
        self.x.join()
        return True

    def handle_msg(self, msg):
        print(msg)
    
    def work(self, input_items, output_items):
        #_len = len(self.payload)
        #if _len > 0:
        #    for x in range(_len):
        #        output_items[0][x] = ord(self.payload[x])
        #        return (_len)
        #else:
        #    return 0
        pass

    def send_payload(self, freq_offset):
        freq_msg = pmt.dict_add(pmt.make_dict(), pmt.intern("freq"), pmt.from_double(freq_offset))
        payload_bytes = [ord(i) for i in self.payload]
        payload_msg = pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(payload_bytes), payload_bytes))
        self.message_port_pub(pmt.intern('freq'), freq_msg)
        self.message_port_pub(pmt.intern('payload'), payload_msg)

    def run(self):
        global run
        while run:
            self.send_payload(self.freq_offset)
            time.sleep(self.pause / 1000)
            self.send_payload(-self.freq_offset)
            time.sleep(self.pause / 1000)
            self.send_payload(self.freq_offset)
            time.sleep(self.period / 1000)