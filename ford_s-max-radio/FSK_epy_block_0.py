"""
FSK channelizer
"""

#  epy_block_0.py
#  created 10/17/2019

from gnuradio import gr
import pmt
import time

class fsk_message_sync_block(gr.sync_block):
    def __init__(self, freq_offset: int = 0, pause: int = 50):
        gr.sync_block.__init__(self,
            name = "FSK channelizer",
            in_sig = None,
            out_sig = None)
        self.message_port_register_in(pmt.intern('trigger'))
        self.message_port_register_out(pmt.intern('freq'))
        self.message_port_register_out(pmt.intern('payload'))
        self.set_msg_handler(pmt.intern('trigger'), self.handle_msg)
        self.freq_offset = freq_offset
        self.pause = pause

    def send_payload(self, payload_msg, freq_offset):
        freq_msg = pmt.dict_add(pmt.make_dict(), pmt.intern("freq"), pmt.from_double(freq_offset))
        self.message_port_pub(pmt.intern('freq'), freq_msg)
        self.message_port_pub(pmt.intern('payload'), payload_msg)

    def run(self, payload):
        self.send_payload(payload, self.freq_offset)
        time.sleep(self.pause / 1000)
        self.send_payload(payload, -self.freq_offset)
        time.sleep(self.pause / 1000)
        self.send_payload(payload, self.freq_offset)
        time.sleep(self.pause / 1000)

    def handle_msg(self, msg):
        payload = pmt.to_python(pmt.cdr(msg))
        print("-> Sending:")
        print("".join("{:02x}".format(i) for i in payload))
        self.run(msg)