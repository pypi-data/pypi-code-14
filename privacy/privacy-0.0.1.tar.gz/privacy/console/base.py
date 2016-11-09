#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
import json
import logging
import argparse

from privacy import conf
from privacy.version import version

logger = logging.getLogger('privacy')


def get_sub_parser_argv():
    argv = sys.argv[2:]
    return argv


def get_main_parser_argv():
    argv = sys.argv[1:2]
    return argv


def execute_command_version():
    parser = argparse.ArgumentParser(
        prog='privacy version --json',
        description='prints the software version')

    parser.add_argument('--json', action='store_true', default=False, help='shows the version as a json')

    args = parser.parse_args(get_sub_parser_argv())

    if args.json:
        print json.dumps({'version': version, 'config': conf.path, 'name': 'privacy'}, indent=2)
    else:
        print "\033[1;33mprivacy\033[0m", '\033[1;34mv{0}\033[0m'.format(version), '\033[1;30m[{0}]\033[0m'.format(conf.path)
