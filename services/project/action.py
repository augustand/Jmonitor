# -*- coding:utf-8 -*-
import multiprocessing
from subprocess import PIPE

import psutil
from pony.orm import db_session, select

from jmonitor.models import Template, Project
from services import daemonize


def do_actions(programs, actions, app):
    if __debug__:
        print programs, actions, app.tasks

    for action in actions:
        if action == "start":
            res = start(programs, app)
        elif action == "stop":
            res = stop(programs, app)
        elif action == "restart":
            res = restart(programs, app)
        else:
            return dict(
                status='fail',
                msg=u'命令不正确'
            )
        return res


@db_session
def start(programs, app):
    for program in programs:
        if not Template.exists(program=program):
            return dict(
                status="fail",
                msg="program:{0}不存在".format(program)
            )

        task = app.tasks.get(program, None)
        if task and not task.is_running():
            task.start()


        p = multiprocessing.Process(target=_start, args=(program,))
        p.daemon = True
        p.start()
        p.join()

    return dict(
        status="ok"
    )


@db_session
def _start(program):
    daemonize()
    for p in select(p for p in Project if p.program == program)[:]:
        if p.pid:
            continue

        pp = psutil.Popen(p.command, stdout=PIPE, shell=True)
        Project[p.id].set(pid=pp.pid)


@db_session
def stop(programs, app):
    for program in programs:
        if not Template.exists(program=program):
            return dict(
                status="fail",
                msg="program:{0}不存在".format(program)
            )

        task = app.tasks.get(program, None)
        if task and task.is_running():
            task.stop()

        p = multiprocessing.Process(target=_stop, args=(program,))
        p.daemon = True
        p.start()
        p.join()

    return dict(
        status="ok"
    )


@db_session
def _stop(program):
    for p in select(p for p in Project if p.program == program)[:]:
        try:
            if p.pid and psutil.Process(p.pid).is_running():
                _p = psutil.Process(p.pid)
                _p.kill()
                _p.wait()
                raise psutil.NoSuchProcess(p.pid)
            else:
                raise psutil.NoSuchProcess(p.pid)
        except psutil.NoSuchProcess:
            Project[p.id].set(pid=0)

    return dict(
        status="ok"
    )


@db_session
def restart(programs, app):
    for program in programs:
        if not Template.exists(program=program):
            return dict(
                status="fail",
                msg="program:{0}不存在".format(program)
            )

        task = app.task.get(program, None)
        if task and task.is_running():
            task.stop()

        p = multiprocessing.Process(target=_restart, args=(program,))
        p.daemon = True
        p.start()
        p.join()

    return dict(
        status="ok"
    )


def _restart(program=None):
    _stop(program)
    _start(program)


if __name__ == '__main__':
    pass
