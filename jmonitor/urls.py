# -*- coding:utf-8 -*-
from services.project import MainHandler
from services.project.handle import ProjectsHandler, ProjectsActionHandler, ProjectHandler

handlers = [
    (r"/", MainHandler),
    (r"/api/projects/?", ProjectsHandler),
    (r"/api/projects/actions/?", ProjectsActionHandler),
    (r"/api/projects/(?P<program>[^/]+)/?", ProjectHandler),
    (r"/api/projects/(?P<program>[^/]+)/(?P<action>[^/]+)/?", ProjectHandler),
]
