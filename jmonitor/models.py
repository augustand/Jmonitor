# -*- coding:utf-8 -*-


from pony.orm import Required, PrimaryKey, Optional

from jmonitor.settings import db


class Project(db.Entity):
    _table_ = "Projects"
    id = PrimaryKey(int, auto=True, index=0)
    program = Required(str)
    process_name = Required(str)
    command = Required(str)
    numprocess = Required(int)
    port = Required(int)
    pid = Optional(int)
    numretry = Required(int, default=3)


class Template(db.Entity):
    _table_ = "Templates"
    program = PrimaryKey(str)
    process_name = Required(str)
    command = Required(str)
    numprocess = Required(int)
    port = Required(int)
    numretry = Required(int, default=3)


class Task(db.Entity):
    _table_ = "Tasks"
    pass


db.generate_mapping(create_tables=True)
