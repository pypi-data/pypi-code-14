import os
import ctypes
import logging
import platform
import re
import sys
import time

from ctypes import (c_char, c_char_p, c_int, c_size_t, c_void_p, POINTER,
                    pointer, c_bool, cast, byref)
from ctypes.util import find_library
from collections import namedtuple
from enum import Enum
from locale import setlocale, LC_NUMERIC
from os import path
from six import string_types
from subprocess import Popen, PIPE
from textwrap import dedent

from .captured_output import captured_output
from ..constant import *
from ..exception import *
from .tecutil import _TecUtil

log = logging.getLogger(__name__)


class ManagerStartReturnCode(Enum):
    Ok                              = 0
    HomeDirectoryNotSpecified       = 1
    LicenseFileNotFound             = 2
    LicenseIsInvalid                = 3
    LicenseExpired                  = 4
    InternalInitializationError     = 5
    EngineUninitialized             = 6
    LicenseFileContainsPermanent    = 7


def find_file(filenames, searchpaths):
    if isinstance(searchpaths, string_types):
        searchpaths = searchpaths.split(os.pathsep)
    for filename in filenames:
        for searchpath in searchpaths:
            fpath = path.join(searchpath, filename)
            if path.exists(fpath):
                return fpath


SDKVersion = namedtuple('SDKVersion', ['MajorVersion', 'MinorVersion',
                                       'MajorRevision', 'MinorRevision'])


