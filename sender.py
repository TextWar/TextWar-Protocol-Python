#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：server.py
import base64
import multiprocessing
import socket  # 导入 socket 模块
import sys
import threading
import time
Head = '[TextWar]'
Time_stamp = 'Time-Stamp'
Data_length = 'Data-Length'


class TextWarProtocol(Exception):
    """Base class for exceptions in this module."""
    pass

class Server(threading.Thread):
    def __init__(self, server, port, result):
        super().__init__()
        self.port = port
        self.server = server
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.s.bind((server, port))  # 绑定服务地址
        self.s.listen(5)
        self.link = None
        self.client = None
        self.before_pak_time = 0
        self.result = result

    def connect(self):
        self.link, self.client = self.s.accept()


    def run(self):
        print("服务器开始接收来自[%s:%s]的请求...." % (self.client[0], self.client[1]))
        while True:  # 利用一个死循环，保持和客户端的通信状态
            out = self.link.recv(1024).decode().replace("\r","")
            if out == "":
                continue
            if out == "exit":
                print("接收到exit")
                break
            print("来自[%s:%s]的客户端向你发来信息：\n%s" % (self.client[0], self.client[1], out))
            list__ = out.split("\n")
            if len(list__) != 5:
                raise TextWarProtocol("line count of message expected " + "5" + ", got " + str(len(list__)) + ".")
            if list__[0] != Head:
                raise TextWarProtocol("head expected " + Head + ", got " + list__[0] + ".")
            if not list__[1].startswith(Time_stamp):
                raise TextWarProtocol("line 2 expected " + Time_stamp + ": TIME_STAMP_HERE" + ", got " + list__[1] + ".")
            if not list__[2].startswith(Data_length):
                raise TextWarProtocol("line 3 expected " + Data_length + ": DATA_LENGTH_HERE" + ", got " + list__[2] + ".")
            if not list__[3] == '':
                raise TextWarProtocol("line 4 expected " + "BLANK" + ", got " + list__[3] + ".")
            if int(list__[1].split(" ")[1]) < self.before_pak_time:
                raise TextWarProtocol("Time slower than the before one ", list__[1])
            if int(list__[2].split(": ")[1]) != len(list__[4][2:][:-1]):
                raise TextWarProtocol(f"Data-Length not match the json data, expected {len(list__[4])}, got {len(list__[4][2:][:-1])}")
            self.before_pak_time = int(list__[1].split(" ")[1])
            self.link.sendall('服务器已经收到你的信息'.encode())
            self.result = base64.b64decode(list__[4])


event = """
{
    "type": "event",
    "value": {
        "name": "textwar:playermoveevent",
        "player": "3489021380",
        "direction": "up"
   }
}

"""

if __name__ == "__main__":
    try:
        host = socket.gethostname()  # 获取本地主机名
        port = 31244  # 设置端口
        list_ = []
        a = Server(host, port, list_)
        a.connect()
        a.start()
        # a.stop()
        # sys.exit()
    except (SystemExit, KeyboardInterrupt):
        sys.exit()
