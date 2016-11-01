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
""" Modul obslugujacy glowne okno interfejsu graficznego. """

from PyQt4.QtGui                 import QWidget
from PyQt4.QtGui                 import QMessageBox
from PyQt4.QtGui                 import QIcon
from PyQt4.QtGui                 import QTreeView
from PyQt4.QtGui                 import QTableView
from PyQt4.QtGui                 import QSplitter
from PyQt4.QtGui                 import QHBoxLayout
from PyQt4.QtCore                import Qt
from django.core.management.base import CommandError
from ajango.gui.controller       import Controller
import ajango

def block_application(window):
    """ Wyswietla wiadomosc o niedostepnosci elementu gui i rzuca blad. """
    message = QMessageBox(window)
    message.setText("Blad interfejsu graficznego.")
    message.setInformativeText("Oprogramowanie w budowie.")
    message.setWindowIcon(QIcon(ajango.__path__[0] +
                                '/gui/resource/icon.png'))
    message.setIcon(QMessageBox.Critical)
    message.exec_()
    raise CommandError("Aplikacja nie gotowa.")

class Window(QWidget):
    """ Klasa okienka interfejsu graficznego Ajango. """
    def __init__(self, file_skeleton):
        self.tree = None
        self.table = None
        self.controller = Controller(self, file_skeleton)
        QWidget.__init__(self)
        self.init_ui()
        self.controller.build_tree()
        block_application(self)
    def get_tree(self):
        """ Zwraca drzewo okna. """
        return self.tree
    def get_table(self):
        """ Zwraca okno z tabela. """
        return self.table
    def init_ui(self):
        """ Inicjalizacja okienka. """
        self.tree = QTreeView(self)
        self.table = QTableView(self)
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.tree)
        splitter.addWidget(self.table)
        vbox = QHBoxLayout()
        vbox.addWidget(splitter)
        self.setLayout(vbox)
        self.setGeometry(300, 300, 500, 200)
        self.setWindowTitle('Ajagno Editor')
        self.setWindowIcon(QIcon(ajango.__path__[0] +
                                 '/gui/resources/icon.png'))
        self.show()
