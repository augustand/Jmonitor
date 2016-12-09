# -*- coding:utf-8 -*-


import sys

from settings import ROOT_PATH, protocols

sys.path.append(ROOT_PATH)

reload(sys)
sys.setdefaultencoding('utf-8')

# sys.path.append('../')
# sys.path.append('gen-py')
# sys.path.insert(0, glob.glob('../../lib/py/build/lib*')[0])



if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(description='project service')
    parser.add_argument('-p', action="store", default=6000, type=int, dest='port', help='project port default 6000')
    parser.add_argument('-debug', action="store", default=True, type=bool, dest='debug', help='debug default true')
    parser.add_argument('-daemon', action="store", default=False, type=bool, dest='daemon', help='daemon default false')
    p = parser.parse_args()

    if p.daemon:
        from misc import daemonize

        daemonize()

    import thriftpy
    from os.path import join as pjoin
    from thriftpy.rpc import make_server
    from service.project_handle import ProjectHandle

    project_thrift = thriftpy.load(pjoin(protocols, "project.thrift"), module_name="project_thrift")
    server = make_server(project_thrift.ProjectHandle, ProjectHandle(), port=p.port)
    server.serve()
