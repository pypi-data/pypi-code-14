# copyright 2016 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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
"""Miscellaneous test utilities."""


def create_transfer_to_bdo(cnx):
    """Create minimal ArchiveTransfer down to a BinaryDataObject and return the later."""
    create = cnx.create_entity
    transfer = create('SEDAArchiveTransfer', title=u'test profile')
    bdo = create_data_object(transfer)
    # commit and clear cache to allow access to container relation
    cnx.commit()
    bdo.cw_clear_all_caches()
    return bdo


def create_archive_unit(parent, **kwargs):
    cnx = kwargs.pop('cnx', getattr(parent, '_cw', None))
    kwargs.setdefault('id', u'au1')
    au = cnx.create_entity('SEDAArchiveUnit', seda_archive_unit=parent, **kwargs)
    alt = cnx.create_entity('SEDAAltArchiveUnitArchiveUnitRefId',
                            reverse_seda_alt_archive_unit_archive_unit_ref_id=au)
    alt_seq = cnx.create_entity(
        'SEDASeqAltArchiveUnitArchiveUnitRefIdManagement',
        reverse_seda_seq_alt_archive_unit_archive_unit_ref_id_management=alt)
    return au, alt, alt_seq


def create_data_object(transfer, **kwargs):
    cnx = kwargs.pop('cnx', getattr(transfer, '_cw', None))
    create = cnx.create_entity
    kwargs.setdefault('id', u'bdo1')
    bdo = create('SEDABinaryDataObject', seda_binary_data_object=transfer, **kwargs)
    choice = create('SEDAAltBinaryDataObjectAttachment',
                    reverse_seda_alt_binary_data_object_attachment=bdo)
    create('SEDAAttachment', seda_attachment=choice)  # Choice cannot be empty
    return bdo


def map_cs_to_type(scheme, rtype, etype=None):
    cnx = scheme._cw
    cnx.execute('SET CS scheme_relation_type RT WHERE CS eid %(cs)s, RT name %(rt)s',
                {'cs': scheme.eid, 'rt': rtype})
    if etype is not None:
        cnx.execute('SET CS scheme_entity_type ET WHERE CS eid %(cs)s, ET name %(et)s',
                    {'cs': scheme.eid, 'et': etype})


def scheme_for_type(cnx, rtype, etype, *concept_labels):
    scheme = cnx.create_entity('ConceptScheme', title=u'{0}/{1} vocabulary'.format(rtype, etype))
    map_cs_to_type(scheme, rtype, etype)
    for label in concept_labels:
        scheme.add_concept(label)
    return scheme


def scheme_for_rtype(cnx, rtype, *concept_labels):
    return scheme_for_type(cnx, rtype, None, *concept_labels)
