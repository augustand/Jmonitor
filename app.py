# -*- coding:utf-8 -*-
import os

from tornado import web

from handlers import MainHandler

class Application(web.Application):
    def __init__(self, config):
        handlers = [
            (r"/", MainHandler),
            (r"/api/projects", ProjectHandler),
            # (r"/id/(?P<id>.*)", Main1Handler),
            # (r"/v1/log/(?P<id>.*)", Main1Handler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            debug=True,
        )

        settings.update(config)
        super(Application, self).__init__(handlers, **settings)
