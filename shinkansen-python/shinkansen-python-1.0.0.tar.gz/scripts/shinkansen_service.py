#!/usr/bin/env python
"""Run the shinkansen service.

Usage:
    shinkansen-service.py [--daemonize [--pidfile=<pidfile>]] [--config=<config_file>]

Options:
    -h --help                              Show this help text
    -d --daemonize                         Daemonize
    -p <pidfile> --pidfile=<pidfile>       The path to the pidfile to be used [Default: /var/run/shinkansen.pid]
    -c <configfile> --config=<configfile>  The path tot he config file to use, see config_local.py. If not given will
                                           attempt to load config_local from the PYTHONPATH.
"""
from docopt import docopt

from shinkansen.service import main


if __name__ == '__main__':
    main(docopt(__doc__))
