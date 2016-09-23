#!/usr/bin/env python2.7

from optparse import OptionParser
import sys

class BaseCheckCommand(object):
    OK_EXIT=0
    WARNING_EXIT=1
    CRITICAL_EXIT=2
    UNKNOWN_EXIT=3

    def __init__(self, **kwargs):
        self.params = kwargs

        # Set or initialize an OptionParser instance, raise if set is not OptionParser
        self.parser = self.params.get('parser') or OptionParser()
        assert isinstance(self.parser, OptionParser),\
                "Passed parser is not an instance of OptionParser"

        # Add default options for threshold values
        self.parser.add_option('-w', '--warning',
                                dest='warning',
                                action='store',
                                help='Sets the value for the warning threshold.',
                                metavar='WARNING_THERSHOLD')

        self.parser.add_option('-c', '--critical',
                                dest='critical',
                                action='store',
                                help='Sets the value for the critical threshold.',
                                metavar='CRITICAL_THRESHOLD')

        self.status    = None
        self.perf_data = None

    def usage(self, exit_code=0, msg=''):
        self.parser.print_help()
        if msg:
            print >> sys.stderr, msg
        sys.exit(exit_code)

    def parse_args(self):
        opts, args = self.parser.parse_args()
        if opts.warning == None or opts.critical == None:
            self.usage(exit_code=127, msg='Warning or Critical threshold not set.')
        if len(args) == 0 or len(args) >= 2:
            self.usage(exit_code=127, msg='Invalid number of collectors passed as arguments.')
        return [opts, args]

    def exit(self, err=None, exit_code=OK_EXIT):
        if err:
            print >> sys.stderr, err.message
            sys.exit(self.UNKNOWN_EXIT)
        else:
            if not self.perf_data == None:
                print("%s | %s") % (self.status, self.perf_data)
            else:
                print(self.status)
            sys.exit(exit_code)
