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
"""Library of views use there and there in the interface"""

from cubicweb import tags, _
from cubicweb.predicates import match_kwargs, is_instance
from cubicweb.view import EntityView
from cubicweb.web.views import tabs

from cubes.seda.xsd2uicfg import FIRST_LEVEL_ETYPES
from cubes.seda.views import add_subobjects_button


class XSDMetaEntityView(EntityView):
    __regid__ = 'seda.xsdmeta'

    def entity_call(self, entity, skip_one_card=False, with_annotation=True):
        cardinality = getattr(entity, 'user_cardinality', '1')
        if cardinality != '1' or not skip_one_card:
            self.w(u' <span class="cardinality">[%s]</span>' % cardinality)
        if with_annotation:
            description = getattr(entity, 'user_annotation', None)
            if description:
                self.w(u' <span class="description text-muted">%s</span>' % description)


class TextEntityAttributeView(EntityView):
    """Attribute view for SEDA relations displaying entity as text (no link to the entity)
    """
    __regid__ = 'seda.reledit.text'
    subvid = 'seda.business'

    def entity_call(self, entity, **kwargs):
        self.w(u'<div>')
        entity.view(self.subvid, w=self.w)
        entity.view('seda.xsdmeta', w=self.w)
        self.w(u'</div>')


class SimpleLinkToEntityAttributeView(TextEntityAttributeView):
    """Attribute view for SEDA relations linking directly to an entity without intermediary entity
    """
    __regid__ = 'seda.reledit.simplelink'
    subvid = 'oneline'


class ComplexLinkEntityAttributeView(EntityView):
    """Attribute view for SEDA relations linking to an entity through an intermediary entity holding
    cardinalities / annotation
    """
    __regid__ = 'seda.reledit.complexlink'

    def entity_call(self, entity):
        rtype = self.cw_extra_kwargs['rtype'].replace('_from', '_to')
        value_rset = entity.related(rtype)
        self.w(u'<div>')
        if value_rset:
            self.w(u'<span class="value">')
            self._cw.view('csv', value_rset, w=self.w)
            self.w(u'</span>')
        else:
            self.wdata(self._cw._('<no value specified>'))
        entity.view('seda.xsdmeta', w=self.w)
        self.w(u'</div>')


class AlternativeEntityAttributeView(EntityView):
    """Attribute view for SEDA alternative entities"""
    __regid__ = 'seda.reledit.alternative'

    def entity_call(self, entity):
        alternatives = []
        for rschema, _targets, role in entity.e_schema.relation_definitions():
            rtype = rschema.type
            if rtype.startswith('seda_') and rtype != self.cw_extra_kwargs['rtype']:
                target_rset = entity.related(rtype, role)
                if target_rset:
                    alternatives.append(self._cw.view('seda.type_meta', rset=target_rset))
        self.w(u'<div class="alternative">')
        if alternatives:
            self.w((' <b>%s</b> ' % self._cw._(' ALT_I18N ')).join(alternatives))
        else:
            self.wdata(self._cw._('<no value specified>'))
        entity.view('seda.xsdmeta', w=self.w)
        self.w(u'</div>')


class BusinessValueEntityView(EntityView):
    """Entity view that will display value of the attribute specified by `value_attr` on the
    entity's class
    """
    __regid__ = 'seda.business'
    no_value_msg = _('<no value specified>')

    def entity_call(self, entity):
        value = self.entity_value(entity)
        if value:
            self.w(u'<span class="value">')
            self.w(value)
            self.w(u'</span>')
        else:
            self.wdata(self._cw._(self.no_value_msg))

    def entity_value(self, entity):
        if entity.value_attr:
            value = entity.printable_value(entity.value_attr)
        else:
            value = None
        return value


class BusinessValueConceptEntityView(BusinessValueEntityView):
    """Specific business value view for concept entity: simply display the concept's label as text.
    """
    __select__ = is_instance('Concept')

    def entity_value(self, entity):
        return entity.label()


class BusinessValueLinkEntityView(BusinessValueEntityView):
    """Similar to seda.business but value is enclosed in a link if some value is specified."""
    __select__ = is_instance(*FIRST_LEVEL_ETYPES)

    def entity_value(self, entity):
        value = super(BusinessValueLinkEntityView, self).entity_value(entity)
        if value:
            value = tags.a(value, href=entity.absolute_url())
        return value


class LinkMetaEntityView(EntityView):
    """Glue seda.business and seda.xsdmeta views together, for use within list."""
    __regid__ = 'seda.link_meta'

    def entity_call(self, entity):
        entity.view('seda.business', w=self.w)
        entity.view('seda.xsdmeta', w=self.w, skip_one_card=True)


class TypeAndMetaEntityView(EntityView):
    """Glue entity's type, seda.business and seda.xsdmeta views together, for use within alternative
    """
    __regid__ = 'seda.type_meta'

    def entity_call(self, entity):
        self.w(entity.dc_type() + u' ')
        entity.view('seda.business', w=self.w)
        entity.view('seda.xsdmeta', w=self.w, skip_one_card=True)


class ListItemView(EntityView):
    """Extended 'oneline' view for entities related to an Agent, including link to remove the
    relation.
    """
    __regid__ = 'seda.listitem'
    __select__ = EntityView.__select__ & match_kwargs('parent', 'tabid')
    business_vid = 'seda.link_meta'

    def entity_call(self, entity, parent, tabid, edit=True, delete=True):
        entity.view(self.business_vid, w=self.w)
        if entity.cw_has_perm('update'):
            self._cw.add_js(('cubicweb.ajax.js', 'cubes.seda.js'))
            editurlparams = {
                '__redirectpath': parent.rest_path(),
                '__redirectparams': 'tab=' + tabid
            }
            if edit or delete:
                self.w(u'<div class="pull-right">')
                if edit:
                    self.w(tags.a(title=self._cw.__('edit'), klass='icon-pencil',
                                  href=entity.absolute_url(vid='edition', **editurlparams)))
                if delete:
                    self.w(tags.a(title=self._cw.__('delete'), klass='icon-trash',
                                  href=entity.absolute_url(vid='deleteconf', **editurlparams)))
                self.w(u'</div>')


class TypeListItemView(ListItemView):
    """Extended 'oneline' view for entities with type."""
    __regid__ = 'seda.type_listitem'
    business_vid = 'seda.type_meta'


class SubObjectsTab(tabs.TabsMixin, EntityView):
    """Base class for tabs with a 'add' button and one or more list of subobjects, driven by the
    `rtype_role_targets` class attribute
    """
    rtype_role_targets = None
    subvid = 'seda.listitem'

    @property
    def tabid(self):
        return self.__regid__

    def entity_call(self, entity):
        self.display_add_button(entity)
        self.display_subobjects_list(entity)

    def display_add_button(self, entity):
        rtype_roles = [(rtype, role) for rtype, role, _ in self.rtype_role_targets]
        button = add_subobjects_button(entity, rtype_roles, self.url_params(entity))
        if button:
            # No button if user cannot add any relation.
            self.w(button)
            self.w(tags.div(klass='clearfix'))

    def display_subobjects_list(self, entity):
        for rtype, role, target in self.rtype_role_targets:
            rset = entity.related(rtype, role)
            if rset:
                if target is not None:
                    self.w('<h2>%s</h2>' % self._cw.__(target + '_plural'))
                self._cw.view('list', rset=rset, parent=self.parent(entity), w=self.w,
                              subvid=self.subvid, tabid=self.tabid)

    def url_params(self, entity):
        return {'__redirectparams': 'tab=' + self.tabid}

    def parent(self, entity):
        return entity
