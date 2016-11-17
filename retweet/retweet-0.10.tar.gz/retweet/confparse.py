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
# along with this program.  If not, see <http://www.gnu.org/licenses/

# Get values of the configuration file
'''Get values of the configuration file'''

# standard library imports
import configparser
import sys
import re

class ConfParse(object):
    '''ConfParse class'''
    def __init__(self, pathtoconf):
        '''Constructor of the ConfParse class'''
        self.user_to_retweet = 'journaldupirate'
        self.consumer_key = ''
        self.consumer_secret = ''
        self.access_token = ''
        self.access_token_secret = ''
        self.retweets = 0
        self.waitminsecs = 1
        self.waitmaxsecs = 1
        self.pathtoconf = pathtoconf
        self.dontretweethashes = []
        self.onlyiftags = []
        self.match_regex = ''
        self.olderthan = 0
        self.youngerthan = 0
        self.like = False
        self.main()

    def main(self):
        '''Main of the ConfParse class'''
        # read the configuration file
        config = configparser.ConfigParser()
        try:
            with open(self.pathtoconf) as conffile:
                config.read_file(conffile)
                ### twitter section
                section = 'twitter'
                if config.has_section(section):
                    self.user_to_retweet = config.get(section, 'screen_name_of_the_user_to_retweet')
                    self.consumer_key = config.get(section, 'consumer_key')
                    self.consumer_secret = config.get(section, 'consumer_secret')
                    self.access_token = config.get(section, 'access_token')
                    self.access_token_secret = config.get(section, 'access_token_secret')
                ### retweet section
                section = 'retweet'
                if config.has_section('retweet'):
                    self.retweets = config.get(section, 'retweets')
                    # waitminsec option
                    if config.has_option(section, 'waitminsecs'):
                        self.waitminsecs = config.get(section, 'waitminsecs')
                    # waitmaxsec option
                    if config.has_option(section, 'waitmaxsecs'):
                        self.waitmaxsecs = config.get(section, 'waitmaxsecs')
                    # do_not_retweet_hashtags option
                    if config.has_option(section, 'do_not_retweet_hashtags'):
                        dontretweethashes = config.get(section, 'do_not_retweet_hashtags')
                        if dontretweethashes:
                            hashes = [i for i in dontretweethashes.split(',') if i != '']
                            self.dontretweethashes = hashes
                    # only_if_hashtags option
                    if config.has_option(section, 'only_if_hashtags'):
                        onlyiftags = config.get(section, 'only_if_hashtags')
                        if onlyiftags:
                            hashtags = [i for i in onlyiftags.split(',') if i != '']
                            self.onlyiftags = hashtags
                    # match option
                    if config.has_option(section, 'match'):
                        regex = config.get(section, 'match')
                        if regex:
                            self.match_regex = regex
                            # throws exception if the regex is not valid
                            re.compile(regex)
                    # older_than option
                    if config.has_option(section, 'older_than'):
                        self.olderthan = config.get(section, 'older_than')
                    # younger_than option
                    if config.has_option(section, 'younger_than'):
                        self.youngerthan = config.get(section, 'younger_than')
                    # like option
                    if config.has_option(section, 'like'):
                        self.like = config.getboolean(section, 'like')
                ### sqlite section
                section = 'sqlite'
                if config.has_section(section):
                    # sqlitepath option
                    if config.has_option(section, 'sqlitepath'):
                        self.sqlitepath = config.get(section, 'sqlitepath')

        except (configparser.Error, IOError, OSError) as err:
            print(err)
            sys.exit(1)
        try:
            self.retweets = int(self.retweets)
        except ValueError as err:
            print(err)
            self.retweets = 0
        try:
            self.waitminsecs = int(self.waitminsecs)
        except ValueError as err:
            print(err)
            self.waitminsecs = 10
        try:
            self.waitmaxsecs = int(self.waitmaxsecs)
        except ValueError as err:
            print(err)
            self.waitmaxsecs = 10
        try:
            self.olderthan = int(self.olderthan)
        except ValueError as err:
            print(err)
            self.olderthan = 0
        try:
            self.youngerthan = int(self.youngerthan)
        except ValueError as err:
            print(err)
            self.youngerthan = 0

    @property
    def confvalues(self):
        '''get the values of the configuration file'''
        return {'user_to_retweet':  self.user_to_retweet,
                'consumer_key': self.consumer_key,
                'consumer_secret': self.consumer_secret,
                'access_token': self.access_token,
                'access_token_secret': self.access_token_secret,
                'retweets': self.retweets,
                'waitminsecs': self.waitminsecs,
                'waitmaxsecs': self.waitmaxsecs,
                'sqlitepath': self.sqlitepath,
                'dontretweethashes': self.dontretweethashes,
                'onlyifhashtags': self.onlyiftags,
                'match_regex': self.match_regex,
                'olderthan': self.olderthan,
                'youngerthan': self.youngerthan,
                'like': self.like}
