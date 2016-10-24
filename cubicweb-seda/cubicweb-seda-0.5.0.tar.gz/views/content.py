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
"""cubicweb-seda views for content of archive units."""

from logilab.common.registry import objectify_predicate
from logilab.mtconverter import xml_escape

from cubicweb import _
from cubicweb.predicates import is_instance
from cubicweb.web.views import tabs, uicfg

from cubes.relationwidget.views import RelationFacetWidget

from cubes.seda.xsd import un_camel_case
from cubes.seda.views import rtags_from_rtype_role_targets, rtags_from_xsd_element, copy_rtag
from cubes.seda.views import viewlib, widgets
from cubes.seda.views import uicfg as sedauicfg  # noqa - ensure those rules are defined first


pvs = uicfg.primaryview_section
pvdc = uicfg.primaryview_display_ctrl
rec = uicfg.reledit_ctrl
afs = uicfg.autoform_section
affk = uicfg.autoform_field_kwargs


@objectify_predicate
def is_typed_reference(cls, req, entity=None, **kwargs):
    """Return positive score for content's typed data object references (IsPartOf, VersionOf, etc.), not
    used those starting directly from archive unit.
    """
    if entity is None or not entity.has_eid():
        try:
            rtype, eid, role = req.form['__linkto'].split(':')
        except KeyError:
            pass
        else:
            if rtype == 'seda_data_object_reference':
                entity = req.entity_from_eid(eid)
    else:
        entity = entity.seda_data_object_reference[0]
    if entity is not None and entity.cw_etype == 'SEDASeqAltArchiveUnitArchiveUnitRefIdManagement':
        return 0
    return 1


content_ordered_fields = [
    ('seda_description_level', 'subject'),
    ('seda_title', 'object'),
    ('seda_description', 'object'),
    ('seda_version', 'object'),
    ('seda_type_from', 'object'),
    ('seda_document_type', 'object'),
    ('seda_status', 'object'),
    ('seda_language_from', 'object'),
    ('seda_description_language_from', 'object'),
]
for rtype, role in content_ordered_fields:
    if role == 'subject':
        pvs.tag_subject_of(('SEDAContent', rtype, '*'), 'attributes')
    else:
        pvs.tag_object_of(('*', rtype, 'SEDAContent'), 'attributes')
    if rtype == 'seda_description_level':
        novalue_label = _('<no value specified>')
    else:
        novalue_label = _('<unauthorized>')
    vid = 'seda.reledit.complexlink' if 'language' in rtype else 'seda.reledit.text'
    if role == 'subject':
        rec.tag_subject_of(('SEDAContent', rtype, '*'),
                           {'rvid': vid, 'novalue_label': novalue_label})
    else:
        rec.tag_object_of(('*', rtype, 'SEDAContent'),
                          {'rvid': vid, 'novalue_label': novalue_label})

afs.tag_subject_of(('SEDAKeywordReference', 'seda_keyword_reference_to_scheme', '*'),
                   'main', 'attributes')
affk.set_field_kwargs('SEDAKeywordReference', 'seda_keyword_reference_to',
                      widget=widgets.ConceptAutoCompleteWidget(
                          slave_name='seda_keyword_reference_to',
                          master_name='seda_keyword_reference_to_scheme'))
affk.set_fields_order('SEDAKeywordReference', ['user_cardinality',
                                               'seda_keyword_reference_to_scheme',
                                               'seda_keyword_reference_to'])

affk.tag_subject_of(('SEDALanguage', 'seda_language_to', '*'),
                    {'widget': RelationFacetWidget})
affk.tag_subject_of(('SEDADescriptionLanguage', 'seda_description_language_to', '*'),
                    {'widget': RelationFacetWidget})

affk.set_fields_order('SEDAContent',
                      ['user_cardinality', 'user_annotation'] + content_ordered_fields)
pvdc.set_fields_order('SEDAContent',
                      ['user_cardinality', 'user_annotation'] + content_ordered_fields)


class ContentTabbedPrimaryView(tabs.TabbedPrimaryView):

    __select__ = tabs.TabbedPrimaryView.__select__ & is_instance('SEDAContent')

    tabs = [
        'main_tab',
        _('seda_content_identification_tab'),
        _('seda_content_restriction_tab'),
        _('seda_content_date_tab'),
        _('seda_content_gps_tab'),
        _('seda_content_service_tab'),
        _('seda_content_agent_tab'),
        _('seda_content_coverage_tab'),
        _('seda_content_indexation_tab'),
        _('seda_content_relation_tab'),
        _('seda_content_event_tab'),
        _('seda_content_history_tab'),
    ]


