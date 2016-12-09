# -*- coding:utf-8 -*-

from apps.project.db.model import Template
from pony.orm import db_session

from project.service.project_task import ProjectTask


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
