"""
A wrapper class around Python RDFLib methods to make a graph behave in a similar
way as Java Apache Jena model.
"""
import sys
try:
    from rdflib import Graph
    from rdflib import BNode
    from rdflib import URIRef
    from rdflib import Literal
    from rdflib.namespace import XSD, RDF
except:
    print "RDFLib is missing from your Python installation"
    print "Install it with"
    print ">  pip install rdflib"
    print ">  pip install rdflib-jsonld"
    sys.exit()

from SeasObjects.common.SERIALIZATION import SERIALIZATION
from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.common.NS import NS
from SeasObjects.rdf.RdfList import RdfList
from SeasObjects.rdf.RdfLiteral import RdfLiteral
from SeasObjects.rdf.Property import Property
from SeasObjects.rdf.Resource import Resource
from SeasObjects.rdf.Statement import Statement

import simplejson
import traceback


class Model(object):

    def __init__(self):
        self.graph = Graph()
        self.top_nodes = []
        
    def createResource(self, id = None):
        return Resource(id = id, model = self)
    
    def createProperty(self, id = None):
        return Property(id)

    def createLiteral(self, element):
        return Literal(element)
    
    def createTypedLiteral(self, element, type):
        return self._convert_element(element, type)
    
    def createList(self):
        return RdfList()
    
    def _append_to_graph(self, subject, predicate, object):
        if isinstance(predicate, Property):
            self.graph.add((subject, URIRef(predicate.id), object))
        else:
            self.graph.add((subject, predicate, object))
    
    def _add_statement(self, statement):
        self._append_to_graph(statement.getSubject(), statement.getPredicate(), statement.getObject())
        
    def _add_element(self, object, predicate, subject = None):
        from SeasObjects.model.Variant import Variant
        
        if isinstance(object, Resource):
            n = object.getNode()
            
            for p in object.listProperties():
                if isinstance(p, list):
                    for pe in p:
                        self._add_statement(pe)
                        if pe.getResource() is not None:
                            self._add_element(pe.getResource(), pe.getPredicate(), n)
                else:
                    self._add_statement(p)
                    if p.getResource() is not None:
                        self._add_element(p.getResource(), p.getPredicate(), n)
                
            for l in object.listLiterals():
                self._add_statement(l)
            
        elif isinstance(object, Property):
            if subject is not None and predicate is not None and object.id is not None:
                self._append_to_graph(subject, predicate, URIRef(object.id))
        
        elif isinstance(object, Literal):
            if subject is not None and predicate is not None:
                self._append_to_graph(subject, predicate, object)
                
        elif isinstance(object, RdfLiteral):
            if subject is not None and predicate is not None:
                self._append_to_graph(subject, predicate, object.getValue())
        
        elif isinstance(object, RdfList):
            self._add_list(object, predicate, subject)
            
        elif isinstance(object, Variant):
            if subject is not None and predicate is not None:
                self._append_to_graph(subject, predicate, object.asTerm())
        
        elif isinstance(object, URIRef):
            self._append_to_graph(subject, predicate, object)
            
        else:
            self._append_to_graph(subject, predicate, Literal(object))
    
    def _convert_element(self, element, type):
        return Literal(element, datatype = URIRef(type))
    
    def is_list(self, node):
        first = self.graph.value(subject=node, predicate=RDF.first)
        return first is not None
            
    def parse_list(self, container, node, klass = None):
        from SeasObjects.model.ValueObject import ValueObject
        from SeasObjects.model.Variant import Variant
        from SeasObjects.common.Tools import Tools
        
        first = self.graph.value(subject=node, predicate=RDF.first)
        if first:
            if isinstance(first, Literal):
                container.append(Variant(first.toPython()))
            elif isinstance(first, URIRef):
                container.append(Variant(first))
            else:
                if klass is None:
                    types = []
                    sl = self.listStatements(subject = first, predicate = URIRef(PROPERTY.RDF_TYPE), object = None)
                    for s in sl:
                        types.append(s.getResource().toString())
                    klass = Tools().mapper.getClass(types, default = Variant)

                item = klass()
                for s in self.find_statements_for_node(first):
                    if s.predicate == NS.SEAS + "valueObject":
                        itemv = ValueObject()
                        for sv in self.find_statements_for_node(s.object):
                            itemv.parse(sv)
                        item.addValueObject(itemv)
                    else:
                        item.parse(s)
                container.append(item)
            rest = self.graph.value(subject=node, predicate=RDF.rest)
            if rest:
                self.parse_list(container, rest, klass)

    def _add_list(self, rdflist, predicate, subject):
        from SeasObjects.model.Obj import Obj
        from SeasObjects.model.Variant import Variant

        elements = rdflist.get_items()
        current = list = BNode()
        self.graph.add((subject, URIRef(predicate.id), list))
        l = len(elements)
        for index, var in enumerate(elements):
            if isinstance(var, Variant):  # support lists with raw values (not just wrapped inside Evaluation
                self.graph.add((current, RDF.first, var.asTerm()))
            elif isinstance(var, Obj):
                self._add_element(var.serialize(self), RDF.first, subject = current)
            elif isinstance(var, Resource):
                var_node = BNode()
                for p in var.properties:
                    self._add_element(p[1], URIRef(p[0]), subject = var_node)
                self.graph.add((current, RDF.first, var_node))
            else:
                self.graph.add((current, RDF.first, Literal(var)))
            
            next = RDF.nil if index == l-1 else BNode()  # last item
            self.graph.add((current, RDF.rest, next))
            current = next
    
    def add(self, element):
        if isinstance(element, list):
            for l in element:
                self._add_element(l, None)
        else:
            self._add_element(element, None)

    def findSubject(self, predicate, object):
        return Resource(model = self, node = self.graph.value(predicate = predicate, object=object))
    
    def findObject(self, subject, predicate):
        return Statement(node = self.graph.value(subject = subject, predicate = predicate), subject = subject, predicate = predicate)
    
    def find_statements_for_node(self, node, predicate = None):
        r = []
        
        for s, p, o in self.graph.triples( (node, predicate, None) ):
            r.append(Statement(model = self, subject = s, predicate = p, object = o, resource = Resource(model = self, node = o)))
        return r
    
    def listStatements(self, subject = None, predicate = None, object = None):
        r = []
        for s, p, o in self.graph.triples( (subject, predicate, object) ):
            r.append(Statement(model = self, subject = s, predicate = p, object = o, resource = Resource(model = self, node = o)))
        return r
    
    def serialize(self, format = SERIALIZATION.JSON_LD):
        return self.graph.serialize(format=format)
    
    def parse(self, data = None, file = None, format = SERIALIZATION.JSON_LD):
        if data is not None:
            try:
                if format == SERIALIZATION.JSON_LD:
                    json = simplejson.loads(data)
                    if isinstance(json, dict) and json.has_key('@graph') and json.has_key('@context'):
                        self.graph.parse(data = simplejson.dumps(json['@graph']), format='json-ld', context=json['@context'])
                    else:
                        self.graph.parse(data = data, format='json-ld')
                # other formats
                else:
                    self.graph.parse(data = data, format=format)
            except:
                print "Could not read the input data into a graph"
                traceback.print_exc()
            return
        
        elif file is not None:
            try:
                f = open(file)
                self.graph.parse(f, format=format)
                f.close()
            except:
                print "Could not read the file into a model"
                traceback.print_exc()
            return
        print "No input to parse into a graph"

