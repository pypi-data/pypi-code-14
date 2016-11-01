# ----------------------------------------------------------------------------
# Copyright 2015-2016 Nervana Systems Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------------
"""
Command line interface for Nervana's deep learning cloud.
"""
from builtins import object

import inspect
import logging
from collections import namedtuple

from ncloud.vendor.python.argparse import ArgumentTypeError
from ncloud.formatting.output import print_table


logger = logging.getLogger()


# command constants
Cmd = namedtuple('Cmd', ['name', 'aliases'])
LS = Cmd('ls', ('list', 'l'))
SHOW = Cmd('show', ('s',))
UL = Cmd('ul', ('upload', 'u'))
LN = Cmd('ln', ('link', 'k'))
RM = Cmd('rm', ('remove',))
ADD = Cmd('add', ('a',))
MODIFY = Cmd('modify', ('m',))
TRAIN = Cmd('train', ('t',))
START = Cmd('start', ())
STOP = Cmd('stop', ())
RESULTS = Cmd('results', ('res', 'r'))
IMPORT = Cmd('import', ('i',))
DEPLOY = Cmd('deploy', ('d',))
PREDICT = Cmd('predict', ('p',))
UNDEPLOY = Cmd('undeploy', ('ud', 'u'))
ADDGRP = Cmd('addgrp', ('addgroup', 'ag'))
RMGRP = Cmd('rmgrp', ('removegroup', 'rmg', 'rg'))
PWRST = Cmd('pwrst', ('pwreset', 'pr'))


def string_argument(string):
    if len(string) > 255:
        raise ArgumentTypeError('"%s" must be less than 255 characters.' %
                                string)
    return string


class Command(object):
    @classmethod
    def parser(cls, subparser):
        raise NotImplementedError("provide a subparser for your command")

    @classmethod
    def arg_names(cls, startidx=1):
        return inspect.getargspec(cls.call).args[startidx:]

    @staticmethod
    def call():
        raise NotImplementedError("provide an implementation for your command")

    @staticmethod
    def display_before(config, args):
        pass

    @staticmethod
    def display_after(config, args, res):
        if res is not None:
            print_table(res)

    @classmethod
    def arg_call(cls, config, args):
        arg_vals = [vars(args)[name] for name in cls.arg_names()]
        cls.display_before(config, args)
        res = cls.call(config, *arg_vals)

        cls.display_after(config, args, res)


class NoRespCommand(Command):
    @staticmethod
    def display_after(config, args, res):
        if not res:
            print_table({"error": "Error: no response from Helium"})
        else:
            print_table(res)


def build_subparser(name, aliases, hlp, classes, subparser):
    parser = subparser.add_parser(name, aliases=aliases, help=hlp,
                                  description=hlp)
    subsubparser = parser.add_subparsers(title=name + ' operations')
    for cls in classes:
        cls.parser(subsubparser)
