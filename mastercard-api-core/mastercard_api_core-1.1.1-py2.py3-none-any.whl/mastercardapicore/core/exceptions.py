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
"""
Global MasterCard core exceptions file
"""

################################################################################
# APIException
################################################################################

class APIException(Exception):
    """Base Class for all the API exceptions"""

    def __init__(self,message,status=None,error_data=None):
        #Call the base class constructor
        super(APIException, self).__init__(message,status,error_data)
        self._message    = message
        self._status     = status
        self._error_data = error_data
        self._error_code = None
        #If error_data is not None set the appropriate message
        if error_data is not None:
            error_dict = {}
            # If error_data is of type dict and has Key 'Errors' which has a key 'Error'
            if isinstance(error_data, dict) and 'Error' in error_data.get("Errors",{}):
                error_dict = error_data['Errors']['Error']

                #Case of multiple errors take the first one
                if isinstance(error_dict, list):
                    error_dict = error_dict[0]

                self.__initErrorDataFromDict(error_dict)


            #If error Data is of Type List
            elif isinstance(error_data,list):
                #Take the first error
                error_dict = error_data[0]

                self.__initErrorDataFromDict(error_dict)



    def __initErrorDataFromDict(self,error_dict):
        self._error_code = error_dict.get("ReasonCode","")
        self._message    = error_dict.get("Message",self._message)

    def getMessage(self):
        return self._message

    def getStatus(self):
        return self._status

    def getErrorCode(self):
        return self._error_code

    def getErrorData(self):
        return self._error_data

    def describe(self):
        exception_data = []
        exception_data.append(self.__class__.__name__)
        exception_data.append(": \"")
        exception_data.append(self.getMessage())
        exception_data.append("\" (status: ")
        exception_data.append("{}".format(self.getStatus()))
        exception_data.append(", error code: ")
        exception_data.append("{}".format(self.getErrorCode()))
        exception_data.append(")")
        return ''.join(exception_data)

    def __str__(self):
        return '%s' % self.describe()



################################################################################
# ApiConnectionException
################################################################################

class APIConnectionException(APIException):
    """
    Exception raised when there are communication problems contacting the API.
    """
    def __init__(self,message=None,status=None,error_data=None):

        if status is None:
            status = 500

        #Call the base class constructor
        super(APIConnectionException, self).__init__(message,status,error_data)



################################################################################
# AuthenticationException
################################################################################

class AuthenticationException(APIException):
    """
    Exception raised where there are problems authenticating a request.
    """
    def __init__(self,message=None,status=None,error_data=None):

        if status is None:
            status = 401

        #Call the base class constructor
        super(AuthenticationException, self).__init__(message,status,error_data)


################################################################################
# InvalidRequestException
################################################################################

class InvalidRequestException(APIException):
    """
    Exception raised when the API request contains errors.
    """
    def __init__(self,message=None,status=None,error_data=None):

        if status is None:
            status = 400

        #Call the base class constructor
        super(InvalidRequestException, self).__init__(message,status,error_data)

        self._field_errors = []

        #If error_data is not None set the appropriate message
        if error_data is not None:
            error_dict = {}
            # If error_data is of type dict and has Key 'Errors' which has a key 'Error'
            if isinstance(error_data, dict) and 'Error' in error_data.get("Errors",{}):
                error_dict = error_data['Errors']['Error']

                #Case of multiple errors take the first one
                if isinstance(error_data, list):
                    error_dict = error_data[0]

                self.__initFieldErrorsFromDict(error_dict)

            #If error Data is of Type List
            elif isinstance(error_data,list):
                #Take the first error
                error_dict = error_data[0]

                self.__initFieldErrorsFromDict(error_dict)


    def __initFieldErrorsFromDict(self,error_dict):
        if "FieldErrors" in error_dict:
            for field_error in error_dict.get("FieldErrors"):
                self._field_errors.append(FieldError(field_error))


    def hasFieldErrors(self):
        return hasattr(self,"_field_errors") and len(self._field_errors) > 0

    def getFieldErrors(self):
        return self._field_errors

    def describe(self):
        des = super(InvalidRequestException, self).describe()
        if self.hasFieldErrors():
            for field_error in self._field_errors:
                des += "\n {}".format(field_error)
        return des

    def __str__(self):
        return '%s' % self.describe()






################################################################################
# NotAllowedException
################################################################################

class NotAllowedException(APIException):
    """
    Exception when a request was not allowed.
    """
    def __init__(message=None,status=None,error_data=None):

        if status is None:
            status = 403
        #Call the base class constructor
        super(NotAllowedException, self).__init__(message,status,error_data)

################################################################################
# ObjectNotFoundException
################################################################################

class ObjectNotFoundException(APIException):
    """
    Exception when a requested object cannot be found.
    """
    def __init__(self,message=None,status=None,error_data=None):

        if status is None:
            status = 404
        #Call the base class constructor
        super(ObjectNotFoundException, self).__init__(message,status,error_data)


################################################################################
# SystemException
################################################################################

class SystemException(APIException):
    """
    Exception when there was a system error processing a request.
    """
    def __init__(self,message=None,status=None,error_data=None):

        if status is None:
            status = 500
        #Call the base class constructor
        super(SystemException, self).__init__(message,status,error_data)


################################################################################
# FieldError
################################################################################

class FieldError(object):

    def __init__(self,params):

        self._name    = params['field']
        self._message = params['message']
        self._code    = params['code']

    def getFieldName(self):
        return self._name

    def getErrorMessage(self):
        return self._message

    def getErrorCode(self):
        return self._code

    def __str__(self):
        return "Field Error: {self._name} \"{self._message}\" ({self._code}) ".format(self=self)
