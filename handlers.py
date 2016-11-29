# -*- coding:utf-8 -*-
from tornado import gen
from tornado import web
from tornado.ioloop import PeriodicCallback


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


class ProjectsHandler(web.RequestHandler):
    def get(self, *args, **kwargs):
        pass


class ProjectHandler(web.RequestHandler):
    def get(self, *args, **kwargs):
        pass


class Task(PeriodicCallback):
    def __init__(self, application, callback_time):
        super(Task, self).__init__(self.post, callback_time)
        self.application = application

    @gen.coroutine
    def post(self):
        print("Hello Tornado")
