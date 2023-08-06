#!/usr/bin/python3
# -*- coding: utf-8 -*-

import bencoder, socket

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 1088


def send_task(argv):
    # print("send_task %s" % argv)
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    # UDP 地址绑定
    udp.bind(('127.0.0.1', SERVER_PORT - 1))
    
    msg = dict(
            y="q",
            q="task",
            argv=argv
        )
    udp.sendto(bencoder.bencode(msg), ('127.0.0.1', SERVER_PORT + 1))

