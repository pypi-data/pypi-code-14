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
"""cubicweb-seda unit tests for schema"""

from contextlib import contextmanager

from cubicweb import ValidationError, Unauthorized
from cubicweb.devtools.testlib import CubicWebTC
from cubicweb.schema import ERQLExpression, RRQLExpression

import testutils


class SchemaTC(CubicWebTC):

    def test_code_lists_constraints_simple(self):
        with self.admin_access.client_cnx() as cnx:
            create = cnx.create_entity

            digest_scheme = create('ConceptScheme', title=u'Digest algorithms')
            digest_concept = digest_scheme.add_concept(label=u'md5')
            reply_scheme = create('ConceptScheme', title=u'Reply code algorithms')
            reply_concept = reply_scheme.add_concept(label=u'ok')
            cnx.commit()

            bdo = testutils.create_transfer_to_bdo(cnx)
            bdo.container[0].cw_set(seda_reply_code_list_version=reply_scheme,
                                    seda_message_digest_algorithm_code_list_version=digest_scheme)
            cnx.commit()

            bdo.cw_set(seda_algorithm=reply_concept)
            with self.assertRaises(ValidationError) as cm:
                cnx.commit()
            self.assertIn('seda_algorithm-subject', cm.exception.errors)

            bdo.cw_set(seda_algorithm=digest_concept)
            cnx.commit()

    def test_code_lists_constraints_complex(self):
        with self.admin_access.client_cnx() as cnx:
            create = cnx.create_entity

            mt_scheme = create('ConceptScheme', title=u'mime types')
            mt_concept = mt_scheme.add_concept(label=u'text/plain')
            other_scheme = create('ConceptScheme', title=u'Reply code algorithms')
            other_concept = other_scheme.add_concept(label=u'ok')
            cnx.commit()

            bdo = testutils.create_transfer_to_bdo(cnx)
            create('SEDAMimeTypeCodeListVersion',
                   seda_mime_type_code_list_version_from=bdo.container,
                   seda_mime_type_code_list_version_to=mt_scheme)
            cnx.commit()

            create('SEDAMimeType', seda_mime_type_from=bdo, seda_mime_type_to=other_concept)
            with self.assertRaises(ValidationError) as cm:
                cnx.commit()
            self.assertIn('seda_mime_type_to-subject', cm.exception.errors)

            create('SEDAMimeType', seda_mime_type_from=bdo, seda_mime_type_to=mt_concept)
            cnx.commit()

    def test_component_archive_unit_rule_constraint(self):
        with self.admin_access.client_cnx() as cnx:
            for rule_type in ('access', 'appraisal'):
                etype = 'SEDASeq{0}RuleRule'.format(rule_type.capitalize())
                scheme = testutils.scheme_for_type(cnx, 'seda_rule', etype)
                concept = scheme.add_concept(label=u'whatever')
                cnx.commit()

                unit, unit_alt, unit_alt_seq = testutils.create_archive_unit(None, cnx=cnx)
                rule_rule = cnx.create_entity(etype.format(rule_type.capitalize()),
                                              seda_rule=concept)
                cnx.create_entity('SEDA{0}Rule'.format(rule_type.capitalize()),
                                  **{'seda_{0}_rule'.format(rule_type): unit_alt_seq,
                                     'seda_seq_{0}_rule_rule'.format(rule_type): rule_rule})
                cnx.commit()

    def test_identifier_unicity_constraint(self):
        """Check that an identifier must be unique within a profile."""
        with self.admin_access.client_cnx() as cnx:
            create = cnx.create_entity
            transfer1 = create('SEDAArchiveTransfer', title=u'Profile1')
            # Create an archive unit with an id
            testutils.create_archive_unit(transfer1, id=u'id1')
            cnx.commit()
            # Creating binary data object with same id should fail
            transfer1 = cnx.entity_from_eid(transfer1.eid)
            bdo = create('SEDABinaryDataObject', id=u'id1', seda_binary_data_object=transfer1)
            alt = create('SEDAAltBinaryDataObjectAttachment',
                         reverse_seda_alt_binary_data_object_attachment=bdo)
            create('SEDAUri', seda_uri=alt)
            with self.assertRaises(ValidationError) as cm:
                cnx.commit()
            self.assertIn('identifier must be unique within a profile',
                          cm.exception.errors.values().pop())
            # Creating an archive unit in another profile with same id works
            transfer2 = create('SEDAArchiveTransfer', title=u'Profile2')
            testutils.create_archive_unit(transfer2, id=u'id1')
            cnx.commit()

    def test_rdef_container_permissions(self):
        """Check that permissions are correctly set on rdefs between entity types contained in
        SEDAArchiveTransfer."""
        for action in ('add', 'delete'):
            # Parent is container
            rdef = self.schema['seda_comment'].rdef('SEDAComment', 'SEDAArchiveTransfer')
            rqlexpr, = [p for p in rdef.permissions[action] if isinstance(p, RRQLExpression)]
            self.assertEqual(rqlexpr.expression, 'U has_update_permission O')
            # Parent is contained in container
            rdef = self.schema['seda_tag'].rdef('SEDATag', 'SEDAContent')
            rqlexpr, = [p for p in rdef.permissions[action] if isinstance(p, RRQLExpression)]
            self.assertEqual(rqlexpr.expression, 'U has_update_permission C, O container C')
            # Parent is subject
            rdef = self.schema['seda_seq_alt_archive_unit_archive_unit_ref_id_management'].rdef(
                'SEDAAltArchiveUnitArchiveUnitRefId',
                'SEDASeqAltArchiveUnitArchiveUnitRefIdManagement')
            rqlexpr, = [p for p in rdef.permissions[action] if isinstance(p, RRQLExpression)]
            self.assertEqual(rqlexpr.expression, 'U has_update_permission C, S container C')

    def test_etype_container_permissions(self):
        """Check that permissions are correctly set on entity types contained in
        SEDAArchiveTransfer."""
        for action in ('update', 'delete'):
            # Parent is container
            etype = self.schema['SEDAComment']
            rqlexpr, = [p for p in etype.permissions[action] if isinstance(p, ERQLExpression)]
            self.assertEqual(rqlexpr.expression, 'U has_{action}_permission C, '
                             'X container C'.format(action=action))

    def test_archive_unit_permissions(self):
        """Check that permissions are correctly set on archive unit that may be either container
        or contained."""
        for action in ('update', 'delete'):
            etype = self.schema['SEDAArchiveUnit']
            rqlexpr1, rqlexpr2 = [p for p in etype.permissions[action]
                                  if isinstance(p, ERQLExpression)]
            self.assertEqual(rqlexpr1.expression,
                             'U has_{action}_permission C, X container C'.format(action=action))
            self.assertEqual(rqlexpr2.expression,
                             'NOT EXISTS(X container C), U in_group G, '
                             'G name IN("managers", "users")')

    def test_rule_default_cardinality(self):
        with self.admin_access.client_cnx() as cnx:
            transfer = cnx.create_entity('SEDAArchiveTransfer', title=u'test profile')
            for rule_type in ('access', 'appraisal'):
                rule_etype = 'SEDA{0}Rule'.format(rule_type.capitalize())
                rule_rtype = 'seda_{0}_rule'.format(rule_type)
                rule = cnx.create_entity(rule_etype, **{rule_rtype: transfer})
                rule_rule_etype = 'SEDASeq{0}RuleRule'.format(rule_type.capitalize())
                rule_rule_rtype = 'reverse_seda_seq_{0}_rule_rule'.format(rule_type)
                rule_rule = cnx.create_entity(rule_rule_etype, **{rule_rule_rtype: rule})
                self.assertEqual(rule_rule.user_cardinality, '1')
                start_date = cnx.create_entity('SEDAStartDate', seda_start_date=rule_rule)
                self.assertEqual(start_date.user_cardinality, '1')

    def test_fti(self):
        # "Reverse" text to be searched in order not to be troubled by other
        # entities that may live in the DB (e.g. Concepts) with similar text.
        with self.admin_access.client_cnx() as cnx:
            transfer = cnx.create_entity('SEDAArchiveTransfer', title=u'Profile')
            unit, unit_alt, unit_alt_seq = testutils.create_archive_unit(transfer)
            content = cnx.create_entity('SEDAContent', seda_content=unit_alt_seq)
            cnx.create_entity('SEDATitle', seda_title=content, title=u'transfer name'[::-1])
            cnx.create_entity('SEDAAccessRule', seda_access_rule=unit_alt_seq,
                              user_annotation=u'some annotation'[::-1])
            testutils.create_data_object(transfer, id=u"bdo1", filename=u'fixed.txt'[::-1])
            cnx.commit()

            for search in ('name', 'annotation', 'fixed'):
                with self.subTest(search=search):
                    rset = cnx.execute('Any X WHERE X has_text %(search)s',
                                       {'search': search[::-1]})
                    self.assertEqual([r for r, in rset.rows], [transfer.eid])


