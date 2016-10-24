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
"""cubicweb-seda views for data objects (BinaryDataObject / PhysicalDataObject)"""

import json

from six import text_type

from logilab.mtconverter import xml_escape

from cubicweb import tags, view, _
from cubicweb.predicates import match_form_params, is_instance
from cubicweb.web.views import uicfg, tabs, ibreadcrumbs

from cubes.relationwidget import views as rwdg
from cubes.skos.views import widgets as skos

from cubes.seda.xsd2yams import RDEF_CONSTRAINTS
from cubes.seda.entities import parent_and_container, simplified_profile, full_seda2_profile
from cubes.seda.views import rtags_from_xsd_element, add_subobject_link
from cubes.seda.views import viewlib, copy_rtag
from cubes.seda.views import uicfg as sedauicfg  # noqa - ensure those rules are defined first


pvs = uicfg.primaryview_section
pvdc = uicfg.primaryview_display_ctrl
rec = uicfg.reledit_ctrl
afs = uicfg.autoform_section
affk = uicfg.autoform_field_kwargs


class ContainedRelationFacetWidget(rwdg.RelationFacetWidget):

    def _render_triggers(self, w, domid, form, field, rtype):
        parent, container = parent_and_container(form.edited_entity)
        assert container is not None
        if container.cw_etype != 'SEDAArchiveTransfer':
            w('XXX FIXME')
            return
        req = form._cw
        try:
            constraint = RDEF_CONSTRAINTS[(form.edited_entity.cw_etype, field.name)]
        except KeyError:
            constraint = RDEF_CONSTRAINTS[field.name]
        rql = 'Any CS WHERE ' + (
            constraint.replace('O in_scheme CS, ', '').replace(', S container AT', ''))
        rql += ', AT eid %(at)s'
        if not req.execute(rql, {'at': container.eid}):
            scheme_relations = [x for x in rql.split() if x.startswith('seda_')]
            if len(scheme_relations) == 1:
                scheme_relation = req._(scheme_relations[0])
            else:
                scheme_relation = req.__(scheme_relations[0] + '_object')
            w(req._('you must specify a scheme for {0} to select a value').format(
                scheme_relation))
        else:
            return super(ContainedRelationFacetWidget, self)._render_triggers(
                w, domid, form, field, rtype)

    def trigger_search_url(self, entity, url_params):
        """Overriden to add information about who is the container

        This information will be used later for proper vocabulary computation.
        """
        # first retrieve the container entity
        _, container = parent_and_container(entity)
        # and put it as an extra url param
        if container is not None:
            url_params['container'] = text_type(container.eid)
        return super(ContainedRelationFacetWidget, self).trigger_search_url(entity, url_params)


class ContainedSearchForRelatedEntitiesView(skos.SearchForRelatedConceptsView):

    __select__ = skos.SearchForRelatedConceptsView.__select__ & match_form_params('container')

    def constrained_rql(self):
        container = int(self._cw.form['container'])
        constraints = self.schema_rdef.constraints
        assert len(constraints) == 1 and 'S container AT' in constraints[0].expression, constraints
        baserql = constraints[0].expression
        baserql = baserql.replace('S container AT', 'AT eid %(at)s')
        return baserql, {'at': container}


pvs.tag_object_of(('*', 'seda_data_object_reference_id', '*'),
                  'relations')
pvdc.tag_object_of(('*', 'seda_data_object_reference_id', '*'),
                   {'vid': 'autolimited',
                    'subvid': 'seda.object-ref.archive-unit',
                    'label': _('referenced by:')})

pvs.tag_subject_of(('*', 'seda_algorithm', '*'), 'attributes')
pvs.tag_object_of(('*', 'seda_target', '*'), 'hidden')  # in the relationship tab

simplified_pvs = copy_rtag(pvs, __name__,
                           is_instance('SEDABinaryDataObject') & simplified_profile())
simplified_pvs.tag_object_of(('*', 'seda_data_object_reference_id', '*'), 'hidden')

for rtype in ('seda_compressed', 'seda_data_object_version_from'):
    # hide relation from autoform because of limitation of _container_eid
    afs.tag_object_of(('*', rtype, '*'), 'main', 'hidden')
    pvs.tag_object_of(('*', rtype, '*'), 'attributes')
    rec.tag_object_of(('*', rtype, '*'),
                      {'rvid': 'seda.reledit.complexlink',
                       'novalue_label': _('<unauthorized>')})
    simplified_pvs.tag_object_of(('*', rtype, '*'), 'hidden')

