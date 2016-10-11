"""test utilities module - provides functions to construct example SAML queries 
and responses

Implementation of SAML 2.0 for NDG Security

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
__date__ = "25/01/16"
__copyright__ = "(C) 2009 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "http://www.apache.org/licenses/LICENSE-2.0"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
from datetime import datetime, timedelta
from uuid import uuid4

from ndg.saml.saml2.core import (
    SAMLVersion, Attribute, AttributeStatement, Assertion, AttributeQuery, 
    Issuer, Subject, NameID, XSStringAttributeValue, Action, AuthzDecisionQuery,
    Response, Status, StatusCode, StatusMessage, AuthzDecisionStatement,
    DecisionType, Conditions
    )

from ndg.saml.common.xml import SAMLConstants

class SAMLUtil(object):
    """SAML utility class based on ANL examples for Earth System Grid:
    http://www.ci.uchicago.edu/wiki/bin/view/ESGProject/ESGSAMLAttributes#ESG_Attribute_Service
    """
    NAMEID_FORMAT = "urn:esg:openid"
    NAMEID_VALUE = "https://openid.localhost/philip.kershaw"
    ISSUER_DN = "/O=NDG/OU=BADC/CN=attributeauthority.badc.rl.ac.uk"
    UNCORRECTED_RESOURCE_URI = "http://LOCALHOST:80/My Secured URI"
    RESOURCE_URI = "http://localhost/My%20Secured%20URI"
    XSSTRING_NS = "http://www.w3.org/2001/XMLSchema#string"
    
    def __init__(self):
        """Set-up ESG core attributes, Group/Role and miscellaneous 
        attributes lists
        """
        self.firstName = None
        self.lastName = None
        self.emailAddress = None
        
        self.__miscAttrList = []
    
    def addAttribute(self, name, value):
        """Add a generic attribute
        @type name: basestring
        @param name: attribute name
        @type value: basestring
        @param value: attribute value
        """
        self.__miscAttrList.append((name, value))

    def buildAssertion(self):
        """Create a SAML Assertion containing ESG core attributes: First
        Name, Last Name, e-mail Address; ESG Group/Role type attributes
        and generic attributes
        @rtype: ndg.security.common.saml.Assertion
        @return: new SAML Assertion object
        """
        
        assertion = Assertion()
        assertion.version = SAMLVersion(SAMLVersion.VERSION_20)
        assertion.id = str(uuid4())
        assertion.issueInstant = datetime.utcnow()
        attributeStatement = AttributeStatement()
        
        for attribute in self.createAttributes():
            attributeStatement.attributes.append(attribute)
            
        assertion.attributeStatements.append(attributeStatement)
        
        return assertion

    def buildAttributeQuery(self, issuer, subjectNameID):
        """Make a SAML Attribute Query
        @type issuer: basestring
        @param issuer: attribute issuer name
        @type subjectNameID: basestring
        @param subjectNameID: identity to query attributes for
        """
        attributeQuery = AttributeQuery()
        attributeQuery.version = SAMLVersion(SAMLVersion.VERSION_20)
        attributeQuery.id = str(uuid4())
        attributeQuery.issueInstant = datetime.utcnow()
        
        attributeQuery.issuer = Issuer()
        attributeQuery.issuer.format = Issuer.X509_SUBJECT
        attributeQuery.issuer.value = issuer
                        
        attributeQuery.subject = Subject()  
        attributeQuery.subject.nameID = NameID()
        attributeQuery.subject.nameID.format = self.__class__.NAMEID_FORMAT
        attributeQuery.subject.nameID.value = subjectNameID
                                    
        attributeQuery.attributes = self.createAttributes()
        
        return attributeQuery
    
    def createAttributes(self):
        """Create SAML Attributes for use in an Assertion or AttributeQuery"""
        
        attributes = []
        if self.firstName is not None:    
            # special case handling for 'FirstName' attribute
            fnAttribute = Attribute()
            fnAttribute.name = "urn:esg:first:name"
            fnAttribute.nameFormat = SAMLUtil.XSSTRING_NS
            fnAttribute.friendlyName = "FirstName"

            firstName = XSStringAttributeValue()
            firstName.value = self.firstName
            fnAttribute.attributeValues.append(firstName)

            attributes.append(fnAttribute)
        

        if self.lastName is not None:
            # special case handling for 'LastName' attribute
            lnAttribute = Attribute()
            lnAttribute.name = "urn:esg:last:name"
            lnAttribute.nameFormat = SAMLUtil.XSSTRING_NS
            lnAttribute.friendlyName = "LastName"

            lastName = XSStringAttributeValue()
            lastName.value = self.lastName
            lnAttribute.attributeValues.append(lastName)

            attributes.append(lnAttribute)
        

        if self.emailAddress is not None:
            # special case handling for 'LastName' attribute
            emailAddressAttribute = Attribute()
            emailAddressAttribute.name = "urn:esg:email:address"
            emailAddressAttribute.nameFormat = SAMLConstants.XSD_NS+"#"+\
                                        XSStringAttributeValue.TYPE_LOCAL_NAME
            emailAddressAttribute.friendlyName = "emailAddress"

            emailAddress = XSStringAttributeValue()
            emailAddress.value = self.emailAddress
            emailAddressAttribute.attributeValues.append(emailAddress)

            attributes.append(emailAddressAttribute)
        
        for name, value in self.__miscAttrList:
            attribute = Attribute()
            attribute.name = name
            attribute.nameFormat = SAMLUtil.XSSTRING_NS

            stringAttributeValue = XSStringAttributeValue()
            stringAttributeValue.value = value
            attribute.attributeValues.append(stringAttributeValue)

            attributes.append(attribute)
            
        return attributes
    
    def buildAuthzDecisionQuery(self, 
                                issuer=ISSUER_DN,
                                issuerFormat=Issuer.X509_SUBJECT,
                                subjectNameID=NAMEID_VALUE, 
                                subjectNameIdFormat=NAMEID_FORMAT,
                                resource=UNCORRECTED_RESOURCE_URI,
                                actions=((Action.HTTP_GET_ACTION, 
                                          Action.GHPP_NS_URI),)):
        """Convenience utility to make an Authorisation decision query"""
        authzDecisionQuery = AuthzDecisionQuery()

        authzDecisionQuery.version = SAMLVersion(SAMLVersion.VERSION_20)
        authzDecisionQuery.id = str(uuid4())
        authzDecisionQuery.issueInstant = datetime.utcnow()
        
        authzDecisionQuery.issuer = Issuer()
        authzDecisionQuery.issuer.format = issuerFormat
        authzDecisionQuery.issuer.value = issuer
        
        authzDecisionQuery.subject = Subject()
        authzDecisionQuery.subject.nameID = NameID()
        authzDecisionQuery.subject.nameID.format = subjectNameIdFormat
        authzDecisionQuery.subject.nameID.value = subjectNameID
        
        authzDecisionQuery.resource = resource
        
        for action, namespace in actions:
            authzDecisionQuery.actions.append(Action())
            authzDecisionQuery.actions[-1].namespace = namespace
            authzDecisionQuery.actions[-1].value = action
            
        return authzDecisionQuery
    
    @classmethod
    def create_authz_decision_query_response(cls):
        """Helper method for Authz Decision Response"""
        response = Response()
        now = datetime.utcnow()
        response.issueInstant = now
        
        # Make up a request ID that this response is responding to
        response.inResponseTo = str(uuid4())
        response.id = str(uuid4())
        response.version = SAMLVersion(SAMLVersion.VERSION_20)
            
        response.issuer = Issuer()
        response.issuer.format = Issuer.X509_SUBJECT
        response.issuer.value = cls.ISSUER_DN
        
        response.status = Status()
        response.status.statusCode = StatusCode()
        response.status.statusCode.value = StatusCode.SUCCESS_URI
        response.status.statusMessage = StatusMessage()        
        response.status.statusMessage.value = "Response created successfully"
           
        assertion = Assertion()
        assertion.version = SAMLVersion(SAMLVersion.VERSION_20)
        assertion.id = str(uuid4())
        assertion.issueInstant = now
        
        authzDecisionStatement = AuthzDecisionStatement()
        authzDecisionStatement.decision = DecisionType.PERMIT
        authzDecisionStatement.resource = cls.RESOURCE_URI
        authzDecisionStatement.actions.append(Action())
        authzDecisionStatement.actions[-1].namespace = Action.GHPP_NS_URI
        authzDecisionStatement.actions[-1].value = Action.HTTP_GET_ACTION
        assertion.authzDecisionStatements.append(authzDecisionStatement)
        
        # Add a conditions statement for a validity of 8 hours
        assertion.conditions = Conditions()
        assertion.conditions.notBefore = now
        assertion.conditions.notOnOrAfter = now + timedelta(seconds=60*60*8)
               
        assertion.subject = Subject()  
        assertion.subject.nameID = NameID()
        assertion.subject.nameID.format = cls.NAMEID_FORMAT
        assertion.subject.nameID.value = cls.NAMEID_VALUE    
            
        assertion.issuer = Issuer()
        assertion.issuer.format = Issuer.X509_SUBJECT
        assertion.issuer.value = cls.ISSUER_DN

        response.assertions.append(assertion)
        
        return response