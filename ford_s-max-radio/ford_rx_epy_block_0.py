"""
Paylaod logger
"""

#  epy_block_0.py
#  created 10/17/2019

from gnuradio import gr
import pmt
import time

class fsk_message_sync_block(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(self,
            name = "Payload logger",
            in_sig = None,
            out_sig = None)
        self.message_port_register_in(pmt.intern('message'))
        self.set_msg_handler(pmt.intern('message'), self.handle_msg)

    def handle_msg(self, msg):
        buff = pmt.to_python(pmt.cdr(msg))
        print("-> Received:")
        #print("payload: ", end="")
        #print("".join("{:02x}".format(i) for i in buff))
        payload = "\\x" + "\\x".join("{:02x}".format(i) for i in buff)
        header = 24 * "\\x55"
        frame = header + payload
        print("frame: {}".format(frame))
            