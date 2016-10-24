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
"""cubicweb-seda views for ArchiveUnit"""

from six import text_type

from logilab.common.registry import objectify_predicate, yes

from cubicweb import tags, _
from cubicweb.predicates import is_instance
from cubicweb.view import EntityView
from cubicweb.web.views import uicfg, baseviews, tabs

from cubes.compound import views as compound
from cubes.relationwidget import views as rwdg

from cubes.seda.entities import simplified_profile, parent_and_container
from cubes.seda.entities.itree import parent_archive_unit
from cubes.seda.views import (add_subobject_link, add_subobjects_button, dropdown_button,
                              rtags_from_rtype_role_targets, copy_rtag, has_rel_perm)
from cubes.seda.views import clone, viewlib, widgets, content
from cubes.seda.views import uicfg as sedauicfg  # noqa - ensure those rules are defined first


afs = uicfg.autoform_section
affk = uicfg.autoform_field_kwargs
pvs = uicfg.primaryview_section
rec = uicfg.reledit_ctrl


@objectify_predicate
def is_archive_unit_ref(cls, req, rset=None, entity=None, **kwargs):
    """Return 1 if a unit_type value is specified in kwargs or in form parameters, and its value is
    'unit_ref'
    """
    try:
        # first check for unit_type specified in form params
        unit_type = req.form['unit_type']
        return int(unit_type == 'unit_ref')
    except KeyError:
        # if it's not, look if we're in the context of a archive unit or its first level choice
        if entity is None:
            assert rset is not None, \
                ('is_archive_unit_ref can only be used in the context of a SEDAArchiveUnit '
                 'or SEDAAltArchiveUnitArchiveUnitRefId entity, but no context entity specified')
            entity = rset.get_entity(0, 0)
        if entity.cw_etype == 'SEDAArchiveUnit':
            entity = entity.first_level_choice
        elif entity.cw_etype == 'SEDAArchiveUnitRefId':
            entity = entity.seda_archive_unit_ref_id_from[0]
            if entity.cw_etype != 'SEDAAltArchiveUnitArchiveUnitRefId':
                return 0  # other kind of reference
        assert entity.cw_etype == 'SEDAAltArchiveUnitArchiveUnitRefId', \
            ('is_archive_unit_ref can only be used in the context of a SEDAArchiveUnit, '
             'SEDAArchiveUnitRefId or SEDAAltArchiveUnitArchiveUnitRefId entity, not %s' % entity)
        return 0 if entity.content_sequence else 1


def unit_ref_vocabulary(form, field):
    """Form vocabulary function for archive unit references, necessary to get parent container while
    the entity is being created.
    """
    req = form._cw
    parent, container = parent_and_container(form.edited_entity)
    assert container is not None
    rset = req.execute('Any XID, X ORDERBY XID WHERE '
                       'X is SEDAArchiveUnit, X id XID, X container R, R eid %(root)s',
                       {'root': container.eid})
    return [(label, str(eid)) for label, eid in rset]

affk.tag_subject_of(('SEDAArchiveUnitRefId', 'seda_archive_unit_ref_id_to', '*'),
                    {'choices': unit_ref_vocabulary})


pvs.tag_subject_of(
    ('SEDAArchiveUnit', 'seda_alt_archive_unit_archive_unit_ref_id', '*'),
    'hidden')


class SkipIBreadCrumbsAdapter(compound.IContainedBreadcrumbsAdapter):
    """IBreadCrumbsAdapter for entities which should not appears in breadcrumb, we want to go back to
    the parent
    """
    __select__ = is_instance('SEDAAltArchiveUnitArchiveUnitRefId',
                             'SEDASeqAltArchiveUnitArchiveUnitRefIdManagement')

    def breadcrumbs(self, view=None, recurs=None):
        parent = self.parent_entity()
        adapter = parent.cw_adapt_to('IBreadCrumbs')
        return adapter.breadcrumbs(view, recurs)


