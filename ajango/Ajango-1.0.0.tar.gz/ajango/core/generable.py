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
""" Obiekt bazowy dla elementow potrafiacych generowac kod samego siebie. """

import abc

#pylint: disable=R0903
class Generable(object):
    """ Klasa bazowa tworzaca fabryke. """
    __metaclass__ = abc.ABCMeta
    @abc.abstractmethod
    def execute(self, view, view_name="view"):
        """
        Wykonanie elementow obiektu.

        Obiekt generuje kod na podstawie wybranej klasy. Metoda ta ma za zadanie
        Przetworzyc elementy obiektu i wywolac odpowiednie metody generujace
        wynikowy kod.

        @param self: Obiekt bazowy
        @param view: Widok generujacy
        @type view: BaseView
        @param view_name: Nazwa obiektu w wygenerowanym kodzie        
        """
        raise NotImplementedError()
