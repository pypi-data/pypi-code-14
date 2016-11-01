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
Modul strony wyswietlajacej napisy.

Obiekt obsluguje strone wyswietlajaca dowolne elemeny.

Obiekt Generujacy
=================

L{ajango.generator.views.empty}
"""

from __future__        import print_function
from ajango.site.sites import SiteBase

class Site(SiteBase):
    """ Klasa strony wyswietlajacej napisy. """
    def __init__(self, ob):
        self.echo = []
        SiteBase.__init__(self, ob)
    def init(self):
        """ Metoda inicjalizujaca. """
        self.type = 'empty'
        self.echo = []
    def add_echo(self, text):
        """ Dodanie napisu do wyswietlenia. """
        self.echo.append(text)
    def content(self):
        """ Buduje dane dla strony. """
        elements = []
        print(self.echo)
        for elem in self.echo:
            elements.append(elem)
        self.data['echo'] = elements
