# coding: utf-8
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
"""cubicweb-saem-ref site customizations"""

import pytz

from logilab.common.date import ustrftime
from logilab.common.decorators import monkeypatch

from cubicweb import cwvreg, _
from cubicweb.cwconfig import register_persistent_options
from cubicweb.uilib import PRINTERS

from cubes.skos import rdfio
from cubes.skos.ccplugin import ImportSkosData
from cubes.seda import dataimport as seda
# XXX during 0.13 migration where seda isn't yet there, ensure it's site_cubicweb is loaded because
# we need some monkey-patches there to import seda code
from cubes.seda import site_cubicweb  # noqa

from cubes.saem_ref import permanent_url
# this import is needed to take account of pg_trgm monkeypatches
# while executing cubicweb-ctl commands (db-rebuild-fti)
from cubes.saem_ref import pg_trgm  # noqa pylint: disable=unused-import


# configure RDF generator to use ark based uri as canonical uris, and deactivating implicit
# 'same_as_urls' in this case

orig_same_as_uris = rdfio.RDFGraphGenerator.same_as_uris


@monkeypatch(rdfio.RDFGraphGenerator, methodname='same_as_uris')
@staticmethod
def same_as_uris(entity):
    if entity.cwuri.startswith('ark:'):
        return ()
    return orig_same_as_uris(entity)


@monkeypatch(rdfio.RDFGraphGenerator, methodname='canonical_uri')
@staticmethod
def canonical_uri(entity):
    return permanent_url(entity)


# deactivate date-format and datetime-format cw properties. This is because we do some advanced date
# manipulation such as allowing partial date and this is not generic enough to allow arbitrary
# setting of date and time formats

base_user_property_keys = cwvreg.CWRegistryStore.user_property_keys


@monkeypatch(cwvreg.CWRegistryStore)
def user_property_keys(self, withsitewide=False):
    props = base_user_property_keys(self, withsitewide)
    return [prop for prop in props if prop not in ('ui.date-format', 'ui.datetime-format')]

# customize display of TZDatetime

register_persistent_options((
    ('timezone',
     {'type': 'choice',
      'choices': pytz.common_timezones,
      'default': 'Europe/Paris',
      'help': _('timezone in which time should be displayed'),
      'group': 'ui', 'sitewide': True,
      }),
))


def print_tzdatetime_local(value, req, *args, **kwargs):
    tz = pytz.timezone(req.property_value('ui.timezone'))
    value = value.replace(tzinfo=pytz.utc).astimezone(tz)
    return ustrftime(value, req.property_value('ui.datetime-format'))

PRINTERS['TZDatetime'] = print_tzdatetime_local


# configure c-c skos-import command's factories to use with proper metadata generator ##############

def _massive_store_factory(cnx):
    from cubicweb.dataimport.massive_store import MassiveObjectStore
    from cubes.saem_ref.sobjects.skos import SAEMMetadataGenerator
    return MassiveObjectStore(cnx, metagen=SAEMMetadataGenerator(cnx))


def _nohook_store_factory(cnx):
    from cubicweb.dataimport.stores import NoHooRQLObjectStore
    from cubes.saem_ref.sobjects.skos import SAEMMetadataGenerator
    return NoHooRQLObjectStore(cnx, metagen=SAEMMetadataGenerator(cnx))


ImportSkosData.cw_store_factories['massive'] = _massive_store_factory
ImportSkosData.cw_store_factories['nohook'] = _nohook_store_factory


# override seda's scheme initialization to set ark on each scheme, and to use an ark enabled store

@monkeypatch(seda)
def init_seda_scheme(cnx, title, _count=[0]):
    description = u'edition 2009' if title.startswith('SEDA :') else None
    # 25651 = Archives départementales de la Gironde (ADGIRONDE)
    # XXX ensure that:
    # * NAA for those vocabulary is 25651
    # * generated ark are identical from one instance to another (for scheme and concepts, see
    #   below)
    _count[0] += 1
    ark = u'25651/v%s' % _count[0]
    scheme = cnx.create_entity('ConceptScheme', title=title, description=description, ark=ark)
    seda.EXTID2EID_CACHE['ark:/' + ark] = scheme.eid
    return scheme


@monkeypatch(seda)
def get_store(cnx):
    from cubes.saem_ref.sobjects.skos import SAEMMetadataGenerator
    metagen = SAEMMetadataGenerator(cnx, naa_what='25651')
    if cnx.repo.system_source.dbdriver == 'postgres':
        from cubicweb.dataimport.massive_store import MassiveObjectStore
        return MassiveObjectStore(cnx, metagen=metagen, eids_seq_range=1000)
    else:
        from cubicweb.dataimport.stores import NoHookRQLObjectStore
        return NoHookRQLObjectStore(cnx, metagen=metagen)


####################################################################################################
# temporary monkey-patches #########################################################################
####################################################################################################

from yams.constraints import Attribute, BoundaryConstraint, cstr_json_loads  # noqa


@monkeypatch(BoundaryConstraint, methodname='deserialize')
@classmethod
def deserialize(cls, value):
    """simple text deserialization"""
    try:
        values = cstr_json_loads(value)
        return cls(**values)
    except ValueError:
        try:
            value, msg = value.split('\n', 1)
        except ValueError:
            msg = None
        op, boundary = value.split(' ', 1)
        return cls(op, eval(boundary), msg or None)


# monkey patch RDFGraphGenerator for proper URI generation untile skos 1.0 is out

@monkeypatch(rdfio.RDFGraphGenerator)
def add_entity(self, entity, reg):
    """Add information about a single entity as defined in the given RDF registry into the RDF
    graph and return related entities for eventual further processing.
    """
    graph = self._graph
    etype = entity.cw_etype
    if etype not in reg.etype2rdf:
        return ()
    uri = graph.uri(self.canonical_uri(entity))
    graph.add(uri, self._type_predicate, graph.uri(reg.etype2rdf[etype]))
    for same_as_uri in self.same_as_uris(entity):
        graph.add(uri, self._same_as_predicate, graph.uri(same_as_uri))
    related = set()
    for rtype, predicate_uri, reverse in reg.predicates_for_subject_etype(etype):
        values = getattr(entity, rtype)
        if values is None:
            continue
        if isinstance(values, (tuple, list)):  # relation
            self._add_relations(uri, predicate_uri, reverse, values)
            related.update(values)
        else:  # attribute.
            assert not reverse, (uri, rtype, predicate_uri, reverse)
            graph.add(uri, graph.uri(predicate_uri), values)
    for rtype, predicate_uri, reverse in reg.predicates_for_object_etype(etype):
        try:
            values = getattr(entity, 'reverse_' + rtype)
        except AttributeError:
            # symmetric relations have no 'reverse_' attribute
            # XXX what if this is simply a bad mapping?
            continue
        related.update(values)
        self._add_relations(uri, predicate_uri, not reverse, values)
    return related


@monkeypatch(rdfio.RDFGraphGenerator)
def _add_relations(self, uri, predicate_uri, reverse, related_entities):
    """Add information about relations with `predicate_uri` between entity with `uri` and
    `related_entities` to the graph.
    """
    graph = self._graph
    predicate = graph.uri(predicate_uri)
    for related_entity in related_entities:
        r_uri = graph.uri(self.canonical_uri(related_entity))
        if reverse:
            graph.add(r_uri, predicate, uri)
        else:
            graph.add(uri, predicate, r_uri)
