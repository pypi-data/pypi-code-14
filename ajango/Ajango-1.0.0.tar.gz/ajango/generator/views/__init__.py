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
Modul generowania widokow.

Modul posiada mechanizmy umozliwiajace wygenerowanie kodu do wywolania widokow
stron dostepnych za pomoca platfromy L{ajango}.

Dostepne parametry
==================

    - I{type} - Typ widoku do stworzenia.
    - I{id} - Unikatowy indentyfikator strony.
    - I{main} - (opcja) Przyjmuje wartosc I{main}. Zaznaczenie jako widoku
                glownego.

Dostepne widoki
===============

System pozwala na wygenerowanie nastepujacych
L{widokow<ajango.generator.views>}.

    - L{widok pusty <ajango.generator.views.empty>}
    - L{widok wprowadzania danych <ajango.generator.views.input>}
    - L{widok wyswietlania danych <ajango.generator.views.display>}
    - L{widok listy <ajango.generator.views.list>}
    - L{widok edycji danych <ajango.generator.views.editable>}
    - L{widok raportu <ajango.generator.views.raport>}
    - L{agregacja widoku <ajango.generator.views.container>}

W celu zapoznania sie z modulem obslugujacym strony w wygenerowanej aplikacji
zajzyj do L{ajango.site.sites}
"""

from xml.dom                     import minidom
from ajango.core.factory         import FactoryBase
from ajango.core.XMLReader       import XMLReader
from ajango.generator.renderer   import DefRenderer
from ajango.core.generable       import Generable
from django.core.management.base import CommandError
import abc

class ViewFactoryObject(FactoryBase):
    """ Klasa obiektu fabryki generatorow widoku. """
    def init(self):
        """ Metoda inicjalizacyjna. """
        self.set_items('View', {
            'empty'     : 'ajango.generator.views.empty',
            'input'     : 'ajango.generator.views.input',
            'list'      : 'ajango.generator.views.list',
            'display'   : 'ajango.generator.views.display',
            'editable'  : 'ajango.generator.views.editable',
            'raport'    : 'ajango.generator.views.raport',
            'container' : 'ajango.generator.views.container',
        })
        if self.object['xmldoc'].tagName.upper() != 'VIEW':
            raise CommandError("Cannot create application from %r" %
                               self.object['xmldoc'].tagName)
        self.str = self.object['xmldoc'].getAttribute('type').lower()
    def execution(self, fun):
        """ Wykonanie zadan obiektu. """
        return fun(self.object['xmldoc'],
                   self.object['imp_renderer'],
                   self.object['app'])

def view_factory(param):
    """ Fabryka generatorow widoku. """
    return ViewFactoryObject(param).get_from_params()

#pylint: disable=R0902
class ViewBase(XMLReader, Generable):
    """ Klasa abstrakcyjna generatora widokow. """
    __metaclass__ = abc.ABCMeta
    DEFAULT_APP_TITLE = "My new Application"
    def __init__(self, xmldoc, importRenderer, app):
        self.name = xmldoc.getAttribute('id').lower()
        if self.name == '':
            self.name = 'index'
        self.app = app
        self.code = ""
        self.type = ""
        self.title = self.DEFAULT_APP_TITLE
        self.header = ""
        if isinstance(importRenderer, dict):
            self.renderer = importRenderer
        else:
            self.renderer = {}
            self.renderer['code'] = DefRenderer(self.name, 'request')
            self.renderer['import'] = importRenderer
        self.xml_name = "VIEW"
        self.add_permited(["TITLE", "HEADER"])
        XMLReader.__init__(self, xmldoc)
    def check(self, name, xmldoc_elem):
        """ Oczytanie nodow wewnetrznych. """
        if name == 'TITLE':
            self.title = xmldoc_elem.getAttribute('value')
            return True
        elif name == 'HEADER':
            self.header = xmldoc_elem.getAttribute('value')
            return True
        return False
    def get_renderer(self, key):
        """ Pobranie renderera. """
        return self.renderer.get(key)
    def get_title(self):
        """ Pobranie tytulu. """
        if self.title == "" or self.title == self.DEFAULT_APP_TITLE:
            return self.name
        return self.title
    def add_line(self, text, tab=0):
        """ Dadanie polecenia do kodu vidoku"""
        self.renderer['code'].add_line(text, tab)
    def add_import(self, imp, from_elem=None):
        """Dodanie importu do biblioteki"""
        self.renderer['import'].add_import(imp, from_elem)
    def get_name(self):
        """ Pobranie nazwy. """
        return self.name
    def make_view_execute(self, view_name="view"):
        """ Budowanie widoku w funkcjach wewnetrzych. """
        if self.type == "":
            raise CommandError("This view must have set type")
        self.add_import("site_factory", "ajango.site.sites")
        self.add_line("%s = site_factory(%r, {'request' : request,"
                      "'appName' : %r, 'viewName' : %r})" %
                      (view_name, self.type, self.app.get_name(), self.name))
        self.execute(None, view_name)
    def make_execute(self, view_name="view"):
        """ Budowanie kodu, funkcja eksportowana na zewnatrz. """
        self.make_view_execute(view_name)
        self.add_line("%s.set_title(%r)" % (view_name, self.title))
        if self.header != "":
            self.add_line("%s.set_header(%r)" % (view_name, self.header))
        self.add_line("%s.set_menu(default_menu())" % view_name)
        self.add_line("return %s.make_site()" % view_name)
    @abc.abstractmethod
    def execute(self, view, view_name="view"):
        """ Wykonanie zadan obiektu. """
        raise NotImplementedError()
    def __str__(self):
        return self.get_name()
    #pylint: disable=R0201
    def is_display_in_menu(self):
        """ Informacja na temat widocznosci w menu glownym aplikacji. """
        return False
