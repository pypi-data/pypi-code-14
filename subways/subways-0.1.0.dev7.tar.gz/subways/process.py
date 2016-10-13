# MIT License

# Copyright (c) 2016 Alexis Bekhdadi (midoriiro) <contact@smartsoftwa.re>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# TODO: write module, function, class, method docstring
# pylint: disable=missing-docstring

import time
import fcntl
import os
import shlex
import subprocess

from subways.utils import AttributeDict


PIPE = subprocess.PIPE
STDOUT = subprocess.STDOUT
DEVNULL = subprocess.DEVNULL


class CommandNotFoundError(Exception):
    pass


class ProcessInputError(Exception):
    pass


class ProcessOutputError(Exception):
    pass


def check_system_command(program):
    for path in os.environ["PATH"].split(os.pathsep):
        path = path.strip('"')
        path = os.path.join(path, program)

        if os.path.exists(path) and os.path.isfile(path):
            return True

    raise CommandNotFoundError(
        '\'{0}\' is not in environment path. '
        'Use your system package manager to install it.'.format(program)
    )


def execute_command(command, stdout=subprocess.PIPE):
    try:
        if isinstance(command, str):
            command = shlex.split(command)

        check_system_command(command[0])

        logger.debug('execute command: %s', ' '.join(command))

        process = subprocess.run(
            command,
            shell=False,
            stdout=stdout,
            stderr=subprocess.STDOUT
        )

        if process.returncode == 0:
            return str(process.stdout.decode('utf-8'))
        else:
            raise subprocess.CalledProcessError(process.returncode, command)
    except SystemCommandNotFound as exception:
        raise exception


class ProcessSettings(AttributeDict):
    pass


class ProcessIOBuffer(AttributeDict):
    pass


class Process:
    def __init__(self, cmd):
        if isinstance(cmd, str):
            cmd = shlex.split(cmd)
        else:
            raise ValueError('Describe your command line as a string.')

        self._cmd = cmd
        self._process = None
        self._settings = None
        self._buffers = ProcessIOBuffer

        self._buffers.stdin = []
        self._buffers.stdout = []
        self._buffers.stderr = []

    def __str__(self):
        return self._cmd

    def buffers(self):
        return self._buffers

    def clear_buffers(self):
        self._buffers.stdin = []
        self._buffers.stdout = []
        self._buffers.stderr = []

    def settings(self):
        return self._settings

    def create(self, **kwargs):
        self._settings = ProcessSettings(
            cmd=self._cmd,
            shell=kwargs.get('shell', False),
            stdin=kwargs.get('stdin', None),
            stdout=kwargs.get('stdout', None),
            stderr=kwargs.get('stderr', None),
            env=kwargs.get('env', None),
            buffered=kwargs.get('buffered', True),
            decode=kwargs.get('decode', True)
        )

        if self._settings.shell:
            self._settings.cmd = shlex.quote(' '.join(self._cmd))

    def _set_non_blocking_file(self, file):
        flags = fcntl.fcntl(file.fileno(), fcntl.F_GETFL)
        fcntl.fcntl(file.fileno(), fcntl.F_SETFL, flags | os.O_NONBLOCK)

    def start(self, blocking=True):
        try:
            self._process = subprocess.Popen(
                self._settings.cmd,
                shell=self._settings.shell,
                stdin=self._settings.stdin,
                stdout=self._settings.stdout,
                stderr=self._settings.stderr,
                env=self._settings.env,
                bufsize=-1 if self._settings.buffered else 0,
                universal_newlines=self._settings.decode
            )
        except ValueError:
            raise ValueError('Arguments are not valid to create process.')

        self._settings.blocking = blocking

        if blocking:
            self._process.wait()
        else:
            self._set_non_blocking_file(self._process.stdout)
            self._set_non_blocking_file(self._process.stderr)

    def stop(self):
        self._process.terminate()

    def wait_exit(self):
        if not self._settings.blocking and self.is_running():
            while self.is_running():
                try:
                    self._process.wait(timeout=0.001)
                except subprocess.TimeoutExpired:
                    pass

    def kill(self):
        self._process.kill()

    def is_running(self):
        return self._process.returncode is None

    def readlines(self, buffer, keep_empty=True, timeout=0):
        if buffer == 'stdout':
            buffer = self._process.stdout
            buffer_copy = self._buffers.stdout
        elif buffer == 'stderr':
            buffer = self._process.stderr
            buffer_copy = self._buffers.stderr
        elif buffer == 'stdin':
            buffer = self._process.stdin
            buffer_copy = self._buffers.stdin
        else:
            raise ValueError('\'buffer\' {0} doesn\'t exist.'.format(buffer))

        if buffer is None:
            return None

        if timeout < 0:
            raise ValueError(
                '\'timeout\' must be equal or greater than 0.'
            )

        time_delta = 0
        process_timeout = 0.001
        buffer_lines = []

        while True:
            try:
                if not self._settings.blocking:
                    self._process.wait(timeout=process_timeout)
                else:
                    raise subprocess.TimeoutExpired(self._settings.cmd, 0)
            except subprocess.TimeoutExpired:
                buffer_line = buffer.readline()

                if not buffer_line and not buffer_lines:
                    continue
                elif not buffer_line and buffer_lines:
                    break

                buffer_lines.append(buffer_line)

                time_delta += process_timeout

                if timeout > 0 and time_delta >= timeout:
                    break

        if not keep_empty:
            buffer_lines = list(filter(None, buffer_lines))

        buffer_copy.extend(buffer_lines)

        return buffer_lines

    def write(self, data):
        length = None

        if self._process.stdin and len(data) > 0:

            if not self._settings.decode:
                data = data.encode()

            length = self._process.stdin.write(data)
            self._buffers.stdin.append(data)
            self._process.stdin.flush()

            time.sleep(0.1)

        return length
