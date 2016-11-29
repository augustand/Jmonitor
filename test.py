# -*- coding:utf-8 -*-
from tinydb import Query
from tinydb import TinyDB
from tinydb import where

if __name__ == '__main__':
    db = TinyDB('./db.json')

    # db.table('project1').insert_multiple([{'name': 'John', 'age': 22}, {'name': 'John', 'age': 37}, {'name': 'Bob', 'age': 42}])



    User = Query()
    print db.search(User.name == 'John')
    # print db.name

    project = db.table('project')
    print project.search(User.name.name == 'John')
    print project.search(where('name').name == 'John')

    project1 = db.table('project1')

    projects = db.table('projects')
    for i in projects.search(User.name == 122):
        print i.eid
        print i.eid
