###########################################################################
#                                                                         #
#  Copyright (C) 2016  Rafal Kobel <rafyco1@gmail.com>                    #
#                                                                         #
#  This program is free software: you can redistribute it and/or modify   #
#  it under the terms of the GNU General Public License as published by   #
#  the Free Software Foundation, either version 3 of the License, or      #
#  (at your option) any later version.                                    #
#                                                                         #
#  This program is distributed in the hope that it will be useful,        #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the           #
#  GNU General Public License for more details.                           #
#                                                                         #
#  You should have received a copy of the GNU General Public License      #
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                         #
###########################################################################
""" Kontroller do obslugi okna interfejsu graficznego Ajango. """

from PyQt4.QtGui import QStandardItemModel
from PyQt4.QtGui import QStandardItem

class Controller(object):
    """ Klasa okienka interfejsu graficznego Ajango. """
    def __init__(self, window, file_skeleton):
        self.window = window
        if isinstance(file_skeleton, list):
            self.file = file_skeleton
        else:
            tab = []
            tab.append(file_skeleton)
            self.file = tab
    def build_tree(self):
        """ Budowanie okna na podstawie wczytanego pliku. """
        tree = self.window.get_tree()
        model = QStandardItemModel()
        item = QStandardItem("AJANGO")
        item.setEditable(False)
        model.appendRow(item)
        tree.setModel(model)
    def get_file_skeleton(self):
        """ Pobranie nazwy pliku szkieletu. """
        return self.file
