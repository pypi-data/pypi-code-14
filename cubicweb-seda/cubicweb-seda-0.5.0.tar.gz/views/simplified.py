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
"""cubicweb-seda views configuration / overrides for simplified profiles."""

from logilab.common.registry import objectify_predicate

from cubicweb.predicates import is_instance
from cubicweb.web.views import uicfg, autoform, formrenderers

from cubes.seda.entities import simplified_profile
from cubes.seda.views import copy_rtag
# ensure those are registered first
from cubes.seda.views import mgmt_rules, archivetransfer, dataobject, archiveunit, content  # noqa


afs = uicfg.autoform_section
simplified_afs = copy_rtag(afs, __name__, simplified_profile())

# appraisal/access rules have a single top level cardinality in simplified profile, as well as
# always a start date. This implies:
# 1. force one and only one eg AppraisalRuleRule,
# 2. force start date, but hide it,
# 3. hide eg AppraisalRuleRule's cardinality.

# 3. hide rule rule's cardinality
simplified_afs.tag_attribute(('SEDASeqAppraisalRuleRule', 'user_cardinality'),
                             'main', 'hidden')
simplified_afs.tag_attribute(('SEDASeqAccessRuleRule', 'user_cardinality'),
                             'main', 'hidden')


# 2. hide start date's cardinality - uicfg is not enough since we want it when edited in the context
# of SEDAContent but not of rule entity types

class StartDateAutomaticEntityForm(autoform.AutomaticEntityForm):
    __select__ = (is_instance('SEDAStartDate')
                  & simplified_profile())

    def editable_attributes(self, strict=False):
        """return a list of (relation schema, role) to edit for the entity"""
        attributes = super(StartDateAutomaticEntityForm, self).editable_attributes(strict)
        if self.linked_to.get(('seda_start_date', 'subject')):
            eid = self.linked_to[('seda_start_date', 'subject')][0]
            start_date_of = self._cw.entity_from_eid(eid)
        else:
            start_date_of = self.edited_entity.reverse_start_date_of
        if start_date_of.cw_etype != 'SEDAContent':
            attributes.remove(('user_cardinality', 'subject'))
        return attributes


class RuleAutomaticEntityForm(autoform.AutomaticEntityForm):
    __select__ = (is_instance('SEDAAppraisalRule', 'SEDAAccessRule')
                  & simplified_profile())

    def should_display_inline_creation_form(self, rschema, existing, card):
        # 1. force creation of one appraisal/access rule
        if not existing and rschema in ('seda_seq_appraisal_rule_rule',
                                        'seda_seq_access_rule_rule'):
            return True
        return super(RuleAutomaticEntityForm, self).should_display_inline_creation_form(
            rschema, existing, card)

    def should_display_add_new_relation_link(self, rschema, existing, card):
        # 1. don't allow creation of more than one appraisal/access rule
        if rschema in ('seda_seq_appraisal_rule_rule',
                       'seda_seq_access_rule_rule'):
            return False
        return super(RuleAutomaticEntityForm, self).should_display_add_new_relation_link(
            rschema, existing, card)


class SeqRuleRuleAutomaticEntityForm(autoform.AutomaticEntityForm):
    __select__ = (is_instance('SEDASeqAppraisalRuleRule', 'SEDASeqAccessRuleRule')
                  & simplified_profile())

    def should_display_inline_creation_form(self, rschema, existing, card):
        # 2. force start date
        if not existing and rschema == 'seda_start_date':
            return True
        return super(SeqRuleRuleAutomaticEntityForm, self).should_display_inline_creation_form(
            rschema, existing, card)


@objectify_predicate
def simplified_rule_rule(cls, req, rtype=None, pform=None, **kwargs):
    # check we're within a simplified profile
    if isinstance(pform, RuleAutomaticEntityForm) and rtype in ('seda_seq_appraisal_rule_rule',
                                                                'seda_seq_access_rule_rule'):
        return 1
    return 0


