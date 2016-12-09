# -*- coding:utf-8 -*-
import argparse
import sys

import thriftpy
from thriftpy.rpc import make_server

sys.path.append('../')
# sys.path.append('gen-py')
# sys.path.insert(0, glob.glob('../../lib/py/build/lib*')[0])



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='project service')
    parser.add_argument(
        '-p',
        action="store",
        default=6000,
        type=int,
        dest='port',
        help='project port default 6000'
    )
    p = parser.parse_args()

    from os.path import join as pjoin
    from project.settings import protocols
    from project.service.project_handle import ProjectHandle

    project_thrift = thriftpy.load(pjoin(protocols, "project.thrift"), module_name="project_thrift")
    server = make_server(project_thrift.ProjectHandle, ProjectHandle(), port=p.port)
    server.serve()
