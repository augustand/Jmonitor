# -*- coding:utf-8 -*-


import json
from os.path import join as pjoin

import thriftpy
from thriftpy.rpc import make_client
from tornado import web

from gateway.settings import protocols


class ProjectsHandler(web.RequestHandler):
    project = make_client(
        thriftpy.load(pjoin(protocols, "project.thrift"), module_name="project_thrift").ProjectHandle,
        port=6000
    )

    def post(self, *args, **kwargs):

        if __debug__:
            print self.request.body

        body = json.loads(self.request.body)
        if not isinstance(body, list):
            return self.write(json.dumps(dict(
                status="fail",
                msg=u"参数不正确"
            )))
        self.write(self.project.add_projects(body))

    def delete(self, *args, **kwargs):

        if __debug__:
            print self.request.body

        body = json.loads(self.request.body)
        self.write(self.project.remove_projects(
            json.dumps(body.get("programs", []))
        ))

    def get(self, *args, **kwargs):
        programs = self.get_argument("programs", "")
        programs = [] if not programs else programs.split(";")
        fields = self.get_argument("fields", [])

        if __debug__:
            print programs, fields

        self.write(self.project.get_projects(json.dumps(dict(
            programs=programs,
            fields=fields
        ))))


class ProjectsActionHandler(web.RequestHandler):
    project = make_client(
        thriftpy.load(pjoin(protocols, "project.thrift"), module_name="project_thrift").ProjectHandle,
        port=6000
    )

    def post(self, *args, **kwargs):
        self.write(self.project.do_actions(json.dumps(dict(
            programs=self.get_argument("programs", []),
            actions=self.get_argument("actions", [])
        ))))


class ProjectHandler(web.RequestHandler):
    project = make_client(
        thriftpy.load(pjoin(protocols, "project.thrift"), module_name="project_thrift").ProjectHandle,
        port=6000
    )

    def put(self, *args, **kwargs):
        # program = kwargs.get("program")
        body = json.loads(self.request.body)
        self.write(self.project.update_project(
            json.dumps(body)
        ))

    def post(self, *args, **kwargs):
        program = kwargs.get("program", None)
        action = kwargs.get("action", None)
        actions = self.get_argument("actions", [action, ])

        res = self.project.do_actions(json.dumps(dict(
            programs=[program, ],
            actions=actions
        )))
        self.write(json.dumps(res))
