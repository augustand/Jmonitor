# -*- coding:utf-8 -*-
import os
import sys
import traceback

from app import Application

reload(sys)
sys.setdefaultencoding('utf-8')

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, parse_command_line, options

define("port", default=6752, help="run on the given port", type=int)
define("debug", default=True, help="run on the given debug", type=bool)
define("daemon", default=False, help="run on the given daemon", type=bool)


class AppManage(object):
    def __init__(self):
        parse_command_line()

    def daemonize(self):
        try:
            # this process would create a parent and a child
            pid = os.fork()
            if pid > 0:
                # take care of the first parent
                sys.exit(0)
        except OSError, err:
            sys.stderr.write("Fork 1 has failed --> %d--[%s]\n" % (err.errno,
                                                                   err.strerror))
            sys.exit(1)

        # change to root
        os.chdir('/')
        # detach from terminal
        os.setsid()
        # file to be created ?
        os.umask(0)
        try:
            # this process creates a parent and a child
            pid = os.fork()
            if pid > 0:
                print "Daemon process pid %d" % pid
                # bam
                sys.exit(0)
        except OSError, err:
            sys.stderr.write("Fork 2 has failed --> %d--[%s]\n" % (err.errno,
                                                                   err.strerror))
            sys.exit(1)

        sys.stdout.flush()
        sys.stderr.flush()

    def start(self):
        if options.daemon:
            self.daemonize()

        print "http://{}:{}".format("localhost", options.port)
        app = Application({
            "debug": options.debug
        })
        HTTPServer(app).listen(options.port)

        loop = IOLoop.instance()
        try:
            loop.start()
        except KeyboardInterrupt:
            print(" Shutting down on SIGINT!")
            loop.stop()
            traceback.format_exc()
        finally:
            pass


if __name__ == "__main__":
    AppManage().start()