class SkipInContextView(baseviews.InContextView):
    """Custom incontext view, for use in title of creation form, among others"""
    __select__ = is_instance('SEDAAltArchiveUnitArchiveUnitRefId',
                             'SEDASeqAltArchiveUnitArchiveUnitRefIdManagement')

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        parent_archive_unit(entity).view('incontext', w=self.w)


class ArchiveUnitRefIdOutOfContextView(baseviews.OutOfContextView):
    """Custom outofcontext view for proper display of SEDAArchiveUnitRefId from in boxes"""
    __select__ = is_instance('SEDAArchiveUnitRefId')

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        parent = entity.cw_adapt_to('IContained').parent
        parent.view('incontext', w=self.w)


class DataObjectReferenceBusinessValueLinkEntityView(viewlib.BusinessValueLinkEntityView):
    __select__ = is_instance('SEDADataObjectReference')

    def entity_call(self, entity):
        do_rset = entity.related('seda_data_object_reference_id', 'subject')
        if do_rset:
            do_rset.one().view(self.__regid__, w=self.w)
        else:
            super(DataObjectReferenceBusinessValueLinkEntityView, self).entity_call(entity)


class ArchiveUnitTabbedPrimaryView(tabs.TabbedPrimaryView):
    __select__ = tabs.TabbedPrimaryView.__select__ & is_instance('SEDAArchiveUnit')

    tabs = [
        'main_tab',
        _('seda_management_tab'),
        _('seda_au_content_tab'),
        _('seda_au_indexation_tab'),
        _('seda_au_history_tab'),
        _('seda_au_archive_units_tab'),
        _('seda_au_data_objects_refs_tab'),
    ]

    def entity_call(self, entity, **kwargs):
        super(ArchiveUnitTabbedPrimaryView, self).entity_call(entity, **kwargs)
        rwdg.boostrap_dialog(self.w, self._cw._, clone._import_div_id(entity), u'')


au_ref_pvs = copy_rtag(pvs, __name__,
                       is_instance('SEDAArchiveUnit') & is_archive_unit_ref())
au_ref_pvs.tag_subject_of(
    ('SEDAArchiveUnit', 'seda_alt_archive_unit_archive_unit_ref_id', '*'),
    'attributes')
rec.tag_subject_of(('SEDAArchiveUnit', 'seda_alt_archive_unit_archive_unit_ref_id', '*'),
                   {'rvid': 'seda.reledit.simplelink',
                    'novalue_label': _('<unauthorized>')})


class RefArchiveUnitSimpleLinkToEntityAttributeView(EntityView):
    __regid__ = 'seda.reledit.simplelink'
    __select__ = is_instance('SEDAAltArchiveUnitArchiveUnitRefId') & is_archive_unit_ref()

    def entity_call(self, entity):
        entity.reference.view('seda.reledit.complexlink',
                              initargs={'rtype': 'seda_archive_unit_ref_id_from'},
                              w=self.w)


class TitleBusinessValueEntityView(viewlib.BusinessValueEntityView):
    """Entity view for SEDAContent entities that will display value of the SEDATitle related
    element.
    """
    # add yes(1) to overtake BusinessValueLinkEntityView
    __select__ = is_instance('SEDAContent') & yes(1)
    no_value_msg = _('<no title specified>')

    def entity_value(self, entity):
        return tags.a(entity.dc_title(), href=entity.absolute_url())


class ArchiveUnitManagementTab(tabs.PrimaryTab):
    """Display management information about an archive unit."""

    __regid__ = 'seda_management_tab'
    __select__ = is_instance('SEDAArchiveUnit') & ~is_archive_unit_ref()

    rtype_role_targets = [
        ('seda_storage_rule', 'object', None),
        ('seda_appraisal_rule', 'object', None),
        ('seda_access_rule', 'object', None),
        ('seda_dissemination_rule', 'object', None),
        ('seda_reuse_rule', 'object', None),
        ('seda_classification_rule', 'object', None),
        ('seda_need_authorization', 'object', None),
    ]
    rsection, display_ctrl = rtags_from_rtype_role_targets(
        'SEDASeqAltArchiveUnitArchiveUnitRefIdManagement', rtype_role_targets
    )

    def entity_call(self, entity, **kwargs):
        seq = entity.first_level_choice.content_sequence
        super(ArchiveUnitManagementTab, self).entity_call(seq, **kwargs)


