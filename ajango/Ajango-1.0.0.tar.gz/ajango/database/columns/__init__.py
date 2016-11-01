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
""" Modul zarzadzania kolumnami. """

from django.core.management.base import CommandError
from ajango.core.factory         import FactoryBase
from ajango.core.generable       import Generable
from ajango.core.hybrid          import Hybrid, get_str_object_factory
import abc

class ColumnFactoryObject(FactoryBase):
    """ Klasa obiektu zarzadzajacego kolumnami. """
    def init(self):
        """ Metoda inicjalizujaca. """
        self.set_items('Column', {
            'default'     : 'ajango.database.columns.default',
            'button'      : 'ajango.database.columns.button'
        })
        get_str_object_factory(self)

def column_factory(param):
    """ Fabryka kolumn. """
    return ColumnFactoryObject(param).get_from_params()

class ColumnBase(Hybrid, Generable):
    """ Klasa bazowa obiektu obslugujacego kolumny. """
    __metaclass__ = abc.ABCMeta
    def __init__(self, xmldoc, param=None):
        self.type = "unKnown"
        self.theme = 'default'
        self.has_prepare = False
        self.data = {}
        self.xml_name = "COLUMN"
        self.label = ""
        self.tag = ""
        self.pre_init()
        Hybrid.__init__(self, xmldoc)
        self.post_init()
    def read_from_xml(self, xmldoc):
        """ Inicjalizacja z danych XML. """
        self.label = self.getAttribute('label')
        self.tag = self.getAttribute('tag')
    def read_from_dict(self, params):
        """ Inicjalizacja ze zmiennej slownikowej. """
        try:
            self.label = params['label']
            self.tag = params['tag']
        except KeyError:
            raise CommandError("Input element is invalid")
    def pre_init(self):
        """ Czynnosci do wykonania przed inicjalizacja. """
        pass
    def post_init(self):
        """ Czynnosci do wykonania po inicjalizacji. """
        pass
    def check(self, name, xml_doc_elem):
        """ Oczytanie nodow wewnetrznych. """
        pass
    def prepare_data(self):
        """ Przygotowanie danych. """
        if self.has_prepare:
            return
        self.has_prepare = True
        self.data['tag'] = self.tag
        self.data['label'] = self.label
        self.data['url'] = '%s/ajango_columns/%s.html' % (self.theme, self.type)
    @abc.abstractmethod
    def get_data(self, value=None):
        """ Pobranie danych dla szablonu. """
        raise CommandError("Please implement this method")
    def get_label(self):
        """ Pobranie opisu kolumny. """
        self.prepare_data()
        return self.label
