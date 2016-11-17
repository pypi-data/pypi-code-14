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
"""cubicweb-seda versions compatibility diagnosis test."""

from cubicweb.devtools.testlib import CubicWebTC

from testutils import create_archive_unit


class CompatAnalyzerTC(CubicWebTC):

    def test_base(self):
        with self.admin_access.repo_cnx() as cnx:
            create = cnx.create_entity

            transfer = create('SEDAArchiveTransfer', title=u'diagnosis testing')
            doctor = transfer.cw_adapt_to('ISEDACompatAnalyzer')
            cnx.commit()
            self.assertDiagnostic(doctor, ['SEDA 2.0', 'SEDA 1.0', 'SEDA 0.2', 'simplified'])

            unit, unit_alt, unit_alt_seq = create_archive_unit(transfer)
            transfer.cw_clear_all_caches()
            cnx.commit()
            self.assertDiagnostic(doctor, ['SEDA 2.0', 'SEDA 0.2', 'simplified'],
                                  'seda1_need_access_rule')

            access_rule = create('SEDAAccessRule', seda_access_rule=unit_alt_seq)
            unit_alt_seq.cw_clear_all_caches()
            cnx.commit()
            self.assertDiagnostic(doctor, ['SEDA 2.0'], 'rule_without_rule')

            access_rule_seq = create('SEDASeqAccessRuleRule',
                                     user_cardinality=u'1..n',
                                     reverse_seda_seq_access_rule_rule=access_rule)
            access_rule.cw_clear_all_caches()
            cnx.commit()
            self.assertDiagnostic(doctor, ['SEDA 2.0'],
                                  'rule_unsupported_card', 'rule_need_start_date')

            access_rule_seq.cw_set(user_cardinality=u'1')
            start_date = create('SEDAStartDate',
                                user_cardinality=u'0..1',
                                seda_start_date=access_rule_seq)
            access_rule_seq.cw_clear_all_caches()
            cnx.commit()
            self.assertDiagnostic(doctor, ['SEDA 2.0'],
                                  'rule_start_unsupported_card')

            start_date.cw_set(user_cardinality=u'1')
            start_date.cw_clear_all_caches()
            access_rule_seq2 = create('SEDASeqAccessRuleRule',
                                      user_cardinality=u'1..n',
                                      reverse_seda_seq_access_rule_rule=access_rule)
            access_rule.cw_clear_all_caches()
            cnx.commit()
            self.assertDiagnostic(doctor, ['SEDA 2.0'],
                                  'rule_with_too_much_rules')

            access_rule_seq2.cw_delete()
            inherit_ctl = create('SEDAAltAccessRulePreventInheritance',
                                 reverse_seda_alt_access_rule_prevent_inheritance=access_rule)
            create('SEDARefNonRuleId', seda_ref_non_rule_id_from=inherit_ctl)
            access_rule.cw_clear_all_caches()
            cnx.commit()
            self.assertDiagnostic(doctor, ['SEDA 2.0'],
                                  'rule_ref_non_rule_id')

    def assertDiagnostic(self, doctor, expected_formats, *expected_rule_ids):
        doctor.entity.cw_clear_all_caches()
        rule_ids = set(rule_id for rule_id, entity in doctor.failing_rules())
        self.assertEqual(rule_ids, set(expected_rule_ids))
        self.assertEqual(doctor.diagnose(), set(expected_formats))
        self.assertEqual(doctor.entity.compat_list, ', '.join(sorted(expected_formats)))


if __name__ == '__main__':
    import unittest
    unittest.main()
