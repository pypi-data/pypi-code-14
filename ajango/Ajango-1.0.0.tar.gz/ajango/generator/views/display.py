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
"""
Obiekt generujacy strone typu 'display'.

Obiekt generuje kod obsugujacy strone wyswietlajaca kod z rekordem bazy danych.
Obiekt do wyswietlenia okreslany jest przez podanie C{id} odpowieniej
pozycji w adresie strony.

Dostepne znaczniki
==================

    1. B{QUERY} - Zapytanie o dane. L{wiecej <ajango.database.query>}.
    2. B{COLUMN} - Kolumna z danymi L{wiecej <ajango.database.columns>}.

Generowany obiekt
=================

L{ajango.site.sites.display}
"""

from ajango.generator.views.list import View as List

class View(List):
    """ Klasa widoku wyswietlajacego. """
    def init(self):
        """ Metoda inicjalizujaca. """
        List.init(self)
        self.type = "display"
