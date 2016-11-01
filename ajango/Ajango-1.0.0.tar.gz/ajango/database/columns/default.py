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
""" Modul domyslnej kolumny. """

from ajango.database.columns import ColumnBase

class Column(ColumnBase):
    """ Klasa domyslnej kolumny. """
    def __init__(self, xmldoc, param=None):
        self.presentation = []
        ColumnBase.__init__(self, xmldoc, param)
    def pre_init(self):
        """ Czynnosci do wykonania przed inicjalizacja. """
        self.type = 'default'
        self.add_permited(["PRESENTATION"])
    def read_from_dict(self, params):
        """ Inicjalizacja ze zmiennej slownikowej. """
        ColumnBase.read_from_dict(self, params)
        try:
            self.presentation = self.object['presentation']
        except KeyError:
            self.presentation = []
    def check(self, name, xmldoc_elem):
        """ Oczytanie nodow wewnetrznych. """
        if name == 'PRESENTATION':
            presentation_type = xmldoc_elem.getAttribute('type')
            self.presentation.append(presentation_type)
    def execute(self, view, view_name="view"):
        """ Wykonanie czynnosci kolumny. """
        if len(self.presentation) > 0:
            view.add_import("presentation_factory",
                            "ajango.site.presentations")
            view.add_line("p = []")
            for elem in self.presentation:
                view.add_line("p.append(presentation_factory(%r))" % elem)
            view.add_line("%s.add_column({'type' : 'default', "
                          "'label' : %r, "
                          "'tag' : %r, "
                          "'presentation' : p })" %
                          (view_name, self.label, self.tag))
        else:
            view.add_line("%s.add_column({'type' : 'default', "
                          "'label' : %r, "
                          "'tag' : %r })" %
                          (view_name, self.label, self.tag))
    def get_data(self, value=None):
        """ Pobranie danych dla szablonu. """
        self.prepare_data()
        result = value['result']
        data = dict(self.data)
        value = result.get_element(self.data['tag'])
        for pres in self.presentation:
            value = pres.get(value)
        data['value'] = value
        return data
