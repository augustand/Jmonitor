# -*- coding:utf-8 -*-
import logging
from os.path import dirname as pdir
from os.path import join as pjoin

ROOT_PATH = pdir(pdir(__file__))

logging.basicConfig(
    filename=pjoin(ROOT_PATH, 'db', 'project.log'),
    format='[%(asctime)-15s] [%(processName)s:%(process)d] %(name)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    level=logging.INFO
)

settings = dict(
    template_path=pjoin(ROOT_PATH, "templates"),
    static_path=pjoin(ROOT_PATH, "static"),
    xsrf_cookies=False,
    cookie_secret="jlogCFF@#$%^&*()(*^fcxfgs3245$#@$%^&*();'><,.<>FDRYTH$#$^%^&jlog",
    debug=False,
)

protocols = pjoin(ROOT_PATH, 'protocols')

project = {
    "port": 6000,
    "host": "localhost",
}

numretry = 3

if __name__ == '__main__':
    pass
