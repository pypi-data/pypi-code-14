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
Modul do wyswietlania danych.

Obiekt obsluguje strone ze szczegolami rekordu z bazy danych. Moga one
pochodzic zarowno z pojedynczej tabeli jak i jako wynik zapytania SQL.

Obiekt Generujacy
=================

L{ajango.generator.views.display}
"""

from django.utils.datastructures    import MultiValueDictKeyError
from django.core.management.base    import CommandError
from ajango.site.sites              import GetSite
from ajango.site.sites.list         import Site   as List
from ajango.database.columns.button import Column as Button

class Site(List, GetSite):
    """ Klasa do wyswietlania danych. """
    def __init__(self, ob):
        self.column = []
        List.__init__(self, ob)
    def init(self):
        """ Metoda inicjalizujaca. """
        self.type = 'display'
        self.column = []
    def get_id(self):
        """ Zwraca id rekordu ktory wyswietla. """
        try:
            identity = self.request.GET['id']
        except MultiValueDictKeyError:
            identity = -1
        return identity
    def content(self):
        """ Buduje dane dla strony. """
        self.data['tabledata'] = []
        results = self.query.get_by_filter({'id' : self.get_id()})
        if len(results) < 1:
            self.data['result'] = False
        else:
            elem = results[0]
            self.data['result'] = True
            line = []
            for col in self.column:
                if isinstance(col, Button):
                    raise CommandError("Display view cannot have Button column")
                else:
                    line.append(col.get_data({'result': elem}))
            self.data['tabledata'] = line
