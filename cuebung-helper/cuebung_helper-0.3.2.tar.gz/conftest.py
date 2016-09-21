"""
    COPYRIGHT (C) 2016 by Sebastian Stigler

    NAME
        conftest.py

    FIRST RELEASE
        2016-07-28  Sebastian Stigler  sebastian.stigler@hs-aalen.de

"""
import pytest
from magic import Magic, MagicException

DEFAULT_EXT = '.py,.md'
DEFAULT_ENC = 'us-ascii,utf-8'


def pytest_addoption(parser):
    """Define options"""
    group = parser.getgroup("general")
    group.addoption('--checkencoding', action='store_true',
                    help="check files for the correct encoding")
    parser.addini("ce_ignore", type="linelist",
                  help="each line specifies a glob pattern of files to ignore")
    parser.addini("ce_ext",
                  help="comma separated extentions (default %s)" % DEFAULT_EXT)
    parser.addini("ce_encoding",
                  help="comma separated encodings (default %s)" % DEFAULT_EXT)


def pytest_sessionstart(session):
    """Initialite some additional attributes of config"""
    config = session.config
    if config.option.checkencoding:
        config.ce_ignore = Ignorer(config.getini("ce_ignore"))
        config.ce_ext = config.getini("ce_ext") or DEFAULT_EXT
        config.ce_encoding = config.getini("ce_encoding") or DEFAULT_ENC


def pytest_collect_file(parent, path):
    """Collect files to test for correct encoding"""
    config = parent.config
    if not config.option.checkencoding:
        return
    if path.ext in config.ce_ext.split(','):
        ignore = config.ce_ignore(path)
        if not ignore:
            return EncodingFile(path, parent)


class EncodingFile(pytest.File):  # pylint: disable=E1101
    """EncodingFile"""

    def collect(self):
        """Detect the encoding of the file"""
        blob = self.fspath.open('rb').read()
        magic = Magic(mime_encoding=True)
        try:
            encoding = magic.from_buffer(blob)
        except MagicException:
            self.add_marker('skip')
            encoding = None
        path = self.fspath
        ppath = self.parent.fspath
        rel_path = path.strpath.replace(ppath.strpath, '', 1)[1:]
        spec = (rel_path, encoding)
        enc = self.parent.config.ce_encoding
        yield EncodingItem('Check file encoding [%s]' % enc, self, spec)


class EncodingItem(pytest.Item):  # pylint: disable=E1101
    """EncodingItem"""

    def __init__(self, name, parent, spec):
        super(EncodingItem, self).__init__(name, parent)
        self.spec = spec
        self.add_marker('encoding')

    def runtest(self):
        """Do the actual encoding check"""
        config = self.parent.config
        if self.spec[1].lower() not in config.ce_encoding.split(','):
            raise EncodingException(self, self.spec)

    def repr_failure(self, excinfo):
        """ called when self.runtest() raises an exception. """
        enc = self.parent.config.ce_encoding
        if isinstance(excinfo.value, EncodingException):
            return "\n".join([
                "Wrong encoding detected. Expacted encoding in [%s]." % enc,
                "   Detected encoding of %r: %r" % excinfo.value.args[1]
            ])
        else:
            return "%r" % excinfo.value

    def reportinfo(self):
        """Infotest on failure"""
        return self.fspath, 1, "usecase: %s %s" % (self.name, self.spec)


class EncodingException(Exception):
    """ custom exception for error reporting. """


class Ignorer:
    """Ignorer Class"""
    def __init__(self, ignorelines):
        self.ignores = ignores = []
        for line in ignorelines:
            i = line.find("#")
            if i != -1:
                line = line[:i]
            ignores.append(line)

    def __call__(self, path):
        for glob in self.ignores:
            if path.fnmatch(glob):
                return True
        return False
# vim: ft=python ts=4 sta sw=4 et ai
# python: 3
