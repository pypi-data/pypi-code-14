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
Modul zarzadzania stronami.

Modul posiada mechanizmy do wyswietlania stron zgodnych z okreslonymi danymi.

Dostepne strony
===============

System pozwala na obsluge nastepujacych L{stron<ajango.site.sites>}.

    - L{pusta strona <ajango.site.sites.empty>}
    - L{strona wprowadzania danych <ajango.site.sites.input>}
    - L{strona wyswietlajaca <ajango.site.sites.display>}
    - L{lista danych <ajango.site.sites.list>}
    - L{strona z mozliwoscia edycji <ajango.site.sites.editable>} (niedostepne)
    - L{strona wyswietlania raportu <ajango.site.sites.raport>}
    - L{agregacja stron <ajango.site.sites.container>}

W celu zapoznania sie z metoda generowania stron w pliku szkieletowym
zajrzyj do L{ajango.generator.views}.
"""

from django.utils.datastructures import MultiValueDictKeyError
from ajango.core.factory         import FactoryBase
from django.core.management.base import CommandError
from django.shortcuts            import render
from abc                         import ABCMeta, abstractmethod
import ajango

class SiteFactoryObject(FactoryBase):
    """ Obiekt fabryki stron. """
    def init(self):
        """ Metoda inicjalizujaca. """
        self.set_items('Site', {
            'empty'     : 'ajango.site.sites.empty',
            'input'     : 'ajango.site.sites.input',
            'list'      : 'ajango.site.sites.list',
            'display'   : 'ajango.site.sites.display',
            'editable'  : 'ajango.site.sites.editable',
            'raport'    : 'ajango.site.sites.raport',
            'container' : 'ajango.site.sites.container'
        })

def site_factory(key, param):
    """ Fabryka stron. """
    return SiteFactoryObject(param).get_class_factory(key)

#pylint: disable=R0902
class SiteBase(object):
    """ Abstrakcyjna klasa obslugujaca strone. """
    __metaclass__ = ABCMeta
    global_view_id_counter = 0
    def __init__(self, ob):
        self.view_id = self.global_view_id_counter
        self.global_view_id_counter = self.global_view_id_counter + 1
        self.request = ob['request']
        self.theme = 'default'
        self.header = ""
        self.type = 'empty' # default type for layout
        self.init()
        self.layout = 'ajango_layout.html'
        self.include = 'ajango_%s.html' % self.type
        self.data = dict()
        self.data['appName'] = ob['appName']
        self.data['viewName'] = ob['viewName']
        self.data['menu'] = []
    def set_view_id(self, view_id):
        """
        Zmiana id widoku niezbedna przy obsludze wiekszej ilosci widokow.
        """
        self.view_id = view_id
    def set_title(self, text):
        """ Ustaw tytul strony. """
        self.data['title'] = text
    def set_header(self, text):
        """ Ustaw tytul sekcji. """
        self.header = text
    def set_theme(self, theme):
        """
        Ustawienie tematu layoutu.

        Ajango wczytuje pliku html z folderu oznaczonego przez zmienna
        ustawiana w tej funkcji. System pobiera pliki o nazwach okreslonych
        na podstawie dokumentacji, ale mozna je umiescic
        w pakietach o nazwach podanych w zmiennej.
        """
        self.theme = theme
    @abstractmethod
    def init(self):
        """ Metoda inicjalizujaca. """
        raise NotImplementedError()
    def set_include(self, text):
        """ Ustawienie glownego pliku ze strona odpowiedniego dla strony. """
        self.include = text
    def set_layout(self, html):
        """ Ustawienie pliku layoutu. """
        self.layout = html
    @abstractmethod
    def content(self):
        """ Ustawienie zmiennych dostarczanych do szblonow. """
        raise NotImplementedError()
    def make_content(self):
        """ Metoda wywolywana przez zewnetrzny interface. """
        if self.header != "":
            self.data['header'] = self.header
        self.data['include_view'] = self.theme + '/' + self.include
        self.data['view_id'] = self.view_id
        self.content()
    def make_content_and_get_data(self):
        """
        Buduje dane kontentu i zwraca informacje na temat danych
        utworzonych przez strone.
        """
        self.make_content()
        return self.data
    def make_site(self):
        """
        Wywolaj renderowanie strony.

        Zwraca informacje jakie powinny byc tworzone w plikach view.py
        frameworku Django.
        """
        self.make_content()
        return render(self.request, self.theme + '/' + self.layout,
                      {'data_site' : self.data})
    def set_menu(self, tab):
        """ Ustawienie menu. """
        self.data['menu'] = tab

class GetSite(object):
    """ Klasa strony odczytujacej dane za pomoca metody post i get. """
    __metaclass__ = ABCMeta
    @abstractmethod
    def get_request(self):
        """ Zwraca obiekt request. """
        raise NotImplementedError()
    def get_id(self):
        """ Zwraca id rekordu ktory wyswietla. """
        try:
            request = self.get_request()
            identity = int(request.GET['id'])
        except MultiValueDictKeyError:
            identity = -1
        except ValueError:
            return -1
        return identity
