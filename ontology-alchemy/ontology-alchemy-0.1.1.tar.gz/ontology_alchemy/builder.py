from collections import defaultdict
from logging import getLogger

from rdflib import Literal, RDF
from six.moves.urllib.parse import urldefrag, urlparse
from toposort import toposort

from ontology_alchemy.base import RDFS_Class, RDFS_Property
from ontology_alchemy.constants import DEFAULT_LANGUAGE_TAG
from ontology_alchemy.schema import (
    is_a_property,
    is_a_literal,
    is_comment_predicate,
    is_domain_predicate,
    is_label_predicate,
    is_range_predicate,
    is_sub_class_predicate,
    is_type_predicate,
)


class OntologyBuilder(object):

    def __init__(self, graph, base_uri=None):
        """
        Build the Python class hierarchy representing the ontology given
        its triplestore graph.

        The supported vocabulary of asserted statements consists of the
        RDF Schema classes and properties as defined in https://www.w3.org/TR/rdf-schema/

        :param graph - the populated `rdflib.Graph` instance for the Ontology
        :param base_uri - The base URI namespace for the Ontology. If not provided,
            will try to infer from ontology definition directly.
        """
        self.base_uri = base_uri or self._infer_base_uri(graph)
        self.graph = graph
        self.namespace = {}
        self.logger = getLogger(__name__)

        self._type_graph = {}
        self._sub_class_graph = defaultdict(set)
        self._asserted_statements = set()

    def build_namespace(self):
        """
        Iterate over all RDF statements describing ontology in a stable ordering
        that guarantees type definitions and inheritance relationships are evaluated first,
        and build the Python class hierarchy under a common namespace object.

        :returns {dict} namespace containing all the defined Python classes

        """
        for s, p, o in self.graph:
            if is_type_predicate(p):
                self._type_graph[s] = o
            elif is_sub_class_predicate(p):
                self._sub_class_graph[s].add(o)
            else:
                self._asserted_statements.add((s, p, o))

        self._build_class_hierarchy()
        self._build_property_proxies()

        return self.namespace

    def add_class(self, class_uri, base_class_uris=None, is_property=False):
        class_name = self._extract_name(class_uri)

        base_classes = (RDFS_Property,) if is_property else (RDFS_Class,)
        if base_class_uris:
            base_classes = tuple(
                self.namespace[self._extract_name(base_class_uri)]
                for base_class_uri in base_class_uris
            )

        self.namespace[class_name] = type(
            class_name,
            base_classes,
            {"__uri__": class_uri}
        )
        self.logger.debug("_add_class() - Added class: %s", class_name)

    def add_property_domain(self, property_uri, domain_uri):
        property_name = self._extract_name(property_uri)
        domain_name = self._extract_name(domain_uri)
        domain_class = self.namespace[domain_name]
        self.namespace[property_name].domain += domain_class

    def add_property_range(self, property_uri, range_uri):
        property_name = self._extract_name(property_uri)
        range_class = self._resolve_range(range_uri)
        self.namespace[property_name].range += range_class

    def add_comment(self, class_uri, comment, lang=DEFAULT_LANGUAGE_TAG):
        class_name = self._extract_name(class_uri)
        self.namespace[class_name].comment += Literal(comment, lang=lang)

    def add_label(self, class_uri, label, lang=DEFAULT_LANGUAGE_TAG):
        class_name = self._extract_name(class_uri)
        self.namespace[class_name].label += Literal(label, lang=lang)

    def _extract_name(self, uri):
        return str(
            uri.replace(self.base_uri, "")
        )

    def _infer_base_uri(self, graph):
        """
        Attempt to infer automatically the base URI for the given ontology
        by looking at definitions.

        The simple heuristic employed is to URL-parse the subject of the first
        encountered triple with RDF.type as its predicate in the RDF graph and
        extract its last path component.

        :param graph - `rdflib.Graph` instance populated with ontology
        :returns {str} the inferred base URI

        """
        for s, p, o in graph.triples((None, RDF.type, None)):
            parsed_url = urlparse(s)
            if parsed_url.fragment:
                return "{}#".format(urldefrag(s)[0])
            else:
                return "{}/".format(s.rsplit('/', 1)[0])

    def _resolve_range(self, range_uri):
        """
        Resolve a rdfs.Property rdfs.range value to a type.

        """
        if is_a_literal(range_uri):
            return Literal

        range_name = self._extract_name(range_uri)
        range_class = self.namespace[range_name]

        return range_class

    def _build_class_hierarchy(self):
        """
        Given the graphs of rdf:type and rdfs:subClassOf relations,
        build the class hierarchy.
        We use topological sort to build the hierarchy in order of
        dependencies and to identify any circular dependencies.

        For reference on the logic rules governing type and subClassOf relations
        see the diagrams here: http://liris.cnrs.fr/~pchampin/2001/rdf-tutorial/node14.html

        """
        for uri in self._type_graph:
            if uri not in self._sub_class_graph:
                # Make sure all types are represented in the sub class graph by adding self links.
                self._sub_class_graph[uri].add(uri)

        for classes in toposort(self._sub_class_graph):
            for class_uri in classes:
                is_property = is_a_property(self._type_graph[class_uri])
                self.add_class(
                    class_uri,
                    base_class_uris=self._sub_class_graph[class_uri],
                    is_property=is_property
                )

        for s, p, o in self._asserted_statements:
            if is_label_predicate(p):
                self.add_label(s, o)
            elif is_comment_predicate(p):
                self.add_comment(s, o)
            elif is_domain_predicate(p):
                self.add_property_domain(s, o)
            elif is_range_predicate(p):
                self.add_property_range(s, o)

    def _build_property_proxies(self):
        """
        Build `PropertyProxy` instances for all (Class, Property) pairs
        that are specified via an rdfs.domain statement.

        """
        visited = set()

        for klass in self.namespace.values():
            if issubclass(klass, RDFS_Property):
                for property_class in set([klass] + klass.__subclasses__()) - visited:
                    self.logger.debug("_build_property_proxies() - propagating property_class: %s", property_class)
                    self._propagate_property(property_class, klass.inferred_domain())
                    visited.add(property_class)

    def _propagate_property(self, property_class, domain_classes):
            for base_class in domain_classes:
                self.logger.debug(
                    "_propagate_property() - adding property %s to domain class: %s", property_class, base_class
                )
                base_class.__properties__.append(property_class)
                self._propagate_property(property_class, base_class.__subclasses__())