class SimplifiedArchiveUnitManagementTab(ArchiveUnitManagementTab):
    __select__ = ArchiveUnitManagementTab.__select__ & simplified_profile()

    rtype_role_targets = [
        ('seda_appraisal_rule', 'object', None),
        ('seda_access_rule', 'object', None),
    ]
    rsection, display_ctrl = rtags_from_rtype_role_targets(
        'SEDASeqAltArchiveUnitArchiveUnitRefIdManagement', rtype_role_targets
    )


class ArchiveUnitSubObjectsTab(viewlib.SubObjectsTab):
    """Abstract subobjects tab specific to archive unit to handle subentities below choice>sequence
    child transparently.
    """

    __abstract__ = True
    __select__ = EntityView.__select__ & is_instance('SEDAArchiveUnit') & ~is_archive_unit_ref()

    def entity_call(self, entity):
        seq = entity.first_level_choice.content_sequence
        self.display_add_button(seq)
        self.display_subobjects_list(seq)

    def url_params(self, entity):
        archive_unit = parent_archive_unit(entity)
        return {'__redirectparams': 'tab=' + self.__regid__,
                '__redirectpath': archive_unit.rest_path()}

    def parent(self, entity):
        return parent_archive_unit(entity)


class ArchiveUnitContentTab(ArchiveUnitSubObjectsTab):
    """Display content information about an archive unit."""

    __regid__ = 'seda_au_content_tab'

    rtype_role_targets = [('seda_content', 'object', None)]

    _('creating SEDAContent (SEDAContent seda_content '
      'SEDASeqAltArchiveUnitArchiveUnitRefIdManagement %(linkto)s)')

    def display_subobjects_list(self, entity):
        rset = entity.related('seda_content', 'object')
        self._cw.view('list', rset=rset, parent=self.parent(entity), w=self.w,
                      subvid=self.subvid, tabid=self.__regid__, delete=len(rset) > 1)


class SimplifiedArchiveUnitContentTab(tabs.TabsMixin, EntityView):
    """Display content information about an archive unit of a simplified profile: direct link to
    some content's attributes.
    """

    __regid__ = 'seda_au_content_tab'
    __select__ = ArchiveUnitContentTab.__select__ & simplified_profile()

    def entity_call(self, entity):
        seq = entity.first_level_choice.content_sequence
        content = seq.related('seda_content', 'object').one()
        content.view('seda.simplified_au_content', w=self.w)


class SimplifiedArchiveUnitContentView(tabs.PrimaryTab):
    """SEDAContent view for underlying SimplifiedArchiveUnitContentTab."""

    __regid__ = 'seda.simplified_au_content'
    __select__ = is_instance('SEDAContent')

    rtype_role_targets = [
        ('seda_description_level', 'subject', None),
        ('seda_title', 'object', None),
        ('seda_start_date', 'object', None),
        ('seda_end_date', 'object', None),
        ('seda_description', 'object', None),
        ('seda_originating_agency_from', 'object', None),
        ('seda_transferring_agency_archive_unit_identifier', 'object', None),
        ('seda_language_from', 'object', None),
    ]
    rsection, display_ctrl = rtags_from_rtype_role_targets('SEDAContent', rtype_role_targets)


class SimplifiedArchiveUnitIndexationTab(tabs.TabsMixin, EntityView):
    """Display content's indexation about an archive unit of a simplified profile.
    """

    __regid__ = 'seda_au_indexation_tab'
    __select__ = ArchiveUnitContentTab.__select__ & simplified_profile()

    def entity_call(self, entity):
        seq = entity.first_level_choice.content_sequence
        content = seq.related('seda_content', 'object').one()
        content.view('seda_content_indexation_tab', w=self.w)


