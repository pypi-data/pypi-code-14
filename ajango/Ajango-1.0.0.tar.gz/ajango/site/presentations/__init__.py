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
Modul zarzadzajacy obiektami wyswietlajacymi.

Pozwala na edytowanie danych wedlug okreslonych warunkow przed wyswietleniem
na ekranie.

Dostepne parametry
==================

    - I{type} - Typ widoku do stworzenia

Dostepne obiekty
================

    - L{powiekszanie liter <ajango.site.presentations.upper>}
"""

from django.core.management.base import CommandError
from ajango.core.factory         import FactoryBase
from ajango.generator.renderer   import DefRenderer
from abc                         import ABCMeta, abstractmethod

class PresentationFactoryObject(FactoryBase):
    """ Obiekt fabryki wyswietlajacej. """
    def init(self):
        """ Metoda inicjalizujaca. """
        self.set_items('Presentation', {
            'upper'    : 'ajango.site.presentations.upper',
        })
    def execution(self, fun):
        """ Wykonanie zadan fabryki. """
        return fun()

def presentation_factory(key):
    """ Fabryka obiektow wyswietlajacych. """
    return PresentationFactoryObject().get_class_factory(key)

class PresentationBase(object):
    """ Abstrakcyjna klasa obiektu wyswietlajacego. """
    __metaclass__ = ABCMeta
    def __init__(self):
        self.init()
    def init(self):
        """ Inicjalizacja obiektu. """
        pass
    @abstractmethod
    def get(self, text):
        """ Przetworzenie napisu. """
        return text
