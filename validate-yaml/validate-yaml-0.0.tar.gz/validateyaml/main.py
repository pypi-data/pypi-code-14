#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
validate yaml
"""

# imports
import argparse
import sys
import yaml

class ValidateYAMLParser(argparse.ArgumentParser):
    """CLI option parser"""
    def __init__(self, **kwargs):
        kwargs.setdefault('formatter_class', argparse.RawTextHelpFormatter)
        kwargs.setdefault('description', __doc__)
        argparse.ArgumentParser.__init__(self, **kwargs)
        self.add_argument('yaml_file', type=argparse.FileType('r'))
        self.options = None

    def parse_args(self, *args, **kw):
        options = argparse.ArgumentParser.parse_args(self, *args, **kw)
        self.validate(options)
        self.options = options
        return options

    def validate(self, options):
        """validate options"""

def main(args=sys.argv[1:]):
    """CLI"""

    # parse command line options
    parser = ValidateYAMLParser()
    options = parser.parse_args(args)

    yaml.load(options.yaml_file)

if __name__ == '__main__':
    main()


