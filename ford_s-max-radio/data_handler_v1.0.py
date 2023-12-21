#!/usr/bin/env python3
# -*- conding: utf-8 -*-
import socket
import time
import threading
from xmlrpc.client import ServerProxy

def init_connection(port, sockets):
    while True:
        try:
            sockets[port] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sockets[port].connect((host, port))
            break
        except socket.error:
            print("Connection failed on port {}, retrying...".format(port))
            time.sleep(1)
    
def send_data(sock, data):
    sock.sendall(data)

if __name__ == "__main__":
    host = 'localhost'
    ports = [2000]
    sockets = dict.fromkeys(ports)
    init_connection(ports[0], sockets)

    s = ServerProxy('http://localhost:8080')
    data = b"\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x35\x55\x4c\xb5\x2b\x34\xb4\xb3\x2d\x4b\x2b\x53\x4a\xab\x32\xaa\xb2\xb5\x2c\xd2\xd3\x54\xab\x52\xb5\x4b\x41\xff"

    while True:
        time.sleep(0.5)
        s.set_freq_offset(330000)
        send_data(sockets[2000], data)

        time.sleep(0.5)
        s.set_freq_offset(-330000)
        send_data(sockets[2000], data)

        time.sleep(0.5)
        s.set_freq_offset(330000)
        send_data(sockets[2000], data)

        time.sleep(5)

    for p in ports:
        sockets[p].close()
