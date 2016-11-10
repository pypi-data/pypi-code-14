# coding: utf-8

# Asynchronous Music Player Daemon client library for Python

# Copyright (C) 2015 Itaï BEN YAACOV

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import inspect


def worker(f, *args):
    """
    Decorator for worker functions.

    The first argument of a function decorated by @worker ('self', when decorating a method) must be either
    a. A Client.
    b. A WorkerGroup.
    c. An object with a WorkerGroup attribute named 'ampd_worker_group'.

    A worker function returns a Worker.
    """

    argspec = inspect.getargspec(f)
    def_locals = dict(Worker=Worker, f=f, __builtins__={})
    def_strs = dict(name=f.__name__, args=inspect.formatargspec(*argspec[:3])[1:-1], arg0=argspec.args[0])
    if args:
        def_locals['retval'] = args[0]
        def_strs['extra'] = ' and retval'
    else:
        def_strs['extra'] = ''
    if f.__name__ == '<lambda>':
        g = eval('lambda {args}: Worker(f({args}), {arg0}.ampd_worker_group){extra}'.format(**def_strs), def_locals)
    else:
        exec('def {name}({args}): return Worker(f({args}), {arg0}.ampd_worker_group){extra}'.format(**def_strs), def_locals)
        g = def_locals[f.__name__]
    g.__defaults__ = f.__defaults__
    g.__doc__ = f.__doc__
    return g


def worker_retval(retval):
    """
    Decorator factory for worker functions.

    Decorated worker function will return 'retval' instead of a Worker object.
    """
    return lambda f: worker(f, retval)


class Worker(object):
    """
    AMPD worker.

    Created by a worker function, namely, a python generator decorated by @worker:

       @worker
       def worker_example(arg1, ...):
           ...
           reply = yield request1(a, b)
           ...
           reply = yield request2()
           ...

    The first argument for the worker function (self, if a method) must be one of:

    a. A Client.
    b. A WorkerGroup.
    c. An object with a WorkerGroup attribute named 'ampd_worker_group'.

    The function returns a new Worker immediately.
    Its code is later executed by the main loop.
    A statement of the form:

        reply = yield request

    suspends execution until something happens and a reply is available.
    The request can be:

    a. An MPD command (other than 'idle' and 'noidle').
       Returns when the server's reply arrives:

           yield play(5)
           reply = yield status()

    b. A command list, returns a list of replies:

           yield command_list(command, ... | iterable)

    c. A passive request, emulating MPD's 'idle' command, with some improvements.
       Returns as soon as one of the conditions is satisfied, with a list of the satisfied conditions:

           reply = yield condition, ... | iterable

       Conditions can be:

       - A SUBSYSTEM name (in uppercase) or ANY to match any subsystem.
       - TIMEOUT(ms) - satisfied after 'ms' milliseconds.
       - CONNECT - client is connected to server.
       - IDLE - client is idle.
       - WORKER(worker, ... | iterable) - all workers are done.

    d. Special request:

           yield _self()

       Returns the executing Worker.

    e. A request list.
       Requests need not be commands.
       Can be slow.

           yield request, ... | iterable

    For MPD commands and subsystems see http://www.musicpd.org/doc/protocol/command_reference.html
    """

    def __init__(self, gen, group):
        self.name = gen.gi_code.co_name
        if not group._client:
            raise RuntimeError("Attempting to start a Worker in a closed WorkerGroup")
        self._gen = gen
        self._group = group
        self._atexit = []
        self._reply = self._request = None
        group._workers.append(self)
        group._client._execute(self)

    def _die(self):
        self._group._workers.remove(self)
        for f in self._atexit:
            f()
        self._gen = self._group = self._atexit = self._reply = None
        self.name += ' (closed)'

    def kill(self):
        """
        Terminate Worker execution.
        """
        if self._gen:
            if self._request:
                self._request._finish(None)
            self._die()

    def add_atexit(self, f):
        """
        Add a cleanup function to be called when the Worker exits.
        """
        self._atexit.append(f)

    def __repr__(self):
        return self.name

    def step(self):
        if not self._gen:
            raise StopIteration
        try:
            reply, self._reply = self._reply, None
            return self._gen.throw(reply) if isinstance(reply, Exception) else self._gen.send(reply)
        except:
            self._die()
            raise