rec.tag_subject_of(('SEDABinaryDataObject', 'seda_alt_binary_data_object_attachment', '*'),
                   {'rvid': 'seda.reledit.alternative',
                    'novalue_label': _('<unauthorized>')})


def uri_cardinality_vocabulary(form, field):
    req = form._cw
    if form.edited_entity.has_eid():
        parent_type = form.edited_entity.cw_adapt_to('IContained').parent.cw_etype
    else:
        try:
            # inlined creation form
            parent_type = json.loads(req.form['arg'][1])
        except KeyError:
            # edition through reledit
            parent_eid = req.form['eid']
            parent_type = req.describe(int(parent_eid))[0]
    if parent_type in ('SEDABinaryDataObject', 'SEDAAltBinaryDataObjectAttachment'):
        return [u'1']
    return [u'0..1', u'1']

affk.tag_attribute(('SEDAUri', 'user_cardinality'),
                   {'choices': uri_cardinality_vocabulary})


for key, rql_expr in RDEF_CONSTRAINTS.items():
    if 'S container AT' in rql_expr:
        try:
            etype, rtype = key
        except ValueError:
            etype = '*'
            rtype = key
        if rtype == 'seda_rule':
            continue  # managed in mgmt_rules module
        affk.tag_subject_of((etype, rtype, '*'),
                            {'widget': ContainedRelationFacetWidget(dialog_options={'width': 800})})


bdo_ordered_fields = [
    ('id', 'subject'),
    ('user_cardinality', 'subject'),
    ('user_annotation', 'subject'),
    ('filename', 'subject'),
    ('seda_compressed', 'object'),
    ('seda_data_object_version_from', 'object'),
    ('seda_algorithm', 'object'),
]
affk.set_fields_order('SEDABinaryDataObject', bdo_ordered_fields)
pvdc.set_fields_order('SEDABinaryDataObject', bdo_ordered_fields)


class BinaryDataObjectTabbedPrimaryView(tabs.TabbedPrimaryView):

    __select__ = tabs.TabbedPrimaryView.__select__ & is_instance('SEDABinaryDataObject')
    tabs = [
        'main_tab',
        _('seda_bdo_format_identification'),
        _('seda_bdo_file_information'),
        _('seda_do_relations'),
    ]


class BinaryDataObjectFormatIdentificationTab(tabs.PrimaryTab):
    """Display format identification information of a binary data object"""

    __regid__ = 'seda_bdo_format_identification'
    __select__ = tabs.PrimaryTab.__select__ & is_instance('SEDABinaryDataObject')

    rsection, display_ctrl = rtags_from_xsd_element('SEDABinaryDataObject', 'FormatIdentification')


class SimplifiedBinaryDataObjectFormatIdentificationTab(BinaryDataObjectFormatIdentificationTab):

    __select__ = BinaryDataObjectFormatIdentificationTab.__select__ & simplified_profile()

    rsection, display_ctrl = rtags_from_xsd_element('SEDABinaryDataObject', 'FormatIdentification')
    rsection.tag_object_of(('*', 'seda_format_id_from', 'SEDABinaryDataObject'), 'hidden')


class BinaryDataObjectFileInfoTab(tabs.PrimaryTab):
    """Display file information of a binary data object"""

    __regid__ = 'seda_bdo_file_information'
    __select__ = is_instance('SEDABinaryDataObject') & full_seda2_profile()

    rsection, display_ctrl = rtags_from_xsd_element('SEDABinaryDataObject', 'FileInfo')


class PhysicalDataObjectTabbedPrimaryView(tabs.TabbedPrimaryView):

    __select__ = tabs.TabbedPrimaryView.__select__ & is_instance('SEDAPhysicalDataObject')
    tabs = [
        'main_tab',
        _('seda_pdo_dimensions'),
        _('seda_do_relations'),
    ]


class PhysicalDataObjectDimensionsTab(tabs.PrimaryTab):
    """Display physical dimensions of a physical data object"""

    __regid__ = 'seda_pdo_dimensions'
    __select__ = tabs.PrimaryTab.__select__ & is_instance('SEDAPhysicalDataObject')

    rsection, display_ctrl = rtags_from_xsd_element('SEDAPhysicalDataObject', 'PhysicalDimensions')


