# -*- coding:utf-8 -*-
from tornado import web

from jmonitor.settings import settings
from urls import handlers


class JmonitorApplication(web.Application):
    def __init__(self, config):
        settings.update(config)

        self.tasks = {}
        super(JmonitorApplication, self).__init__(handlers, **settings)
