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
Obiekt sprawdzajacy pole regula regex.

Obiekt porownuje wprowadzony tekst z wyrazeniem regularnym podanym w parametrze.

Dostepne znaczniki
==================

    -I{param} - Analizowane wyrazenie regularne.

"""

from ajango.database.validate import ValidateBase
import re

class Validate(ValidateBase):
    """ Klasa sprawdzajace pole regula regex. """
    def pre_init(self):
        """ Czynnosci przed inicjalizacja. """
        self.type = 'regex'
    def is_valid(self, text):
        """ Sprawdza czy pola wejsciowe sa poprawnie wypelnione. """
        rule = self.get_param()
        results = re.findall(rule, text)
        if len(results) <= 0:
            self.messages.append("Value must be match with %r rule." %
                                 rule)
            return False
        return True
        