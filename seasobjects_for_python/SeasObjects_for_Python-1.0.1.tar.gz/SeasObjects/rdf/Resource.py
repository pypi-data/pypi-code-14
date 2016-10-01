"""
A wrapper class around Python RDFLib methods to make a graph behave in a similar
way as Java Apache Jena model.
"""
import sys
try:
    from rdflib import BNode, URIRef, Literal
except:
    import sys
    print "RDFLib is missing from your Python installation"
    print "Install it with"
    print ">  pip install rdflib"
    print ">  pip install rdflib-jsonld"
    sys.exit()

from RdfList import RdfList
from SeasObjects.rdf.RdfLiteral import RdfLiteral
from rdflib.namespace import RDF


class Resource(object):
    def __init__(self, id = None, model = None, node = None):
        self.properties = {}
        self.literals = {}
        self.id = id
        self.model = model
        self.node = node
        if self.node is None:
            if id is None:
                self.node = BNode()
            else:
                self.node = URIRef(id)
    
    def toString(self):
        return str(self.node)
    
    def isAnon(self):
        return isinstance(self.node, BNode)
    
    def addProperty(self, propertyType, property):
        if self.properties.has_key(propertyType.getUri()):
            self.properties[propertyType.getUri()].append(property)
        else:
            self.properties[propertyType.getUri()] = [property]
            
    def addLiteral(self, literalType, literal):
        if self.literals.has_key(literalType.getUri()):
            self.literals[literalType.getUri()].append(literal)
        else:
            self.literals[literalType.getUri()] = [literal]

    def getProperties(self):
        return self.properties
    
    def getProperty(self, property = None):
        if property is None:
            return self.properties
        else:
            if self.properties.has_key(property.getUri()):
                l = self.properties[property.getUri()]
                if len(l) > 0:
                    return self.createStatement(self.model, property.getUri(), l[0])
            return None

    def getLiterals(self):
        return self.literals

    def getNode(self):
        return self.node
    
    def getModel(self):
        return self.model
    
    def createStatement(self, m, predicateUri, obj, subject = None):
        from SeasObjects.rdf.Statement import Statement
        from SeasObjects.model.Variant import Variant
        
        s = Statement(m)
        s.setSubject(subject)
        s.setPredicate(URIRef(predicateUri))
        object = None
        
        if isinstance(obj, Literal):
            object = obj
        elif isinstance(obj, URIRef):
            object = obj
        elif isinstance(obj, Variant):
            object = obj.asTerm()
        elif isinstance(obj, RdfLiteral):
            object = self.makeLiteral(obj)
        elif isinstance(obj, Resource):
            object = obj.getNode()
            s.setResource(obj)
        else:
            object = self.makeLiteral(obj)
        
        s.setObject(object)
    
        return s

    def createListStatements(self, m, predicateUri, obj):
        from SeasObjects.rdf.Statement import Statement
        from SeasObjects.model.Obj import Obj
        from SeasObjects.model.Variant import Variant
        
        lst = obj.get_items()
        ss = []
        # Initial blank node
        s = Statement(m)
    
        bNode = current = BNode()
        
        s.setSubject(self.node)
        s.setPredicate(URIRef(predicateUri))
        s.setObject(bNode)
        ss.append(s)

        l = len(lst)
        for index in range(l):
            var = lst[index]
            
             # Statement for first list element (the actual object)
            if isinstance(var, RdfLiteral):
                o = makeLiteral(var)
            elif isinstance(var, Resource):
                o = bNode
                ss.extend(var.listProperties(subject = o))
            elif isinstance(var, Variant):
                o = var.asTerm()
            elif isinstance(var, Obj):
                r = var.serialize(self.model)
                o = r.getNode()
                ss.extend(r.listProperties())
            else:
                o = Literal(var)
        
            firstS = Statement(m)
            firstS.setSubject(current);
            firstS.setPredicate(RDF.first)
            firstS.setObject(o)
            ss.append(firstS)
        
            # Statement for the rest of the list
            if index == l-1: # last item, put in nil
                next = RDF.nil
            else:
                next = BNode() # not last, need a new blank node
        
            restS = Statement(m)
            restS.setSubject(current)
            restS.setPredicate(RDF.rest)
            restS.setObject(next)
            ss.append(restS)
            current = next # set pointer ready for the next loop
        
        return ss;
    
    def listProperties(self, property = None, subject = None):
        statements = []

        if property:
            if self.properties.has_key(property.getUri()):
                statements.extend(self._fetch_properties(subject, property.getUri()))
        else:
            for propertyUri in self.properties:
                statements.extend(self._fetch_properties(subject, propertyUri))
 
        return statements
    
    def _fetch_properties(self, subject, uri):
        statements = []
        if subject is None: subject = self.node
        
        l = self.properties[uri]
        for property in l:
            # Convert RDF list into statements
            if isinstance(property, RdfList):
                statements.append(self.createListStatements(self.model, uri, property))
            
            else: # Convert other types of properties into statements
                s = self.createStatement(self.model, uri, property, subject)
                if s is not None: 
                    statements.append(s)

        return statements

    def listLiterals(self):
        statements = []

        for propertyUri in self.literals:
            l = self.literals[propertyUri]
            for property in l:
                s = self.createStatement(self.model, propertyUri, property)
                if s is not None: 
                    statements.append(s)

        return statements
    
    def findProperties(self):
        return self.model.find_statements_for_node(self.node)
    
    def findProperty(self, p):
        return self.model.find_statements_for_node(self.node, predicate = URIRef(p.getUri()))

    # transforms the resource into a Python list. Requires that the node
    # is in the form of an RDF list (has first, rest properties
    def toList(self, klass):
        l = []
        self.model.parse_list(l, self.node, klass)
        return l

    def makeLiteral(self, l):
        if isinstance(l, RdfLiteral):
            return Literal(l.getValue())
        else:
            return Literal(l)
   