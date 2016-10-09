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
import os
import sys
from PyQt5.QtGui import QPixmap, QBrush, QColor
from PyQt5.QtWidgets import QMainWindow, QApplication, QHeaderView, QTreeWidgetItem
from comunio.ui.windows.stats import Ui_StatisticsWindow
from comunio.scraper.ComunioSession import ComunioSession
from comunio.database.DatabaseManager import DatabaseManager
from comunio.calc.StatisticsCalculator import StatisticsCalculator


class StatisticsViewer(QMainWindow, Ui_StatisticsWindow):
    u"""
    Class that models the QT GUI for displaying Comunio statistics
    """

    def __init__(self, comunio_session,
                 database_manager,
                 calculator,
                 parent = None):
        u"""
        Sets up the interactive UI elements

        :param comunio_session:  An initialized comunio session
        :param database_manager: An initialized Database Manager object
        :param calculator:       An initialized StatisticsCalculator object
        :param parent:           The parent window
        """
        super(StatisticsViewer, self).__init__(parent)
        self.setupUi(self)

        self.__comunio_session = comunio_session
        self.__database_manager = database_manager
        self.__statistics_calculator = calculator

        for i in xrange(0, 8):  # Makes headers all the same size
            self.player_table.header().setSectionResizeMode(i, QHeaderView.Stretch)
        self.player_table.itemSelectionChanged.connect(self.__select_player)

        self.__players = []
        self.__insert_sorted_players_into_players_list()

        self.__fill_initial_data()
        self.__fill_player_table()

    def __fill_initial_data(self):
        u"""
        Fills the initial data, like the player's cash or team value information

        :return: None
        """
        cash = self.__database_manager.get_last_cash_amount()
        team_value = self.__database_manager.get_last_team_value_amount()
        display_name = self.__comunio_session.get_screen_name()

        self.greeting_label.setText(self.greeting_label.text().replace(u"<username>", display_name))
        self.cash_display.setText(u"{:,}€".format(cash))
        self.team_value_display.setText(u"{:,}€".format(team_value))

        self.total_assets_display.setText(u"{:,}".format(cash + team_value))
        self.balance_display.setText(u"{:,}".format(self.__statistics_calculator.calculate_total_assets_delta()))

    def __fill_player_table(self):
        u"""
        Fills the player table with the current data in the local database

        :return: None
        """
        for player in self.__players:

            position = player[u"position"]
            name = player[u"name"]
            points = unicode(player[u"points"])
            current_value = player[u"value"]
            buy_value = self.__database_manager.get_player_buy_value(name)
            total_player_delta = current_value - buy_value
            total_player_delta_bg = self.__get_color_formatting(total_player_delta)

            yesterday_value = self.__database_manager.get_player_on_day(name, -1)
            try:
                yesterday_value = yesterday_value[u"value"]
                tendency = current_value - yesterday_value
                yesterday_value = u"{:,}".format(yesterday_value)
                tendency_bg = self.__get_color_formatting(tendency)
                tendency = u"{:,}€".format(tendency)

            except TypeError:
                yesterday_value = u"---"
                tendency = u"---"
                tendency_bg = QBrush(QColor(237, 212, 0))

            buy_value = u"{:,}".format(buy_value)
            current_value = u"{:,}€".format(current_value)
            total_player_delta = u"{:,}€".format(total_player_delta)

            tree_widget_item = QTreeWidgetItem([position, name, points, buy_value, yesterday_value,
                                                current_value, total_player_delta, tendency])
            self.player_table.addTopLevelItem(tree_widget_item)

            tree_widget_item.setBackground(6, total_player_delta_bg)
            tree_widget_item.setBackground(7, tendency_bg)

    @staticmethod
    def __get_color_formatting(value):
        u"""
        Evaluates a monetary value an defines a color for it. Red for negative numbers, yellow for 0 and
        green for positive colors

        :param value: the value to be used
        :return:      the QBrush appropriate for the value
        """
        if value > 0:
            return QBrush(QColor(115, 210, 22))  # Green
        elif value == 0:
            return QBrush(QColor(237, 212, 0))   # Yellow
        else:  # If value < 0
            return QBrush(QColor(239, 41, 41))   # Red

    def __insert_sorted_players_into_players_list(self):
        u"""
        Sorts the list of current players in the comunio team by their position, from Goalkeeper to Striker and enters
        them in that order into the self.__players list.
        Furthermore, the players are given two new keys, which will eventually contain the paths to their graphs.

        :return: None
        """
        players = self.__database_manager.get_players_on_day(0)
        order = [u"Torhüter", u"Abwehr", u"Mittelfeld", u"Sturm"]
        for position in order:
            for player in players:
                if player[u"position"] == position:
                    player[u"points_graph"] = None
                    player[u"value_graph"] = None
                    self.__players.append(player)

    def __select_player(self):
        u"""
        Called whenever the user selects a player from the table. Fills the side info and generates
        the value history graph

        :return: None
        """
        player_index = self.player_table.selectedIndexes()[0].row()
        player = self.__players[player_index]

        self.player_name_label.setText(player[u"name"])
        self.player_position_label.setText(player[u"position"])
        self.player_points_label.setText(unicode(player[u"points"]))
        self.player_value_label.setText(u"{:,}".format(player[u"value"]))
        self.fill_graphs(player_index)

    def fill_graphs(self, player_index):
        u"""
        Fills the player value graph widget with a graph displaying the player's previous values
        over time as well as the player points graph with the player's points over time

        :param player_index: The player index in the self.__players attribute
        :return:             None
        """
        if self.__players[player_index][u"value_graph"] is None or self.__players[player_index][u"points_graph"] is None:

            player_name = self.__players[player_index][u"name"]

            value_graph_image = self.__statistics_calculator.generate_time_graph(player_name, u"value")
            points_graph_image = self.__statistics_calculator.generate_time_graph(player_name, u"points")
            self.__players[player_index][u"value_graph"] = QPixmap(value_graph_image)
            self.__players[player_index][u"points_graph"] = QPixmap(points_graph_image)
            os.remove(value_graph_image)
            os.remove(points_graph_image)

        self.value_graph.setPixmap(self.__players[player_index][u"value_graph"])
        self.points_graph.setPixmap(self.__players[player_index][u"points_graph"])


def start(comunio_session, database_manager, calculator):
    u"""
    Starts the Statistics Viewer GUI.

    :param comunio_session:  An initialized comunio session
    :param database_manager: An initialized Database Manager object
    :param calculator:       An initialized StatisticsCalculator object
    :return:                 None
    """
    app = QApplication(sys.argv)
    form = StatisticsViewer(comunio_session, database_manager, calculator)
    form.show()
    app.exec_()
