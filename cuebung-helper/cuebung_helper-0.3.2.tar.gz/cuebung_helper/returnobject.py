"""
    COPYRIGHT (C) 2016 by Sebastian Stigler

    NAME
        returnobject.py -- ReturnObjects

    FIRST RELEASE
        2016-06-29  Sebastian Stigler  sebastian.stigler@hs-aalen.de

"""
from os.path import basename
from cuebung_helper import __version__
from .helper import (_islistofstrings, _cmplistofstrings, _cleanresult,
                     _lob2los, Boolean, Text, Config)
from .emitter import emit, MsgType

__author__ = "Sebastian Stigler"
__copyright__ = "Sebastian Stigler"
__license__ = "mit"
__all__ = ['PopenReturnObject', 'ReferenceReturnObject']


class ReturnObject():
    """Object to wrap the complete return stat of a systemcall"""

    def __init__(self, stdout=None, stderr=None, returncode=0, timedout=False,
                 error=None):
        self._stdout = stdout or []
        self._stderr = stderr or []
        self._returncode = returncode
        self._timedout = timedout
        self._error = error or []
        self.checkrep()

    @property
    def stdout(self):
        """Getter for stdout"""
        return self._stdout

    @property
    def stderr(self):
        """Getter for stderr"""
        return self._stderr

    @property
    def returncode(self):
        """Getter for returncode"""
        return self._returncode

    @property
    def timedout(self):
        """Getter for timedout"""
        return self._timedout

    @property
    def error(self):
        """Getter for error"""
        return self._error

    def checkrep(self):
        """Check the internal representation of the entries"""
        if not _islistofstrings(self.stdout):
            raise ValueError("stdout must be a list of strings.")
        if not _islistofstrings(self.stderr):
            raise ValueError("stderr must be a list of strings.")
        if not (isinstance(self.returncode, int) and
                0 <= self.returncode <= 255):
            raise ValueError("returncode is not an integer or the value is "
                             "not in [0, 255].")
        if not isinstance(self.timedout, bool):
            raise ValueError("timedout is not a bool.")
        if not _islistofstrings(self.error):
            raise ValueError("error must be a list of strings.")

    def __repr__(self):
        txt = ("{c}(stdout={o}, stderr={e}, returncode={r}, timedout={t}, "
               "error={x})")
        return txt.format(c=self.__class__.__name__, o=self.stdout,
                          e=self.stderr, r=self.returncode, t=self.timedout,
                          x=self.error)

    def __eq__(self, other):
        """Check if two ReturnObjects are equal"""
        if not isinstance(other, ReturnObject):
            raise TypeError('incompatible types %s == %s' % (type(self),
                                                             type(other)))
        if not _cmplistofstrings(self.stdout, other.stdout):
            return False
        if not _cmplistofstrings(self.stderr, other.stderr):
            return False
        if self.returncode != other.returncode:
            return False
        if self.timedout != other.timedout:
            return False
        if not _cmplistofstrings(self.error, other.error):
            return False
        return True

    def __ne__(self, other):
        """Check if two ReturnObjects are not equal"""
        return not self.__eq__(other)

    def to_dict(self, msg=None):
        """Return a dict"""
        return {'msg': msg, 'stdout': self.stdout, 'stderr': self.stderr,
                'returncode': self.returncode, 'timedout': self.timedout,
                'error': self.error}


class PopenReturnObject(ReturnObject):
    """Parse the output of an Popen call to an ReturnObject"""
    def __init__(self, stdout=None, stderr=None, returncode=0, timedout=False,
                 error=None, cfg=None):
        self._cfg = cfg or Config(False, 'N/A', 'N/A')
        super().__init__(stdout, stderr, returncode, timedout, error)

    @property
    def cfg(self):
        """Getter for cfg"""
        return self._cfg

    @property
    def use_stdin(self):
        """Getter for use_stdin"""
        return self._cfg.use_stdin

    @property
    def command(self):
        """Getter for command"""
        return self._cfg.command

    @property
    def args(self):
        """Getter for args"""
        return self._cfg.args

    def checkrep(self):
        """extedned version"""
        super().checkrep()
        if not isinstance(self.cfg, Config):
            raise ValueError('cfg must be a Config object')
        if not isinstance(self.use_stdin, bool):
            raise ValueError('cfg.use_stdin has to be a bool')
        if not isinstance(self.command, str) or len(self.cfg.command) == 0:
            raise ValueError('cfg.command has to be a none empty string')
        if not isinstance(self.args, str):
            raise ValueError('cfg.args has to be a string')

    def __repr__(self):
        txt = super().__repr__()[:-1]
        txt += ', cfg={c})'.format(c=self.cfg)
        return txt

    @classmethod
    def from_popen(cls, result, error=b'', cfg=None):
        """Create a new RetrunObject from the result of a subprocess.popen
        call"""
        stdout = _cleanresult(result.stdout)
        stderr = _cleanresult(result.stderr)
        error = _lob2los(error.split(b'\n'))
        return cls(stdout, stderr, result.returncode, False, error, cfg)


