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
Modul strony z edycja danych.

Obiekt obsluguje strone pozwalajaca na edytowanie danych.

Obiekt Generujacy
=================

L{ajango.generator.views.editable}
"""

from __future__                  import print_function
from django.utils.datastructures import MultiValueDictKeyError
from ajango.site.sites           import SiteBase
from ajango.database.inputs      import input_factory
from ajango.database.inputs      import InputManager
from ajango.database.query       import DataEdit
from ajango.database             import get_table_by_name

class Site(SiteBase):
    """ Klasa strony wprowadzania danych. """
    def __init__(self, ob):
        self.inputs = InputManager()
        self.table = ""
        self.models = None
        self.editable_ob = None 
        SiteBase.__init__(self, ob)
        self.identity = self.get_id()
    def init(self):
        """ Metoda inicjalizujaca. """
        self.type = 'editable'
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
    def get_id(self):
        """ Zwraca id rekordu ktory wyswietla. """
        try:
            identity = self.request.GET['id']
        except MultiValueDictKeyError:
            try:
                identity = self.request.POST['identity']
            except MultiValueDictKeyError:
                identity = -1
        return identity
    def send_data(self, post):
        """ Wprowadzenie informacji do bazy danych. """
        data = DataEdit(self.table, self.editable_ob)
        data.set_models(self.models)
        data.edit_with_post(post)
        data.save()
    def content(self):
        """ Buduje dane dla strony. """
        table_ob = get_table_by_name(self.table, self.models)
        try:
            self.editable_ob = table_ob.objects.filter(id=self.identity)[0]
        except IndexError:
            self.editable_ob = None
        data = []
        self.data['result'] = True
        self.data['identity'] = self.identity
        if self.editable_ob == None:
            self.data['result'] = False
            return
        if self._is_form_available():
            if self.inputs.is_valid(self.request.POST):
                self.send_data(self.request.POST)
                self.data['result'] = False
                return
            self.inputs.set_data(self.request.POST)
        else:
            self.inputs.set_data_table(self.editable_ob)
        for elem in self.inputs.get_inputs():
            data.append(elem.get_data())
        self.data['tabledata'] = data
