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

from cubes.seda.entities import generated


class SEDAArchiveTransfer(generated.SEDAArchiveTransfer):

    def dc_title(self):
        return self.title

    @property
    def formats_compat(self):
        if self.compat_list is None:
            return set()
        return set(self.compat_list.split(', '))

    @property
    def comments(self):
        return self.reverse_seda_comment

    @property
    def archive_units(self):
        return self.reverse_seda_archive_unit

    @property
    def physical_data_objects(self):
        return self.reverse_seda_physical_data_object

    @property
    def binary_data_objects(self):
        return self.reverse_seda_binary_data_object


class SEDAArchiveUnit(generated.SEDAArchiveUnit):

    @property
    def first_level_choice(self):
        """Return the choice element of an archive unit (SEDAAltArchiveUnitArchiveUnitRefId),
        holding either a reference or descriptive content
        """
        return self.related('seda_alt_archive_unit_archive_unit_ref_id', 'subject').one()


class SEDABinaryDataObject(generated.SEDABinaryDataObject):

    @property
    def format_id(self):
        return self.reverse_seda_format_id_from[0] if self.reverse_seda_format_id_from else None

    @property
    def encoding(self):
        return self.reverse_seda_encoding_from[0] if self.reverse_seda_encoding_from else None

    @property
    def referenced_by(self):
        """Return an iterator on archive unit's content sequences referencing this data-object."""
        for ref in self.reverse_seda_data_object_reference_id:
            for seq in ref.seda_data_object_reference:
                yield seq


class SEDAAltArchiveUnitArchiveUnitRefId(generated.SEDAAltArchiveUnitArchiveUnitRefId):

    @property
    def reference(self):
        """Return the reference element for an archive unit which has no content"""
        rset = self.related('seda_archive_unit_ref_id_from', 'object')
        if rset:
            return rset.one()
        return None

    @property
    def content_sequence(self):
        """Return the sequence element holding content for an archive unit which is not a reference
        """
        rset = self.related('seda_seq_alt_archive_unit_archive_unit_ref_id_management', 'subject')
        if rset:
            return rset.one()
        return None


class SEDASeqAltArchiveUnitArchiveUnitRefIdManagement(
        generated.SEDASeqAltArchiveUnitArchiveUnitRefIdManagement):

    @property
    def contents(self):
        return self.reverse_seda_content


class SEDAContent(generated.SEDAContent):

    def dc_title(self):
        seda_descr_lvl = self.seda_description_level
        title = (seda_descr_lvl[0].label() if seda_descr_lvl
                 else self._cw._('<no description level specified>'))
        return u'{0} ({1})'.format(title, self.title.title or self._cw._('<no title specified>'))

    @property
    def title(self):
        return self.reverse_seda_title[0]

    @property
    def keywords(self):
        return self.reverse_seda_keyword

    @property
    def type(self):
        return self.reverse_seda_type_from[0] if self.reverse_seda_type_from else None

    @property
    def description_level_concept(self):
        return self.seda_description_level[0] if self.seda_description_level else None

    @property
    def description(self):
        return self.reverse_seda_description[0] if self.reverse_seda_description else None

    @property
    def start_date(self):
        return self.reverse_seda_start_date[0] if self.reverse_seda_start_date else None

    @property
    def end_date(self):
        return self.reverse_seda_end_date[0] if self.reverse_seda_end_date else None


class SEDAKeyword(generated.SEDAKeyword):

    @property
    def content_string(self):
        return self.seda_keyword_content[0].keyword_content

    @property
    def reference(self):
        return (self.reverse_seda_keyword_reference_from[0]
                if self.reverse_seda_keyword_reference_from else None)


class SEDAKeywordReference(generated.SEDAKeywordReference):

    @property
    def scheme(self):
        return (self.seda_keyword_reference_to_scheme[0] if self.seda_keyword_reference_to_scheme
                else None)

    @property
    def concept(self):
        return self.seda_keyword_reference_to[0] if self.seda_keyword_reference_to else None


class RuleMixIn(object):

    @property
    def _rule_type(self):
        return self.cw_etype[4:-4].lower()

    @property
    def rules(self):
        return getattr(self, 'seda_seq_{0}_rule_rule'.format(self._rule_type))

    @property
    def inheritance_control(self):
        alt = getattr(self, 'seda_alt_{0}_rule_prevent_inheritance'.format(self._rule_type))
        return alt[0] if alt else None


class SEDAAccessRule(RuleMixIn, generated.SEDAAccessRule):
    pass


class SEDAAppraisalRule(RuleMixIn, generated.SEDAAppraisalRule):

    @property
    def final_action_concept(self):
        if self.seda_final_action:
            return self.seda_final_action[0]
        return None


class SEDAClassificationRule(RuleMixIn, generated.SEDAClassificationRule):
    pass


class SEDADisseminationRule(RuleMixIn, generated.SEDADisseminationRule):
    pass


class SEDAReuseRule(RuleMixIn, generated.SEDAReuseRule):
    pass


class SEDAStorageRule(RuleMixIn, generated.SEDAStorageRule):

    @property
    def final_action_concept(self):
        if self.seda_final_action:
            return self.seda_final_action[0]
        return None


class RuleRuleMixIn(object):

    @property
    def start_date(self):
        return self.reverse_seda_start_date[0] if self.reverse_seda_start_date else None

    @property
    def rule_concept(self):
        return self.seda_rule[0] if self.seda_rule else None


class SEDASeqAccessRuleRule(RuleRuleMixIn, generated.SEDASeqAccessRuleRule):
    pass


class SEDASeqAppraisalRuleRule(RuleRuleMixIn, generated.SEDASeqAppraisalRuleRule):
    pass


class SEDASeqClassificationRuleRule(RuleRuleMixIn, generated.SEDASeqClassificationRuleRule):
    pass


class SEDASeqDisseminationRuleRule(RuleRuleMixIn, generated.SEDASeqDisseminationRuleRule):
    pass


class SEDASeqReuseRuleRule(RuleRuleMixIn, generated.SEDASeqReuseRuleRule):
    pass


class SEDASeqStorageRuleRule(RuleRuleMixIn, generated.SEDASeqStorageRuleRule):
    pass


class SEDAFormatId(generated.SEDAFormatId):

    @property
    def concept(self):
        return self.seda_format_id_to[0] if self.seda_format_id_to else None


class SEDAEncoding(generated.SEDAEncoding):

    @property
    def concept(self):
        return self.seda_encoding_to[0] if self.seda_encoding_to else None


class SEDAType(generated.SEDAType):

    @property
    def concept(self):
        return self.seda_type_to[0] if self.seda_type_to else None
