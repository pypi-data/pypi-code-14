
# copyright 2016 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of CubicWeb SearchUi.
#
# CubicWeb is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# CubicWeb is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with CubicWeb.  If not, see <http://www.gnu.org/licenses/>.

from cubicweb.web.views.boxes import SearchBox
from cubicweb.web.views.json import JsonEntityView, JsonMixIn
from cubicweb.view import View
from cubicweb import schema

class SearchUiSearchBox(SearchBox):
    def render_body(self, w):
        self._cw.add_js("cubes.searchui.bundle.js")
        self._cw.add_css("cubes.searchui.bundle.css")
        w(u"<div id='cwsearch' data-baseURL='%s'></div>" % self._cw.base_url())


class EjsonExportDCview(JsonEntityView):
    """Display the entity ejson view with the dc attributes"""
    __regid__ = 'ejson_dc'

    def call(self):
        entities = []
        for entity in self.cw_rset.entities():
            serializer = entity.cw_adapt_to('ISerializable')
            data = serializer.serialize()
            data["dc_title"] = entity.dc_title()
            entities.append(data)
        self.wdata(entities)


IGNORE = set()
IGNORE.update(schema.SCHEMA_TYPES)
IGNORE.update(schema.WORKFLOW_TYPES)
IGNORE.update(schema.INTERNAL_TYPES)
IGNORE.update(schema.UNIQUE_CONSTRAINTS)
IGNORE.update(['CWGroup', 'CWUser', 'Bookmark'])

class SearchBoxConfigView(JsonMixIn, View):
    __regid__ = "searchboxconfig"

    def call(self):
        data = {}
        data["user"] = self._cw.user.cw_adapt_to('ISerializable').serialize()
        data["ignore"] = sorted(IGNORE)
        rql="Any X ORDERBY N WHERE X is_instance_of CWEType, X final False, X name N, NOT X name IN( %s ), NOT X name LIKE 'CW%%'"%','.join('"%s"'%item for item in IGNORE)
        rset = self._cw.execute(rql)
        data["entities"] = list(item.cw_adapt_to('ISerializable').serialize() for item in rset.entities())

        self.wdata(data)

def registration_callback(vreg):
    vreg.register_and_replace(SearchUiSearchBox, SearchBox)
    vreg.register(EjsonExportDCview)
    vreg.register(SearchBoxConfigView)