class DataObjectRelationsTab(tabs.PrimaryTab):
    """Display relations of a binary or physical data object"""

    __regid__ = 'seda_do_relations'
    __select__ = (is_instance('SEDABinaryDataObject', 'SEDAPhysicalDataObject')
                  & full_seda2_profile())

    _('creating SEDARelationship (SEDARelationship seda_relationship '
      'SEDABinaryDataObject %(linkto)s)')
    _('creating SEDARelationship (SEDARelationship seda_relationship '
      'SEDAPhysicalDataObject %(linkto)s)')

    def entity_call(self, entity):
        rschema = self._cw.vreg.schema.rschema('seda_relationship')
        if rschema.has_perm(self._cw, 'add', toeid=entity.eid):
            urlparams = {'__redirectparams': 'tab=' + self.__regid__}
            self.w(add_subobject_link(entity, 'seda_relationship', 'object', urlparams,
                                      msg=self._cw._('add a SEDARelationship'),
                                      klass='btn btn-success pull-right'))
            self.w(tags.div(klass='clearfix'))
        rset = entity.related('seda_relationship', 'object')
        if rset:
            self._cw.view('list', rset=rset, parent=entity, w=self.w, tabid=self.__regid__,
                          subvid='seda.listitem')
        rset = entity.related('seda_target', 'object')
        if rset:
            self.w(u'<h2>{0}</h2>'.format(self._cw._('Relationship target of')))
            self.w(u'<div>{0}</div>'.format(
                self._cw._('This object is used as a relationship target of the following '
                           'entities')))
            self._cw.view('list', rset=rset, subvid='seda.relationship.reverse', w=self.w)


class RelationshipBusinessValueLinkEntityView(viewlib.BusinessValueLinkEntityView):

    __select__ = is_instance('SEDARelationship')

    def entity_value(self, entity):
        target = entity.seda_target[0] if entity.seda_target else None
        if target:
            value = tags.a(target.dc_title(), href=target.absolute_url())
        else:
            value = xml_escape(self._cw._('<no data-object specified>'))
        if entity.seda_type_relationship:
            concept = entity.seda_type_relationship[0]
            msg = self._cw._(', of relationship type %s') % concept.label()
        else:
            msg = self._cw._(', no relationship type specified')
        value += xml_escape(msg)
        return value


class RelationshipReverseEntityView(view.EntityView):

    __regid__ = 'seda.relationship.reverse'
    __select__ = is_instance('SEDARelationship')

    def entity_call(self, entity):
        target = entity.seda_relationship[0]
        self.w(tags.a(target.dc_title(), href=target.absolute_url()))
        if entity.seda_type_relationship:
            concept = entity.seda_type_relationship[0]
            msg = self._cw._(', of relationship type %s') % concept.label()
        else:
            msg = self._cw._(', no relationship type specified')
        self.w(xml_escape(msg))


class ObjectReferencepArchiveUnitEntityView(view.EntityView):

    __regid__ = 'seda.object-ref.archive-unit'
    __select__ = is_instance('SEDADataObjectReference')

    def entity_call(self, entity):
        au_seq = entity.seda_data_object_reference[0]
        au_choice = au_seq.reverse_seda_seq_alt_archive_unit_archive_unit_ref_id_management[0]
        archive_unit = au_choice.reverse_seda_alt_archive_unit_archive_unit_ref_id[0]
        self._cw.view('listitem', rset=archive_unit.as_rset(), w=self.w)


class UnitBusinessValueEntityView(viewlib.BusinessValueEntityView):

    __select__ = is_instance('SEDAWidth', 'SEDAHeight', 'SEDADepth', 'SEDAShape',
                             'SEDADiameter', 'SEDALength', 'SEDAThickness', 'SEDAWeight')

    def entity_call(self, entity):
        super(UnitBusinessValueEntityView, self).entity_call(entity)
        if entity.seda_unit:
            unit = self._cw._('unit: {0}').format(entity.seda_unit[0].label())
        else:
            unit = self._cw._('<no unit specified>')
        self.w(u' (%s)' % xml_escape(unit))


class IBreadCrumbsAdapter(ibreadcrumbs.IBreadCrumbsAdapter):
    """Override adapter from compound when BDO is within a simplified profile to display the archive
    unit as parent.
    """
    __select__ = is_instance('SEDABinaryDataObject') & simplified_profile()

    def parent_entity(self):
        return self.entity.cw_adapt_to('ITreeBase').parent()
