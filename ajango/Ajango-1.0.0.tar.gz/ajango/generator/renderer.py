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
""" Pakiet generowania plikow jezyka Python. """

import abc

TABULATOR = '    '

class Line(object):
    """ Generowanie linni kodu. """
    def __init__(self, text, tab):
        self.text = text
        self.tab = tab
    def get_text(self):
        """ Pobranie tekstu kodu. """
        return self.text
    def set_tab(self, tab=0):
        """ Ustawienie ilosci tabulacji w linni. """
        self.tab = tab

#pylint: disable=W0612
class BaseRenderer(object):
    """ Klasa bazowa obiektow generujacych kod. """
    __metaclass__ = abc.ABCMeta
    @staticmethod
    def cout(text, tab, enter=True):
        """ Zwraca fragment kodu z odpowiednim odstepem. """
        result = ""
        for i in range(tab):
            result += TABULATOR
        result = result + text
        if enter == True:
            result = result + "\n"
        return result
    @abc.abstractmethod
    def render(self, tab=0):
        """ Renderowanie elementu. """
        raise NotImplementedError()

class DefRenderer(BaseRenderer):
    """ Klasa obiektu renderujacego funkcje. """
    def __init__(self, name, args=''):
        """ Metoda inicjalizujaca. """
        self.name = name
        self.args = args
        self.line = []
    def add_line(self, text, tab=0):
        """ Dodanie linni kodu w funkcji. """
        self.line.append(DefRenderer.cout(text, tab, False))
    def render(self, tab=0):
        """ Renderowanie funkcji. """
        result = DefRenderer.cout("def %s(%s):" % (self.name, self.args), tab)
        i = 0
        for once in self.line:
            result = result + DefRenderer.cout(once, tab + 1)
            i = i + 1
        if i == 0:
            result = result + DefRenderer.cout("pass", tab + 1)
        result = result + "\n"
        return result

class ImportRenderer(BaseRenderer):
    """ Klasa obiektu generujacego importy. """
    def __init__(self):
        self.imports = []
    def add_import(self, imp, from_import=None):
        """ Dodanie pojedynczego importu. """
        if from_import == None:
            self.imports.append("import %s" % imp)
        else:
            self.imports.append("from %s import %s" % (from_import, imp))
    def render(self, tab=0):
        """ Renderowanie importow. """
        result = ''
        imp = set(self.imports)
        for once in imp:
            result = result + self.cout(once, tab)
        return result