class SimplifiedArchiveUnitContentIndexationView(content.ContentIndexationTab):

    __select__ = content.ContentIndexationTab.__select__ & simplified_profile()

    rtype_role_targets = [('seda_keyword', 'object', 'SEDAKeyword')]
    tabid = 'seda_au_indexation_tab'

    def url_params(self, entity):
        params = super(SimplifiedArchiveUnitContentIndexationView, self).url_params(entity)
        params['__redirectpath'] = self.parent(entity).rest_path()
        return params

    def parent(self, entity):
        return (entity.seda_content[0]
                .reverse_seda_seq_alt_archive_unit_archive_unit_ref_id_management[0]
                .reverse_seda_alt_archive_unit_archive_unit_ref_id[0])


class SimplifiedArchiveUnitHistoryTab(tabs.TabsMixin, EntityView):
    """Display content's custodial history about an archive unit of a simplified profile.
    """

    __regid__ = 'seda_au_history_tab'
    __select__ = ArchiveUnitContentTab.__select__ & simplified_profile()

    def entity_call(self, entity):
        seq = entity.first_level_choice.content_sequence
        content = seq.related('seda_content', 'object').one()
        content.view('seda_content_history_tab', w=self.w)


class SimplifiedArchiveUnitContentHistoryView(content.ContentHistoryTab):

    __select__ = content.ContentHistoryTab.__select__ & simplified_profile()

    tabid = 'seda_au_history_tab'

    def url_params(self, entity):
        params = super(SimplifiedArchiveUnitContentHistoryView, self).url_params(entity)
        params['__redirectpath'] = self.parent(entity).rest_path()
        return params

    def parent(self, entity):
        # return parent archive unit for the SEDAContent entity
        return (entity.seda_content[0]
                .reverse_seda_seq_alt_archive_unit_archive_unit_ref_id_management[0]
                .reverse_seda_alt_archive_unit_archive_unit_ref_id[0])


class ArchiveUnitArchiveUnitsTab(tabs.TabsMixin, EntityView):
    """Tab for sub-archive units of an archive unit"""

    __regid__ = 'seda_au_archive_units_tab'
    __select__ = is_instance('SEDAArchiveUnit') & ~is_archive_unit_ref()

    rtype = 'seda_archive_unit'
    role = 'object'

    _('creating SEDAArchiveUnit (SEDAArchiveUnit seda_archive_unit '
      'SEDASeqAltArchiveUnitArchiveUnitRefIdManagement %(linkto)s)')

    sub_unit_types = [('unit_content', _('archive unit (content)')),
                      ('unit_ref', _('archive unit (reference)'))]

    def entity_call(self, entity):
        seq = entity.first_level_choice.content_sequence
        urlparams = {'__redirectparams': 'tab=' + self.__regid__,
                     '__redirectpath': entity.rest_path()}
        links = []
        for unit_type, label in self.sub_unit_types:
            urlparams['unit_type'] = unit_type
            link = add_subobject_link(seq, self.rtype, self.role, urlparams,
                                      msg=self._cw._(label), klass='')
            if link:
                links.append(link)
        if links:
            add_link = dropdown_button(entity._cw.__('add'), links)
            self.w(add_link)
            self.w(tags.div(klass='clearfix'))
        rset = seq.related(self.rtype, self.role)
        if rset:
            subvid = 'seda.listitem'
            self._cw.view('list', rset=rset, w=self.w, subvid=subvid, parent=entity,
                          tabid=self.__regid__)


class SimplifiedArchiveUnitArchiveUnitsTab(ArchiveUnitArchiveUnitsTab):

    __select__ = ArchiveUnitArchiveUnitsTab.__select__ & simplified_profile()

    sub_unit_types = [('unit_content', _('seda_archive_unit_object'))]


