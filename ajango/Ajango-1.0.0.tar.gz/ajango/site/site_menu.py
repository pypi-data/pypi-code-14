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
""" Klasa budowania menu strony. """

class MenuData(object):
    """ Pole menu. """
    def __init__(self, url, name):
        self.url = url
        self.name = name
    def get_url(self):
        """ Pobranie adresu url pola menu. """
        return self.url
    def get_name(self):
        """ Pobranie nazwy menusa. """
        return self.name

class SiteMenu(object):
    """ Klasa obslugujaca menu strony. """
    def __init__(self, project_name):
        self.project_name = project_name
        self.tab = []
    def add_view(self, view, title):
        """ Dodanie widoku do menu. """
        data = MenuData("/%s/%s" % (self.project_name, view), title)
        self.tab.append(data)
    def get_tab(self):
        """ Pobranie tablicy z ustawieniami menu. """
        return self.tab
