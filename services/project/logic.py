# -*- coding:utf-8 -*-

from pony.orm import db_session, delete, select
from pony.orm.serialization import to_dict

from jmonitor.models import Template, Project
from services import gen_fields
from services.tasks import ProjectTask


@db_session
def add_projects(projects, app):
    for project in projects:
        program = project.get("program")
        process_name = project.get("process_name")
        command = project.get("command")
        numprocess = int(project.get("numprocess"))
        port = int(project.get("port"))

        # 添加一个定时任务
        app.tasks[program] = ProjectTask(program, 1000 * 5)
        if Template.exists(program=program):
            return dict(
                msg="program:{0}已经存在".format(program),
                status="fail"
            )

        Template(**project)

        for i in range(numprocess):
            Project(**{
                "program": program,
                "process_name": process_name.format(port=i),
                "command": command.format(port=i + port),
                "numprocess": numprocess,
                "port": port
            })

    return dict(
        status="ok",
        msg=""
    )


@db_session
def remove_projects(programs, app):
    try:

        # 删除定时任务
        for program in programs:
            task = app.tasks.get(program, None)
            if task:
                if task.is_running():
                    task.stop()

                del app.tasks[program]

        delete(p for p in Template if p.program in programs)
        delete(p for p in Project if p.program in programs)

        return dict(
            status="ok",
            msg=""
        )
    except Exception, e:
        return dict(
            status="fail",
            msg=e.message
        )


@db_session
def get_projects(programs=None, fields=None, **kwargs):
    if programs or fields:
        res = eval("select({0} for p in Project {1})".format(
            gen_fields('p', fields),
            "" if not programs else "if p.program in programs"
        ))
    else:
        res = select(p for p in Project)

    _data = res[:] if programs or fields else res.first()
    if __debug__:
        print res.get_sql()
        print to_dict(_data)

    try:
        return dict(
            status="ok",
            data=to_dict(_data)
        )
    except Exception, e:
        return dict(
            status="fail",
            msg=e.message
        )


@db_session
def update_project(program=None, **data):
    try:

        Template[program].set(**data)
        delete(p for p in Project if p.program == program)

        process_name = data.get("process_name")
        command = data.get("command")
        numprocess = int(data.get("numprocess"))
        port = int(data.get("port"))
        for i in range(numprocess):
            Project(**{
                "program": program,
                "process_name": process_name.format(port=i),
                "command": command.format(port=i + port),
                "numprocess": numprocess,
                "port": port
            })
        return dict(
            status="ok",
            msg=""
        )
    except Exception, e:
        return dict(
            status="fail",
            msg=e.message
        )


if __name__ == '__main__':
    pass

'''
db.insert("Person", name="Ben", age=33, returning='id')

x = "John"
data = db.select("* from Person where name = $x")

data = db.select("* from Person where name = $x", {"x" : "Susan"})

data = db.select("* from Person where name = $(x.lower()) and age > $(y + 2)")

select(c for c in Customer).order_by(Customer.name).limit(10)

g = Group[101]
g.students.filter(lambda student: student.gpa > 3)[:]

g.students.order_by(Student.name).page(2, pagesize=3)

g.students.order_by(lambda s: s.name).limit(3, offset=3)

Query.random()

select(p for p in Product if p.price > 100).for_update()

@db_session(retry=3)
def your_function():
    ...

update(p.set(price=price * 1.1) for p in Product if p.category.name == "T-Shirt")

delete(p for p in Product if p.category.name == "Floppy disk")
'''