class ContentIdentificationTab(tabs.PrimaryTab):
    """Display identification data about an archive unit content."""

    __regid__ = 'seda_content_identification_tab'
    __select__ = tabs.PrimaryTab.__select__ & is_instance('SEDAContent')

    rtype_role_targets = [
        ('seda_source', 'object', None),
        ('seda_file_plan_position', 'object', None),
        ('seda_system_id', 'object', None),
        ('seda_originating_system_id', 'object', None),
        ('seda_archival_agency_archive_unit_identifier', 'object', None),
        ('seda_originating_agency_archive_unit_identifier', 'object', None),
        ('seda_transferring_agency_archive_unit_identifier', 'object', None),
    ]
    rsection, display_ctrl = rtags_from_rtype_role_targets('SEDAContent', rtype_role_targets)


class ContentRestrictionTab(tabs.PrimaryTab):
    """Display restrictions about an archive unit content."""

    __regid__ = 'seda_content_restriction_tab'
    __select__ = tabs.PrimaryTab.__select__ & is_instance('SEDAContent')

    rtype_role_targets = [
        ('seda_restriction_rule_id_ref', 'object', None),
        ('seda_restriction_value', 'object', None),
        ('seda_restriction_end_date', 'object', None),
    ]
    rsection, display_ctrl = rtags_from_rtype_role_targets('SEDAContent', rtype_role_targets)


class ContentDateTab(tabs.PrimaryTab):
    """Display date information about an archive unit content."""

    __regid__ = 'seda_content_date_tab'
    __select__ = tabs.PrimaryTab.__select__ & is_instance('SEDAContent')

    rtype_role_targets = [
        ('seda_created_date', 'object', None),
        ('seda_transacted_date', 'object', None),
        ('seda_acquired_date', 'object', None),
        ('seda_sent_date', 'object', None),
        ('seda_received_date', 'object', None),
        ('seda_registered_date', 'object', None),
        ('seda_start_date', 'object', None),
        ('seda_end_date', 'object', None),
    ]
    rsection, display_ctrl = rtags_from_rtype_role_targets('SEDAContent', rtype_role_targets)


class ContentGpsTab(tabs.PrimaryTab):
    """Display GPS information about an archive unit content."""

    __regid__ = 'seda_content_gps_tab'
    __select__ = tabs.PrimaryTab.__select__ & is_instance('SEDAContent')

    rsection, display_ctrl = rtags_from_xsd_element('SEDAContent', 'Gps')


class ContentServiceTab(tabs.PrimaryTab):
    """Display service information about an archive unit content."""

    __regid__ = 'seda_content_service_tab'
    __select__ = tabs.PrimaryTab.__select__ & is_instance('SEDAContent')

    rtype_role_targets = [
        ('seda_originating_agency_from', 'object', None),
        ('seda_submission_agency_from', 'object', None),
        ('seda_authorized_agent_from', 'object', None),
    ]
    rsection, display_ctrl = rtags_from_rtype_role_targets('SEDAContent', rtype_role_targets)


class ContentAgentTab(viewlib.SubObjectsTab):
    """Display agents related to an archive unit content."""

    __regid__ = 'seda_content_agent_tab'
    __select__ = viewlib.SubObjectsTab.__select__ & is_instance('SEDAContent')

    rtype_role_targets = [
        ('seda_writer_from', 'object', None),
        ('seda_addressee_from', 'object', None),
        ('seda_recipient_from', 'object', None),
    ]
    subvid = 'seda.type_listitem'

    _('creating SEDAWriter (SEDAWriter seda_writer_from SEDAContent %(linkto)s)')
    _('creating SEDAAddressee (SEDAAddressee seda_addressee_from SEDAContent %(linkto)s)')
    _('creating SEDARecipient (SEDARecipient seda_recipient_from SEDAContent %(linto)s)')


class ContentCoverageTab(viewlib.SubObjectsTab):
    """Display coverage information about an archive unit content."""

    __regid__ = 'seda_content_coverage_tab'
    __select__ = viewlib.SubObjectsTab.__select__ & is_instance('SEDAContent')

    rtype_role_targets = [('seda_spatial', 'object', None),
                          ('seda_temporal', 'object', None),
                          ('seda_juridictional', 'object', None)]
    subvid = 'seda.type_listitem'

    _('creating SEDASpatial (SEDASpatial seda_spatial SEDAContent %(linkto)s)')
    _('creating SEDATemporal (SEDATemporal seda_temporal SEDAContent %(linkto)s)')
    _('creating SEDAJuridictional (SEDAJuridictional seda_juridictional SEDAContent %(linkto)s)')


