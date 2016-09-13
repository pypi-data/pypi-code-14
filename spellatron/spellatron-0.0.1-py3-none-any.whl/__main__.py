import time
import signal
import logging

from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import define, options, parse_command_line

from . import applications


define(u'port', default=8080, type=int, help=u'Server port to bind to')
define(u'host', default=u'127.0.0.1', type=str, help=u'Server host')


def shutdown(server_instance):
    ioloop_instance = IOLoop.instance()
    logging.info(u'Stopping push server gracefully.')
    server_instance.stop()

    def finalize():
        ioloop_instance.stop()
        logging.info(u'Push server stopped.')

    ioloop_instance.add_timeout(time.time() + 1.5, finalize)


class AppRunner(object):
    application_class = applications.DefaultApplication

    def start(self):
        application = self.application_class(**options.as_dict())
        server = HTTPServer(application)
        server.listen(options.port, options.host)
        shutdown_handler = lambda sig, frame: shutdown(server)
        signal.signal(signal.SIGINT, shutdown_handler)
        signal.signal(signal.SIGTERM, shutdown_handler)
        logging.info(u"Starting push server on {0}:{1}.".format(
            options.host, options.port
        ))
        IOLoop.instance().start()


def main():
    parse_command_line()
    runner = AppRunner()
    runner.start()


if __name__ == u'__main__':
    main()
