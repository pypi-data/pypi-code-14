#######################################################################
# Tests for managesieve3 module.
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
#  I really need to create a dummy server so I can test the socket
#   connection parts.
# starttls doesn't have a test yet.
########################################################################

from __future__ import unicode_literals

#import logging
#logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

from managesieve3 import (Managesieve,
                          BaseException,
                          _ServerResponseBase,
                          ServerResponseNo,
                          ServerResponseBye,
                          ServerProtocolError,
                          _Reader,
                          _Writer,
                          _cmd_authenticate,
                          _cmd_starttls,
                          _cmd_logout,
                          _cmd_capability,
                          _cmd_havespace,
                          _cmd_putscript,
                          _cmd_listscripts,
                          _cmd_setactive,
                          _cmd_getscript,
                          _cmd_deletescript,
                          _cmd_renamescript,
                          _cmd_checkscript,
                          _cmd_noop,
                          )

import io
import sys
import base64
import unittest

_PY2 = sys.version_info[0] == 2
_PY3 = sys.version_info[0] == 3

# a test vacation script
script = '''
# vacation expires:
require "vacation";
vacation
:days 7
:subject "Out of office reply"
:addresses [ "someone@example.org" ]
text:

I will be until August 18th and will have limited access to email.

.
;
keep;
'''

