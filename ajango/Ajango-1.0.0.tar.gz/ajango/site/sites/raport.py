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
Modul wyswietlania raportu.

Obiekt obsluguje strone wyswietlajaca raport na podstawie wybranych danych.

Obiekt Generujacy
=================

L{ajango.generator.views.raport}
"""

from django.core.management.base    import CommandError
from ajango.site.sites              import GetSite
from ajango.site.sites.list         import Site   as List
from ajango.database.columns.button import Column as Button

class Site(List, GetSite):
    """ Klasa wyswietlania raportu. """
    def __init__(self, ob):
        self.list_mode = False
        List.__init__(self, ob)
        self.set_layout("ajango_raport.html")
    def get_request(self):
        """ Zwraca obiekt request. """
        return self.request
    def set_template(self, template, is_build=True):
        """ Ustawienie pliku z szablonem dla raportu. """
        if is_build:
            template = "ajango_raports/ajango_%s.html" % template
        self.set_include(template)
    def set_list_mode(self, value):
        """ Wlaczenie lub wylaczenie trybu listy. """
        self.list_mode = value
    def content(self):
        """ Buduje dane dla strony. """
        self.data['tabledata'] = []
        elem_id = self.get_id()
        if elem_id >= 0:
            results = self.query.get_by_filter({'id' : elem_id})
        else:
            results = self.query.get_all()
        if len(results) < 1:
            self.data['result'] = False
        else:
            data = []
            for elem in results:
                line = []
                for col in self.column:
                    if isinstance(col, Button):
                        raise CommandError("Display view cannot "
                                           "have Button column")
                    else:
                        line.append(col.get_data({'result' : elem}))
                data.append(list(line))
            self.data['tabledata'] = data
        self.data['list_mode'] = self.list_mode
