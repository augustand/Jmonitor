# -*- coding:utf-8 -*-
from tornado import gen
from tornado import web


class MainHandler(web.RequestHandler):
    def get(self):
        # list = ["a", "b", "c"]
        # for i in list:
        #     IOLoop.instance().add_callback(self.sleep, i)
        #     IOLoop.instance().call_later(5, self.sleep, i=i)
        #     print("when i sleep")
        self.write("ok")

    @gen.coroutine
    def sleep(self, i):
        print(i)
