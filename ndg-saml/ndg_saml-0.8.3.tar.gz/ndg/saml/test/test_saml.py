"""SAML unit test package

NERC DataGrid Project

This implementation is adapted from the Java OpenSAML implementation.  The 
copyright and licence information are included here:

Copyright [2005] [University Corporation for Advanced Internet Development, Inc.]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
__author__ = "P J Kershaw"
__date__ = "21/07/09"
__copyright__ = "(C) 2009 Science and Technology Facilities Council"
__license__ = "http://www.apache.org/licenses/LICENSE-2.0"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = '$Id$'
import logging
logging.basicConfig(level=logging.DEBUG)
    
from datetime import datetime, timedelta
from uuid import uuid4
from cStringIO import StringIO

import unittest
import pickle

from ndg.saml import importElementTree
ElementTree = importElementTree()

from ndg.saml.utils import SAMLDateTime
from ndg.saml.saml2.core import (SAMLVersion, AuthzDecisionStatement, Assertion, 
                                 AttributeQuery, Response, Issuer, Subject, 
                                 NameID, StatusCode, StatusMessage, Status, 
                                 Conditions, DecisionType, Action, 
                                 AuthzDecisionQuery)

from ndg.saml.xml.etree import (prettyPrint, AssertionElementTree, 
                                AttributeQueryElementTree, ResponseElementTree)
from ndg.saml.test.utils import SAMLUtil
            

class SAMLTestCase(unittest.TestCase):
    """Test SAML implementation for use with CMIP5 federation"""
    NAMEID_FORMAT = SAMLUtil.NAMEID_FORMAT
    NAMEID_VALUE = SAMLUtil.NAMEID_VALUE
    ISSUER_DN = SAMLUtil.ISSUER_DN
    UNCORRECTED_RESOURCE_URI = SAMLUtil.UNCORRECTED_RESOURCE_URI
    RESOURCE_URI = SAMLUtil.RESOURCE_URI
    
    def _createAttributeAssertionHelper(self):
        samlUtil = SAMLUtil()
        
        # ESG core attributes
        samlUtil.firstName = "Philip"
        samlUtil.lastName = "Kershaw"
        samlUtil.emailAddress = "p.j.k@somewhere"
        
        # BADC specific attributes
        badcRoleList = (
            'urn:badc:security:authz:1.0:attr:admin', 
            'urn:badc:security:authz:1.0:attr:rapid', 
            'urn:badc:security:authz:1.0:attr:coapec', 
            'urn:badc:security:authz:1.0:attr:midas', 
            'urn:badc:security:authz:1.0:attr:quest', 
            'urn:badc:security:authz:1.0:attr:staff'
        )
        for role in badcRoleList:
            samlUtil.addAttribute("urn:badc:security:authz:1.0:attr", role)
        
        # Make an assertion object
        assertion = samlUtil.buildAssertion()
        
        return assertion
        
    def test01CreateAssertion(self):
         
        assertion = self._createAttributeAssertionHelper()

        
        # Create ElementTree Assertion Element
        assertionElem = AssertionElementTree.toXML(assertion)
        
        self.assert_(ElementTree.iselement(assertionElem))
        
        # Serialise to output 
        xmlOutput = prettyPrint(assertionElem)       
        self.assert_(len(xmlOutput))
        
        print("\n"+"_"*80)
        print(xmlOutput)
        print("_"*80)

    def test02ParseAssertion(self):
        assertion = self._createAttributeAssertionHelper()
        
        # Create ElementTree Assertion Element
        assertionElem = AssertionElementTree.toXML(assertion)
        
        self.assert_(ElementTree.iselement(assertionElem))
        
        # Serialise to output 
        xmlOutput = prettyPrint(assertionElem)       
           
        print("\n"+"_"*80)
        print(xmlOutput)
        print("_"*80)
                
        assertionStream = StringIO()
        assertionStream.write(xmlOutput)
        assertionStream.seek(0)

        tree = ElementTree.parse(assertionStream)
        elem2 = tree.getroot()
        
        assertion2 = AssertionElementTree.fromXML(elem2)
        self.assert_(assertion2)
        
    def test03CreateAttributeQuery(self):
        samlUtil = SAMLUtil()
        samlUtil.firstName = ''
        samlUtil.lastName = ''
        samlUtil.emailAddress = ''
        attributeQuery = samlUtil.buildAttributeQuery(SAMLTestCase.ISSUER_DN,
                                                      SAMLTestCase.NAMEID_VALUE)
        
        elem = AttributeQueryElementTree.toXML(attributeQuery)
        xmlOutput = prettyPrint(elem)
           
        print("\n"+"_"*80)
        print(xmlOutput)
        print("_"*80)

    def test04ParseAttributeQuery(self):
        samlUtil = SAMLUtil()
        samlUtil.firstName = ''
        samlUtil.lastName = ''
        samlUtil.emailAddress = ''
        attributeQuery = samlUtil.buildAttributeQuery(SAMLTestCase.ISSUER_DN,
                                                      SAMLTestCase.NAMEID_VALUE)
        
        elem = AttributeQueryElementTree.toXML(attributeQuery)        
        xmlOutput = prettyPrint(elem)       
        print("\n"+"_"*80)
        print(xmlOutput)
                
        attributeQueryStream = StringIO()
        attributeQueryStream.write(xmlOutput)
        attributeQueryStream.seek(0)

        tree = ElementTree.parse(attributeQueryStream)
        elem2 = tree.getroot()
        
        attributeQuery2 = AttributeQueryElementTree.fromXML(elem2)
        self.assert_(attributeQuery2.id == attributeQuery.id)
        self.assert_(attributeQuery2.issuer.value==attributeQuery.issuer.value)
        self.assert_(attributeQuery2.subject.nameID.value == \
                     attributeQuery.subject.nameID.value)
        
        self.assert_(attributeQuery2.attributes[1].name == \
                     attributeQuery.attributes[1].name)
        
        xmlOutput2 = prettyPrint(elem2)       
        print("_"*80)
        print(xmlOutput2)
        print("_"*80)

    def _createAttributeQueryResponse(self):
        response = Response()
        response.issueInstant = datetime.utcnow()
        
        # Make up a request ID that this response is responding to
        response.inResponseTo = str(uuid4())
        response.id = str(uuid4())
        response.version = SAMLVersion(SAMLVersion.VERSION_20)
            
        response.issuer = Issuer()
        response.issuer.format = Issuer.X509_SUBJECT
        response.issuer.value = \
                        SAMLTestCase.ISSUER_DN
        
        response.status = Status()
        response.status.statusCode = StatusCode()
        response.status.statusCode.value = StatusCode.SUCCESS_URI
        response.status.statusMessage = StatusMessage()        
        response.status.statusMessage.value = "Response created successfully"
           
        assertion = self._createAttributeAssertionHelper()
        
        # Add a conditions statement for a validity of 8 hours
        assertion.conditions = Conditions()
        assertion.conditions.notBefore = datetime.utcnow()
        assertion.conditions.notOnOrAfter = (assertion.conditions.notBefore + 
                                             timedelta(seconds=60*60*8))
        
        assertion.subject = Subject()  
        assertion.subject.nameID = NameID()
        assertion.subject.nameID.format = SAMLTestCase.NAMEID_FORMAT
        assertion.subject.nameID.value = SAMLTestCase.NAMEID_VALUE    
            
        assertion.issuer = Issuer()
        assertion.issuer.format = Issuer.X509_SUBJECT
        assertion.issuer.value = SAMLTestCase.ISSUER_DN

        response.assertions.append(assertion)
        
        return response
        
    def test05CreateAttributeQueryResponse(self):
        response = self._createAttributeQueryResponse()
        
        # Create ElementTree Assertion Element
        responseElem = ResponseElementTree.toXML(response)
        
        self.assert_(ElementTree.iselement(responseElem))
        
        # Serialise to output        
        xmlOutput = prettyPrint(responseElem)       
        self.assert_(len(xmlOutput))
        print("\n"+"_"*80)
        print(xmlOutput)
        print("_"*80)
    
    def test06CreateAuthzDecisionQuery(self):
        samlUtil = SAMLUtil()
        authzDecisionQuery = samlUtil.buildAuthzDecisionQuery()
        
        self.assert_(":80" not in authzDecisionQuery.resource)
        self.assert_("localhost" in authzDecisionQuery.resource)
        self.assert_(" " not in authzDecisionQuery.resource)
        
        authzDecisionQuery.resource = \
            "https://Somewhere.ac.uk:443/My Secured URI?blah=4&yes=True"
            
        self.assert_(":443" not in authzDecisionQuery.resource)
        self.assert_("somewhere.ac.uk" in authzDecisionQuery.resource)
        self.assert_("yes=True" in authzDecisionQuery.resource)
        
        authzDecisionQuery.actions.append(Action())
        authzDecisionQuery.actions[0].namespace = Action.GHPP_NS_URI
        authzDecisionQuery.actions[0].value = Action.HTTP_GET_ACTION
        
        self.assert_(
            authzDecisionQuery.actions[0].value == Action.HTTP_GET_ACTION)
        self.assert_(
            authzDecisionQuery.actions[0].namespace == Action.GHPP_NS_URI)
        
        # Try out the restricted vocabulary
        try:
            authzDecisionQuery.actions[0].value = "delete everything"
            self.fail("Expecting AttributeError raised for incorrect action "
                      "setting.")
        except AttributeError, e:
            print("Caught incorrect action type setting: %s" % e)
        
        authzDecisionQuery.actions[0].actionTypes = {'urn:malicious': 
                                                     ("delete everything",)}
        
        # Try again now that the actipn types have been adjusted
        authzDecisionQuery.actions[0].namespace = 'urn:malicious'
        authzDecisionQuery.actions[0].value = "delete everything"
        
    def test09CreateAuthzDecisionQueryResponse(self):
        response = SAMLUtil.create_authz_decision_query_response()
        self.assert_(response.assertions[0])
        self.assert_(response.assertions[0].authzDecisionStatements[0])
        self.assert_(response.assertions[0].authzDecisionStatements[0
            ].decision == DecisionType.PERMIT)
        self.assert_(response.assertions[0].authzDecisionStatements[0
            ].resource == SAMLTestCase.RESOURCE_URI)
        self.assert_(response.assertions[0].authzDecisionStatements[0
            ].decision == DecisionType.PERMIT)
        self.assert_(response.assertions[0].authzDecisionStatements[0
            ].actions[-1].namespace == Action.GHPP_NS_URI)
        self.assert_(response.assertions[0].authzDecisionStatements[0
            ].actions[-1].value == Action.HTTP_GET_ACTION)
 
    def test12PickleAssertion(self):
        # Test pickling with __slots__
        assertion = self._createAttributeAssertionHelper()
        assertion.issuer = Issuer()
        assertion.issuer.format = Issuer.X509_SUBJECT
        assertion.issuer.value = SAMLTestCase.ISSUER_DN
        
        jar = pickle.dumps(assertion)
        assertion2 = pickle.loads(jar)
        self.assert_(isinstance(assertion2, Assertion))
        self.assert_(assertion2.issuer.value == assertion.issuer.value)
        self.assert_(assertion2.issuer.format == assertion.issuer.format)
        self.assert_(len(assertion2.attributeStatements)==1)
        self.assert_(len(assertion2.attributeStatements[0].attributes) > 0)
        self.assert_(assertion2.attributeStatements[0].attributes[0
                     ].attributeValues[0
                     ].value == assertion.attributeStatements[0].attributes[0
                                ].attributeValues[0].value)
        
    def test13PickleAttributeQuery(self):
        # Test pickling with __slots__
        samlUtil = SAMLUtil()
        samlUtil.firstName = ''
        samlUtil.lastName = ''
        samlUtil.emailAddress = ''
        query = samlUtil.buildAttributeQuery(SAMLTestCase.ISSUER_DN,
                                             SAMLTestCase.NAMEID_VALUE)
        
        jar = pickle.dumps(query)
        query2 = pickle.loads(jar)

        self.assert_(isinstance(query2, AttributeQuery))
        self.assert_(query2.subject.nameID.value == query.subject.nameID.value)
        self.assert_((query2.subject.nameID.format == 
                      query.subject.nameID.format))
        self.assert_(query2.issuer.value == query.issuer.value)
        self.assert_(query2.issuer.format == query.issuer.format)
        self.assert_(query2.issueInstant == query.issueInstant)
        self.assert_(query2.id == query.id)
        self.assert_(len(query2.attributes) == 3)
        self.assert_(query2.attributes[0].name == "urn:esg:first:name")
        self.assert_(query2.attributes[1].nameFormat == SAMLUtil.XSSTRING_NS)

    def test14PickleAttributeQueryResponse(self):
        response = self._createAttributeQueryResponse()
        
        jar = pickle.dumps(response)
        response2 = pickle.loads(jar)
        
        self.assert_(isinstance(response2, Response))
        self.assert_((response2.status.statusCode.value == 
                      response.status.statusCode.value))
        self.assert_((response2.status.statusMessage.value == 
                      response.status.statusMessage.value))
        self.assert_(len(response2.assertions) == 1)
        self.assert_(response2.assertions[0].id == response.assertions[0].id)
        self.assert_((response2.assertions[0].conditions.notBefore == 
                      response.assertions[0].conditions.notBefore))
        self.assert_((response2.assertions[0].conditions.notOnOrAfter == 
                      response.assertions[0].conditions.notOnOrAfter))
        self.assert_(len(response2.assertions[0].attributeStatements) == 1)
        self.assert_(len(response2.assertions[0].attributeStatements[0
                                                            ].attributes) == 9)
        self.assert_(response2.assertions[0].attributeStatements[0].attributes[1
                     ].attributeValues[0
                     ].value == response.assertions[0].attributeStatements[0
                                    ].attributes[1].attributeValues[0].value)
             
    def test15PickleAuthzDecisionQuery(self):
        samlUtil = SAMLUtil()
        query = samlUtil.buildAuthzDecisionQuery()
             
        jar = pickle.dumps(query)
        query2 = pickle.loads(jar)
        
        self.assert_(isinstance(query2, AuthzDecisionQuery))
        self.assert_(query.resource == query2.resource)
        self.assert_(query.version == query2.version)
        self.assert_(len(query2.actions) == 1)
        self.assert_(query2.actions[0].value == Action.HTTP_GET_ACTION)
        self.assert_(query2.actions[0].namespace == Action.GHPP_NS_URI)

    def test16PickleAuthzDecisionResponse(self):
        response = SAMLUtil.create_authz_decision_query_response()
        
        jar = pickle.dumps(response)
        response2 = pickle.loads(jar)
        
        self.assert_(isinstance(response2, Response))
        
        self.assert_(len(response.assertions) == 1)
        self.assert_(len(response.assertions[0].authzDecisionStatements) == 1)
         
        self.assert_(response.assertions[0].authzDecisionStatements[0
                        ].resource == response2.assertions[0
                                        ].authzDecisionStatements[0].resource)
        
        self.assert_(len(response.assertions[0].authzDecisionStatements[0
                        ].actions) == 1)
        self.assert_(response.assertions[0].authzDecisionStatements[0
                        ].actions[0].value == response2.assertions[0
                                        ].authzDecisionStatements[0
                                                ].actions[0].value)
        
        self.assert_(response2.assertions[0].authzDecisionStatements[0
                        ].actions[0].namespace == Action.GHPP_NS_URI)        

        self.assert_(response2.assertions[0].authzDecisionStatements[0
                        ].decision == DecisionType.PERMIT)        
        
    def test17SAMLDatetime(self):
        # Test parsing of Datetimes following 
        # http://www.w3.org/TR/xmlschema-2/#dateTime 
        
        # No seconds fraction
        self.assert_(SAMLDateTime.fromString('2010-10-20T14:49:50Z'))
        
        self.assertRaises(TypeError, SAMLDateTime.fromString, None)
        
        
if __name__ == "__main__":
    unittest.main()        
