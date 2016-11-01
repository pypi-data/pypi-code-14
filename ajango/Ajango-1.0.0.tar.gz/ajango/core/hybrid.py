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
Modul z klasa abstrakcyjna dla obiektow ktore moga byc inicjalizowane zarowno
przez dane XML jak i przez zmienna slowinkowa.
"""

from django.core.management.base  import CommandError
from ajango.core.XMLReader        import XMLReader
from xml.dom                      import minidom
import abc

def get_str_object_factory(obj, default='default'):
    """ Zwraca okreslenie typu obiektu w postaci napisu. """
    if isinstance(obj.object, minidom.Element):
        obj.str = obj.object.getAttribute('type')
        if obj.str == "":
            obj.str = default
        obj.param = obj.object.getAttribute('param')
    else:
        try:
            obj.str = obj.object['type']
        except KeyError:
            raise CommandError("Input element is invalid")

class Hybrid(XMLReader):
    """ Klasa . """
    __metaclass__ = abc.ABCMeta
    def __init__(self, param):
        self.object = param
        if self.is_read_from_xmldoc():
            XMLReader.__init__(self, param, param)
        else:
            self.read_from_dict(param)
    def init(self):
        """ Inicjalizacja obiektu. """
        self.read_from_xml(self.object)
    @abc.abstractmethod
    def read_from_xml(self, xmldoc):
        """ Inicjalizacja z danych XML. """
        raise NotImplementedError()
    @abc.abstractmethod
    def read_from_dict(self, param):
        """ Inicjalizacja ze zmiennej slownikowej. """
        raise NotImplementedError()
    def is_read_from_xmldoc(self):
        """ Sparwdzanie czy obiekt jest odczytany z XML'a. """
        return isinstance(self.object, minidom.Element)
