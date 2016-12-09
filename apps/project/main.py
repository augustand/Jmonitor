# -*- coding:utf-8 -*-
import thriftpy

from thriftpy.rpc import make_server


class Dispatcher(object):
    def ping(self):
        return "pong"


if __name__ == '__main__':
    pingpong_thrift = thriftpy.load("./protocols/pingpong.thrift", module_name="pingpong_thrift")
    server = make_server(pingpong_thrift.PingPong, Dispatcher(), '127.0.0.1', 6000)
    server.serve()
