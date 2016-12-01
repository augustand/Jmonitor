# -*- coding:utf-8 -*-
import json
import multiprocessing
from subprocess import PIPE

import etcd
import psutil
from tinydb import TinyDB
from tinydb import where
from tornado import gen
from tornado import web

from config import settings
from mesc import get_host_ip
from tasks import ProjectTask


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
        pts = templates.search(where('program') == program)
        if pts:
            self.write("program:{0}已经存在".format(program))
            return

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

        # 把项目实例的变化添加到etcd中
        host, port = self.application.settings.get("etcd").split(":")
        client = etcd.Client(host=host, port=int(port))
        for i in range(numprocs):
            client.write(
                "/projects/{0}/{1}".format(program, process_name.format(process_num=i)),
                "{0}:{1}".format(get_host_ip(), i + numprocs_start)
            )

        # 添加一个定时任务
        self.application.task[program] = ProjectTask(program, self.application, 1000 * 5)

        self.write(json.dumps(projects.all()))


class ProjectHandler(web.RequestHandler):
    def get(self, program=None):

        task = self.get_argument("task", None)
        if not task:
            db_path = settings.get("db_path")
            project = TinyDB(db_path).table('projects')
            self.write(json.dumps(project.search(where('program') == program)))
        else:
            method = getattr(self, task, None)
            if not method:
                self.write("task:{0}不存在".format(program))
            else:
                method(program)

    def start(self, program=None):
        db_path = settings.get("db_path")
        templates = TinyDB(db_path).table('templates')
        pts = templates.search(where("program") == program)
        if not pts:
            self.write("program:{0}不存在".format(program))
            return

        task = self.application.task.get(program, None)
        if task and not task.is_running(): task.start()

        p = multiprocessing.Process(target=self._start, args=(program,))
        p.daemon = True
        p.start()
        p.join()

    def _start(self, program):
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
        templates = TinyDB(db_path).table('templates')
        pts = templates.search(where("program") == program)
        if not pts:
            self.write("program:{0}不存在".format(program))
            return

        task = self.application.task.get(program, None)
        if task and task.is_running(): task.stop()

        p = multiprocessing.Process(target=self._stop, args=(program,))
        p.daemon = True
        p.start()
        p.join()

    def _stop(self, program=None):
        db_path = settings.get("db_path")
        projects = TinyDB(db_path).table('projects')
        for p in projects.search(where("program") == program):
            pid = p.get("pid", None)
            try:
                if pid and psutil.Process(pid).is_running():
                    _p = psutil.Process(pid)
                    _p.kill()
                    _p.wait()
                    raise psutil.NoSuchProcess(pid)
                else:
                    raise psutil.NoSuchProcess(pid)
            except psutil.NoSuchProcess as e:
                projects.update({"pid": 0}, where('process_name') == p.get("process_name"))

    def restart(self, program=None):
        db_path = settings.get("db_path")
        templates = TinyDB(db_path).table('templates')
        pts = templates.search(where("program") == program)
        if not pts:
            self.write("program:{0}不存在".format(program))
            return

        p = multiprocessing.Process(target=self._restart, args=(program,))
        p.daemon = True
        p.start()
        p.join()

    def _restart(self, program=None):
        self._stop(program)
        self._start(program)

    def put(self, program=None):
        body = json.loads(self.request.body)
        program = body.get("program")
        process_name = body.get("process_name")
        command = body.get("command")
        numprocs = int(body.get("numprocs"))
        numprocs_start = int(body.get("numprocs_start"))

        self._stop(program)

        db_path = settings.get("db_path")
        templates = TinyDB(db_path).table('templates')
        templates.update({
            "program": program,
            "process_name": process_name,
            "command": command,
            "numprocs": numprocs,
            "numprocs_start": numprocs_start
        }, where('program') == program)

        projects = TinyDB(db_path).table('projects')
        projects.remove(eids=[i.eid for i in projects.search(where('program') == program)])
        for i in range(numprocs):
            projects.insert({
                "program": program,
                "process_name": process_name.format(process_num=i),
                "command": command.format(process_num=i + numprocs_start),
                "numprocs": numprocs,
                "numprocs_start": numprocs_start
            })

        # 把项目实例的变化反映到etcd中
        host, port = self.application.settings.get("etcd").split(":")
        client = etcd.Client(host=host, port=int(port))

        # 删除
        client.delete('/projects', recursive=True)

        # 添加
        for i in range(numprocs):
            client.write(
                "/projects/{0}/{1}".format(program, process_name.format(process_num=i)),
                "{0}:{1}".format(get_host_ip(), i + numprocs_start)
            )

        p = multiprocessing.Process(target=self._start, args=(program,))
        p.daemon = True
        p.start()
        p.join()

    def delete(self, program=None):
        db_path = settings.get("db_path")
        templates = TinyDB(db_path).table('templates')
        pts = templates.search(where('program') == program)
        if not pts:
            self.write("program:{0}不存在".format(program))
            return

        task = self.application.task.get(program, None)
        if task and task.is_running(): task.stop()

        self._stop(program)

        db_path = settings.get("db_path")

        templates = TinyDB(db_path).table('templates')
        templates.remove(eids=[i.eid for i in templates.search(where('program') == program)])

        project = TinyDB(db_path).table('projects')
        project.remove(eids=[i.eid for i in project.search(where('program') == program)])

        del self.application.task[program]

        # 把项目实例从etcd中删除
        host, port = self.application.settings.get("etcd").split(":")
        client = etcd.Client(host=host, port=int(port))
        client.delete('/projects', recursive=True)


if __name__ == '__main__':
    p = psutil.Popen("python manage.py --port=12345 --daemon=True", stdout=PIPE, shell=True)
    print p.name()
    # print p.stdout.read()
    print p.parent()
    print p.children()

    pass
