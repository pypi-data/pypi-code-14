"""
    COPYRIGHT (C) 2016 by Sebastian Stigler

    NAME
        runcode.py -- Run c code

    FIRST RELEASE
        2016-07-04  Sebastian Stigler  sebastian.stigler@hs-aalen.de

"""
import errno
import os
from shlex import quote
from subprocess import Popen, PIPE
from cuebung_helper import __version__
from .timeout_decorator import timeout as mytimeout, MyTimeoutError
from .returnobject import PopenReturnObject, ReferenceReturnObject
from .helper import _islistofstrings, Command, Config
from .emitter import emit, MsgType

__all__ = ['RunCode', 'Command', 'Make']
__author__ = "Sebastian Stigler"
__copyright__ = "Sebastian Stigler"
__license__ = "mit"

BLOCK_SIZE = 100000


class RunCode():
    """Run c code in a subprocess"""

    def __init__(self, command, args=None, formatlist=None, timeout=5,
                 fifo='error'):
        if isinstance(command, Command):
            self._command = command
        else:
            self._command = Command('', command)
        self._args = args or ()
        self._formatlist = formatlist or []
        self._timeout = timeout
        self._fifo = fifo
        self._fifofd = None
        self.checkrep()
        # May fail with TypeError if the args and argsstring don't fit together
        self._argsstringlist = [fstr % arg for fstr, arg in
                                zip(self.formatlist, self.args)]

    @property
    def cmd(self):
        """Getter for cmd"""
        return ' '.join(self.command).strip()

    @property
    def command(self):
        """Getter for command"""
        return self._command

    @property
    def args(self):
        """Getter for args"""
        return self._args

    @property
    def formatlist(self):
        """Getter for formatlist"""
        return self._formatlist

    @property
    def argsstring(self):
        """Getter for argsstring"""
        return " ".join(self._argsstringlist)

    @property
    def argsstringlist(self):
        """Getter for argsstring"""
        return self._argsstringlist

    @property
    def quoted_argsstring(self):
        """Getter for quoted argssting"""
        return ' ' + ' '.join(quote(arg) for arg in self.argsstringlist)

    @property
    def timeout(self):
        """Getter for timeout"""
        return self._timeout

    @property
    def fifo(self):
        """Getter for fifo"""
        return self._fifo

    def _cfg(self, use_stdin):
        """Get config  for PopenReturnObject"""
        if use_stdin:
            return Config(use_stdin, self.command.filename, self.argsstring)
        else:
            return Config(use_stdin, self.command.filename,
                          self.quoted_argsstring)

    def checkrep(self):
        """Consistency check"""
        if not isinstance(self.command.ldpreload, str):
            raise ValueError('command.ldpreload must be a string')
        if not (len(self.command.ldpreload) == 0 or
                self.command.ldpreload.startswith('LD_PRELOAD=')):
            raise ValueError('command.ldpreload must be empty or start with '
                             '"LD_PRELOAD="')
        if not (isinstance(self.command.filename, str) and
                len(self.command.filename) > 0):
            raise ValueError('command.filename must be a none empty string')
        if not isinstance(self.args, tuple):
            raise ValueError('args has to be a tuple of values or None')
        if not _islistofstrings(self.formatlist):
            raise ValueError('formatlist must be a list of formatstrings')
        if not all(entry.startswith('%') for entry in self.formatlist):
            raise ValueError('formatlist must be a string composed of '
                             'space separated formatstrings like "%s" "%d" '
                             'and "%f" (including padding and truncation)')
        if len(self.formatlist) != len(self.args):
            raise ValueError('formatlist and args must be of equal length')
        if not (isinstance(self.timeout, (int, float)) and self.timeout >= 0):
            raise ValueError('timeout must be an positiv number')
        if not isinstance(self.fifo, str) or len(self.fifo) < 1:
            raise ValueError('fifo mut be a valid filename for a named pipe')

    def _prepare_named_pipe(self):
        """Prepare a new named pipe

        :return: a read and non blocking file descripter to the fifo
        """
        if os.path.exists(self.fifo):
            os.unlink(self.fifo)  # pragma: no cover
        if not os.path.exists(self.fifo):  # pragma: no cover
            os.mkfifo(self.fifo, 0o600)
        self._fifofd = os.open(self.fifo, os.O_RDONLY | os.O_NONBLOCK)

    def _fetch_named_pipe(self):
        """Fetch data from named pipe

        :return: bytestring
        """
        try:
            error = os.read(self._fifofd, BLOCK_SIZE)
        except IOError as err:  # pragma: no cover
            if (err.errno == errno.EAGAIN or  # pragma: no cover
                    err.errno == errno.EWOULDBLOCK):  # pragma: no cover
                error = b''  # pragma: no cover
            else:  # pragma: no cover
                raise  # pragma: no cover
        return error

    def _cleanup_named_pipe(self):
        """Cleanup named pipe"""
        os.close(self._fifofd)
        if os.path.exists(self.fifo):  # pragma: no cover
            os.unlink(self.fifo)

    def _run(self, use_stdin):
        """Run the command and store the result in a PopenReturnObject

        :param use_stdin: stream the argument via stdin to the program or pass
            the arguments as commandline parameters.

        :return: a `PopenReturnObject`
        """
        cmd = self.cmd
        if not use_stdin:
            cmd += self.quoted_argsstring
        res = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE,
                    bufsize=0)
        if use_stdin:
            argsstring = self.argsstring + '\n'
            res.stdin.write(argsstring.encode())
        res.wait()
        error = self._fetch_named_pipe()
        return PopenReturnObject.from_popen(res, error, self._cfg(use_stdin))

    def run(self, use_stdin=False):
        """Run the command under the timeout constraint"""
        self._prepare_named_pipe()
        try:
            ret = mytimeout(self.timeout, False)(self._run)(use_stdin)
        except MyTimeoutError:
            ret = PopenReturnObject(timedout=True, cfg=self._cfg(use_stdin))
        finally:
            self._cleanup_named_pipe()
        return ret

    def __repr__(self):
        txt = "{n}(cmd={c}, args={a}, formatlist={s}, timeout={t}, fifo={f})"
        return txt.format(n=self.__class__.__name__, c=self.cmd, a=self.args,
                          s=self.formatlist, t=self.timeout, f=self.fifo)


