# copyright 2015-2016 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.
"""cubicweb-saem-ref views for import/export of AuthorityRecord from/to EAC"""

from cubicweb import tags
from cubicweb.web import formfields as ff

from cubes.eac import views as eac

from cubes.saem_ref import user_has_naa


def naa_form_vocabulary(form, field):
    """Field vocabulary function returning the list of available authorities"""
    rset = form._cw.execute('Any XN, X ORDERBY XN WHERE X is ArkNameAssigningAuthority, X who XN')
    return [(name, unicode(eid)) for name, eid in rset]


class EACImportForm(eac.EACImportForm):
    """EAC-CPF import controller - overriden to add an NAA file, necessary to the service."""
    naafield = ff.StringField(name='naa', required=True,
                              choices=naa_form_vocabulary, sort=False)


class EACImportView(eac.EACImportView):
    """EAC-CPF import controller - overriden to provide NAA information to the service."""
    def service_kwargs(self, posted):
        """Subclass access point to provide extra arguments to the service (e.g. saem_ref cube).
        """
        return {'naa': self._cw.cnx.entity_from_eid(posted['naa'])}


class EACImportViewNoNaa(eac.EACImportView):
    __select__ = eac.EACImportView.__select__ & ~user_has_naa()

    def call(self):
        self.w(tags.h1(self._cw.__('Importing an AuthorityRecord from a EAC-CPF file')))
        if not self._cw.user.authority:
            msg = self._cw._("You must <a href='{0}'>be in an organization</a> to access "
                             "this functionnality.")
            url = self._cw.user.absolute_url(vid='edition')
        else:
            msg = self._cw._("Your organization must <a href='{0}'>have an NAA configured</a> to "
                             "access this functionnality.")
            url = self._cw.user.authority[0].absolute_url(vid='edition')
        self.w(tags.div(msg.format(url)))


def registration_callback(vreg):
    vreg.register_all(globals().values(), __name__, (EACImportForm, EACImportView))
    vreg.register_and_replace(EACImportForm, eac.EACImportForm)
    vreg.register_and_replace(EACImportView, eac.EACImportView)
