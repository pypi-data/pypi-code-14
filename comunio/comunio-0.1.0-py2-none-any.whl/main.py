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
import argparse
from comunio.ui.StatisticsViewer import start as start_gui
from comunio.scraper.ComunioSession import ComunioSession
from comunio.database.DatabaseManager import DatabaseManager
from comunio.calc.StatisticsCalculator import StatisticsCalculator


def main():
    u"""
    Starts the Program by analyzing the given command line parameters and acting accordingly

    :return: None
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(u"username",  help=u"The username with which to log in to comunio.de")
    parser.add_argument(u"password", help=u"The password with which to log in to comunio.de")
    parser.add_argument(u"-g", u"--gui", action=u"store_true", help=u"Starts the program in GUI mode")
    parser.add_argument(u"-u", u"--update", action=u"store_true", help=u"Only updates the database, then quits")
    parser.add_argument(u"-s", u"--summary", action=u"store_true", help=u"Lists the current state of the comunio account")
    args = parser.parse_args()

    comunio = ComunioSession(args.username, args.password)
    database = DatabaseManager(comunio)
    calculator = StatisticsCalculator(comunio, database)

    if args.gui:
        start_gui(comunio, database)
    elif args.list:
        print u"Cash:       {:,}".format(database.get_last_cash_amount())
        print u"Team value: {:,}".format(database.get_last_team_value_amount())
        print u"Balance:    {:,}".format(calculator.calculate_total_assets_delta())
        print u"\n\nPlayers:\n"
        for player in database.get_players_on_day(0):
            print player
    elif args.update:
        database.update_database()

if __name__ == u'__main__':
    main()
