#  coding: utf-8
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
"""cubicweb-saem-ref entity's classes and adapters for SEDA classes"""

from cubicweb.predicates import is_instance, is_in_state

from cubes.compound.entities import IClonableAdapter
from cubes.oaipmh import MetadataFormat
from cubes.oaipmh.entities import OAISetSpec
from cubes.seda.entities.custom import SEDAArchiveTransfer
from cubes.seda.entities.profile_generation import SEDA1XSDExport
from cubes.seda.views import export

from cubes.saem_ref import cwuri_url
from cubes.saem_ref.entities import oai


SEDA1XSDExport.cwuri_url = cwuri_url


class SEDAArchiveTransferIClonableAdapter(IClonableAdapter):
    """Cloning adapter for SEDA profiles."""
    __select__ = IClonableAdapter.__select__ & is_in_state('published')
    rtype = 'new_version_of'
    skiprtypes = ()


class SEDAArchiveTransfer(SEDAArchiveTransfer):
    SEDAArchiveTransfer.fetch_attrs.append('ark')

    def __getstate__(self):
        # Exclude ark from copy to have so that it can be generated for the clone
        odict = self.__dict__.copy()
        odict['cw_attr_cache'].pop('ark', None)
        return odict

    @property
    def predecessor(self):
        """The predecessor of the current profile, that is the one that has been replaced by it"""
        predecessors = self.new_version_of
        if predecessors:
            return predecessors[0]
        return None

    @property
    def successor(self):
        """The successor of the current profile, that is the one that has replaced it"""
        successors = self.reverse_new_version_of
        if successors:
            return successors[0]
        return None


class TransferringAgentOAISetSpec(OAISetSpec):
    """OAI-PMH set specifier to match SEDAArchiveTransfer related to a transferring
    agent.
    """

    def setspecs(self, cnx):
        rset = cnx.execute(
            'Any A WHERE X archival_role R, R name "deposit", X ark A')
        desc = 'SEDA Profile used by organization {0}'
        for value, in rset.rows:
            yield value, desc.format(value)

    def setspec_restrictions(self, value):
        qs = ('A use_profile X, A archival_role R'
              ', R name "deposit", A ark %(value)s'
              ', X in_state ST, NOT ST name "draft"')
        return qs, {'value': value}


PROFILE_METADATA_FORMATS = {
    'seda02xsd': (
        MetadataFormat(
            # XXX Shouldn't be a ZIP...
            schema='http://www.archivesdefrance.culture.gouv.fr/seda/seda_v0-2.zip',
            namespace='fr:gouv:ae:archive:draft:standard_echange_v0.2'),
        'saem_ref.oai.seda.0.2-xsd',
    ),
    'seda02rng': (
        MetadataFormat(
            schema='http://www.archivesdefrance.culture.gouv.fr/seda/seda_v0-2.zip',
            namespace='fr:gouv:ae:archive:draft:standard_echange_v0.2'),
        'saem_ref.oai.seda.0.2-rng',
    ),
    'seda1rng': (
        MetadataFormat(
            schema='http://www.archivesdefrance.culture.gouv.fr/seda/seda_v1-0.zip',
            namespace='fr:gouv:culture:archivesdefrance:seda:v1.0'),
        'saem_ref.oai.seda.1.0-rng',
    ),
    'seda2rng': (
        MetadataFormat(
            schema='http://www.archivesdefrance.culture.gouv.fr/seda/seda_v2-0.zip',
            namespace='fr:gouv:culture:archivesdefrance:seda:v2.0'),
        'saem_ref.oai.seda.2.0-rng',
    ),
}


class SEDAArchiveTransferOAIPMHRecordAdapter(oai.OAIPMHActiveRecordAdapter):
    """OAI-PMH adapter for SEDAArchiveTransfer entity type."""
    __select__ = oai.OAIPMHActiveRecordAdapter.__select__ & is_instance('SEDAArchiveTransfer')
    metadata_formats = PROFILE_METADATA_FORMATS.copy()

    @classmethod
    def set_definition(cls):
        specifier = oai.PublicETypeOAISetSpec(
            'SEDAArchiveTransfer', cls.identifier_attribute, 'profile')
        specifier['transferring_agent'] = TransferringAgentOAISetSpec()
        return specifier


class DeletedSEDAArchiveTransferOAIPMHRecordAdapter(oai.OAIPMHDeletedRecordAdapter):
    """OAI-PMH adapter for deleted SEDAArchiveTransfer."""
    __select__ = oai.OAIPMHDeletedRecordAdapter.__select__ & is_instance('SEDAArchiveTransfer')
    metadata_formats = PROFILE_METADATA_FORMATS.copy()


class OAISEDAExportView(export.SEDAExportView):
    __abstract__ = True

    def call(self):
        version, format = self.__regid__.replace('saem_ref.oai.seda.', '').split('-')
        self._cw.view('seda.export', rset=self.cw_rset, version=version, format=format, w=self.w)


class OAISEDA02XSDExportView(OAISEDAExportView):
    __regid__ = 'saem_ref.oai.seda.0.2-xsd'


class OAISEDA02RNGExportView(OAISEDAExportView):
    __regid__ = 'saem_ref.oai.seda.0.2-rng'


class OAISEDA1RNGExportView(OAISEDAExportView):
    __regid__ = 'saem_ref.oai.seda.1.0-rng'


class OAISEDA2RNGExportView(OAISEDAExportView):
    __regid__ = 'saem_ref.oai.seda.2.0-rng'
