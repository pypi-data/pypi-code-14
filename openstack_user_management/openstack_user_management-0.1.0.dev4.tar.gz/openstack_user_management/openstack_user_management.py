#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os

from connectors.openstack_connector import OpenstackConnector

__copyright__ = 'Copyright (C) 2016 B3LAB'
__description__ = """OpenStack User Management"""
__version__ = '1.0.0'

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def parse_arguments(cmdline=""):
    """Parse the arguments"""

    parser = argparse.ArgumentParser(
        description=__description__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s {version}'.format(version=__version__)
    )

    a = parser.parse_args(cmdline)
    return a


def main():
    try:
        conn = OpenstackConnector()
        print conn

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()  # pragma: no cover
