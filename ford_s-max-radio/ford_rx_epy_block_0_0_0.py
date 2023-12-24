"""
Manchester decode
"""

#  epy_block_0.py
#  created 10/17/2019

from gnuradio import gr
import pmt
import time

class fsk_message_sync_block(gr.sync_block):
    def __init__(self, sync_word = (0,1,1,1,1,1,1,1,1)):
        gr.sync_block.__init__(self,
            name = "Extract payload",
            in_sig = None,
            out_sig = None)
        self.message_port_register_in(pmt.intern('msg'))
        self.message_port_register_out(pmt.intern('bits'))
        self.message_port_register_out(pmt.intern('bytes'))
        self.set_msg_handler(pmt.intern('msg'), self.handle_msg)
        self.sync_word = list(sync_word)

    def find_list_position(self, main_list, sublist):
        try:
            position = -1
            while True:
                position = main_list.index(sublist[0], position + 1)
                if main_list[position:position + len(sublist)] == sublist:
                    return position
        except ValueError:
            return -1

    def handle_msg(self, msg):
        buff = pmt.to_python(pmt.cdr(msg))
        #print(buff)
        #print(buff.index(self.sync_word))
        pos = self.find_list_position(buff, self.sync_word)
        payload = buff[pos + len(self.sync_word):]
        msg = pmt.cons(pmt.string_to_symbol("payload"), pmt.to_pmt(payload))
        self.message_port_pub(pmt.intern('bits'), msg)
        byte_array = [int("".join(map(str, payload[i:i+8])), 2) for i in range(0, len(payload), 8)]
        byte_str = "".join("{:02x}".format(i) for i in byte_array)
        msg = pmt.cons(pmt.string_to_symbol("payload"), pmt.to_pmt(byte_str))
        self.message_port_pub(pmt.intern('bytes'), msg)