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
Modul obiektow sprawdzajacych.

Obiekty sprawdzajace zastosowane sa w formularzach wprowadzania danych. Maja
one za zadanie zweryfikowanie czy napisy wprowadzone przez uzytkownika przyjmuja
zadana forme.

Dostepne parametry
==================

    - I{type} - Typ walidatora
    - I{param} - Parametr zalezny od typu

Dostepne Walidacje
==================

Walidatory moga sprawdzic nastepujace warunki:

    - L{pole jest puste <ajango.database.validate.isempty>}
    - L{pole spelnia wyrazenie regularne <ajango.database.validate.regex>}
    - L{pole jest mniejsze niz parametr <ajango.database.validate.lt>}
    - L{pole jest wieksze niz parametr <ajango.database.validate.gt>}
"""

from django.core.management.base import CommandError
from ajango.core.factory         import FactoryBase
from ajango.core.generable       import Generable
from ajango.core.hybrid          import Hybrid, get_str_object_factory
import abc

class ValidateFactoryObject(FactoryBase):
    """ Fabryka obiektow sprawdzajacych. """
    def __init__(self, param=None):
        self.param = None
        FactoryBase.__init__(self, param)
    def init(self):
        """ Metoda inicjalizujaca. """
        self.set_items('Validate', {
            'isempty' : 'ajango.database.validate.isempty',
            'regex'   : 'ajango.database.validate.regex',
            'lt'      : 'ajango.database.validate.lt',
            'gt'      : 'ajango.database.validate.gt'
        })
        get_str_object_factory(self, 'isempty')

def validate_factory(param):
    """ Fabryka obiektow sprawdzajacych. """
    return ValidateFactoryObject(param).get_from_params()

class ValidateBase(Hybrid, Generable):
    """ Klasa abstrakcyjna obiektu sprawdzajacego. """
    __metaclass__ = abc.ABCMeta
    def __init__(self, param):
        self.has_prepare = False
        self.type = "unKnown"
        self.data = {}
        self.xml_name = "VALIDATE"
        self.pre_init()
        self.messages = []
        self.param = ""
        Hybrid.__init__(self, param)
        self.post_init()
    def pre_init(self):
        """ Czynnosci przed inicjalizacja. """
        pass
    def post_init(self):
        """ Czynnosci po inicjalizacji. """
        pass
    def get_param(self):
        """ Pobranie parametru validatora. """
        return self.param
    def read_from_xml(self, xmldoc):
        """ Inicjalizacja z danych XML. """
        self.param = self.getAttribute('param')
    def read_from_dict(self, params):
        """ Inicjalizacja ze zmiennej slownikowej. """
        try:
            self.param = params['param']
        except KeyError:
            raise CommandError("Input element is invalid")
    @abc.abstractmethod
    def is_valid(self, text):
        """ Sprawdza czy pola wejsiowe sa poprawnie wypelnione. """
        raise CommandError("File not implemented yet.")
    def execute(self, view, view_name="view"):
        """ Wykonanie zadan obiektu. """
        view.add_line("vm.add_validate({'type': %r, 'param': %r })" %
                      (self.type, self.param))
    def get_messages(self):
        """ Pobiera wiadomosci bledu pol wejsiowych. """
        return self.messages
    def check(self, name, xmldoc_elem):
        pass

class ValidationManager(Generable):
    """ Klasa zarzadzajaca obiektami sprawdzajacymi. """
    def __init__(self):
        self.validations = []
        self.messages = []
    def __len__(self):
        return len(self.validations)
    def add_validate(self, param):
        """ Dodanie obiektu sprawdzajacego. """
        self.validations.append(validate_factory(param))
    def is_valid(self, text):
        """ Sprawdza czy pola wejsciowe sa poprawnie wypelnione. """
        for elem in self.validations:
            if not elem.is_valid(text):
                self.messages += elem.get_messages()
                return False
        return True
    def get_messages(self):
        """ Pobranie wiadomosci bledu pola wejsciowego. """
        return self.messages
    def execute(self, view, view_name="view"):
        """ Wykonanie zadan obiektu. """
        if len(self.validations) > 0:
            view.add_import("ValidationManager", "ajango.database.validate")
            view.add_line("vm = ValidationManager()")
            for elem in self.validations:
                elem.execute(view)
