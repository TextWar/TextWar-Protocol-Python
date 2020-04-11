#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：server.py
import base64
import multiprocessing
import socket  # 导入 socket 模块
import sys
import time


def get_format(json):
    return """[TextWar]\r\nTime-Stamp: {}\r\nData-Length: {}\r\n\r\n{}""".format(int(time.time()), len(json),
                                                                                 base64.b64encode(
                                                                                     json.encode()).decode())


class Server(object):
    def __init__(self, server, port):
        self.port = port
        self.server = server
        self.p = None

    def start(self, json):
        self.p = multiprocessing.Process(target=self.loop, args=(json,))
        self.p.start()

    def loop(self, json):
        while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            s.bind((self.server, self.port))  # 绑定端口

            s.listen(0)  # 等待客户端连接
            c, addr = s.accept()  # 建立客户端连接
            while 1:
                time.sleep(0.5)
                c.send(get_format(json.get()).encode())


    def stop(self):
        self.p.terminate()
        self.p.c.close()
        self.p.s.close()
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
        a = Server(host, port)
        ab = multiprocessing.Queue(1)
        a.start(ab)

        while True:
            ab.put(event)
        # a.stop()
        # sys.exit()
    except (SystemExit, KeyboardInterrupt):
        sys.exit()
