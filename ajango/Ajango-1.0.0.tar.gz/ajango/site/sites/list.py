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
Modul obslugujacy strone z lista elementow.

Obiekt obsluguje strone z lista elementow. Moga one pochodzic zarowno
z pojedynczej tabeli jak i jako wynik zapytania SQL.

Obiekt Generujacy
=================

L{ajango.generator.views.list}
"""

from __future__              import print_function
from ajango.site.sites       import SiteBase
from ajango.database.columns import column_factory

def print_debug(text):
    """
    Wyswietlenie informacji debugowej. Funkcja opcjonalna.

    Aby uzyc nalezy zmienic wartosc wewnatrz instrukcji C{if} z C{False}
    na C{True}.
    """
    if False:
        print(text)

class Site(SiteBase):
    """ Klasa obslugujaca strone tabeli z lista elementow. """
    def __init__(self, ob):
        self.table = ""
        self.column = []
        self.query = None
        SiteBase.__init__(self, ob)
    def get_request(self):
        """ Zwraca obiekt request. """
        return self.request
    def init(self):
        """ Inicjalizacja metody. """
        self.type = 'list'
    def add_column(self, param):
        """ Dodanie nowej kolumny do wyswietlenia. """
        col = column_factory(param)
        self.column.append(col)
    def set_query(self, query):
        """ Ustawienie zapytania dla strony. """
        self.query = query
    def content(self):
        """ Ustawienie zmiennych dostarczanych do szablonow. """
        self.data['tableheader'] = []
        for col in self.column:
            self.data['tableheader'].append(col.get_label())
        data = []
        results = self.query.get_all()
        print_debug("======== Column list ===============")
        for elem in results:
            line = []
            for col in self.column:
                line.append(col.get_data({'result' : elem}))
                print_debug(line)
                print_debug("------------------------------------")
            data.append(list(line))
            print_debug(data)
            print_debug("====================================")
        self.data['tabledata'] = data
