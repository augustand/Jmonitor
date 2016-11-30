# -*- coding:utf-8 -*-
import atexit
import sys
import traceback
from signal import signal, SIGTERM, SIGQUIT, SIGINT

from app import Application
from handlers import Task
from mesc import daemonize

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

    def start(self):
        if options.daemon: daemonize()

        print "http://{}:{}".format("localhost", options.port)
        app = Application({
            "debug": options.debug
        })
        Task(app, 1000 * 5).start()
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


def term_sig_handler(signum, frame):
    print 'catched singal: %d' % signum, frame
    sys.exit()


@atexit.register
def atexit_fun():
    print 'i am exit, stack track:'
    exc_type, exc_value, exc_tb = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_tb)


if __name__ == "__main__":
    parse_command_line()
    signal(SIGTERM, term_sig_handler)
    signal(SIGINT, term_sig_handler)
    signal(SIGQUIT, term_sig_handler)

    AppManage().start()
