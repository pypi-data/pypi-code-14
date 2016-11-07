"""
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
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from toktokkie.utils.iconizing.Iconizer import Iconizer
from toktokkie.ui.qt.pyuic.iconizer import Ui_FolderIconizerWindow


class IconizerQtGui(QMainWindow, Ui_FolderIconizerWindow):
    """
    Class that defines the functionality of the Folder Iconizer GUI
    """

    def __init__(self, parent: QMainWindow = None) -> None:
        """
        Initializes the interactive components of the GUI

        :param parent: The parent QT GUI
        """
        super().__init__(parent)
        self.setupUi(self)

        self.iconizer = Iconizer()

        self.browse_directory_button.clicked.connect(self.browse_for_directory)
        self.start_button.clicked.connect(self.start_iconizing)

    def browse_for_directory(self) -> None:
        """
        Lets the user browse for a local directory path

        :return: None
        """
        # noinspection PyCallByClass,PyTypeChecker, PyArgumentList
        directory = QFileDialog.getExistingDirectory(self, "Browse")
        if directory:
            self.directory_path_edit.setText(directory)

    def start_iconizing(self) -> None:
        """
        Starts the iconizing process for the specified directory

        :return: None
        """
        if self.recursive_check.checkState():
            self.iconizer.recursive_iconize(self.directory_path_edit.text())
        else:
            self.iconizer.iconize_directory(self.directory_path_edit.text())
