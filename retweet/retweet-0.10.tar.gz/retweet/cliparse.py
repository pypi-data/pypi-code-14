# -*- coding: utf-8 -*-
# Copyright © 2015-2016 Carl Chenet <carl.chenet@ohmytux.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

# CLI parsing
'''CLI parsing'''

# standard library imports
from argparse import ArgumentParser
import os.path
import sys

class CliParse(object):
    '''CliParse class'''
    def __init__(self):
        '''Constructor for the CliParse class'''
        self.main()

    def main(self):
        '''main of CliParse class'''
        retweetepilog = 'For more information: https://retweet.readthedocs.org'
        retweetdescription = 'Retweet retweets all tweets from a Twitter account' 
        parser = ArgumentParser(prog='retweet',
                                description=retweetdescription,
                                epilog=retweetepilog)
        parser.add_argument('pathtoconf', metavar='FILE', type=str,
                            help='the path to the retweet configuration')
        parser.add_argument('-l', '--limit', dest='limit', type=int, action='store',
                            help='the number of status to get from Twitter')
        parser.add_argument('-n', '--dry-run', dest='dryrun',
                            action='store_true', default=False,
                            help='Do not actually feed database and do not send the tweets')
        parser.add_argument('-v', '--version',
                            action='version',
                            version='%(prog)s 0.10',
                            help='print the version of retweet and exit')
        args = parser.parse_args()
        if not os.path.exists(args.pathtoconf):
            print('the path you provided for the configuration file does not exists')
            sys.exit(1)
        if not os.path.isfile(args.pathtoconf):
            print('the path you provided for the configuration is not a file')
            sys.exit(1)
        if args.limit:
            if args.limit > 20:
                sys.exit('-l or --limit option integer should be equal or less than 20')
        self.args = args

    @property
    def arguments(self):
        '''return the path to the config file'''
        return self.args
