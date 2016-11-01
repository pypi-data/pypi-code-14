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
""" Modul zarzadzania polami wejsciowymi. """

from __future__                  import print_function
from django.core.management.base import CommandError
from ajango.core.factory         import FactoryBase
from ajango.database.validate    import ValidationManager
from ajango.core.generable       import Generable
from ajango.core.hybrid          import Hybrid, get_str_object_factory

class InputFactoryObject(FactoryBase):
    """ Klasa fabryki pol wejsciowych. """
    def init(self):
        """ Metoda inicujujaca. """
        self.set_items('Input', {
            'default'     : 'ajango.database.inputs.default',
            'number'      : 'ajango.database.inputs.number'
        })
        get_str_object_factory(self)

def input_factory(params):
    """ Fabryka pol wejsciowych. """
    return InputFactoryObject(params).get_from_params()

#pylint: disable=R0902
class InputBase(Hybrid, Generable):
    """ Abstrakcyjna klasa pola wejsiowego. """
    def __init__(self, params):
        self.type = "unKnown"
        self.theme = 'default'
        self.default = ""
        self.messages = []
        self.has_prepare = False
        self.data = {}
        self.xml_name = "INPUT"
        self.pre_init()
        self.label = ""
        self.default = ""
        self.tag = ""
        self.validation_manager = ValidationManager()
        Hybrid.__init__(self, params)
        self.value = self.default
        self.post_init()
    def read_from_xml(self, xmldoc):
        """ Inicjalizacja z danych XML. """
        self.label = self.getAttribute('label')
        self.default = self.getAttribute('default')
        self.tag = self.getAttribute('tag')
    def read_from_dict(self, params):
        """ Inicjalizacja ze zmiennej slownikowej. """
        try:
            self.validation_manager = params['vm']
            if self.validation_manager == None:
                self.validation_manager = ValidationManager()
        except KeyError:
            self.validation_manager = ValidationManager()
        try:
            self.label = params['label']
            self.default = params['default']
            self.tag = params['tag']
        except KeyError:
            raise CommandError("Input element is invalid")
    def pre_init(self):
        """ Czynnosci przed inicjalizacja. """
        self.add_permited(["VALIDATE"])
    def post_init(self):
        """ Czynnosci po inicjalizacji. """
        pass
    def execute(self, view, view_name='view'):
        """ Wykonanie zadan obiektu. """
        self.validation_manager.execute(view)
        if len(self.validation_manager) > 0:
            view.add_line("%s.add_input({'type': %r, "
                          "'label': %r, "
                          "'tag': %r, "
                          "'default': %r, "
                          "'vm': vm })" %
                          (view_name, self.type, self.label,
                           self.tag, self.default))
        else:
            view.add_line("%s.add_input({'type': %r, "
                          "'label': %r, "
                          "'tag': %r, "
                          "'default': %r })" %
                          (view_name, self.type, self.label,
                           self.tag, self.default))
    def set_value(self, value):
        """ Ustawienie wartosci. """
        self.value = value
    def check(self, name, xmldoc_elem):
        """ Oczytanie nodow wewnetrznych. """
        if name == 'VALIDATE':
            self.validation_manager.add_validate(xmldoc_elem)
    def prepare_data(self):
        """ Przygotowanie danych dla szablonu. """
        if self.has_prepare:
            return
        # Id dla fromularza, do uzycia przy kilku widokach na jednej stronie
        self.has_prepare = True
        self.data['label'] = self.label
        self.data['default'] = self.default
        self.data['value'] = self.value
        self.data['tag'] = self.tag
        self.data['url'] = '%s/ajango_inputs/%s.html' % (self.theme, self.type)
        self.data['messages'] = self.messages
    def get_data(self):
        """ Pobieranie danych dla szablonu. """
        self.prepare_data()
        return dict(self.data)
    def get_label(self):
        """ Pobranie opisu pola wejsiowego. """
        self.prepare_data()
        return self.label
    def get_messages(self):
        """ Pobranie wiadomosci bledu pola wejsciowego. """
        return self.messages
    def is_valid(self, data):
        """ Sprawdzenie pole wejsciowe jest poprawnie wypelnione. """
        value = False
        try:
            text = data[self.tag]
            value = self.validation_manager.is_valid(text)
            self.messages += self.validation_manager.get_messages()
        except KeyError:
            self.messages.append("Cannot read data named %r from POST" %
                                 self.tag)
        return value

class InputManager(object):
    """ Klasa zarzadzajaca obiektami pol wejsiowych. """
    def __init__(self):
        self.inputs = []
        self.messages = []
    def add_input(self, input_ob):
        """ Dodaj pole wejsiowe. """
        self.inputs.append(input_ob)
    def get_inputs(self):
        """ Zwraca tablice elementow kontenera. """
        return self.inputs
    def is_valid(self, data):
        """ Sprawdza czy pola wejsiowe sa poprawnie wypelnione. """
        result = True
        for elem in self.inputs:
            if not elem.is_valid(data):
                self.messages += elem.get_messages()
                result = False
        return result
    def set_data(self, data):
        """ Ustawienie elementow danymi z parametru. """
        for elem in self.inputs:
            try:
                value = data[elem.tag]
                elem.value = value
            except KeyError:
                print("There are no tag %r in data object" % elem.tag)
                elem.value = elem.default
    def set_data_table(self, table_el):
        """ Ustwienie elementow na podstawie tabeli. """
        for elem in self.inputs:
            value = table_el.serializable_value(elem.tag)
            elem.value = value
    def get_messages(self):
        """ Pobiera wiadomosci bledu pol wejsiowych. """
        return self.messages
