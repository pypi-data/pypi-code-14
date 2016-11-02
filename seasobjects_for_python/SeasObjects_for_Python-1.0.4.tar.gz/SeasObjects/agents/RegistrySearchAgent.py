#!/usr/bin/python

""" 
"""

import sys
import traceback

from rdflib import URIRef

from SeasObjects.agents.Agent import Agent
from SeasObjects.model.Activity import Activity
from SeasObjects.model.Coordinates import Coordinates
from SeasObjects.model.Condition import Condition
from SeasObjects.model.Entity import Entity
from SeasObjects.model.Input import Input
from SeasObjects.model.Output import Output
from SeasObjects.model.ValueObject import ValueObject
from SeasObjects.model.Variant import Variant
from SeasObjects.model.Ring import Ring
from SeasObjects.model.Response import Response
from SeasObjects.factory.RequestFactory import RequestFactory
from SeasObjects.common.Tools import Tools
from SeasObjects.common.SERIALIZATION import SERIALIZATION
from SeasObjects.common.NS import NS
from SeasObjects.common.CONTENTTYPES import CONTENTTYPE
from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.common.PROPERTY import PROPERTY

content_type = "text/turtle"
seas_register_search_uri = "http://seas.asema.com/webapps/rs/search"
caller_seas_uri = ""
serialization = SERIALIZATION.TURTLE
debug = False

entity = Entity()

