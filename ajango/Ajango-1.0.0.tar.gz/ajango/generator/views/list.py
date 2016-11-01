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
Obiekt generujacy strone typu 'list'.

Obiekt generuje kod obsugujacy strone wyswietlajaca liste rekordow. Dane sa
wybierane na postawie zapytania podanego w znaczniku B{QUERY}.

Dostepne znaczniki
==================

    1. B{QUERY} - Zapytanie o dane. L{wiecej <ajango.database.query>}.
    2. B{COLUMN} - Kolumna z danymi L{wiecej <ajango.database.columns>}.

Generowany obiekt
=================

L{ajango.site.sites.list}
"""

from django.core.management.base import CommandError
from ajango.generator.views      import ViewBase
from ajango.database.columns     import column_factory
from ajango.database.query       import Query

class View(ViewBase):
    """ Klasa widoku wyswietlajacego liste danych. """
    def __init__(self, xmldoc, importRenderer, app):
        self.column = []
        self.query = None
        ViewBase.__init__(self, xmldoc, importRenderer, app)
    def init(self):
        """ Metoda inicjalizujaca. """
        self.type = "list"
        self.add_permited(["QUERY", "COLUMN"])
    def post_init(self):
        """ Czynnosci do wykonania po inicjalizacji. """
        if self.query == None:
            raise CommandError("Query object define")
        if len(self.column) == 0:
            raise CommandError("Don't define any column")
    def check(self, name, xmldoc_elem):
        """ Oczytanie nodow wewnetrznych. """
        if ViewBase.check(self, name, xmldoc_elem):
            return True
        if name.upper() == "QUERY":
            self.query = Query(xmldoc_elem)
            return True
        if name.upper() == "COLUMN":
            self.column.append(column_factory(xmldoc_elem))
            return True
        return False
    def execute(self, view, view_name="view"):
        """ Wykonanie zadan obiektu. """
        self.query.execute(self, view_name)
        for elem in self.column:
            elem.execute(self, view_name)