class TestCommands(unittest.TestCase):
    def _test_command(self, cmd, args, expected_from_client, from_server, expected_result, expectedException=None):

        # collect what the client sends
        from_client = io.BytesIO()

        # what the server will return
        from_server = io.BytesIO(from_server)

        try:
            result = cmd(_Reader(from_server.read, from_server.readline),
                         _Writer(from_client.write),
                         *args)
        except BaseException as ex:
            # equality test doesn't seem to work, so just compare their types and values
            self.assertEqual(type(ex), type(expectedException))
            if isinstance(ex, _ServerResponseBase):
                self.assertEqual(ex.name, expectedException.name)
                self.assertEqual(ex.code, expectedException.code)
                self.assertEqual(ex.text, expectedException.text)
                self.assertEqual(ex.results, expectedException.results)
            elif isinstance(ex, ServerProtocolError):
                self.assertEqual(str(ex), str(expectedException))
            else:
                self.assertFalse('unexpected exception type {}'.format(type(ex)))
        else:
            if expectedException is not None:
                self.assertFalse('expected to raise an exception {}, but did not'.format(expectedException))
            # check the result
            self.assertEqual(result, expected_result)

        # and check what the client actually sent to the server, to see that it matches what we expected
        self.assertEqual(expected_from_client, from_client.getvalue())


    def test_authenticate(self):
        # failure
        data = base64.b64encode(b'\0'.join(s.encode('utf-8') for s in ['eric', 'cyrus', 'invalid password'])),
        self._test_command(_cmd_authenticate,
                           [b'PLAIN', data],
                           (b'AUTHENTICATE "PLAIN"\r\n'
                            b'{36+}\r\nZXJpYwBjeXJ1cwBpbnZhbGlkIHBhc3N3b3Jk\r\n'
                            ),
                           (b'{0}\r\n'
                            b'\r\n'
                            b'NO "Authentication Error"\r\n'),
                           None,
                           ServerResponseNo(b'AUTHENTICATE', None, 'Authentication Error', [b'']))

        # success
        data = base64.b64encode(b'\0'.join(s.encode('utf-8') for s in ['eric', 'cyrus', 'valid password'])),
        self._test_command(_cmd_authenticate,
                           [b'PLAIN', data],
                           (b'AUTHENTICATE "PLAIN"\r\n'
                            b'{36+}\r\nZXJpYwBjeXJ1cwB2YWxpZCBwYXNzd29yZA==\r\n'
                            ),
                           (b'{0}\r\n'
                            b'\r\n'
                            b'OK\r\n'),
                           None)


    def test_starttls(self):
        # this only tests the cleartext part of the transaction
        # I'll need to mock a server, or set up an actual sieve server to test the rest
        self._test_command(_cmd_starttls,
                           [],
                           b'STARTTLS\r\n',
                           b'OK "Begin TLS negotiation now"\r\n',
                           None)


    def test_logout(self):
        self._test_command(_cmd_logout,
                           [],
                           b'LOGOUT\r\n',
                           b'OK "Logout Complete"\r\n',
                           None)

    def test_capability(self):
        self._test_command(_cmd_capability,
                           [],
                           b'CAPABILITY\r\n',
                           (b'"IMPLEMENTATION" "Cyrus timsieved v2.4.17-Fedora-RPM-2.4.17-6.fc20"\r\n'
                            b'"SIEVE" "comparator-i;ascii-numeric fileinto reject vacation imapflags notify envelope relational regex subaddress copy"\r\n'
                            b'"UNAUTHENTICATE"\r\n'
                            b'OK\r\n'),
                           {b'IMPLEMENTATION': b'Cyrus timsieved v2.4.17-Fedora-RPM-2.4.17-6.fc20', b'UNAUTHENTICATE': None, b'SIEVE': b'comparator-i;ascii-numeric fileinto reject vacation imapflags notify envelope relational regex subaddress copy'})


    def test_havespace(self):
        self._test_command(_cmd_havespace,
                           ['foo', 999999999],
                           b'HAVESPACE "foo" 999999999\r\n',
                           b'NO (QUOTA/MAXSIZE) "Script size is too large. Max script size is 32768 bytes"\r\n',
                           (False, ['QUOTA', 'MAXSIZE'], 'Script size is too large. Max script size is 32768 bytes'))

        self._test_command(_cmd_havespace,
                           ['foo', 1],
                           b'HAVESPACE "foo" 1\r\n',
                           b'OK\r\n',
                           (True, None, None))

    def test_putscript(self):
        self._test_command(_cmd_putscript,
                           ['some-script', script],
                           b'PUTSCRIPT "some-script" {211+}\r\n\n# vacation expires:\nrequire "vacation";\nvacation\n:days 7\n:subject "Out of office reply"\n:addresses [ "someone@example.org" ]\ntext:\n\nI will be until August 18th and will have limited access to email.\n\n.\n;\nkeep;\n\r\n\r\n',
                           b'OK\r\n',
                           None)


    def test_listscripts(self):
        # with an active script
        self._test_command(_cmd_listscripts,
                           [],
                           b'LISTSCRIPTS\r\n',
                           (b'"foo"\r\n'
                            b'"some-script" ACTIVE\r\n'
                            b'"vacation"\r\n'
                            b'OK\r\n'),
                           ({'foo', 'some-script', 'vacation'}, 'some-script'))

        # with no active script
        self._test_command(_cmd_listscripts,
                           [],
                           b'LISTSCRIPTS\r\n',
                           (b'"foo"\r\n'
                            b'"some-script"\r\n'
                            b'"vacation"\r\n'
                            b'OK\r\n'),
                           ({'foo', 'some-script', 'vacation'}, None))

        # protocol violation: multiple active scripts
        self._test_command(_cmd_listscripts,
                           [],
                           b'LISTSCRIPTS\r\n',
                           (b'"foo" ACTIVE\r\n'
                            b'"some-script"\r\n'
                            b'"vacation" ACTIVE\r\n'
                            b'OK\r\n'),
                           None,
                           ServerProtocolError('ACTIVE specified multiple times'))


    def test_setactive(self):
        self._test_command(_cmd_setactive,
                           ['some-script'],
                           b'SETACTIVE "some-script"\r\n',
                           b'OK\r\n',
                           None)

        self._test_command(_cmd_setactive,
                           [None],
                           b'SETACTIVE ""\r\n',
                           b'OK\r\n',
                           None)


    def test_getscript(self):
        # a non-existent script
        self._test_command(_cmd_getscript,
                           ['unknown'],
                           b'GETSCRIPT "unknown"\r\n',
                           b'NO (NONEXISTENT) "Script doesn\'t exist"\r\n',
                           None,
                           ServerResponseNo(b'GETSCRIPT', b'NONEXISTENT', "Script doesn't exist", []))

        # a valid script
        self._test_command(_cmd_getscript,
                           ['some-script'],
                           b'GETSCRIPT "some-script"\r\n',
                           (b'{225}\r\n'
                            b'\r\n# vacation expires:\r\nrequire "vacation";\r\nvacation\r\n:days 7\r\n:subject "Out of office reply"\r\n:addresses [ "someone@example.org" ]\r\ntext:\r\n\r\nI will be until August 18th and will have limited access to email.\r\n\r\n.\r\n;\r\nkeep;\r\n\r\n'
                            b'OK\r\n'),
                           script.replace('\n', '\r\n'))  # the script comes back with \n mapped to \r\n


    def test_deletescript(self):
        # a script that does exist
        self._test_command(_cmd_deletescript,
                           ['some-script'],
                           b'DELETESCRIPT "some-script"\r\n',
                           b'OK\r\n',
                           None)

        # a script that does not exist
        self._test_command(_cmd_deletescript,
                           ['bad-script'],
                           b'DELETESCRIPT "bad-script"\r\n',
                           b'NO "Error deleting script"\r\n',
                           None,
                           ServerResponseNo(b'DELETESCRIPT', None, "Error deleting script", []))

        # try to delete the active script
        self._test_command(_cmd_deletescript,
                           ['some-script'],
                           b'DELETESCRIPT "some-script"\r\n',
                           b'NO (ACTIVE) "Active script cannot be deleted"\r\n',
                           None,
                           ServerResponseNo(b'DELETESCRIPT', b'ACTIVE', "Active script cannot be deleted", []))


    def cmd_renamescript(self):
        # timsieved doesn't support this, so I'm guessing on the return string being ok
        self._test_command(_cmd_renamescript,
                           ['old-name', 'new-name'],
                           b'RENAMESCRIPT "old-name" "new-name"\r\n',
                           b'OK\r\n',
                           None)


    def test_checkscript(self):
        # timsieved doesn't support this, so I'm guessing on the return string being ok
        self._test_command(_cmd_checkscript,
                           [script],
                           b'CHECKSCRIPT {211+}\r\n\n# vacation expires:\nrequire "vacation";\nvacation\n:days 7\n:subject "Out of office reply"\n:addresses [ "someone@example.org" ]\ntext:\n\nI will be until August 18th and will have limited access to email.\n\n.\n;\nkeep;\n\r\n\r\n',
                           b'OK\r\n',
                           (True, None, None))


    def test_noop(self):
        # with an active script
        self._test_command(_cmd_noop,
                           [],
                           b'NOOP\r\n',
                           b'OK "Done"\r\n',
                           None)


class TestAll(unittest.TestCase):
    def test_all(self):
        import managesieve3
        import __future__

        # check that __all__ in the module contains everything that should be
        #  public, and only those symbols
        all = set(managesieve3.__all__)

        # check that things in __all__ only appear once
        self.assertEqual(len(all), len(managesieve3.__all__),
                         'some symbols appear more than once in __all__')

        # get the list of public symbols, but exclude future features
        # using __future__._Feature is a hack, but I can't see how else to do this
        found = set(name for name in dir(managesieve3) if not (name.startswith('_') or isinstance(getattr(managesieve3, name), __future__._Feature)))

        # make sure it matches __all__
        self.assertEqual(all, found)



unittest.main()
