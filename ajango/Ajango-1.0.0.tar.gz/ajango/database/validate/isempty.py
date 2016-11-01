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
Obiekt sprawdzajacy czy pole jest puste.

Sprawdzenie czy pole jest wypelnione dowolnymi znakami. Znaki biale rowniez
pozwalaja na prawidlowe wprowadzenie danych do bazy. Tylko pusty napis jest
rozpoznany jako blad.

Dostepne znaczniki
==================

Obiekt nie przybiera zadnych parametrow z wyjatkiem pola typu.
"""

from ajango.database.validate import ValidateBase

class Validate(ValidateBase):
    """ Klasa sprawdzajace czy pole jest puste. """
    def pre_init(self):
        """ Czynnosci przed inicjalizacja. """
        self.type = 'isempty'
    def is_valid(self, text):
        """ Sprawdza czy pola wejsciowe sa poprawnie wypelnione. """
        if text == None or text == "":
            self.messages.append("Value %r cannot be empty" % self.type)
            return False
        return True
        