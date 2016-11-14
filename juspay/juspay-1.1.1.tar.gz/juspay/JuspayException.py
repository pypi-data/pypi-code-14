class JuspayException(Exception):

    def __init__(self, http_status=None, message=None,
                 json_body=None, headers=None):
        super(JuspayException, self).__init__(json_body)

        self._message = message
        self.http_status = http_status
        self.json_body = json_body
        self.headers = headers or {}

    def __str__(self):
        if self._message is not None and self.http_status is not None:
            return u"ERROR: Request failed with httpResponseCode : {0}.\nerrorMessage : {1}".format(self.http_status, self._message)
        elif self._message is not None:
            return u"ERROR: Request failed. Message : {0}".format(self._message)    
        elif self.json_body is not None:
            return u"ERROR: Request failed with httpResponseCode : {0}\n{1}".format(self.http_status, self.json_body)
        else:
            return u"ERROR: Request failed with unknown reason, please contact support@juspay.in."
        

class InvalidRequestException(JuspayException):
    pass

class AuthenticationException(JuspayException):
    pass

class APIException(JuspayException):
    pass

class APIConnectionException(JuspayException):
    pass

class InvalidArguementException(JuspayException):
    def __init__(self, message=None):
        super(InvalidArguementException, self)\
            .__init__(message=message or "Please pass requiered parameters.")