class ArchiveUnitDataObjectReferencesTab(ArchiveUnitSubObjectsTab):
    """Tab for data object references of an archive unit"""

    __regid__ = 'seda_au_data_objects_refs_tab'

    rtype_role_targets = [('seda_data_object_reference', 'object', None)]

    _('creating SEDADataObjectReference (SEDADataObjectReference seda_data_object_reference '
      'SEDASeqAltArchiveUnitArchiveUnitRefIdManagement %(linkto)s)')


class SimplifiedArchiveUnitDataObjectReferencesTab(ArchiveUnitDataObjectReferencesTab):
    """Tab for data object references of an archive unit within a simplified transfer: see
    referenced data object as if they were children of the archive unit referencing them (only one
    reference is allowed in such case, so this is fine).
    """

    __select__ = ArchiveUnitDataObjectReferencesTab.__select__ & simplified_profile()

    rtype_role_targets = [('seda_binary_data_object', 'object', 'SEDABinaryDataObject')]

    def display_add_button(self, entity):
        rtype_roles = [(rtype, role) for rtype, role, _ in self.rtype_role_targets]
        params = self.url_params(entity)
        params['referenced_by'] = text_type(entity.eid)
        transfer = entity.container[0]
        if transfer.cw_etype == 'SEDAArchiveTransfer':
            button = add_subobjects_button(transfer, rtype_roles, params)
        else:
            if has_rel_perm('add', entity, 'seda_data_object_reference', 'object'):
                vreg = self._cw.vreg
                url = vreg['etypes'].etype_class('SEDABinaryDataObject').cw_create_url(
                    self._cw, **params)
                msg = self._cw.__('seda_binary_data_object_object')
                link = tags.a(msg, href=url, title=self._cw.__('New SEDABinaryDataObject'))
                button = dropdown_button(entity._cw._(msg), [link])
            else:
                button = None
        if button:
            # No button if user cannot add any relation.
            self.w(button)
            self.w(tags.div(klass='clearfix'))

    def display_subobjects_list(self, entity):
        rset = self._cw.execute(
            'Any DO, DOID, DOUC ORDERBY DOID WHERE '
            'DO id DOID, DO user_cardinality DOUC, '
            'REF seda_data_object_reference_id DO, REF seda_data_object_reference SEQ, '
            'SEQ eid %(x)s', {'x': entity.eid})
        if rset:
            self._cw.view('list', rset=rset, parent=self.parent(entity), w=self.w,
                          subvid=self.subvid, tabid=self.tabid)


# Top level ArchiveUnit form: create to distinct forms, one form archive unit reference and the
# other for archive unit content. This is done by a mix of uicfg, form and renderer customization
# depending on a 'unit_type' parameter in form params.

pvs.tag_object_of(('*', 'seda_data_object_reference',
                   'SEDASeqAltArchiveUnitArchiveUnitRefIdManagement'),
                  'hidden')
afs.tag_object_of(('*', 'seda_data_object_reference',
                   'SEDASeqAltArchiveUnitArchiveUnitRefIdManagement'),
                  'main', 'hidden')


au_ref_afs = copy_rtag(afs, __name__,
                       is_instance('SEDAAltArchiveUnitArchiveUnitRefId')
                       & is_archive_unit_ref())
au_ref_afs.tag_object_of(
    ('*', 'seda_archive_unit_ref_id_from', 'SEDAAltArchiveUnitArchiveUnitRefId'),
    'inlined', 'inlined')
au_ref_afs.tag_subject_of(
    ('SEDAAltArchiveUnitArchiveUnitRefId',
     'seda_seq_alt_archive_unit_archive_unit_ref_id_management', '*'),
    'inlined', 'hidden')

au_content_afs = copy_rtag(afs, __name__,
                           is_instance('SEDAAltArchiveUnitArchiveUnitRefId')
                           & ~is_archive_unit_ref())
au_content_afs.tag_object_of(
    ('*', 'seda_archive_unit_ref_id_from', 'SEDAAltArchiveUnitArchiveUnitRefId'),
    'inlined', 'hidden')