class ValidationConfig:
    """Config class for the valiation of your RunCode output with the Reference
    """
    timedout = Boolean()
    returncode = Boolean()
    output_linecount = Boolean()
    stderr = Boolean()
    stdout = Boolean()
    error = Boolean()


class EmitMessages:
    """Text for the validaton of your RunCode output"""
    class Passed:
        """Text for passed tests"""
        general = "Test bestanden."

    class Failed:
        """Text for failed tests"""
        general = Text("Test nicht bestanden.")
        timedout = Text("Test wurde abgebrochen, da er zu lange gedauert hat.")
        returncode = Text("Das Programm liefert den falschen Returncode.")
        output_linecount = Text("Die Ausgabe ist zu lang oder zu kurz.")
        stderr = Text("Die stderr Ausgabe ist inkorrekt.")
        stdout = Text("Die stdout Ausgabe ist inkorrekt.")
        error = Text("Es wurden Befehle benutzt, die nicht erlaubt sind.")

    class Template:
        """Template text for the command"""
        commandline_arg = Text("{command} {args}")
        stdin = Text('echo "{args}" | {command}')

    passed = Passed()
    failed = Failed()
    use_stdin = Boolean()
    _templ = Template()

    @property
    def command_templ(self):
        """Getter for the command template"""
        if self.use_stdin:
            return self._templ.stdin
        else:
            return self._templ.commandline_arg

    @command_templ.setter
    def command_templ(self, value):
        """Setter for the command template"""
        if isinstance(value, str):
            if self.use_stdin:
                self._templ.stdin = value
            else:
                self._templ.commandline_arg = value
        else:
            raise ValueError('value must be a string')


class ReferenceReturnObject(ReturnObject):
    """Implements some specific compare functions which emits custom
    messages"""

    def __init__(self, *args, **kwargs):
        self.dont_check = ValidationConfig()
        self.txt = EmitMessages()
        super().__init__(*args, **kwargs)

    def validate(self, other, msg_extra=None):
        """Compare the `other` PopenReturnObject with this one

        Will emit some messages if there are differences in the two objects

        :param other: a `PopenReturnObject` instance
        :param msg_extra: a costum message for the to sent dict.

        :return: True iff  self == other
                 False iff self != other
        """

        if not isinstance(other, PopenReturnObject):
            raise TypeError('validate only results of RunCode')

        msg = self._merge(other)

        if msg_extra is not None:
            msg['msg_extra'] = msg_extra

        self.txt.use_stdin = other.use_stdin
        command = self.txt.command_templ
        msg['command'] = command.format(  # pylint: disable=E1101
            command=basename(other.command),
            args=other.args)
        for event in ['timedout', 'returncode', 'output_linecount', 'stderr',
                      'stdout', 'error']:
            if len(msg[event]) == 2:
                if not getattr(self.dont_check, event):
                    msg['msg'] = getattr(self.txt.failed, event)
                    emit(msg, msgtype=MsgType['failed_' + event])
                    return False
        if self != other:
            msg['msg'] = self.txt.failed.general
            emit(msg, msgtype=MsgType.failed)
            return False

        msg['msg'] = self.txt.passed.general
        emit(msg, msgtype=MsgType.passed)
        return True

    def _merge(self, other):
        """Merge the dict of self and other

        Add a `result` subkey to the <key> entry if the <key> entries of self
        and other are not equal.

        :param other: a `PopenReturnObject` instance
        :return: `dict` with merged entries
        """
        self_dict = self.to_dict()
        other_dict = other.to_dict()
        result = {}
        txt_olc = 'output_linecount'
        result[txt_olc] = {'reference': 0}
        result_lc = 0
        for key in other_dict.keys():
            if key.startswith('msg'):
                continue
            result[key] = {}
            result[key]['reference'] = self_dict[key]
            if isinstance(other_dict[key], list):
                if key in ['stdout', 'stderr']:
                    result[txt_olc]['reference'] += len(self_dict[key])
                    result_lc += len(other_dict[key])
                if not _cmplistofstrings(self_dict[key], other_dict[key]):
                    result[key]['result'] = other_dict[key]
            else:
                if self_dict[key] != other_dict[key]:
                    result[key]['result'] = other_dict[key]
        if result_lc != result[txt_olc]['reference']:
            result[txt_olc]['result'] = result_lc
        return result

# vim: ft=python ts=4 sta sw=4 et ai
# python: 3
