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
    def __init__(self, payload: str = "", period: int = 1000, pause: int = 50):
        gr.sync_block.__init__(self,
            name = "Synchronized FSK message block",
            in_sig = None,
            out_sig = None)
        self.message_port_register_out(pmt.intern('chan1'))
        self.message_port_register_out(pmt.intern('chan0'))
        self.payload = payload
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

    def send_payload(self, chan):
        payload_bytes = [ord(i) for i in self.payload]
        payload_msg = pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(payload_bytes), payload_bytes))
        self.message_port_pub(pmt.intern(chan), payload_msg)

    def run(self):
        global run
        while run:
            self.send_payload('chan0')
            time.sleep(self.pause / 1000)
            self.send_payload('chan1')
            time.sleep(self.pause / 1000)
            self.send_payload('chan0')
            time.sleep(self.period / 1000)