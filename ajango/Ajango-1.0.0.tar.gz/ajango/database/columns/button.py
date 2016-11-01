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
""" Modul kolumny z przyciskiem. """

from ajango.database.columns import ColumnBase

class Column(ColumnBase):
    """ Klasa kolumny z przyciskiem. """
    def __init__(self, xmldoc, param=None):
        self.view = None
        self.value = None
        ColumnBase.__init__(self, xmldoc, param)
    def pre_init(self):
        """ Czynnosci do wykonania przed inicjalizacja. """
        self.type = 'button'
    def read_from_xml(self, xmldoc):
        """ Inicjalizacja z danych XML. """
        ColumnBase.read_from_xml(self, xmldoc)
        self.view = self.getAttribute('view')
        self.value = self.getAttribute('value')
    def read_from_dict(self, params):
        """ Inicjalizacja ze zmiennej slownikowej. """
        ColumnBase.read_from_dict(self, params)
        self.view = self.object['view']
    def execute(self, view, view_name='view'):
        """ Wykonanie czynnosci kolumny. """
        view.add_line("%s.add_column({'type' : 'button', "
                      "'label' : %r, "
                      "'tag' : %r, "
                      "'view' : %r})" %
                      (view_name, self.label, self.tag, self.view))
    def prepare_data(self):
        """ Przygotowanie danych. """
        ColumnBase.prepare_data(self)
        self.data['view'] = self.view
    def get_data(self, value=None):
        """ Pobranie danych dla szablonu. """
        self.prepare_data()
        result = value['result']
        data = dict(self.data)
        data['id'] = result.get_element('id')
        data['type'] = self.type
        return data
