import shlex

import spur

LOCAL = ['127.0.0.1', 'localhost']

STATUS_NOT_RUNNING = 0
STATUS_INIT_COMPLETED = 2
STATUS_TEST_STARTED = 3
STATUS_TEST_COMPLETED = 4


class ScaleRunnerDriver(object):
    def __init__(self, config):
        self.command = config['command']
        self.host = config['host']

        if host['address'] in LOCAL:
            self.shell = spur.LocalShell()
        else:
            self.shell = spur.SshShell(hostname=self.host['address'],
                                       username=self.host['username'],
                                       password=self.host['password'])

        self.process = None
        self._status = STATUS_NOT_RUNNING

    def _spawn(command):
        return self.shell.spawn(['sh', '-c', command])

    def _run(command):
        return self.shell.run(['sh', '-c', command])

    def run(self):
        self._status = STATUS_INIT_COMPLETED

    def start_test(self):
        self.process = self._spawn(self.command)
        self._status = STATUS_TEST_STARTED

    def stop_test(self):
        if self.process is not None and not self.process.is_running():
            self.process.send_signal('SIGKILL')
        self.process = None
        self._status = STATUS_NOT_RUNNING

    def status(self):
        if self.process is not None and not self.process.is_running():
            self._status = STATUS_TEST_COMPLETED
        return self._status
