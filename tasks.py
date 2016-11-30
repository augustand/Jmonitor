# -*- coding:utf-8 -*-
import multiprocessing
from subprocess import PIPE

import psutil
from tinydb import TinyDB
from tinydb import where
from tornado import gen
from tornado.ioloop import PeriodicCallback

from config import settings


class ProjectTask(PeriodicCallback):
    def __init__(self, program, application, callback_time):
        super(ProjectTask, self).__init__(self.callback, callback_time)
        self.application = application
        self.program = program

    @gen.coroutine
    def callback(self):
        p = multiprocessing.Process(target=self.__callback, args=(self.program,))
        p.daemon = True
        p.start()
        p.join()

    def __callback(self, program):
        print "Task:{0}".format(program)
        db_path = settings.get("db_path")
        projects = TinyDB(db_path).table('projects')

        for p in projects.search(where('process_name') == program):
            pid = p.get("pid", None)

            try:
                if pid and psutil.Process(pid).is_running():
                    continue
                else:
                    raise psutil.NoSuchProcess(pid)
            except psutil.NoSuchProcess as e:
                pp = psutil.Popen(p.get("command"), stdout=PIPE, shell=True)
                projects.update({"pid": pp.pid}, where('process_name') == p.get("process_name"))
                print "重新启动{0}:{1}".format(pp.name(), pp.pid)
