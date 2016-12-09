# -*- coding:utf-8 -*-

import logging
from os.path import dirname as pdir
from os.path import join as pjoin

from pony.orm import Database

ROOT_PATH = pdir(pdir(__file__))
DB_PATH = pjoin(ROOT_PATH, 'db', 'project.db')
logging.basicConfig(
    filename=pjoin(ROOT_PATH, 'db', 'project.log'),
    format='[%(asctime)-15s] [%(processName)s:%(process)d] %(name)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    level=logging.INFO
)

db = Database('sqlite', DB_PATH, create_db=True)

protocols = pjoin(ROOT_PATH, 'protocols')