au_content_afs.tag_subject_of(
    ('SEDAAltArchiveUnitArchiveUnitRefId',
     'seda_seq_alt_archive_unit_archive_unit_ref_id_management', '*'),
    'inlined', 'inlined')


class AltArchiveUnitRefIdSimplifiedAutomaticEntityForm(widgets.SimplifiedAutomaticEntityForm):
    """Force display of AltArchiveUnitArchiveUnitRefId's sub-ArchiveUnitRefId or
    SeqAltArchiveUnitArchiveUnitRefIdManagement (uicfg will control which of them is displayed).
    """

    __select__ = (widgets.SimplifiedAutomaticEntityForm.__select__
                  & is_instance('SEDAAltArchiveUnitArchiveUnitRefId'))


class ArchiveUnitNoTitleEntityInlinedFormRenderer(widgets.NoTitleEntityInlinedFormRenderer):
    """Don't display any title nor remove link for AltArchiveUnitArchiveUnitRefId,
    SeqAltArchiveUnitArchiveUnitRefIdManagement or ArchiveUnitRefId in the context of an archive
    unit reference.
    """

    __select__ = (widgets.NoTitleEntityInlinedFormRenderer.__select__
                  & (is_instance('SEDAAltArchiveUnitArchiveUnitRefId',
                                 'SEDASeqAltArchiveUnitArchiveUnitRefIdManagement')
                     | (is_instance('SEDAArchiveUnitRefId')
                        & is_archive_unit_ref())))


bdo_afs = copy_rtag(afs, __name__,
                    is_instance('SEDABinaryDataObject', 'SEDAPhysicalDataObject')
                    & simplified_profile())
bdo_afs.tag_object_of(
    ('SEDADataObjectReference', 'seda_data_object_reference_id', '*'),
    'main', 'inlined')
bdo_afs.tag_object_of(
    ('SEDACustodialHistoryFile', 'seda_data_object_reference_id', '*'),
    'main', 'hidden')

do_ref_afs = copy_rtag(afs, __name__,
                       # Add yes to overtake afs for DataObjectReference defined in content
                       is_instance('SEDADataObjectReference') & simplified_profile() & yes())
do_ref_afs.tag_subject_of(
    ('SEDADataObjectReference', 'seda_data_object_reference_id', '*'),
    'inlined', 'hidden')
do_ref_afs.tag_attribute(
    ('SEDADataObjectReference', 'user_cardinality'),
    'inlined', 'hidden')


class DataObjectSimplifiedAutomaticEntityForm(widgets.SimplifiedAutomaticEntityForm):
    """On creation of a BinaryDataObject or PhysicalDataObject's in the context of a simplified
    profile, add a field to handle the creation of the relation to the archive unit specified in
    `req.form`.
    """

    # don't add match_form_params('referenced_by') since it's only specified for creation, not
    # edition
    __select__ = (widgets.SimplifiedAutomaticEntityForm.__select__
                  & is_instance('SEDABinaryDataObject', 'SEDAPhysicalDataObject')
                  & simplified_profile())

    def inlined_form_views(self):
        views = super(DataObjectSimplifiedAutomaticEntityForm, self).inlined_form_views()
        ref_forms = [v.form for v in views if v.rtype == 'seda_data_object_reference_id']
        if ref_forms:  # may be empty if user has no write access
            ref_form = ref_forms[0]
            if not ref_form.edited_entity.has_eid() and not ref_form.posting:
                ref_form.add_hidden(name='seda_data_object_reference', eidparam=True,
                                    role='subject',
                                    value=self._cw.form['referenced_by'])
        return views


class DataObjectReferenceNoTitleEntityInlinedFormRenderer(widgets.NoTitleEntityInlinedFormRenderer):
    """Don't display any title nor remove link for DataObjectReference in the context of a
    simplified profile.
    """

    __select__ = (widgets.NoTitleEntityInlinedFormRenderer.__select__
                  & is_instance('SEDADataObjectReference')
                  & simplified_profile())
