# -*- coding:utf-8 -*-
import multiprocessing
from subprocess import PIPE

import psutil
from pony.orm import select, db_session
from tornado import gen
from tornado.ioloop import PeriodicCallback

from jmonitor.models import Project
from services import daemonize


class ProjectTask(PeriodicCallback):
    def __init__(self, program, callback_time):
        super(ProjectTask, self).__init__(self.callback, callback_time)
        self.program = program

    @gen.coroutine
    def callback(self):
        p = multiprocessing.Process(target=self.__callback, args=(self.program,))
        p.daemon = True
        p.start()
        p.join()

    def __callback(self, program):

        daemonize()
        print "Task:{0}".format(program)
        with db_session:
            for p in select(p for p in Project if p.program == program)[:]:
                try:
                    pid = p.pid
                    if pid and psutil.Process(pid).is_running():
                        continue
                    else:
                        raise psutil.NoSuchProcess(pid)
                except psutil.NoSuchProcess:
                    pp = psutil.Popen(p.command, stdout=PIPE, shell=True)
                    Project[p.id].set(pid=pp.pid)
                    print "重新启动{0}:{1}".format(pp.name(), pp.pid)
