#!/usr/bin/env python3
# -*- conding: utf-8 -*-
import socket
import time
import threading
from xmlrpc.client import ServerProxy
import os
import sys

def init_connection(host, port, sock):
    while True:
        try:
            sock[port] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock[port].connect((host, port))
            break
        except socket.error:
            print("Connection failed on port {}, retrying...".format(port))
            time.sleep(1)
    
def send_data(sock, data):
    sock.sendall(data)

def main():
    host = 'localhost'
    port = 2000
    sock = {port: None}
    init_connection(host, port, sock)

    data = b"\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x4D\x55\x53\x2D\x4A\xCD\x2D\x2C\xCB\x4D\x2B\x35\x52\xAA\xCB\x55\x55\x4B\x2D\x32\xD3\x52\xCA\xD5\x53\x32\xB0"

    while True:
        try:
            time.sleep(1)
            send_data(sock[port], data)
        except KeyboardInterrupt:
            print('Shutting down...')
            sock[port].close()
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)

if __name__ == '__main__':
    main()