class SecurityTC(CubicWebTC):

    @contextmanager
    def assertUnauthorized(self, cnx):
        with self.assertRaises(Unauthorized) as cm:
            yield cm
            cnx.commit()
        cnx.rollback()

    def test_profile(self):
        with self.admin_access.repo_cnx() as cnx:
            self.create_user(cnx, login='alice')
            self.create_user(cnx, login='bob')
            cnx.commit()
        with self.new_access('alice').repo_cnx() as cnx:
            transfer = cnx.create_entity('SEDAArchiveTransfer', title=u'Alice Profile')
            testutils.create_archive_unit(transfer)
            cnx.create_entity('Agent', name=u'Archival inc.',
                              reverse_seda_archival_agency=transfer)
            cnx.create_entity('SEDAComment', comment=u'Whooot.',
                              seda_comment=transfer)
            scheme = cnx.create_entity('ConceptScheme', title=u'Some vocabulary')
            cnx.create_entity('SEDAMimeTypeCodeListVersion',
                              seda_mime_type_code_list_version_from=transfer,
                              seda_mime_type_code_list_version_to=scheme)
            cnx.commit()
        with self.new_access('bob').repo_cnx() as cnx:
            transfer = cnx.entity_from_eid(transfer.eid)
            # modification of the container
            with self.assertUnauthorized(cnx):
                transfer.cw_set(title=u'Bob Profile')
            # modification of a contained entity
            comment = transfer.reverse_seda_comment[0]
            with self.assertUnauthorized(cnx):
                comment.cw_set(comment=u'You got hacked')
            with self.assertUnauthorized(cnx):
                cnx.create_entity('SEDAComment', seda_comment=transfer)
            # modification of a relation from the container to a non contained entity
            with self.assertUnauthorized(cnx):
                cnx.create_entity('Agent', name=u'Bob Archival inc.',
                                  reverse_seda_archival_agency=transfer)
            # modification of a relation from a contained entity to a non contained entity
            mtclv = transfer.reverse_seda_mime_type_code_list_version_from[0]
            with self.assertUnauthorized(cnx):
                scheme = cnx.create_entity('ConceptScheme', title=u'Some nasty vocabulary')
                mtclv.cw_set(seda_mime_type_code_list_version_to=scheme)
            # deletion of a contained entity
            with self.assertUnauthorized(cnx):
                comment.cw_delete()
            # deletion of a outer relation
            with self.assertUnauthorized(cnx):
                transfer.reverse_seda_mime_type_code_list_version_from[0].cw_set(
                    seda_mime_type_code_list_version_to=None)
            # deletion of an archive unit
            with self.assertUnauthorized(cnx):
                transfer.archive_units[0].cw_delete()
            # deletion of the container
            with self.assertUnauthorized(cnx):
                transfer.cw_delete()

    def test_archive_unit(self):
        with self.admin_access.repo_cnx() as cnx:
            unit, unit_alt, unit_alt_seq = testutils.create_archive_unit(None, cnx=cnx)
            content = cnx.create_entity('SEDAContent', seda_content=unit_alt_seq)
            title = cnx.create_entity('SEDATitle', seda_title=content)
            cnx.commit()

            # unit has no parent, modifications are allowed.
            unit.cw_set(user_annotation=u'argh')
            title.cw_set(title=u'gloup')
            cnx.commit()

        with self.new_access('anon').client_cnx() as cnx:
            title = cnx.entity_from_eid(title.eid)
            unit = cnx.entity_from_eid(unit.eid)
            with self.assertUnauthorized(cnx):
                title.cw_set(title=u'zorglub')
            with self.assertUnauthorized(cnx):
                unit.cw_set(user_annotation=u'zorglub')
            with self.assertUnauthorized(cnx):
                cnx.create_entity(
                    'SEDATitle', seda_title=cnx.create_entity(
                        'SEDAContent', seda_content=unit_alt_seq))
            with self.assertUnauthorized(cnx):
                title.cw_delete()
            with self.assertUnauthorized(cnx):
                unit.cw_delete()
        with self.admin_access.repo_cnx() as cnx:
            unit = cnx.entity_from_eid(unit.eid)
            unit.cw_delete()
            cnx.commit()


if __name__ == '__main__':
    import unittest
    unittest.main()
