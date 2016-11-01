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
Obiekt sprawdzajacy czy pole ma wartosc mniejsza od podanej w parametrze.

Dostepne znaczniki
==================

    - I{param} - Liczba z ktora porownywane jest pole.
"""

from django.core.management.base import CommandError
from ajango.database.validate import ValidateBase

class Validate(ValidateBase):
    """
    Klasa sprawdzajace czy pole ma wartosc mniejsza od podanej w parametrze.
    """
    def __init__(self, param):
        self.number = 0
        ValidateBase.__init__(self, param)
    def pre_init(self):
        """ Czynnosci przed inicjalizacja. """
        self.type = 'lt'
    def post_init(self):
        """ Czynnosci po inicjalizacji. """
        try:
            self.number = int(self.get_param())
        except ValueError:
            raise CommandError("Param value %r is not number." %
                               self.get_param())
    def is_valid(self, text):
        """ Sprawdza czy pola wejsciowe sa poprawnie wypelnione. """
        try:
            number_value = int(text)
        except ValueError:
            self.messages.append("Value must be a number.")
            return False
        if number_value >= self.number:
            self.messages.append("Value %r must be less then %r" %
                                 (number_value, self.number))
            return False
        return True
        