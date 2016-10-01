#!/usr/bin/python

""" 
An example class for making a registration to the SEAS registry using Python
"""

import sys

from SeasObjects.agents.Agent import Agent
from SeasObjects.factory.RequestFactory import RequestFactory
from SeasObjects.common.Tools import Tools
from SeasObjects.common.SERIALIZATION import SERIALIZATION
from SeasObjects.common.CONTENTTYPES import CONTENTTYPE


REGISTRATION_SERVER_ADDRESS = "http://seas.asema.com/webapps/rs/register"


class RegistrationAgent(Agent):
    def __init__(self, identity):
        Agent.__init__(self)
        self.identity = identity
        self.entities = []

    def addEntity(self, e):
        self.entities.append(e)
        
    def makeRegistration(self):
        request = RequestFactory().createRegistrationRequest(self.identity)

        for e in self.entities:
            request.addEntity(e)
            
        messageBody = Tools().toString(request, SERIALIZATION.TURTLE);
        print "Sending SEAS registration:\n%s\n"%messageBody

        self.runQuery(REGISTRATION_SERVER_ADDRESS, CONTENTTYPE.TURTLE, CONTENTTYPE.TURTLE, messageBody)

        return True
