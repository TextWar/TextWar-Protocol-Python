#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：client.py
import base64
import multiprocessing
import socket  # 导入 socket 模块
from multiprocessing import Queue
from time import sleep
import threading

Head = '[TextWar]'
Time_stamp = 'Time-Stamp'
Data_length = 'Data-Length'


class TextWarProtocol(Exception):
    """Base class for exceptions in this module."""
    pass


class Client(object):
    def __init__(self, server, port):
        self.p = None
        self.server = server
        self.port = port
        self.before_pak_time = 0

    def loop(self, output):
        s = socket.socket()  # 创建 socket 对象
        while True:
            try:
                s.connect((self.server, self.port))
            except Exception as e:
                sleep(0.5)
                print("Cannot connect ", e)
                continue
            break
        while True:
            out = s.recv(1024).decode().replace("\r", "")
            list_ = out.split("\n")
            if len(list_) != 5:
                raise TextWarProtocol("line count of message expected " + "5" + ", got " + str(len(list_)) + ".")
            if list_[0] != Head:
                raise TextWarProtocol("head expected " + Head + ", got " + list_[0] + ".")
            if not list_[1].startswith(Time_stamp):
                raise TextWarProtocol("line 2 expected " + Time_stamp + ": TIME_STAMP_HERE" + ", got " + list_[1] + ".")
            if not list_[2].startswith(Data_length):
                raise TextWarProtocol("line 3 expected " + Data_length + ": DATA_LENGTH_HERE" + ", got " + list_[2] + ".")
            if not list_[3] == '':
                raise TextWarProtocol("line 4 expected " + "BLANK" + ", got " + list_[3] + ".")
            if int(list_[1].split(" ")[1]) < self.before_pak_time:
                raise TextWarProtocol("Time slower than the before one ", list_[1])
            self.before_pak_time = int(list_[1].split(" ")[1])
            output.put(base64.b64decode(list_[4]).decode())

    def start(self, out):
        self.p = multiprocessing.Process(target=self.loop, args=(out,))
        self.p.start()

    def out(self):
        return self.p.output

    def stop(self):
        self.p.s.stop()
        self.p.terminate()


if __name__ == "__main__":
    a = Queue(maxsize=1)
    Client(socket.gethostname(), 31244).start(a)
    while 1:
        print(a.get())
