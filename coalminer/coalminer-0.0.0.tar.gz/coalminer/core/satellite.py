import json
import time
import random
import uuid
import gevent
import logging
import coloredlogs
import zmq.green as zmq
from collections import defaultdict
from agentzero.core import SocketManager


logger = logging.getLogger('pipeline')


class Pipeline(object):
    def __init__(self):
        self.id = uuid.uuid4().hex
        self.context = zmq.Context()
        self.sockets = SocketManager(zmq, self.context)
        self.sockets.create('jobs_out', zmq.REP)
        size = 1024
        self.sockets.set_socket_option('jobs_out', zmq.SNDHWM, size)
        self.sockets.set_socket_option('jobs_out', zmq.RCVHWM, size)
        self.counters = defaultdict(int)

    @property
    def name(self):
        return self.__class__.__name__

    def reply_job(self):
        request = self.sockets.recv_safe('jobs_out', polling_timeout=-1)
        if request:
            phase = request['phase']

            last_job = request.pop('last_job', None)
            if last_job is not None:
                if 'error' in last_job:
                    self.counters[b'.'.join([phase['name'], bytes(phase['id']), 'failure'])] += 1
                    logger.info("{error}".format(**last_job))
                else:
                    self.counters[b'.'.join([phase['name'], bytes(phase['id']), 'success'])] += 1
                    logger.debug("JOB DONE: {0}".format(last_job))

            logger.debug("JOB REQUESTED %s", request)

            phase_id = phase['id']
            phase_name = phase['name']
            phase_identity = b'.'.join([phase_name, bytes(phase_id)])

            self.sockets.set_socket_option('jobs_out', zmq.IDENTITY, bytes(phase_identity))
            args = {}

            if phase['name'] == 'RandomGenerator':
                args[b'size'] = 1024
                args[b'encoding'] = bytes(random.choice(['hex', 'base64']))

            elif phase['name'] == 'StringReverser':
                args[b'string'] = 'Foo Bar Amazing'

            return self.sockets.send_safe('jobs_out', {
                'job': phase['name'],
                'arguments': args
            }, polling_timeout=-1)

    def bind(self):
        self.sockets.bind('jobs_out', 'tcp://127.0.0.1:3000', zmq.POLLIN | zmq.POLLOUT)

    def loop_once(self):
        self.reply_job()
        gevent.sleep()

    def run(self):
        self.bind()

        while True:
            self.loop_once()
            logger.info(json.dumps(dict(self.counters), indent=2))


def main():
    import gevent.monkey
    coloredlogs.install(level=logging.INFO)
    gevent.monkey.patch_all()

    Pipeline().run()


if __name__ == '__main__':
    main()
