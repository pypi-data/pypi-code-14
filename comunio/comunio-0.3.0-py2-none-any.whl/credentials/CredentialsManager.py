u"""
LICENSE:
Copyright 2016 Hermann Krumrey

This file is part of comunio-manager.

    comunio-manager is a program that allows a user to track his/her comunio.de
    profile

    comunio-manager is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    comunio-manager is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with comunio-manager.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

# imports
from __future__ import with_statement
from __future__ import absolute_import
import os
import ConfigParser
from typing import Tuple
from io import open


class CredentialsManager(object):
    u"""
    Class that manages a user's login credentials
    """

    def __init__(self, credentials=None):
        u"""
        Creates a new CredentialsManager object. It can be passed a username and a password, if they
        are not supplied, it will be attempted to access the local configuration file.

        :param credentials: Tuple consisting of username, password
        """
        self.config_file_location = os.path.join(os.path.expanduser(u"~"), u".comunio", u"config")

        if credentials is None:
            self.get_credentials_from_config()
        else:
            self.username, self.password = credentials

    def get_credentials_from_config(self):
        u"""
        Parses the local config file for a username and password

        :return: username, password
        """
        try:
            parser = ConfigParser.ConfigParser()
            parser.read(self.config_file_location)
            self.username = parser.get(u"credentials", u"username")
            self.password = parser.get(u"credentials", u"password")
        except (KeyError, ConfigParser.NoSectionError):
            with open(self.config_file_location, u'w') as config:
                config.write(u"[credentials]\nusername=\npassword=\n")
            self.username = u""
            self.password = u""

    def get_credentials(self):
        u"""
        :return: the credentials as a tuple of username, password
        """
        return self.username, self.password

    def get_config_file_location(self):
        u"""
        :return: the config file's location
        """
        return self.config_file_location

    def set_credentials(self, credentials):
        u"""
        Sets the credentials of the CredentialsManager

        :param credentials: the credentials to store as a tuple of username, password
        :return: None
        """
        self.username, self.password = credentials

    def store_credentials(self):
        u"""
        Stores the current credentials in the config file

        :return: None
        """
        with open(self.config_file_location, u'w') as config:
            config.write(u"[credentials]\nusername=" + self.username + u"\npassword=" + self.password + u"\n")