class _TecInterprocess(object):

    Message = namedtuple('Message', ['level', 'message'])

    def __init__(self):
        self.handle = None
        self.tecinterprocess_path = None
        self.started = None
        self.stopped = None
        self._last_message = None

        if ctypes.sizeof(c_void_p) != 8:
            msg = '64-bit Python is required to use PyTecplot'
            raise TecplotLibraryNotLoadedError(msg)

        setlocale(LC_NUMERIC, 'C')

        load = {'Darwin': self.load_darwin,
                'Linux': self.load_linux,
                'Windows': self.load_windows}

        log.debug('Attempting to load Tecplot interprocess library')
        load[platform.system()]()
        log.debug('Successfully loaded Tecplot interprocess library')
        log.info('Interproces Library: {}'.format(self.tecinterprocess_path))

    @property
    def tecsdkhome(self):
        if not hasattr(self, '_tecsdkhome'):
            try:
                self.tecsdkhome = os.environ['TECSDKHOME']
                if not path.isdir(self._tecsdkhome):
                    raise OSError
            except (KeyError, OSError):
                if self.tecinterprocess_path is not None:
                    log.debug('reading tecinterprocess path to get SDK home')
                    tecinterproc_dir = path.dirname(self.tecinterprocess_path)
                    self.tecsdkhome = path.dirname(tecinterproc_dir)
                else:
                    self.tecsdkhome = ''
        return self._tecsdkhome

    @tecsdkhome.setter
    def tecsdkhome(self, tecsdkhome):
        self._tecsdkhome = tecsdkhome

    def load_linux(self):

        def _syslibpath():
            ret = []
            try:
                log.debug('acquiring system library search path using ldconfig')
                cmd = 'ldconfig -v -N'
                proc = Popen(cmd, shell=True,
                             executable=os.environ.get('SHELL', '/bin/bash'),
                             env=os.environ, stdout=PIPE, stderr=PIPE)
                ptrn = re.compile(r'^\t')
                for line in proc.communicate()[0][:-1].decode().split('\n'):
                    if not ptrn.match(line):
                        d = line.split(':')[0]
                        if path.exists(d) and path.isdir(d):
                            ret.append(d)
            except:
                log.debug('diagnostic command failed: ' + cmd)
            return ret

        def _missinglibs(lib):
            ret = []
            try:
                log.debug('looking for missing libs using ldd')
                cmd = 'ldd ' + lib
                proc = Popen(cmd, shell=True,
                             executable=os.environ.get('SHELL', '/bin/bash'),
                             env=os.environ, stdout=PIPE, stderr=PIPE)
                out, err = proc.communicate()
                if 'command not found' not in err.decode():
                    if len(out.decode().split('\n')) < 3:
                        log.debug(out.decode())
                    for line in out.decode().split('\n'):
                        if line.endswith('not found'):
                            ret.append(line.split()[0])
            except:
                log.debug('diagnostic command failed: ' + cmd)
            return ret

        def _find_library(libnames):
            libpath = os.environ.get('LD_LIBRARY_PATH', None)
            for libname in libnames:
                ret = None
                if libpath is not None:
                    ret = find_file([libname], libpath)
                if ret is None:
                    ret = find_file([libname], _syslibpath())
                if ret is not None:
                    return ret

        def _dl_abspath(libname):
            """Returns the absolute path of the loaded dynamic library"""
            log.debug('using libc to get path to tecinterprocess library')

            class dl_phdr_info(ctypes.Structure):
                _fields_ = [
                    ('padding0', c_void_p),  # ignore it
                    ('dlpi_name', c_char_p)]
            callback_t = ctypes.CFUNCTYPE(c_int, POINTER(dl_phdr_info),
                                          POINTER(c_size_t), c_char_p)
            _dl_abspath.lib_abspath = None

            def callback(info, size, data):
                if data in info.contents.dlpi_name:
                    _dl_abspath.lib_abspath = \
                        info.contents.dlpi_name.decode()
                return 0

            libc = ctypes.CDLL(None)
            libc.dl_iterate_phdr.argtypes = [callback_t, c_char_p]
            libc.dl_iterate_phdr.restype = c_int
            libc.dl_iterate_phdr(callback_t(callback), libname.encode())
            return _dl_abspath.lib_abspath

        libname = 'tecinterprocess'
        fmts = ['lib{name}.so']
        libnames = [fmt.format(name=libname) for fmt in fmts]

        cdllexcept = {}
        for lib in libnames:
            try:
                self.handle = ctypes.cdll.LoadLibrary(lib)
                if self.handle is not None:
                    self.tecinterprocess_path = _dl_abspath(lib)
                    return
                else:
                    raise OSError
            except (OSError, TypeError) as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                info = [str(x) for x in [e, exc_type,
                        '{}:{}'.format(fname, exc_tb.tb_lineno)]]
                cdllexcept[lib] = '\n'.join(info)
                continue

        msg = dedent('''\
            The Tecplot interprocess library or one of its
            dependencies could not be found. This is usually the result of
            not setting the environment path LD_LIBRARY_PATH to the
            directory containing the tecplot executables.

            LD_LIBRARY_PATH={libpath}

            Interprocess library file name(s):
                {libnames}
        ''').format(libpath=os.environ.get('LD_LIBRARY_PATH', None),
                    libnames='\n    '.join(libnames))

        self.tecinterprocess_path = _find_library(libnames)
        if self.tecinterprocess_path is None:
            raise TecplotLibraryNotFoundError(msg)

        msg += dedent('''
        Found interprocess library file:
            {foundlib}

        Your Tecplot 360 EX may be out of date. Please install the latest
        version of 360 EX which can be obtained here:
            http://www.tecplot.com/downloads
        ''').format(foundlib=self.tecinterprocess_path)

        missinglibs = _missinglibs(self.tecinterprocess_path)
        if len(missinglibs):
            msg += dedent('''
                Missing libraries:
                    {missinglibs}
            ''').format(missinglibs='\n    '.join(missinglibs))

        lib = path.basename(self.tecinterprocess_path)
        msg += dedent('''
            Python ctypes exception caught while trying to load library:
                {cdllexcept}
        ''').format(cdllexcept='\n    '.join(cdllexcept[lib].split('\n')))

        if sys.version_info < (3,):  # pragma: no branch
            log.error(msg)
            sys.exit(1)

        raise TecplotLibraryNotLoadedError(msg)

    def load_darwin(self):

        def _missinglibs(lib):
            ret = []
            try:
                log.debug('looking for missing libs using otool')
                cmd = 'otool -L ' + lib
                proc = Popen(cmd, shell=True,
                             executable=os.environ.get('SHELL', '/bin/bash'),
                             env=os.environ, stdout=PIPE, stderr=PIPE)
                out, err = proc.communicate()
                if 'command not found' not in err.decode():
                    for line in out.decode().split('\n'):
                        if line.endswith('not found'):
                            ret.append(line.split()[0])
            except:
                log.debug('diagnostic command failed: ' + cmd)
            return ret

        def _find_library(libnames):
            for libname in libnames:
                ret = find_library(libname)
                if ret is not None:
                    return ret

        libname = 'tecinterprocess'
        fmts = ['lib{name}.so']
        libnames = [fmt.format(name=libname) for fmt in fmts]

        cdllexcept = {}
        self.tecinterprocess_path = _find_library(libnames)
        for lib in libnames:
            try:
                self.handle = ctypes.cdll.LoadLibrary(lib)
                if self.handle is not None:
                    return
                else:
                    raise OSError
            except (OSError, TypeError) as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                info = [str(x) for x in [e, exc_type, fname, exc_tb.tb_lineno]]
                cdllexcept[lib] = '\n'.join(info)
                continue

        msg = dedent('''\
            The Tecplot interprocess library or one of its
            dependencies could not be found. This is usually the result of
            not setting the environment path DYLD_LIBRARY_PATH to the
            directory containing the tecplot executables.

            DYLD_LIBRARY_PATH={libpath}

            Interprocess library file name(s):
                {libnames}
        ''').format(libpath=os.environ.get('DYLD_LIBRARY_PATH', None),
                    libnames='\n    '.join(libnames))

        if self.tecinterprocess_path is None:
            raise TecplotLibraryNotFoundError(msg)

        msg += dedent('''
        Found interprocess library file:
            {foundlib}

        Your Tecplot 360 EX may be out of date. Please install the latest
        version of 360 EX which can be obtained here:
            http://www.tecplot.com/downloads
        ''').format(foundlib=self.tecinterprocess_path)

        missinglibs = _missinglibs(self.tecinterprocess_path)
        if len(missinglibs):
            msg += dedent('''
                Missing libraries:
                    {missinglibs}
            ''').format(missinglibs='\n    '.join(missinglibs))

        lib = path.basename(self.tecinterprocess_path)
        msg += dedent('''
            Python ctypes exception caught while trying to load library:
                {cdllexcept}
        ''').format(cdllexcept='\n    '.join(cdllexcept[lib].split('\n')))

        raise TecplotLibraryNotLoadedError(msg)

    def load_windows(self):

        libname = 'tecinterprocess'
        # We need to search for (debug) tecinterprocessd.dll first,
        # otherwise we might find a (release) tecinterprocess.dll
        # before finding tecinterprocessd.dll
        fmts = ['{name}d.dll', '{name}.dll']
        libnames = [fmt.format(name=libname) for fmt in fmts]

        self.tecinterprocess_path = find_file(libnames, os.environ['PATH'])

        cdllexcept = {}
        if self.tecinterprocess_path is not None:
            try:
                self.handle = ctypes.cdll.LoadLibrary(self.tecinterprocess_path)
                if self.handle is not None:
                    return
                else:
                    raise OSError
            except OSError as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                info = [str(x) for x in [e, exc_type, fname, exc_tb.tb_lineno]]
                lib = path.basename(self.tecinterprocess_path)
                cdllexcept[lib] = '\n'.join(info)

        msg = dedent('''\
            The Tecplot interprocess library or one of its dependencies could
            not be found. This is usually the result of not setting the
            environment path PATH to the directory containing the tecplot
            executables. Alternatively, your Tecplot 360 EX may be out of date.
            Please install the latest version of 360 EX which can be obtained
            here:
                http://www.tecplot.com/downloads

            PATH={libpath}

            Interprocess library file names:
                {libnames}

            Found interprocess library file:
                {foundlib}
        ''').format(libpath=os.environ.get('PATH', None),
                    libnames='\n    '.join(libnames),
                    foundlib=self.tecinterprocess_path)

        if self.tecinterprocess_path is None:
            raise TecplotLibraryNotFoundError(msg)
        else:
            lib = path.basename(self.tecinterprocess_path)
            info = '\n    '.join(cdllexcept[lib].split('\n'))
            msg += dedent('''
                Python ctypes exception caught while trying to load library:
                    {cdllexcept}
            ''').format(cdllexcept=info)

        raise TecplotLibraryNotLoadedError(msg)

    def start(self):
        if self.stopped:
            msg = 'PyTecplot cannot be restarted after it has been stopped.'
            raise TecplotLibraryNotLoadedError(msg)

        if self.started:
            return

        log.debug('Attempting to start Tecplot engine')
        msg = 'tecinterprocess path: {0} [{1}]'
        log.debug(msg.format(self.tecinterprocess_path,
                  time.ctime(os.stat(self.tecinterprocess_path).st_mtime)))

        log.debug('SDK home: "{}"'.format(self.tecsdkhome))

        with captured_output(log.debug):
            result = ManagerStartReturnCode(
                self.handle.Start(self.tecsdkhome.encode()))

        errmsg = {
            ManagerStartReturnCode.HomeDirectoryNotSpecified:
                'Missing home directory',
            ManagerStartReturnCode.LicenseFileNotFound: 'Missing license',
            ManagerStartReturnCode.LicenseIsInvalid: 'Invalid license',
            ManagerStartReturnCode.LicenseExpired: 'Expired license',
            ManagerStartReturnCode.InternalInitializationError:
                'Internal initialization error',
            ManagerStartReturnCode.EngineUninitialized:
                'Engine initialization failed',
            ManagerStartReturnCode.LicenseFileContainsPermanent: dedent('''\
            A license file was found, but it is a permanent license. At this
            time only time limited licenses are supported.''')}

        if result != ManagerStartReturnCode.Ok:
            raise TecplotLicenseError(errmsg[result])

        log.info('Tecplot engine started - license acquired')
        info = self.handle.LicenseInfo().decode()
        log.info('License information:\n  ' + info.replace('\n', '\n  '))
        self.started = True

    def stop(self):
        if self.stopped:
            return
        with captured_output(log.debug):
            if self.started:
                self.handle.Stop()
        self.started = False
        self.stopped = True
        log.info('Tecplot engine stopped - license released')

    @property
    def license_is_valid(self):
        return self.started and self.handle.LicenseIsValid()

    def acquire_license(self):
        self.start()
        if not self.license_is_valid and not self.handle.AcquireLicense():
            raise TecplotLicenseError('Could not acquire a valid license.')

    def release_license(self):
        if self.license_is_valid:
            self.handle.ReleaseLicense()

    @property
    def last_message(self):
        return self._last_message

    def clear_last_message(self):
        self._last_message = None

    def log_last_message(self):
        if self.last_message:
            if self.last_message.message:
                log.log(self.last_message.level, self.last_message.message)

    def update_last_message(self):
        last_message = None
        msg = self.handle.GetTUAssertErrorMessage()
        if msg:
            last_message = _TecInterprocess.Message(
                level=logging.CRITICAL,
                message=msg.decode('utf-8'))
            self.handle.ClearErrorMessage()
        elif __debug__:
            log_level = {
                MessageBoxType.Error: logging.ERROR,
                MessageBoxType.Warning: logging.WARNING,
                MessageBoxType.Information: logging.INFO}
            msg_ptr = self.handle.tecUtilLastErrorMessage()
            msg = cast(msg_ptr, c_char_p).value
            self.handle.tecUtilStringDealloc(byref(msg_ptr))
            if msg:
                # get message type/level
                mbox_val = self.handle.tecUtilLastErrorMessageType()
                mbox_type = MessageBoxType(mbox_val)
                last_message = _TecInterprocess.Message(
                    level=log_level.get(mbox_type, logging.WARNING),
                    message=msg.decode('utf-8'))
                # clean up
                self.handle.tecUtilParentLockStart(False)
                try:
                    self.handle.tecUtilLastErrorMessageClear()
                finally:
                    self.handle.tecUtilParentLockFinish()
        if last_message:
            self._last_message = last_message
        return last_message

    @property
    def sdk_version_info(self):
        if not hasattr(self, '_sdk_version_info'):
            try:
                self._sdk_version_info = SDKVersion(
                    self.handle.tecUtilTecplotGetMajorVersion(),
                    self.handle.tecUtilTecplotGetMinorVersion(),
                    self.handle.tecUtilTecplotGetMajorRevision(),
                    self.handle.tecUtilTecplotGetMinorRevision())
            except AttributeError:
                self._sdk_version_info = SDKVersion(0, 0, 0, 0)
        return self._sdk_version_info

    @property
    def sdk_version(self):
        version_info = self.sdk_version_info
        if version_info == SDKVersion(0, 0, 0, 0):
            return 'unknown'
        else:
            return '{}.{}-{}-{}'.format(*version_info)

    def initialize_tecutil(self):
        try:
            self.handle.LicenseInfo.restype = c_char_p
            self.handle.Start.argtypes = (c_char_p,)
            self.handle.GetTUAssertErrorMessage.restype = c_char_p

            return _TecUtil(self)

        except AttributeError:
            msg = dedent('''
                Your Tecplot 360 EX Installation may be out-of-date.
                Please install the latest version of Tecplot 360 EX.''')
            if self.tecsdkhome:
                msg += '\nTecplot 360 EX installation found here:'
                msg += '\n  '+self.tecsdkhome
            msg += '\nversion: {}'.format(self.sdk_version)
            raise TecplotInitializationError(msg.replace('\n','\n  '))

_tecinterprocess = _TecInterprocess()
_tecutil = _tecinterprocess.initialize_tecutil()
