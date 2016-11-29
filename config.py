# -*- coding:utf-8 -*-
from os.path import dirname as pdir
from os.path import join as pjoin

ROOT_PATH = pdir(__file__)
settings = dict(
    template_path=pjoin(ROOT_PATH, "templates"),
    static_path=pjoin(ROOT_PATH, "static"),
    xsrf_cookies=False,
    cookie_secret="jlogCFF@#$%^&*()(*^fcxfgs3245$#@$%^&*();'><,.<>FDRYTH$#$^%^&jlog",
    debug=False,
    db_path=pjoin(ROOT_PATH, "db.json"),
)

if __name__ == '__main__':
    pass