class Make():
    """Wrapper for make, make clean and make test"""

    txt_clean_err = 'Ausführung von "make clean" ist fehlgeschlagen.'
    txt_timeout = 'Das Kompilieren dauert zu lange.'
    txt_errors = 'Es sind Kompiler-Fehler aufgetreten.'
    txt_warnings = 'Es sind Kompiler Warnungen aufgetreten.'
    txt_ok = 'Das Kompilieren war erfolgreich.'

    def __init__(self, ignore_warnings=False, timeout=30):
        self.timeout = timeout
        self.ignore_warnings = ignore_warnings

    def clean(self):
        """Run make clean, check result and emit messages"""
        result = RunCode('make', ('clean',), ['%s'],
                         timeout=self.timeout).run()
        if result.timedout or result.returncode != 0:
            reference = ReferenceReturnObject()
            msg = reference._merge(result)  # pylint: disable=W0212
            msg['msg_extra'] = 'make clean'
            msg['msg'] = self.txt_clean_err
            emit(msg, msgtype=MsgType.failed)
            return False
        return True

    def test(self):
        """Run make test, check result and emit messages"""
        result = RunCode('make', ('test',), ['%s'], timeout=self.timeout).run()
        return self.checkresult(result, 'make test')

    def all(self):
        """Run make all, check result and emit messages"""
        result = RunCode('make', ('all',), ['%s'], timeout=self.timeout).run()
        return self.checkresult(result, 'make all')

    def checkresult(self, result, msg_extra):
        """check result and emit message"""
        reference = ReferenceReturnObject()
        msg = reference._merge(result)  # pylint: disable=W0212
        msg['msg_extra'] = msg_extra
        cls = self.__class__

        if result.timedout:
            msg['msg'] = cls.txt_timeout
            emit(msg, msgtype=MsgType.failed_timedout)
            return False
        if result.returncode != 0:
            msg['msg'] = cls.txt_errors
            emit(msg, msgtype=MsgType.failed_returncode)
            return False
        if result.stderr != []:
            msg['msg'] = cls.txt_warnings
            emit(msg, msgtype=MsgType.failed_stderr)
            return self.ignore_warnings
        else:
            msg['msg'] = cls.txt_ok
            emit(msg, msgtype=MsgType.passed)
            return True

# vim: ft=python ts=4 sta sw=4 et ai
# python: 3
