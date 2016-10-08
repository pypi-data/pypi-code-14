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
from __future__ import absolute_import
import sys
import argparse
from typing import Dict
from argparse import Namespace
from comunio.metadata import SentryLogger
from comunio.ui.LoginScreen import start as start_logi_gui
from comunio.ui.StatisticsViewer import start as start_gui
from comunio.scraper.ComunioSession import ComunioSession
from comunio.database.DatabaseManager import DatabaseManager
from comunio.calc.StatisticsCalculator import StatisticsCalculator
from comunio.credentials.CredentialsManager import CredentialsManager


def parse_arguments():
    u"""
    Parses the command line aruments

    :return: the arguments as an argsparse namespace
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(u"-g", u"--gui", action=u"store_true",
                        help=u"Starts the program in GUI mode")
    parser.add_argument(u"-u", u"--username",
                        help=u"The username with which to log in to comunio.de")
    parser.add_argument(u"-p", u"--password",
                        help=u"The password with which to log in to comunio.de")
    parser.add_argument(u"-k", u"--keep_creds", action=u"store_true",
                        help=u"Stores the given credentials in a local config file")
    parser.add_argument(u"-r", u"--refresh", action=u"store_true",
                        help=u"Only updates the database, then quits")
    parser.add_argument(u"-s", u"--summary", action=u"store_true",
                        help=u"Lists the current state of the comunio account")
    return parser.parse_args()


def main():
    u"""
    Starts the Program by analyzing the given command line parameters and acting accordingly

    :return: None
    """
    try:

        args = parse_arguments()

        if args.username and args.password:
            credentials = CredentialsManager((args.username, args.password))
        else:
            credentials = CredentialsManager()

        if args.gui:
            handle_gui(credentials)
        else:
            handle_cli(vars(args), credentials)

    except Exception, e:
        SentryLogger.sentry.captureException()
        raise e


def handle_cli(args, credentials):
    u"""
    Handles the behavious of the CLI of the program

    :param args:        the previously parsed console arguments
    :param credentials: the previously defined credential manager
    :return:            None
    """
    if credentials.get_credentials() == (u"", u""):
        print u"Please supply a username and password:\n"
        print u"    Either via the --password and the --username parameters"
        print u"        OR"
        print u"    The config file found in " + credentials.get_config_file_location()
        sys.exit(1)

    if not args[u"refresh"] and not args[u"summary"]:
        print u"No valid options passed. See the --help option for more information"
        sys.exit(1)

    if args[u"keep_creds"]:
        credentials.store_credentials()

    try:
        comunio = ComunioSession(credentials.get_credentials()[0], credentials.get_credentials()[1])
        database = DatabaseManager(comunio)
        calculator = StatisticsCalculator(comunio, database)

        if args[u"refresh"]:
            database.update_database()
            print u"Database Successfully Updated"

        elif args[u"summary"]:
            print u"Cash:       {:,}".format(database.get_last_cash_amount())
            print u"Team value: {:,}".format(database.get_last_team_value_amount())
            print u"Balance:    {:,}".format(calculator.calculate_total_assets_delta())
            print u"\n\nPlayers:\n"
            for player in database.get_players_on_day(0):
                print player

        else:
            print u"No valid options passed. See the --help option for more information"

    except ReferenceError:
        print u"Player data unavailable due to having 5 players on the transfer list."
        print u"Please Remove a player from the transfer list to continue."
        print u"The program will now exit"
    except ConnectionError:
        print u"Connection to Comunio failed due to Network error"
    except PermissionError:
        print u"The provided credentials are invalid"


def handle_gui(credentials):
    u"""
    Handles the GUI initialization of the program

    :param credentials: the previously defined credential manager
    :return:            None
    """
    comunio = start_logi_gui(credentials)
    if comunio is not None:
        database = DatabaseManager(comunio)
        start_gui(comunio, database)
