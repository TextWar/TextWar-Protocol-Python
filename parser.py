#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：client.py
import base64
import multiprocessing
import socket  # 导入 socket 模块
import time
from multiprocessing import Queue
from time import sleep
import threading


def get_format(json):
    return """[TextWar]\r\nTime-Stamp: {}\r\nData-Length: {}\r\n\r\n{}""".format(int(time.time()), len(base64.b64encode(
                                                                                     json.encode())),
                                                                                 base64.b64encode(
                                                                                     json.encode())).encode()

class TextWarProtocol(Exception):
    """Base class for exceptions in this module."""
    pass


class Client:
    def __init__(self):
        self.s = socket.socket()  # 创建套接字

    def connect(self, server, port):
        while self.s.connect_ex((server, port)) == 111:
            pass
        return self


    def send(self, json):
        print("aa")
        self.s.sendall(get_format(json))
        return self.s.recv(1024).decode()

    def stop(self):
        self.s.close()
        # self.s.sendall("exit".encode())

client = Client()
client.connect(socket.gethostname(), 31244)
client.send("{'hello':'world'}")
client.stop()

       # 关闭连接

# if __name__ == "__main__":
#     a = Queue(maxsize=1)
#     Client(socket.gethostname(), 31244).start(a)
#     while 1:
#         print(a.get())
