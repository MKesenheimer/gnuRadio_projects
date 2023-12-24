"""
Manchester decode
"""

#  epy_block_0.py
#  created 10/17/2019

from gnuradio import gr
import pmt
import time

class fsk_message_sync_block(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(self,
            name = "Manchester decode",
            in_sig = None,
            out_sig = None)
        self.message_port_register_in(pmt.intern('msg'))
        self.message_port_register_out(pmt.intern('msg'))
        self.set_msg_handler(pmt.intern('msg'), self.handle_msg)

    def access_bit(self, data, num):
        base = int(num // 8)
        shift = int(num % 8)
        return (data[base] >> shift) & 0x1

    def observe_edge(self, first, second):
        if first < second:
            return 0
        if first > second:
            return 1

    def handle_msg(self, msg):
        buff = pmt.to_python(pmt.cdr(msg))
        #print("-> Received:")
        #print("bits ({}): ".format(len(buff)), end="")
        #print("".join("{}".format(i) for i in buff))
        #manchester = [self.observe_edge(buff[i], buff[i+1]) for i in range(0, len(buff), 2)]
        l = len(buff)
        l = l - 1 if l % 2 else l # makes length even by subtracting 1 if odd
        manchester = []
        for i in range(0, l, 2):
            if (a := self.observe_edge(buff[i], buff[i+1])) is not None: manchester.append(a)
        #print("manchester: ", end="")
        #print("".join("{}".format(i) for i in manchester))
        msg = pmt.cons(pmt.string_to_symbol("frame"), pmt.to_pmt(manchester))
        self.message_port_pub(pmt.intern('msg'), msg)