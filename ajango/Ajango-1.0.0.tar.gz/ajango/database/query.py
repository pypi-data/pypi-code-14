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
Modul zarzadzania zapytaniami do bazy danych.

Umozliwia wykonanie zapytania SQL dla wybranych elementow.

Dostepne znaczniki
==================

    1. B{TABLE} - Tabela do ktorej nalezy wstawic dane.
        - I{name} - Nazwa tabeli
"""

from django.core.management.base import CommandError
from ajango.core.generable       import Generable
from ajango.core.hybrid          import Hybrid
from ajango.database             import get_table_by_name

class Result(object):
    """ Obiekt odpowiedzi. """
    def __init__(self, data):
        self.data = data
    def get_element(self, key):
        """ Pobierz odpowiedni element. """
        return self.data.serializable_value(key)
    def set_data(self, data):
        """ Ustawienie danych. """
        self.data = data

class Query(Hybrid, Generable):
    """ Obiekt zapytania. """
    def __init__(self, param):
        self.xml_name = "QUERY"
        self.xml_permited = ["TABLE"]
        self.table = ""
        self.models = None
        self._table_object = None
        Hybrid.__init__(self, param)
    def read_from_xml(self, xmldoc):
        """ Inicjalizacja z danych XML. """
        pass
    def read_from_dict(self, param):
        """ Inicjalizacja ze zmiennej slownikowej. """
        self.table = param['table']
    def check(self, name, xmldoc_elem):
        """ Odczytanie nodow wewnetrznych. """
        if name == "TABLE":
            if self.table != "":
                raise CommandError("There are only one table name.")
            self.table = xmldoc_elem.getAttribute('name')
    def set_models(self, models):
        """ Ustawienie modelu. """
        self.models = models
    def execute(self, view, view_name='view'):
        """ Wykonanie zadan obiektu. """
        view.add_import("models", ".")
        view.add_import("Query", "ajango.database.query")
        view.add_line("query = Query({ 'table': %r })" % self.table)
        view.add_line("query.set_models(models)")
        view.add_line("%s.set_query(query)" % view_name)
    def _get_table_object(self):
        """ Zwraca obiekt tabeli zgodny z biblioteka minidom. """
        if self._table_object == None:
            self._table_object = get_table_by_name(self.table, self.models)
        return self._table_object
    @staticmethod
    def _get_base(elems):
        """ Czesc wspolna dla metod pobierajacych dane 'get'. """
        results = []
        for elem in elems:
            results.append(Result(elem))
        return results
    def get_by_filter(self, option):
        """ Pobiera dane na podstawie filtra. """
        table = self._get_table_object()
        id_param = option['id']
        elems = table.objects.filter(id=id_param)
        return Query._get_base(elems)
    def get_all(self):
        """ Pobiera wszystkie dane z tabeli. """
        table = self._get_table_object()
        elems = table.objects.all()
        return Query._get_base(elems)

class DataCreate(object):
    """ Klasa wprowadzajaca dane do bazy. """
    def __init__(self, table):
        self.table = table
        self.models = None
        self._table_object = None
        self.data = None
    def set_models(self, models):
        """ Ustawienie modelu. """
        self.models = models
    def _get_table_object(self):
        """ Zwraca obiekt tabeli zgodny z biblioteka minidom. """
        if self._table_object == None:
            self._table_object = get_table_by_name(self.table, self.models)
        return self._table_object
    def create_from_post(self, post):
        """ Wprowadz do bazy dane na podstawie odpowiedzi formularza. """
        table = self._get_table_object()
        table_inputs = []
        for elem in post.keys():
            if elem == 'view_id' or elem.find('middlewaretoken') > -1:
                continue
            table_inputs.append(elem)
        data = table()
        for elem in table_inputs:
            setattr(data, elem, post[elem])
        self.data = data
    def save(self):
        """ Zapisanie danych do bazy. """
        self.data.save()

class DataEdit(object):
    """ Klasa edytujaca dane do bazy. """
    def __init__(self, table, editable_ob):
        self.table = table
        self.editable_ob = editable_ob
    def edit_with_post(self, post):
        """ Wprowadz do bazy dane na podstawie odpowiedzi formularza. """
        table_inputs = []
        for elem in post.keys():
            if elem == 'view_id' or elem.find('middlewaretoken') > -1 or elem == 'identity':
                print ("Element pominiety: %s" % elem)
                continue
            print("Element: %s " % elem)
            table_inputs.append(elem)
        for elem in table_inputs:
            setattr(self.editable_ob, elem, post[elem])
    def set_models(self, models):
        """ 
        Ustawienie modelu. (metoda przestarzala)
        """
        pass
    def save(self):
        """ Zapisanie danych do bazy. """
        self.editable_ob.save()