class ContentIndexationTab(viewlib.SubObjectsTab):
    """Display indexation (keywords and tags) about an archive unit content."""

    __regid__ = 'seda_content_indexation_tab'
    __select__ = viewlib.SubObjectsTab.__select__ & is_instance('SEDAContent')

    rtype_role_targets = [
        ('seda_keyword', 'object', 'SEDAKeyword'),
        ('seda_tag', 'object', 'SEDATag'),
    ]

    _('creating SEDAKeyword (SEDAKeyword seda_keyword SEDAContent %(linkto)s)')
    _('creating SEDATag (SEDATag seda_tag SEDAContent %(linkto)s)')


class ContentRelationTab(viewlib.SubObjectsTab):
    """Display relation information about an archive unit content."""

    __regid__ = 'seda_content_relation_tab'
    __select__ = viewlib.SubObjectsTab.__select__ & is_instance('SEDAContent')

    rtype_role_targets = [('seda_is_version_of', 'object', None),
                          ('seda_replaces', 'object', None),
                          ('seda_requires', 'object', None),
                          ('seda_is_part_of', 'object', None),
                          ('seda_references', 'object', None)]

    _('creating SEDAIsVersionOf (SEDAIsVersionOf seda_is_version_of SEDAContent %(linkto)s)')
    _('creating SEDAReplaces (SEDAReplaces seda_replaces SEDAContent %(linkto)s)')
    _('creating SEDARequires (SEDARequires seda_requires SEDAContent %(linkto)s)')
    _('creating SEDAIsPartOf (SEDAIsPartOf seda_is_part_of SEDAContent %(linkto)s)')
    _('creating SEDAReferences (SEDAReferences seda_references SEDAContent %(linkto)s)')


class ContentEventTab(viewlib.SubObjectsTab):
    """Display events about an archive unit content."""

    __regid__ = 'seda_content_event_tab'
    __select__ = viewlib.SubObjectsTab.__select__ & is_instance('SEDAContent')

    rtype_role_targets = [
        ('seda_event', 'object', None),
    ]

    _('creating SEDAEvent (SEDAEvent seda_event SEDAContent %(linkto)s)')


class ContentHistoryTab(viewlib.SubObjectsTab):
    """Display custodial history information about an archive unit content."""

    __regid__ = 'seda_content_history_tab'
    __select__ = viewlib.SubObjectsTab.__select__ & is_instance('SEDAContent')

    rtype_role_targets = [('seda_custodial_history_item', 'object', None)]

    _('creating SEDACustodialHistoryItem (SEDACustodialHistoryItem seda_custodial_history_item '
      'SEDAContent %(linkto)s)')


# Remove from relations section and autoform what is shown in tabs
for cls in (ContentIdentificationTab,
            ContentDateTab,
            ContentServiceTab,
            ContentAgentTab,
            ContentIndexationTab,
            ContentEventTab):
    for rtype, role, target in cls.rtype_role_targets:
        if role == 'object':
            pvs.tag_object_of(('*', rtype, 'SEDAContent'), 'hidden')
            afs.tag_object_of(('*', rtype, 'SEDAContent'), 'main', 'hidden')
        else:
            pvs.tag_subject_of(('SEDAContent', rtype, '*'), 'hidden')
            afs.tag_subject_of(('SEDAContent', rtype, '*'), 'main', 'hidden')


class KeywordBusinessValueEntityView(viewlib.LinkMetaEntityView):

    __select__ = viewlib.BusinessValueEntityView.__select__ & is_instance('SEDAKeyword')

    def entity_call(self, entity):
        if entity.seda_keyword_content[0].keyword_content:
            content = entity.seda_keyword_content[0].keyword_content
        else:
            content = self._cw._('<no value specified>')
        msg = xml_escape(self._cw._('keyword: {0}').format(content))
        self.w(u'<span class="value">{0} {1}</span>'.format(msg, entity.view('seda.xsdmeta')))
        if entity.reverse_seda_keyword_type_from:
            kwt = entity.reverse_seda_keyword_type_from[0]
            if kwt.seda_keyword_type_to:
                kwt_value = kwt.seda_keyword_type_to[0].label()
            else:
                kwt_value = self._cw._('<no type specified>')
            msg = xml_escape(self._cw._('keyword type: {0}').format(kwt_value))
            self.w(u'<br/><span>{0} {1}</span>'.format(msg, kwt.view('seda.xsdmeta')))
        if entity.reverse_seda_keyword_reference_from:
            kwr = entity.reverse_seda_keyword_reference_from[0]
            if kwr.concept:
                kwr_value = kwr.concept.view('oneline')
                msg = xml_escape(self._cw._('keyword reference: {0}')).format(kwr_value)
            elif kwr.scheme:
                kwr_value = kwr.scheme.view('oneline')
                msg = xml_escape(self._cw._('keyword scheme: {0}')).format(kwr_value)
            else:
                msg = xml_escape(self._cw._('<no reference specified>'))
            self.w(u'<br/><span>{0} {1}</span>'.format(msg, kwr.view('seda.xsdmeta')))


