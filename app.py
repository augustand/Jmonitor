# -*- coding:utf-8 -*-

from tornado import web

from config import settings
from handlers import MainHandler, ProjectsHandler, ProjectHandler


class Application(web.Application):
    def __init__(self, config):
        handlers = [
            (r"/", MainHandler),
            (r"/api/projects", ProjectsHandler),
            (r"/api/project/(?P<program>.*)", ProjectHandler),
            # (r"/id/(?P<id>.*)", Main1Handler),
            # (r"/v1/log/(?P<id>.*)", Main1Handler),
        ]

        settings.update(config)
        super(Application, self).__init__(handlers, **settings)
