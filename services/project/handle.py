# -*- coding:utf-8 -*-


import json

from tornado import web

from services.project import logic
from services.project.action import do_actions


class ProjectsHandler(web.RequestHandler):
    def post(self, *args, **kwargs):

        if __debug__:
            print self.request.body

        body = json.loads(self.request.body)
        if not isinstance(body, list):
            return self.write(json.dumps(dict(
                status="fail",
                msg=u"参数不正确"
            )))
        self.write(json.dumps(logic.add_projects(
            body,
            self.application
        )))

    def delete(self, *args, **kwargs):

        if __debug__:
            print self.request.body

        body = json.loads(self.request.body)
        self.write(logic.remove_projects(
            body.get("programs", []),
            self.application
        ))

    def get(self, *args, **kwargs):
        programs = self.get_argument("programs", "")
        programs = [] if not programs else programs.split(";")
        fields = self.get_argument("fields", [])

        if __debug__:
            print programs, fields

        self.write(logic.get_projects(**dict(
            programs=programs,
            fields=fields
        )))


class ProjectsActionHandler(web.RequestHandler):
    def post(self, *args, **kwargs):
        programs = self.get_argument("programs", [])
        actions = self.get_argument("actions", [])

        self.write(json.dumps(do_actions(
            programs,
            actions,
            self.application
        )))


class ProjectHandler(web.RequestHandler):
    def put(self, *args, **kwargs):
        # program = kwargs.get("program")
        body = json.loads(self.request.body)
        self.write(logic.update_project(
            self.application,
            **body
        ))

    def post(self, *args, **kwargs):
        program = kwargs.get("program", None)
        action = kwargs.get("action", None)
        actions = self.get_argument("actions", [action, ])

        res = do_actions([program, ], actions, self.application)
        self.write(json.dumps(res))
