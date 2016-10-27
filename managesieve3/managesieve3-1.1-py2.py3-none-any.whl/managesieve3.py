#######################################################################
# managesieve3 is a python2 and python3 implementation an RFC-5804
#  client to remotely manage sieve scripts.
#
# Copyright 2015 True Blade Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Notes:
#  See https://pypi.python.org/pypi/managesieve for a python2 only
# module that provides basically the same functionality.
########################################################################

from __future__ import unicode_literals

import re as _re
import ssl as _ssl
import socket as _socket
import base64 as _base64
import logging as _logging
import itertools as _itertools

__all__ = ['Managesieve', 'BaseException', 'ServerResponseNo', 'ServerResponseBye', 'ServerProtocolError']

# get the logger we're going to use
_logger = _logging.getLogger(__name__)

_RES_OK  = b'OK'
_RES_NO  = b'NO'
_RES_BYE = b'BYTE'

_CRLF = b'\r\n'

########################################################################
# exceptions

class BaseException(Exception):
    pass


class _ServerResponseBase(BaseException):
    def __init__(self, name, code, text, results):
        self.name = name.decode('ascii')
        self.code = None if code is None else code.decode('ascii').split('/')
        self.text = text
        self.results = results

    def __str__(self):
        return '{}(name={!r}, code={!r}, text={!r}, results={!r})'.format(self.__class__.__name__, self.name, self.code, self.text, self.results)


# the server returned a 'NO' response
class ServerResponseNo(_ServerResponseBase):
    pass


# the server returned a 'BYE' response
class ServerResponseBye(_ServerResponseBase):
    pass


# a protocol error: unexpected result from server server returned a 'BYE' response
class ServerProtocolError(BaseException):
    pass

#
########################################################################

########################################################################
# helper routines

# turns into an RFC-5840 "string", which is still bytes
def _stringify(bytes):
    return b''.join([b'"', bytes, b'"'])


def _literal(bytes):
    # an RFC-5840 literal. can contain arbitrary bytes, since it's prefixed with the length
    return b''.join([b'{', str(len(bytes)).encode('ascii'), b'+}', _CRLF, bytes, _CRLF])


#
########################################################################

# various regexes
_re_oknobye = _re.compile(br'(?P<type>' + _RES_OK + b'|' + _RES_NO + b'|' + _RES_BYE + br')( \((?P<code>.*)\))?( (?P<rest>.*))?$')
_re_quote = _re.compile(br'"(?P<string>[^"]*)"( (?P<rest>.*))?$')
_re_atom  = _re.compile(br'(?P<atom>[^ ]+)( (?P<rest>.*))?$')
_re_literal = _re.compile(br'{(?P<length>\d+)}$')
_re_capability = _re.compile(br'"(?P<name>[^"]*)"( "(?P<value>[^"]*)")?$')

########################################################################
# routines to parse the responses

def _parse_simple(type, code, text, results):
    # we don't care about anything that's returned. we know it's OK
    return None


def _parse_capability(type, code, text, results):
    caps = {}
    for name_value in results:
        # name_value must be length 1 or 2
        if len(name_value) == 1:
            name, value = name_value[0], None
        else:
            name, value = name_value

        caps[name.upper()] = value

    return caps


def _parse_listscripts(type, code, text, results):
    result = set()
    default = None
    for r in results:
        # must be length 1 or 2
        if len(r) == 1:
            name, flag = r[0], None
        else:
            name, flag = r
        name = name.decode('utf-8')
        if flag is not None:
            if flag != b'ACTIVE':
                raise ServerProtocolError('unknown script flag %s' % flag)
            if default:
                raise ServerProtocolError('ACTIVE specified multiple times')
            default = name
        result.add(name)
    return result, default


def _parse_getscript(type, code, text, results):
    if len(results) == 1:
        return results[0].decode('utf-8')
    if len(results) == 0:
        return ''
    raise ServerProtocolError('unexpected results {!r}'.format(results))

#
########################################################################

########################################################################
# our abstract reader/writer objects. they exist mainly to make testing
#  easier

class _Reader(object):
    def __init__(self, read, readline):
        self.read = read
        self.readline = readline


class _Writer(object):
    def __init__(self, send):
        self.send = send

#
########################################################################

########################################################################
# routines for interacting with the server. these take _Reader and
#  _Writer objects

