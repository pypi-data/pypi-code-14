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
Modul strony wprowadzajacej dane.

Obiekt obsluguje strone umozliwiajaca wprowadzenie nowych danych.

Obiekt Generujacy
=================

L{ajango.generator.views.input}
"""

from __future__             import print_function
from ajango.site.sites      import SiteBase
from ajango.database.inputs import input_factory
from ajango.database.inputs import InputManager
from ajango.database.query  import DataCreate

class Site(SiteBase):
    """ Klasa strony wprowadzania danych. """
    def __init__(self, ob):
        self.inputs = InputManager()
        self.table = ""
        self.models = None
        SiteBase.__init__(self, ob)
    def init(self):
        """ Metoda inicjalizujaca. """
        self.type = 'input'
    def add_input(self, param):
        """ Dodanie pola wprowadzania danych. """
        self.inputs.add_input(input_factory(param))
    def set_table_name(self, table):
        """ Ustawienie nazwy tabeli do pobrania. """
        self.table = table
    def set_models(self, models):
        """ Ustawienie modelu dla strony. """
        self.models = models
    def _is_form_available(self):
        """ Sprawdzenie czy dostepne sa dane dla obecnego widoku. """
        try:
            return (self.request.method == 'POST' and
                    self.request.POST['view_id'] == ("view_%d" % self.view_id))
        except KeyError:
            return False
    def send_data(self, post):
        """ Wprowadzenie informacji do bazy danych. """
        data = DataCreate(self.table)
        data.set_models(self.models)
        data.create_from_post(post)
        data.save()
    def content(self):
        """ Buduje dane dla strony. """
        data = []
        self.data['result'] = True
        if self._is_form_available():
            if self.inputs.is_valid(self.request.POST):
                self.send_data(self.request.POST)
            self.inputs.set_data(self.request.POST)
        for elem in self.inputs.get_inputs():
            data.append(elem.get_data())
        self.data['tabledata'] = data
