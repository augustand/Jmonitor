# -*- coding:utf-8 -*-

from pony.orm import db_session

from apps.project.db.model import Template
from apps.project.service.project_task import ProjectTask


def do_actions(programs, actions):
    if __debug__:
        print programs, actions

    for action in actions:
        if action == "start":
            res = start(programs)
        elif action == "stop":
            res = stop(programs)
        elif action == "restart":
            res = restart(programs)
        else:
            return dict(
                status='fail',
                msg=u'命令不正确'
            )
        return res


@db_session
def start(programs):
    for program in programs:
        if not Template.exists(program=program):
            return dict(
                status="fail",
                msg="program:{0}不存在".format(program)
            )

        # 启动定时任务
        ProjectTask().start(program)
    return dict(
        status="ok"
    )


@db_session
def stop(programs):
    for program in programs:
        if not Template.exists(program=program):
            return dict(
                status="fail",
                msg="program:{0}不存在".format(program)
            )

        # 停止定时任务
        ProjectTask().stop(program)

    return dict(
        status="ok"
    )


@db_session
def restart(programs):
    stop(programs)
    start(programs)

    return dict(
        status="ok"
    )


if __name__ == '__main__':
    pass