def _command(name, parser, reader, writer, args=None, options=None):
    _logger.info('executing command %r', name)
    cmd = b' '.join(_itertools.chain([name], [] if args is None else args)) + _CRLF
    _logger.debug('C: %r', cmd)
    writer.send(cmd)
    if options:
        for o in options:
            cmd = _literal(o)
            _logger.debug('C: %r', cmd)
            writer.send(cmd)

    # get the response
    return _read_response(name, parser, reader)


def _read_response(name, parser, reader):
    # read lines until we have a OK/NO/BYE
    results = []
    while True:
        line = _readline(reader)

        # check for ok/no/bye
        m = _re_oknobye.match(line)
        if m:
            # an ok/no/bye, parse and return
            type, code, text = m.group('type', 'code', 'rest')
            type = type.upper()
            if text is not None:
                text = _string_or_literal(text, reader).decode('utf-8')

            _logger.info('response %s: %r %r %r %r', name, type, code, text, results)

            result = parser(type, code, text, results)
            _logger.debug('parsed response %s: %r', name, result)

            if type != _RES_OK:
                if type == _RES_NO:
                    raise ServerResponseNo(name, code, text, results)
                if type == _RES_BYE:
                    raise ServerResponseBye(name, code, text, results)
                raise ServerProtocolError()

            return result

        # check for a literal
        m = _re_literal.match(line)
        if m:
            length = int(m.group('length'))

            # read 'length' bytes, then expect a cr/lf
            data = reader.read(length+2)
            _logger.debug('S: %s', repr(data))
            results.append(_strip_crlf(data))
            continue

        # check for a list of quoted strings or atoms
        l = []
        while True:
            # the order is important here: check from quoted strings, them atoms
            m = _re_quote.match(line)
            if m:
                l.append(m.group('string'))
            else:
                m = _re_atom.match(line)
                if m:
                    l.append(m.group('atom'))
                else:
                    raise ServerProtocolError('invalid server response')
            line = m.group('rest')
            if line is None:
                break
        results.append(l)


def _readline(reader):
    # read a line, but strip off the cr/lf
    # also, check for EOF
    line = reader.readline()
    _logger.debug('S: %s', repr(line))
    if not line:
        raise IOError('readline: EOF')
    return _strip_crlf(line)


def _strip_crlf(line):
    if line[-2:] != _CRLF:
        raise ServerProtocolError('line expected to end with CR/LF {!r}'.format(line))
    return line[:-2]


def _string_or_literal(line, reader):
    # check for a literal. if so, read more
    # line is a bytes object
    m = _re_literal.match(line)
    if m:
        length = int(m.group('length'))

        # read 'length' bytes, then expect a cr/lf
        data = reader.read(length+2)
        _logger.debug('S: %s', repr(data))

        return _strip_crlf(data)
    else:
        # not a literal, just return the line without quotes
        # this odd construct is needed to get the first and list chars of the bytes object
        #  in both python2 and python3
        if not (line[0:1] == b'"' and line[len(line)-1:len(line)] == b'"'):
            raise ServerProtocolError('expecting string to have quotes, not {!r}'.format(line))
        return line[1:-1]

#
########################################################################

########################################################################
# the manage sieve commands, which take reader/writer objects

def _cmd_authenticate(reader, writer, auth_type, options):
    return _command(b'AUTHENTICATE',
                    _parse_simple,
                    reader,
                    writer,
                    args=[_stringify(auth_type)],
                    options=options)


def _cmd_starttls(reader, writer):
    return _command(b'STARTTLS',
                    _parse_simple,
                    reader,
                    writer)


def _cmd_logout(reader, writer):
    return _command(b'LOGOUT',
                    _parse_simple,
                    reader,
                    writer)


def _cmd_capability(reader, writer):
    return _command(b'CAPABILITY',
                    _parse_capability,
                    reader,
                    writer)


def _cmd_havespace(reader, writer, name, size):
    try:
        _command(b'HAVESPACE',
                 _parse_simple,
                 reader,
                 writer,
                 args=[_stringify(name.encode('utf-8')),
                       str(size).encode('ascii')])
        return True, None, None
    except ServerResponseNo as ex:
        return False, ex.code, ex.text


def _cmd_putscript(reader, writer, name, contents):
    return _command(b'PUTSCRIPT',
                    _parse_simple,
                    reader,
                    writer,
                    args=[_stringify(name.encode('utf-8')),
                          _literal(contents.encode('utf-8'))])


def _cmd_listscripts(reader, writer):
    # returns a tuple: (scripts, active)
    # scripts is a set of script names that exist
    # active is either the name of the active script, or None if no active script exists
    return _command(b'LISTSCRIPTS',
                    _parse_listscripts,
                    reader,
                    writer)


