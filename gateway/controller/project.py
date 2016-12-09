# -*- coding:utf-8 -*-


import json
from os.path import join as pjoin

import thriftpy
from thriftpy.rpc import make_client
from tornado import web

from gateway.settings import protocols


class ProjectsHandler(web.RequestHandler):
    def post(self, *args, **kwargs):
        self.project = make_client(
            thriftpy.load(pjoin(protocols, "project.thrift"), module_name="project_thrift").ProjectHandle,
            port=6000
        )

        if __debug__:
            print self.request.body

        body = json.loads(self.request.body)
        if not isinstance(body, list):
            return self.write(json.dumps(dict(
                status="fail",
                msg=u"参数不正确"
            )))
        self.write(self.project.add_projects(self.request.body))
        self.project.close()

    def delete(self, *args, **kwargs):
        self.project = make_client(
            thriftpy.load(pjoin(protocols, "project.thrift"), module_name="project_thrift").ProjectHandle,
            port=6000
        )

        if __debug__:
            print self.request.body

        body = json.loads(self.request.body)
        self.write(self.project.remove_projects(
            json.dumps(body.get("programs", []))
        ))
        self.project.close()

    def get(self, *args, **kwargs):
        self.project = make_client(
            thriftpy.load(pjoin(protocols, "project.thrift"), module_name="project_thrift").ProjectHandle,
            port=6000
        )

        programs = self.get_argument("programs", "")
        programs = [] if not programs else programs.split(";")
        fields = self.get_argument("fields", [])

        if __debug__:
            print programs, fields

        self.write(self.project.get_projects(json.dumps(dict(
            programs=programs,
            fields=fields
        ))))
        self.project.close()


class ProjectsActionHandler(web.RequestHandler):
    def post(self, *args, **kwargs):
        self.project = make_client(
            thriftpy.load(pjoin(protocols, "project.thrift"), module_name="project_thrift").ProjectHandle,
            port=6000
        )

        self.write(self.project.do_actions(json.dumps(dict(
            programs=self.get_argument("programs", []),
            actions=self.get_argument("actions", [])
        ))))
        self.project.close()


class ProjectHandler(web.RequestHandler):
    def put(self, *args, **kwargs):
        self.project = make_client(
            thriftpy.load(pjoin(protocols, "project.thrift"), module_name="project_thrift").ProjectHandle,
            port=6000
        )

        # program = kwargs.get("program")
        body = json.loads(self.request.body)
        self.write(self.project.update_project(
            json.dumps(body)
        ))
        self.project.close()

    def post(self, *args, **kwargs):
        self.project = make_client(
            thriftpy.load(pjoin(protocols, "project.thrift"), module_name="project_thrift").ProjectHandle,
            port=6000
        )

        program = kwargs.get("program", None)
        action = kwargs.get("action", None)
        d = json.dumps(dict(
            programs=[program, ],
            actions=self.get_argument("actions", [action, ])
        ))

        if __debug__:
            print kwargs
            print d

        self.write(self.project.do_actions(d))
        self.finish()