class RegistrySearchAgent(Agent):
    def __init__(self):
        global entity
        entity.clearTypes()
        Agent.__init__(self)
    
    def setSenderUri(self, generatedBy):
        global caller_seas_uri
        caller_seas_uri = generatedBy
        
    def search(self):
        global entity
        payload = self.generateSearchMessage()
        try :
            if debug:
                print "Request to SEAS Search Service:"
                print payload
            resp_str = self.runQuery(seas_register_search_uri, content_type, content_type, payload)
            response = Response().fromString(resp_str, serialization)
            if response != None:
                if debug:
                    print "Response from SEAS Search Service:"
                    print Tools().toString(response, serialization)
                return response.getEntities()
            else:
                if debug:
                    print "Response from SEAS Search Service:"
                    print resp_str
                return None
        except:
            print "Exception while sending an HTTP request to " + seas_register_search_uri
            traceback.print_exc()
            return None
        
    def clear(self):
        global entity
        entity = Entity()
        
    def setEntity(self, searchEntity):
        global entity
        entity = searchEntity

    def generateSearchMessage(self):
        global entity
        request = RequestFactory().create(caller_seas_uri)
        request.setMethod(RESOURCE.SEAS_READ)
        request.addEntity(entity)
        return Tools().toString(request, serialization)
        
    def setServiceUri(self, serviceUri):
        seas_register_search_uri = serviceUri
        
    def ofName(self, searchString):
        self.ofName(searchString, False)
        
    def ofDescription(self, searchString):
        condition = Condition()
        condition.addRegex("(?i)" + searchString)
        entity.add(URIRef(PROPERTY.RDFS_COMMENT), condition)
        
    def anyOfNames(self, searchStrings):
        global entity
        if len(searchStrings) > 0:
            condition = Condition()
            for s in searchStrings:
                condition.addRegex("(?i)" + s)
            entity.add(URIRef(PROPERTY.RDFS_LABEL), condition)
            
    def ofName(self, searchString, exactMatch):
        global entity
        if exactMatch:
            entity.setName(searchString)
        else:
            condition = Condition()
            condition.addRegex("(?i)" + searchString)
            entity.add(URIRef(PROPERTY.RDFS_LABEL), condition)
            
    def ofType(self, type):
        global entity
        entity.addType(type)
    
    def anyOfTypes(self, types):
        global entity
        if len(types) == 1:
            self.ofType(types[0])
        if len(types) > 1:
            condition = Condition()
            for type in types:
                condition.addOr(Obj(type))
            entity.setType(condition)
            
    def clearTypes(self):
        global entity
        entity.clearTypes()
        
    def ofInputType(self, type):
        global entity
        if entity.hasCapability():
            a = entity.getCapabilities()[0]
            i = Input()
            i.setType(type)
            a.addInput(i)
        else:
            a = Activity()
            i = Input()
            i.setType(type)
            a.addInput(i)
            entity.addCapability(a)
        
    def ofOutputType(self, type):
        global entity
        if entity.hasCapability():
            a = entity.getCapabilities()[0]
            o = Output()
            o.setType(type)
            a.addOutput(o)
        else:
            a = Activity()
            o = Output()
            o.setType(type)
            a.addOutput(o)
            entity.addCapability(a)
                
    def polygonSearchArea(self, polygon):
        global entity
        entity.add(URIRef(RESOURCE.SEAS_POLYGON), polygon)
        
    def multipolygonSearchArea(self, polygons):
        global entity
        for polygon in polygons:
            entity.add(URIRef(RESOURCE.SEAS_POLYGON), polygon)
        
    def rectangeSearchArea(self, minCoords, maxCoords):
        global entity
        entity.add(URIRef(PROPERTY.SEAS_MINLOCATION), minCoords)
        entity.add(URIRef(PROPERTY.SEAS_MAXLOCATION), maxCoords)
        
    def pointSearchArea(self, center, kilometers):
        global entity
        ring = Ring()
        ring.add(URIRef(PROPERTY.GEO_LAT), center.getLatitude())
        ring.add(URIRef(PROPERTY.GEO_LONG), center.getLongitude())
        maxR = ValueObject()
        maxR.setQuantity(RESOURCE.SEAS_DISTANCE)
        maxR.setUnit(RESOURCE.SEAS_KILOMETER)
        maxR.setValue(Variant(kilometers))
        ring.setMaxRadius(maxR)
        entity.add(URIRef(NS.SEAS + "ring"), ring)
        
    def debugMode(self, value):
        global debug
        debug = value
        
    def searchByPointAndType(self, mySeasUri, latitude, longitude, distanceInKm, types):
        agent = RegistrySearchAgent()
        agent.clear()
        agent.setSenderUri(mySeasUri)
        agent.anyOfTypes(types)
        coords = Coordinates()
        coords.setLatitude(latitude)
        coords.setLongitude(longitude)
        agent.pointSearchArea(coords, distanceInKm)
        return agent.search()
        
    def searchByNameAndType(self, mySeasUri, keywords, types):
        agent = RegistrySearchAgent()
        agent.clear()
        agent.setSenderUri(mySeasUri)
        agent.anyOfTypes(types)
        agent.anyOfNames(keywords)
        return agent.search()

    def searchServicesByOutputType(self, mySeasUri, type):
        agent = RegistrySearchAgent()
        agent.clear()
        agent.setSenderUri(mySeasUri)
        agent.ofType(RESOURCE.SEAS_SERVICE)
        agent.ofOutputType(type)
        return agent.search()

    def searchServicesByInputType(self, mySeasUri, type):
        agent = RegistrySearchAgent()
        agent.clear()
        agent.setSenderUri(mySeasUri)
        agent.ofType(RESOURCE.SEAS_SERVICE)
        agent.ofInputType(type)
        return agent.search()

    def searchByDescription(self, mySeasUri, searchString, types = [RESOURCE.SEAS_ENTITY]):
        agent = RegistrySearchAgent()
        agent.clear()
        agent.setSenderUri(mySeasUri)
        agent.anyOfTypes(types)
        agent.ofDescription(searchString)
        return agent.search()

    def fetchBySeasId(self, mySeasUri, idToFetch):
        agent = RegistrySearchAgent()
        agent.clear()
        agent.setSenderUri(mySeasUri)
        entity = Entity(idToFetch)
        entity.clearTypes()
        agent.setEntity(entity)
        resEntities = agent.search()
        if len(resEntities) > 0:
            return resEntities[0]
        else:
            return None

    # TO BE REMOVED - deprecated    
    def searchForItemsByPoint(self, callId, caller_identity, latitude, longitude, distance, types):
        request = RequestFactory().create(caller_identity)

        e = Entity()

        # The types we want to search
        e.clearTypes()
        for t in types:
            e.addType(t)

        ring = Ring()
        radius = ValueObject()

        radius.setQuantity(NS.SEAS + "Distance");
        radius.setUnit(NS.SEAS + "KiloMeter");
        radius.setValue(Variant(distance));

        ring.add(URIRef(NS.GEO + "lat"), latitude)
        ring.add(URIRef(NS.GEO + "long"), longitude)
        ring.setMaxRadius(radius)

        e.add(URIRef(NS.SEAS + "ring"), ring);
        request.addEntity(e);

        requestString = Tools().toString(request, SERIALIZATION.TURTLE);
        
        print "Sending search query:\n%s\n"%requestString

        return self.runQuery(seas_register_search_uri, CONTENTTYPE.TURTLE, CONTENTTYPE.TURTLE, requestString)

    # TO BE REMOVED - deprecated    
    def searchForServicesByOutputType(self, callId, caller_identity, output_type):
        request = RequestFactory().create(caller_identity)

        e = Entity()

        # The types we want to search
        e.setType(RESOURCE.SEAS_SERVICE)

        activity = Activity()
        
        output = Output()
        output.setType(output_type)
        
        activity.setOutput(output)
        
        e.addCapability(activity)
        
        request.addEntity(e);

        requestString = Tools().toString(request, SERIALIZATION.TURTLE);
        
        print "Sending search query:\n%s\n"%requestString

        return  self.runQuery(seas_register_search_uri, CONTENTTYPE.TURTLE, CONTENTTYPE.TURTLE, requestString)
