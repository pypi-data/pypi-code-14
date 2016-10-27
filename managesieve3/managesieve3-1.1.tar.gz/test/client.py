#######################################################################
# A quick and dirty script to log client-server traffic. Only for
#  hacking around and testing purposes.
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
#  This is not a unit test! It's just to log client-server traffic.
########################################################################

from __future__ import print_function, unicode_literals

import logging
import argparse

import managesieve3

# a sample script
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

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--hostname', default='localhost', help='hostname to connect to')
    parser.add_argument('--port', default=4190, type=int, help='port to connect to')
    parser.add_argument('username')
    parser.add_argument('authuser')
    parser.add_argument('password')

    args = parser.parse_args()

    return args.hostname, args.port, args.username, args.authuser, args.password


def main():
    hostname, port, username, authuser, password = get_args()

    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    c = managesieve3.Managesieve(hostname, port)

    print()
    c.cmd_starttls(cert_reqs=False)
    print()

    c.login_plain(username, authuser, password)
    print()

    print(c.cmd_listscripts())
    print()

    print(c.cmd_capability())
    print()

    c.cmd_putscript('some-script', script)
    print()

    c.cmd_setactive('some-script')
    print()

    c.cmd_setactive(None)
    print()

    #print(c.cmd_renamescript('foo', 'bar'))
    #print()

    print(c.cmd_listscripts())
    print()

    print(c.cmd_getscript('some-script'))
    print()

    #c.cmd_deletescript('some-script')
    #print()

    print('havespace', c.cmd_havespace('foo', 999999999))
    print()

    print('havespace', c.cmd_havespace('foo', 1))
    print()

    print('noop', c.cmd_noop())
    print()

    #print(c.cmd_checkscript(script))
    #print()

    #print(c.cmd_checkscript('x'))
    c.cmd_logout()


if __name__ == '__main__':
    main()
