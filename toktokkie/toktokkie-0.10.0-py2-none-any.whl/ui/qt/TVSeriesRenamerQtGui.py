u"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of toktokkie.

    toktokkie is a program that allows convenient managing of various
    local media collections, mostly focused on video.

    toktokkie is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    toktokkie is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with toktokkie.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

# imports
from __future__ import division
from __future__ import absolute_import
import os
from toktokkie.ui.qt.pyuic.tv_series_renamer import Ui_TVSeriesRenamer
from toktokkie.utils.renaming.TVSeriesRenamer import TVSeriesRenamer
from toktokkie.utils.metadata.MetaDataManager import MetaDataManager
from toktokkie.utils.renaming.schemes.SchemeManager import SchemeManager
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTreeWidgetItem, QHeaderView


class TVSeriesRenamerQtGui(QMainWindow, Ui_TVSeriesRenamer):
    u"""
    Class that models th QT GUI for the TV Series Renamer
    """

    def __init__(self, parent = None):
        u"""
        Sets up the interactive UI elements

        :param parent: the parent window
        """
        super(TVSeriesRenamerQtGui, self).__init__(parent)
        self.setupUi(self)

        # Initialize UI elements
        self.browse_button.clicked.connect(self.browse_for_directory)
        self.directory_entry.textChanged.connect(self.parse_directory)
        self.cancel_button.clicked.connect(lambda: self.cancel(True))
        self.confirm_button.clicked.connect(self.confirm)
        self.rename_list.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.selection_remover_button.clicked.connect(self.remove_selection)
        self.recursive_check.stateChanged.connect(self.parse_directory)

        for scheme in SchemeManager.get_scheme_names():
            self.scheme_selector.addItem(scheme)

        # Local Variables
        self.confirmation = []
        self.renamer = None

    # noinspection PyArgumentList
    def browse_for_directory(self):
        u"""
        Brings up a directory browser window.
        Once a directory was selected, the new directory is then inserted into the
        directory path entry.

        :return: None
        """
        # noinspection PyCallByClass,PyTypeChecker
        directory = QFileDialog.getExistingDirectory(self, u"Browse")
        if directory:
            self.directory_entry.setText(directory)

    def parse_directory(self):
        u"""
        Checks the currently entered directory for episode files to rename.
        All discovered episodes are then displayed in the rename list

        :return: None
        """
        self.cancel(False)
        directory = self.directory_entry.text()

        if os.path.isdir(directory) and \
                (MetaDataManager.is_media_directory(directory, media_type=u"tv_series")
                 or self.recursive_check.checkState()):

            self.meta_warning_label.setVisible(False)

            renaming_scheme = self.scheme_selector.currentText()
            renaming_scheme = SchemeManager.get_scheme_from_scheme_name(renaming_scheme)
            self.renamer = TVSeriesRenamer(directory, renaming_scheme, self.recursive_check.checkState())

            self.confirmation = self.renamer.request_confirmation()
            for item in self.confirmation:
                self.rename_list.addTopLevelItem(QTreeWidgetItem([item.get_names()[0], item.get_names()[1]]))

    def cancel(self, directory_entry = True):
        u"""
        Cancels the current Renaming process and resets the UI

        :param directory_entry: Clearing the directory entry can be disabled optionally
        :return: None
        """
        self.renamer = None
        self.rename_list.clear()
        self.meta_warning_label.setVisible(True)
        if directory_entry:
            self.directory_entry.clear()

    def confirm(self):
        u"""
        Starts the renaming process

        :return: None
        """
        if self.renamer is not None:
            for item in self.confirmation:
                item.confirmed = True

            self.renamer.confirm(self.confirmation)
            self.renamer.start_rename()
            self.parse_directory()

    def remove_selection(self):
        u"""
        Removes the selected items from the list

        :return: None
        """
        for index, row in enumerate(self.rename_list.selectedIndexes()):
            if index % 2 != 0:
                continue
            self.confirmation.pop(row.row() - int(index / 2))
        self.rename_list.clear()
        for item in self.confirmation:
            self.rename_list.addTopLevelItem(QTreeWidgetItem([item.get_names()[0], item.get_names()[1]]))
