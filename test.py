# -*- coding:utf-8 -*-
from tinydb import TinyDB

'''
# 把项目实例的变化添加到etcd中
        host, port = self.application.settings.get("etcd").split(":")
        client = etcd.Client(host=host, port=int(port))
        for i in range(numprocs):
            client.write(
                "/projects/{0}/{1}".format(program, process_name.format(process_num=i)),
                "{0}:{1}".format(get_host_ip(), i + numprocs_start)
            )



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


 # 把项目实例从etcd中删除
        host, port = self.application.settings.get("etcd").split(":")
        client = etcd.Client(host=host, port=int(port))
        client.delete('/projects', recursive=True)
'''
if __name__ == '__main__':
    db = TinyDB('./db.json')


    # db.table('project1').insert_multiple([{'name': 'John', 'age': 22}, {'name': 'John', 'age': 37}, {'name': 'Bob', 'age': 42}])



    # User = Query()
    # print db.search(User.name == 'John')
    # # print db.name
    #
    # project = db.table('project')
    # print project.search(User.name.name == 'John')
    # print project.search(where('name').name == 'John')
    #
    # project1 = db.table('project1')
    #
    # projects = db.table('projects')
    # for i in projects.search(User.name == 122):
    #     print i.eid
    #     print i.eid

    # print isinstance([1,2,{"ss":1}],list)
