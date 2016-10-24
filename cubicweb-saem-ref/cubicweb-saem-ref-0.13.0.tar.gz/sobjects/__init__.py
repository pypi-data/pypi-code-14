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
"""cubicweb-saem-ref server objects"""

from itertools import imap

from cubicweb.predicates import match_user_groups
from cubicweb.server import Service

from cubes.eac import sobjects as eac

from .. import user_has_naa


class EACImportService(eac.EACImportService):
    """Service to import an AuthorityRecord from an EAC XML file - overriden from the EAC cube to adapt
    selector and automatically set ark_naa / authority relations.
    """

    __select__ = eac.EACImportService.__select__ & user_has_naa()

    def call(self, stream, import_log, naa=None, **kwargs):
        authority = self._cw.user.authority[0]
        if naa is None:
            naa = authority.ark_naa[0]
        self._authority = authority
        self._naa = naa
        return super(EACImportService, self).call(stream, import_log, **kwargs)

    def external_entities_stream(self, extentities, extid2eid):
        extentities = super(EACImportService, self).external_entities_stream(extentities, extid2eid)

        extid2eid[self._naa.cwuri] = self._naa.eid
        extid2eid[self._authority.cwuri] = self._authority.eid

        def set_authority_or_naa(extentity):
            """insert function to set parent authority in the ext-entities stream"""
            if extentity.etype == 'AuthorityRecord':
                extentity.values['ark_naa'] = set([self._naa.cwuri])
            elif extentity.etype == 'Agent':
                extentity.values['authority'] = set([self._authority.cwuri])
            return extentity

        return imap(set_authority_or_naa, extentities)


class AllocateArk(Service):
    """Service to allocate an ark identifier given an
    ArkNameAssigningAuthority entity.
    """
    __regid__ = 'saem_ref.attribute-ark'
    __select__ = match_user_groups('managers', 'users')

    def call(self, naa):
        generator = self._cw.vreg['adapters'].select('IARKGenerator', self._cw,
                                                     naa_what=naa.what)
        return generator.generate_ark()


def registration_callback(vreg):
    vreg.register_all(globals().values(), __name__, [EACImportService])
    vreg.register_and_replace(EACImportService, eac.EACImportService)
