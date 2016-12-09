from os.path import join as pjoin

import thriftpy
from thriftpy.rpc import make_client

from gateway.settings import protocols

project_thrift = thriftpy.load(pjoin(protocols, "project.thrift"), module_name="project_thrift")
print project_thrift

c = make_client(project_thrift.ProjectHandle, port=6000)
print c
print c.get_projects("{}")
