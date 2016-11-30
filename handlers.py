# -*- coding:utf-8 -*-
import json
import multiprocessing
from subprocess import PIPE

import psutil
from tinydb import TinyDB
from tinydb import where
from tornado import gen
from tornado import web
from tornado.ioloop import PeriodicCallback

from config import settings
from mesc import daemonize1


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
    def get(self):
        db_path = settings.get("db_path")
        project = TinyDB(db_path).table('projects')
        self.write(json.dumps(project.all()))

    def post(self):
        body = json.loads(self.request.body)

        program = body.get("program")
        process_name = body.get("process_name")
        command = body.get("command")
        numprocs = int(body.get("numprocs"))
        numprocs_start = int(body.get("numprocs_start"))

        db_path = settings.get("db_path")
        templates = TinyDB(db_path).table('templates')
        templates.insert({
            "program": program,
            "process_name": process_name,
            "command": command,
            "numprocs": numprocs,
            "numprocs_start": numprocs_start
        })

        projects = TinyDB(db_path).table('projects')
        for i in range(numprocs):
            projects.insert({
                "program": program,
                "process_name": process_name.format(process_num=i),
                "command": command.format(process_num=i + numprocs_start),
                "numprocs": numprocs,
                "numprocs_start": numprocs_start
            })

        self.write(json.dumps(projects.all()))


class ProjectHandler(web.RequestHandler):
    def get(self, name=None):

        task = self.get_argument("task", None)
        if not task:
            db_path = settings.get("db_path")
            project = TinyDB(db_path).table('projects')
            self.write(json.dumps(project.search(where('program') == name)))
        else:
            method = getattr(self, task, None)
            if not method:
                pass
            else:
                method(name)

    def start(self, program=None):
        daemonize1()
        db_path = settings.get("db_path")
        projects = TinyDB(db_path).table('projects')

        for p in projects.search(where("program") == program):
            pid = p.get("pid", None)
            if pid: continue

            command = p.get("command")
            pp = psutil.Popen(command, stdout=PIPE, shell=True)
            process_name = p.get("process_name")
            projects.update({"pid": pp.pid}, where('process_name') == process_name)

    def stop(self, program=None):
        db_path = settings.get("db_path")
        projects = TinyDB(db_path).table('projects')
        for p in projects.search(where("program") == program):
            pid = p.get("pid", None)

            if not pid: continue

            _p = psutil.Process(pid)
            _p.kill()
            _p.wait()

            if not _p.is_running():
                projects.update({"pid": 0}, where('process_name') == p.get("process_name"))

    def put(self, name=None):
        body = self.request.body
        db_path = settings.get("db_path")
        project = TinyDB(db_path).table('projects')
        project.update(json.loads(body), where('name') == int(name))
        self.write(json.dumps(project.all()))

    def delete(self, name=None):
        db_path = settings.get("db_path")
        project = TinyDB(db_path).table('projects')
        project.remove(eids=[i.eid for i in project.search(where('name') == 122)])
        self.write(json.dumps(project.all()))


class Task(PeriodicCallback):
    def __init__(self, application, callback_time):
        super(Task, self).__init__(self.callback, callback_time)
        self.application = application

    @gen.coroutine
    def callback(self):
        p = multiprocessing.Process(target=self.__callback)
        p.daemon = True
        p.start()
        p.join()

    def __callback(self):
        print "Task"
        db_path = settings.get("db_path")
        projects = TinyDB(db_path).table('projects')

        for p in projects.all():
            pid = p.get("pid", None)

            try:
                if pid and psutil.Process(pid).is_running():
                    continue
                else:
                    raise psutil.NoSuchProcess(pid)
            except psutil.NoSuchProcess:
                pp = psutil.Popen(p.get("command"), stdout=PIPE, shell=True)
                projects.update({"pid": pp.pid}, where('process_name') == p.get("process_name"))


if __name__ == '__main__':
    p = psutil.Popen("python manage.py --port=12345 --daemon=True", stdout=PIPE, shell=True)
    print p.name()
    # print p.stdout.read()
    print p.parent()
    print p.children()

    pass
