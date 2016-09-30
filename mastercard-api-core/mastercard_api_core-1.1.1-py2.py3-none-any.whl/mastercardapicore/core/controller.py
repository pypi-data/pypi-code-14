#
# Copyright (c) 2016 MasterCard International Incorporated
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of
# conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list of
# conditions and the following disclaimer in the documentation and/or other materials
# provided with the distribution.
# Neither the name of the MasterCard International Incorporated nor the names of its
# contributors may be used to endorse or promote products derived from this software
# without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#
from requests import Request, Session
from mastercardapicore.core import Config
from mastercardapicore.core import Constants
from mastercardapicore.security import Authentication
from mastercardapicore.core.exceptions import APIException, ObjectNotFoundException, InvalidRequestException, SystemException
import mastercardapicore.core.util as util
import json

class APIController(object):


    ACTION_CREATE = "CREATE"
    ACTION_DELETE = "DELETE"
    ACTION_UPDATE = "UPDATE"
    ACTION_READ   = "READ"
    ACTION_LIST   = "LIST"
    ACTION_QUERY  = "QUERY"

    HTTP_METHOD_GET    = "GET"
    HTTP_METHOD_POST   = "POST"
    HTTP_METHOD_PUT    = "PUT"
    HTTP_METHOD_DELETE = "DELETE"

    KEY_ID     = "id"
    KEY_FORMAT = "Format"
    KEY_ACCEPT = "Accept"
    KEY_USER_AGENT = "User-Agent"
    KEY_CONTENT_TYPE = "Content-Type"
    APPLICATION_JSON = "application/json"
    PYTHON_SDK       = "Python_SDK"
    JSON             = "JSON"


    def __init__(self):

        #Set the parameters
        self.baseURL = Config.getAPIBaseURL()
        
        #Verify if the URL is correct
        if not util.validateURL(self.baseURL):
            raise APIException("URL: '" + self.baseURL + "' is not a valid url")


    def __check(self):
        """
        Check the pre-conditions before execute can be called
        """

        if Config.getAuthentication() is None or not isinstance(Config.getAuthentication(),Authentication):
            raise  APIException("No or incorrect authentication has been configured")


    def removeForwardSlashFromTail(self,text):
        """
        Removes the trailing / from url if any and returns the url
        """
        return text[:-1] if text.endswith("/") else text

    def getURL(self,config,metadata,inputMap):
        """
        Forms the complete URL by combining baseURL and replaced path variables in resourcePath from inputMap
        """

        resourcePath = config.getResourcePath()
        action= config.getAction()

        if not metadata.getHost() is None:
            baseURL = metadata.getHost()
        else: 
            baseURL = self.baseURL
            
        print "baseURL:::: "+baseURL
    
        #Remove the Trailing slash from base URL
        baseURL = self.removeForwardSlashFromTail(baseURL)

        #Remove the Trailing slash from the resource path
        resourcePath = self.removeForwardSlashFromTail(resourcePath)

        #Combine the  base URL and the path
        fullURL = baseURL + resourcePath

        #Replace the path variables
        fullURL = util.getReplacedPath(fullURL,inputMap)

        #This step is if id is in inputMap but was not specified in URL as /{id}
        #If the action is read,update or delete we add this id
        if APIController.KEY_ID in inputMap:
            if action.upper() in [APIController.ACTION_READ,APIController.ACTION_UPDATE,APIController.ACTION_DELETE]:
                fullURL += "/"+str(inputMap[APIController.KEY_ID])
                del inputMap[APIController.KEY_ID] #Remove from input path otherwise this would get add in query params as well

        return fullURL

    def getRequestObject(self,config,metadata,inputMap):
        """
        Gets the Request Object with URL and
        """
        
        #Separate the headers from the inputMap
        headerMap = util.subMap(inputMap,config.getHeaderParams())

        #Separate the query from the inputMap
        queryMap  = util.subMap(inputMap,config.getQueryParams())
        
        #Extract the action
        action = config.getAction()
        
        #getting the url
        fullURL = self.getURL(config,metadata,inputMap)

        #get method from action
        method  = self.getMethod(action)        

        if method is None:
            raise APIException("Invalid action supplied: " + action);

        #Create the request object
        request = Request()
        #set the request parameters
        request.method = method
        request.url    = fullURL
        request.headers[APIController.KEY_ACCEPT]       = APIController.APPLICATION_JSON
        request.headers[APIController.KEY_CONTENT_TYPE] = APIController.APPLICATION_JSON
        request.headers[APIController.KEY_USER_AGENT]   = APIController.PYTHON_SDK+"/"+metadata.getVersion()

        #Add inputMap to params if action in read,delete,list,query
        if action.upper() in [APIController.ACTION_READ,APIController.ACTION_DELETE,APIController.ACTION_LIST,APIController.ACTION_QUERY]:
            request.params = inputMap
        elif action.upper() in [APIController.ACTION_CREATE,APIController.ACTION_UPDATE]:
            request.data = json.dumps(inputMap)

        #Set the query parameter Format as JSON
        request.params[APIController.KEY_FORMAT] = APIController.JSON

        #Add the query in queryMap
        request.params.update(queryMap)
        
        #Add headers
        for key, value in headerMap.items():
            request.headers[key] = value

        #Sign the request
        #This should add the authorization header in the request
        if (Config.getAuthentication()):
            Config.getAuthentication().signRequest(fullURL,request)

        return request


    def getMethod(self,action):

        actions = {
            APIController.ACTION_CREATE:APIController.HTTP_METHOD_POST,
            APIController.ACTION_DELETE:APIController.HTTP_METHOD_DELETE,
            APIController.ACTION_UPDATE:APIController.HTTP_METHOD_PUT,
            APIController.ACTION_READ:APIController.HTTP_METHOD_GET,
            APIController.ACTION_LIST:APIController.HTTP_METHOD_GET,
            APIController.ACTION_QUERY:APIController.HTTP_METHOD_GET
        }

        return actions.get(action.upper(),None)

    def execute(self,config,metadata,inputMap):

        #Check preconditions for execute
        self.__check()

        request = self.getRequestObject(config,metadata,inputMap)

        prepreq = request.prepare()

        ##Log the request parameters if Debug is on
        if Config.isDebug():
            print "------ Request ----"
            print ""
            print "URL"
            print prepreq.url
            print ""
            print "Headers"
            print prepreq.headers
            print ""
            print "Body"
            print prepreq.body
            print " "


        #Make the request
        sess = Session()
        response = sess.send(prepreq)
        sess.close()

        ##Log the response parameters if Debug is on
        if Config.isDebug():
            print "------ Response ----"
            print ""
            print "Status Code"
            print response.status_code
            print ""
            print "Headers"
            print response.headers
            print ""
            print "Body"
            print response.content
            print " "

        content = response.content

        return self.handleResponse(response,content)


    def handleResponse(self,response,content):
        """
        Handles the exception and response
        """
        status = response.status_code
        if content:
            try:
                if isinstance(content,bytes):
                    content = content.decode("utf-8")
                content= json.loads(content)
            except (ValueError, TypeError):
                pass

        else:
             content= ""

        if 200 <= status <= 299:
            return content
        elif 300 <= status <= 399:
            raise InvalidRequestException("Unexpected response code returned from the API causing redirect",status,content)
        elif status == 400:
            raise InvalidRequestException("Bad request",status,content)
        elif status == 401:
            raise APIException("You are not authorized to make this request",status,content)
        elif status == 403:
            raise APIException("You are not authorized to make this request",status,content)
        elif status == 404:
            raise ObjectNotFoundException("Object not found",status,content)
        elif status == 405:
            raise APIException("Operation not allowed",status,content)
        else:
            raise SystemException("Internal Server Error",status,content)