def _cmd_setactive(reader, writer, name):
    if name is None:
        name = ''
    return _command(b'SETACTIVE',
                    _parse_simple,
                    reader,
                    writer,
                    args=[_stringify(name.encode('utf-8'))])


def _cmd_getscript(reader, writer, name):
    return _command(b'GETSCRIPT',
                    _parse_getscript,
                    reader,
                    writer,
                    args=[_stringify(name.encode('utf-8'))])


def _cmd_deletescript(reader, writer, name):
    return _command(b'DELETESCRIPT',
                    _parse_simple,
                    reader,
                    writer,
                    args=[_stringify(name.encode('utf-8'))])


def _cmd_renamescript(reader, writer, oldname, newname):
    return _command(b'RENAMESCRIPT',
                    _parse_simple,
                    reader,
                    writer,
                    args=[_stringify(oldname.encode('utf-8')),
                          _stringify(newname.encode('utf-8'))])


def _cmd_checkscript(reader, writer, contents):
    try:
        _command(b'CHECKSCRIPT',
                 _parse_simple,
                 reader,
                 writer,
                 args=[_literal(contents.encode('utf-8'))])
        return True, None, None
    except ServerResponseNo as ex:
        return False, ex.code, ex.text


def _cmd_noop(reader, writer):
    return _command(b'NOOP',
                    _parse_simple,
                    reader,
                    writer)
#
########################################################################


class Managesieve(object):
    # note we're not using 'brw': we read via the file, but write directly to the socket
    #  this is to prevent buffering the writes, which has an issue once TLS is running
    _filemode = 'br'

    def __init__(self, host=None, port=None):
        if host is None:
            host = 'localhost'
        if port is None:
            port = 4190

        _logger.info('connecting to %s:%s', host, port)
        self._sock = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
        self._sock.connect((host, port))
        self._file = self._sock.makefile(self._filemode)

        # read the initial greeting, as if CAPABILITY had been executed
        self._capabilities = self._read_response_capability()


    def _reader(self):
        return _Reader(self._file.read, self._file.readline)


    def _writer(self):
        return _Writer(self._sock.send)


    # the supported commands, in RFC-5804 order

    def cmd_authenticate(self, auth_type, options=None):
        return _cmd_authenticate(self._reader(), self._writer(), auth_type, options)



    def cmd_starttls(self, keyfile=None, certfile=None, cert_reqs=_ssl.CERT_NONE,
                     ssl_version=_ssl.PROTOCOL_SSLv23, ca_certs=None, ciphers=None):
        _cmd_starttls(self._reader(), self._writer())
        self._sock = _ssl.wrap_socket(self._sock, keyfile=keyfile, certfile=certfile,
                                      cert_reqs=cert_reqs, ssl_version=ssl_version,
                                      ca_certs=ca_certs, ciphers=ciphers)
        self._file = self._sock.makefile(self._filemode)

        # now under TLS, read the capability result
        self._capabilities = self._read_response_capability()
        return self._capabilities


    def cmd_logout(self):
        # forget our capabilities
        self._capabilities = None
        return _cmd_logout(self._reader(), self._writer())


    def cmd_capability(self):
        return _cmd_capability(self._reader(), self._writer())


    def cmd_havespace(self, name, size):
        return _cmd_havespace(self._reader(), self._writer(), name, size)


    def cmd_putscript(self, name, contents):
        return _cmd_putscript(self._reader(), self._writer(), name, contents)


    def cmd_listscripts(self):
        return _cmd_listscripts(self._reader(), self._writer())


    def cmd_setactive(self, name):
        return _cmd_setactive(self._reader(), self._writer(), name)


    def cmd_getscript(self, name):
        return _cmd_getscript(self._reader(), self._writer(), name)


    def cmd_deletescript(self, name):
        return _cmd_deletescript(self._reader(), self._writer(), name)


    def cmd_renamescript(self, oldname, newname):
        return _cmd_renamescript(self._reader(), self._writer(), oldname, newname)


    def cmd_checkscript(self, contents):
        return _cmd_checkscript(self._reader(), self._writer(), contents)


    def cmd_noop(self):
        return _cmd_noop(self._reader(), self._writer())


    def login_plain(self, username, authuser, password):
        # encode as UTF-8, then join with \0, then base64
        data = _base64.b64encode(b'\0'.join(s.encode('utf-8') for s in [username, authuser, password]))
        return self.cmd_authenticate(b'PLAIN', [data])


    def _read_response_capability(self):
        return _read_response(b'capability', _parse_capability, self._reader())