TYPED_REFERENCE_ENTITY_TYPES = ('SEDAAltIsPartOfArchiveUnitRefId',
                                'SEDAAltIsVersionOfArchiveUnitRefId',
                                'SEDAAltReferencesArchiveUnitRefId',
                                'SEDAAltReplacesArchiveUnitRefId',
                                'SEDAAltRequiresArchiveUnitRefId')


class BusinessValueLinkedEntityView(viewlib.BusinessValueEntityView):

    __select__ = is_instance(*TYPED_REFERENCE_ENTITY_TYPES)

    def entity_value(self, entity):
        alt_rtype = (un_camel_case(entity.cw_etype).replace('seda_', 'seda_alt_')
                     + '_archive_unit_ref_id')
        alt = getattr(entity, alt_rtype)[0]
        alternatives = []
        for rtype, value_rtype in (
                ('seda_data_object_reference', 'seda_data_object_reference_id'),
                ('seda_archive_unit_ref_id_from', 'seda_archive_unit_ref_id_to'),
                ('seda_repository_archive_unit_pid', None),
                ('seda_repository_object_pid', None)):
            value = alt.related(rtype, role='object')
            if value:
                value = value.one()
                target_value = getattr(value, value_rtype) if value_rtype else None
                if target_value:
                    content = target_value[0].view('oneline')
                else:
                    content = xml_escape(self._cw._('<no value specified>'))
                alternatives.append(value.dc_type() + ' ' + content)
        return (u'<b>{0}</b>'.format(self._cw._(' ALT_I18N '))).join(alternatives)


do_ref_afs = copy_rtag(afs, __name__,
                       is_instance('SEDADataObjectReference') & is_typed_reference())
do_ref_afs.tag_attribute(('SEDADataObjectReference', 'user_cardinality'), 'main', 'hidden')

for etype in TYPED_REFERENCE_ENTITY_TYPES:
    affk.set_fields_order(etype, [('seda_data_object_reference', 'object'),
                                  ('seda_repository_object_pid', 'object'),
                                  ('seda_archive_unit_ref_id_from', 'object'),
                                  ('seda_repository_archive_unit_pid', 'object')])


class EventLinkMetaEntityView(viewlib.LinkMetaEntityView):

    __select__ = viewlib.LinkMetaEntityView.__select__ & is_instance('SEDAEvent')

    def entity_call(self, entity):
        entity.view('seda.xsdmeta', w=self.w, skip_one_card=True, with_annotation=False)
        attrs = []
        for rtype in ['seda_event_type_from',
                      'seda_event_identifier',
                      'seda_event_detail']:
            related = getattr(entity, 'reverse_' + rtype)
            if related:
                if related[0].user_cardinality == '1':
                    card = self._cw._('mandatory')
                else:
                    card = self._cw._('optional')
                value = ''
                if rtype == 'seda_event_type_from':
                    value = related[0].seda_event_type_to
                    if value:
                        value = value[0].label()
                attrs.append(u'{rtype} {value} {card}'.format(rtype=self._cw.__(rtype + '_object'),
                                                              value=value,
                                                              card=card))
        if attrs:
            self.w(u' ({0})'.format(', '.join(attrs)))
        description = getattr(entity, 'user_annotation', None)
        if description:
            self.w(u' <div class="description text-muted">%s</div>' % description)


affk.set_fields_order('SEDAEvent', ['user_cardinality',
                                    ('seda_event_type_from', 'object'),
                                    ('seda_event_identifier', 'object'),
                                    ('seda_event_detail', 'object')])


class CustodialHistoryItemLinkMetaEntityView(viewlib.LinkMetaEntityView):

    __select__ = viewlib.LinkMetaEntityView.__select__ & is_instance('SEDACustodialHistoryItem')

    def entity_call(self, entity):
        super(CustodialHistoryItemLinkMetaEntityView, self).entity_call(entity)
        if entity.reverse_seda_when:
            when = entity.reverse_seda_when[0]
            if when.user_cardinality == '1':
                self.w(self._cw._(' (mandatory timestamp)'))
            else:
                self.w(self._cw._(' (optional timestamp)'))