# 1. don't allow deletion of our appraisal/access rule

class RuleRuleInlineEntityEditionFormView(autoform.InlineEntityEditionFormView):
    __select__ = (autoform.InlineEntityEditionFormView.__select__
                  & simplified_rule_rule())
    removejs = None


class RuleRuleInlineEntityCreationFormView(autoform.InlineEntityCreationFormView):
    __select__ = (autoform.InlineEntityCreationFormView.__select__
                  & simplified_rule_rule())
    removejs = None


# 2. hide start date

@objectify_predicate
def simplified_start_date(cls, req, rtype=None, pform=None, **kwargs):
    # check we're within a simplified profile
    if isinstance(pform, SeqRuleRuleAutomaticEntityForm) and rtype == 'seda_start_date':
        return 1
    return 0


class StartDateInlineEntityEditionFormView(autoform.InlineEntityEditionFormView):
    __select__ = (autoform.InlineEntityEditionFormView.__select__
                  & simplified_start_date())
    removejs = None
    form_renderer_id = 'notitle'


class StartDateInlineEntityCreationFormView(autoform.InlineEntityCreationFormView):
    __select__ = (autoform.InlineEntityCreationFormView.__select__
                  & simplified_start_date())
    removejs = None
    form_renderer_id = 'notitle'


# simplified profil will have a single appraisal/access rule, hence 'ignore inherited rules' is
# enough, no need for explicit rule deactivation. This implies:
# 1. hide explicit rule deactivation
# 2. force appearance (hence choice) of the ignore all rules entity
# 3. adapt alternative's title, so it doesn't appear like an alternative

# 1. hide explicit rule deactivation
simplified_afs.tag_object_of(('*', 'seda_ref_non_rule_id_from', '*'),
                             'main', 'hidden')


class AltInheritanceAutomaticEntityForm(autoform.AutomaticEntityForm):
    __select__ = (is_instance('SEDAAltAccessRulePreventInheritance',
                              'SEDAAltAppraisalRulePreventInheritance')
                  & simplified_profile())

    # 3. adapt alternative's title, so it doesn't appear like an alternative
    def __init__(self, *args, **kwargs):
        super(AltInheritanceAutomaticEntityForm, self).__init__(*args, **kwargs)
        self.form_renderer_id = 'not-an-alt'

    # 2. force appearance (hence choice) of the ignore all rules entity
    def should_display_inline_creation_form(self, rschema, existing, card):
        if not existing and rschema == 'seda_prevent_inheritance':
            return True
        return super(AltInheritanceAutomaticEntityForm, self).should_display_inline_creation_form(
            rschema, existing, card)


# 2. force appearance (hence choice) of the ignore all rules entity

@objectify_predicate
def simplified_prevent_inheritance(cls, req, rtype=None, pform=None, **kwargs):
    if isinstance(pform, AltInheritanceAutomaticEntityForm) and rtype == 'seda_prevent_inheritance':
        return 1
    return 0


class PreventInheritanceInlineEntityEditionFormView(autoform.InlineEntityEditionFormView):
    __select__ = (autoform.InlineEntityEditionFormView.__select__
                  & simplified_prevent_inheritance())
    removejs = None


class PreventInheritanceInlineEntityCreationFormView(autoform.InlineEntityCreationFormView):
    __select__ = (autoform.InlineEntityCreationFormView.__select__
                  & simplified_prevent_inheritance())
    removejs = None


class NotAnAltEntityInlinedFormRenderer(formrenderers.EntityInlinedFormRenderer):
    """Custom form renderer that remove 'Alternative :' from an alternative's inlined form's title.
    """
    __regid__ = 'not-an-alt'

    def render_title(self, w, form, values):
        values['title'] = values['title'].split(':', 1)[1]
        super(NotAnAltEntityInlinedFormRenderer, self).render_title(w, form, values)
