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
Modul fabryki.

Fabryka umozliwia wczytanie dowolnych obiektow danego typu za pomoca klucza.
Kazda z fabryk dostepnych w bibliotece powinna miec zadeklarowany zestaw
obiektow dostepnych dla uzytkownika.

Rozbudowa Fabryki
=================

W celu rozbudowy wybranej fabryki o dodatkowe opcje nalezy w pliku
I{settings.py} odpowiednim dla danego projektu dodac opcje C{AJANGO_FACTORY}.
Opcja ta ma przyjmowac slownik w ktorym kluczami sa opisy obiektow zdefiniowane
w przez funkcje L{set_items() <ajango.core.factory.FactoryBase.set_items>}.
Wartosci stanowia slowniki z opisem obiektow ktore moga byc pobierane przez
fabryke.

W ramach tych obiektow nalezy zadeklarowac jako klucz nazwe po ktorej fabryka
wybierze obiekt, a jako wartosc nazwe modulu w ktorym wystepuje dany obiekt.

Przyklad dodania wywolania obiektu do fabryki o nazwie Site::

    AJANGO_FACTORY = {
        'Site' : {'panel' : 'example.sites.panel'},
    }
"""

import importlib
from django.core.management.base  import CommandError
from django.core.exceptions       import ImproperlyConfigured
from django.utils.termcolors      import make_style
from django.core.management.color import supports_color
from django.conf                  import settings
from abc                          import ABCMeta

class FactoryBase(object):
    """ Klasa bazowa tworzaca fabryke. """
    __metaclass__ = ABCMeta
    def __init__(self, param=None):
        self.class_name = ''
        self.base_address = {}
        self.object = param
        self.str = None
        self.init()
    def init(self):
        """ 
        Metoda inicjalizujaca.

        @param self: Obiekt fabryki
        """
        pass
    def execution(self, fun):
        """
        Wykonanie zadan obiektu.

        @param self: Obiekt fabryki
        @param fun: Funkcja inicjalizujaca obiekt utworzony przez fabryke
        """
        return fun(self.object)
    def _get_base_address(self):
        """
        Pobierz tabele z klasami inicjalizujacymi.

        @param self: Obiekt fabryki
        """
        return self.base_address
    def _create_object(self, key):
        """
        Tworzenie obiektu.

        @param self: Obiekt fabryki
        @param key: Klucz obiektu
        @type key: str
        """
        obj = "unKnown"
        try:
            base_address = self._get_base_address()
            obj = base_address[key]
            module = importlib.import_module(obj)
            fun = getattr(module, self.class_name)
            return self.execution(fun)
        except KeyError:
            raise CommandError("Doesn't know %s type: %r" %
                               (self.class_name, key))
        except ImportError:
            raise CommandError("Module %r doesn't exist" % obj)
    def get_class_factory(self, key):
        """
        Pobranie obiektu na podstawie klucza.

        @param self: Obiekt fabryki
        @param key: Klucz obiektu
        @type key: str
        """
        if supports_color():
            blue = make_style(fg='cyan')
        else:
            blue = lambda text: text
        print("Create '" + blue(key) + "' from '" +
              blue(type(self).__name__) + "'")
        return self._create_object(key)
    def get_from_params(self):
        """
        Pobranie obiektu na podstawie danych fabryki.

        @param self: Obiekt fabryki
        """
        if supports_color():
            blue = make_style(fg='cyan')
        else:
            blue = lambda text: text
        print("Create '" + blue(self.str) + "' from '" +
              blue(type(self).__name__) + "'")
        return self._create_object(self.str)
    def __add_modules(self, modules):
        """
        Dodanie nowego modulu w fabryce.

        @param self: Obiekt fabryki

        @param modules: Zestaw obiektow dostepnych w fabryce
        @type modules: Slownik w ktorym B{klucz} jest kluczem dla fabryki,
            a B{wartosc} jest adresem modulu w ktorym znajduje sie obiekt.
        """
        for elem in modules.keys():
            if elem in self.base_address:
                raise CommandError("Cannot rewrite %r key" % elem)
            self.base_address[elem] = modules[elem]
    def __set_class_name(self, class_name):
        """
        Ustawienie nazwy klasy obiektu dostepnego dla fabryki w module.

        Metoda wprowadza nazwe obiektu i probuje wczytac dane poczatkowe z
        pliku settingsow.

        @param self: Obiekt fabryki
        self.class_name = class_name

        @param class_name: Nazwa klasy znajdujacej sie w pliku modulu
        @type class_name: str
        """
        if self.class_name != "":
            raise CommandError("Cannot update class_name for factory [%r]" %
                               class_name)
        self.class_name = class_name
        self.__read_items_from_settings()
    def set_items(self, class_name, modules):
        """
        Ustwienie opcji fabryki.

        Metoda ta powinna byc wywolana w ramach metody
        L{init(self) <ajango.core.factory.FactoryBase.init>} w klasie
        fabryki. Moze ona byc wywolana jednokrotnie. Ponowne wywolanie moze
        spowodowac nieokreslone bledy.

        @param self: Obiekt fabryki

        @param class_name: Nazwa klasy znajdujacej sie w pliku modulu
        @type class_name: str

        @param modules: Zestaw obiektow dostepnych w fabryce
        @type modules: Slownik w ktorym B{klucz} jest kluczem dla fabryki,
            a B{wartosc} jest adresem modulu w ktorym znajduje sie obiekt.
        """
        self.__set_class_name(class_name)
        self.__add_modules(modules)
    def __read_items_from_settings(self):
        """
        Wczytanie obiektow do fabryki z settingsow.

        Wiecej informacji na temat dodawania obiektow do fabryki w opisie
        modulu L{Factory <ajango.core.factory>}

        @param self: Obiekt fabryki
        """
        try:
            if not self.class_name in settings.AJANGO_FACTORY:
                # fabyrka nie ma zdefiniowanych elementow dodatkowych
                return
            tab = settings.AJANGO_FACTORY[self.class_name]
            self.__add_modules(tab)
        except AttributeError:
            # Brak definicji dla dodatkowych obiektow fabryki
            return
        except ImproperlyConfigured:
            # Plik settings.py nie ma poprawnej konfiguracji
            return
