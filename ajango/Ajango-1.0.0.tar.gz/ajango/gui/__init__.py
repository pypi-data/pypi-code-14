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
""" Pakiet obslugujacy interfejs graficzny biblioteki Ajango. """

from ajango.gui.window import Window
from PyQt4.QtGui       import QApplication
from argparse          import ArgumentParser
import sys

#pylint: disable=R0903
class Application(object):
    """ Klasa uruchamiajaca aplikacje okienkowa. """
    @staticmethod
    def main(file_skeleton_arg):
        """ Obsluga uruchomienia aplikacji okienkowej Ajango. """
        file_skeleton = file_skeleton_arg
        parser = ArgumentParser(description="Gui interface for Ajango.")
        parser.add_argument('--file',
                            action='store', const=file_skeleton,
                            default=file_skeleton_arg,
                            help="Address of skeleton file")
        parser.parse_args()
        app = QApplication(sys.argv)
        Window(file_skeleton)
        sys.exit(app.exec_())
