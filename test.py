# -*- coding:utf-8 -*-
from tinydb import Query
from tinydb import TinyDB
from tinydb import where


def _main():
    '''
    API设计实践,以user为例

    获取所有的,分页的,片段的用户数据
    GET /api/users -d {"page":1,"size":2,"skip":3,fields:["user_name","passwd"]}

    添加一个用户
    POST /api/users -d {"user_name":123}

    批量删除数据,
    DELETE /api/users -d {user_ids:[user_id1,user_id2,...]}

    批量修改数据
    PUT /api/users -d {user_ids:[user_id1,user_id2,...],data:{"user_name":12345,"passwd":2222}}



    '''
    pass


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
