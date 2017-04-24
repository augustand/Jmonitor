# -*- coding:utf-8 -*-
import functools
import json
import logging
from os.path import join as pjoin

import thriftpy
from thriftpy.rpc import make_client
from tornado import web

from gateway.settings import protocols, project

logger = logging.getLogger()


class ProjectClient(object):
    def __init__(self):
        self.project = make_client(
            thriftpy.load(pjoin(protocols, "project.thrift"), module_name="project_thrift").ProjectHandle,
            port=6000
        )

    def retry(self, numretry=3):
        def _func(func):
            @functools.wraps(func)
            def __func(*args, **kwargs):
                _numretry = numretry
                while _numretry > 0:
                    try:
                        res = self.project.ping()
                        if res == 'ok':
                            logger.info('calling function: {}\n'.format(func.__name__))
                            res1 = func(*args, **kwargs)
                            logger.info('return value: {}\n'.format(res1))
                            return res1
                    except Exception, e:
                        logger.error(e.message)

                        self.project = make_client(
                            thriftpy.load(pjoin(protocols, "project.thrift"),
                                          module_name="project_thrift").ProjectHandle,
                            port=project["port"]
                        )
                        _numretry -= 1
                else:
                    logger.error("had retried {} times, but still error".format(numretry))
                    return

            return __func

        return _func

    @retry(numretry=5)
    def add_projects(self, data):
        res = self.project.add_projects(data)
        return res

    @retry()
    def remove_projects(self, data):
        res = self.project.remove_projects(data)
        return res

    @retry()
    def get_projects(self, data):
        res = self.project.get_projects(data)
        return res

    @retry()
    def update_project(self, data):
        res = self.project.update_project(data)
        return res

    @retry()
    def do_actions(self, data):
        res = self.project.do_actions(data)
        return res


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
