#coding=utf8
"""
BigRLab Python client
Licence:
Copyright (c) 2016 Pandeng Li
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

try:
    import http.client as httplib
except ImportError:
    import httplib


import os.path
import json
import uuid


import datetime


VERBOSE=True
DD_TIMEOUT = 2000 # seconds, for long blocking training alls, as needed

def LOG(msg):
    """Output a log message."""
    # XXX: may want to use python log manager classes instead of this stupid print
    if VERBOSE:
        msg = str(datetime.datetime.now()) + ' ' + msg
        print (msg)
LOG('I am a remote client of bigrlab')
### Exception classes :

class DDCommunicationError(Exception):
    def __init__(self, url, http_method,  headers, body, response=None):
        self.msg = """BigRLab Communication Error"""
        self.http_method = http_method
        self.req_headers = headers
        self.req_body = body
        self.url = url
        self.res_headers = None
        if response is not None:
            self.res_headers = response.get_info()
            
    def __str__(self):
        msg = "%s %s\n"%(str(self.http_method),str(self.url))
        for h,v in self.req_headers.iteritems():
            msg += "%s:%s\n"%(h,v)
        msg += "\n"
        if self.req_body is not None:
            msg += str(self.req_body)[:100]
        msg += "\n"
        msg += "--\n"
        msg += str(self.res_headers)
        msg += "\n"
        return msg
class DDDataError(Exception):
    def __init__(self, url, http_method,  headers, body, data=None):
        self.msg = "BigRLab Data Error"
        self.http_method = http_method
        self.req_headers = headers
        self.req_body = body
        self.url = url
        self.data = data

    def __str__(self):
        msg = "%s %s\n"%(str(self.http_method),str(self.url))
        if self.data is not None:
            msg += str(self.data)[:100]
        msg += "\n"
        for h,v in self.req_headers.iteritems():
            msg += "%s:%s\n"%(h,v)
        msg += "\n"
        if self.req_body is not None:
            msg += str(self.req_body)
        msg += "\n"
        msg += "--\n"
        msg += str(self.data)
        msg += "\n"
        return msg

API_METHODS_URL = {
    "0.1" : {
        "info":"BigRLab server running successful",
        "services":"/services",
        "train":"/train",
        "predict":"/cn_class"
    }
}

class BigRLab(object):
    """HTTP requests to the BigRLab server
    """

    # return types
    RETURN_PYTHON=0
    RETURN_JSON=1
    RETURN_NONE=2

    __HTTP=0
    __HTTPS=1
		#defualut host and port
    def __init__(self,host="115.182.90.112",port=8080,proto=0,apiversion="0.1"):
        """ BigRLab class constructor
        Parameters:
        host -- the BigRLab server host
        port -- the BigRLab server port
        proto -- user http (0,default) or https connection
        """
        self.apiversion = apiversion
        self.__urls = API_METHODS_URL[apiversion]
        self.__host = host
        self.__port = port
        self.__proto = proto
        self.__returntype=self.RETURN_PYTHON
        if proto == self.__HTTP:
            self.__ddurl='http://%s:%d'%(host,port)
        else:
            self.__ddurl='https://%s:%d'%(host,port)


    def set_return_format(self,f):
        assert f == self.RETURN_PYTHON or f == self.RETURN_JSON or f == self.RETURN_NONE
        self.__returntype = f

    def __return_format(self,js):
        if self.__returntype == self.RETURN_PYTHON:
            return json.loads(js.decode('utf-8'))
        elif self.__returntype == self.RETURN_JSON:
            return js
        else:
            return None


    def post(self,method,body):
        """POST request to BigRLab server"""
        
        r = None
        u = ""
        headers = {"Content-type": "BigRLab_Request"
                    , "Accept": "text/plain"}
        try:
            u = self.__ddurl + method
            if self.__proto == self.__HTTP:
                LOG("curl -X POST 'http://%s:%s%s' -d '%s'"%(self.__host,
                                                             self.__port,
                                                             method,
                                                             body))
                """连接BigRLab server"""
                c=httplib.HTTPConnection(self.__host,self.__port,timeout=DD_TIMEOUT)
            else:
                LOG("curl -k -X POST 'https://%s:%s%s' -d '%s'"%(self.__host,
                                                                 self.__port,
                                                                 method,
                                                                 body))
                c=httplib.HTTPSConnection(self.__host,self.__port, timeout=DD_TIMEOUT)
            c.request('POST',method,body,headers)
            r = c.getresponse()
            data = r.read()
            #print data
            
        except:
            raise DDCommunicationError(u,"POST",headers,body,r)

        # LOG(data)
        try:
            return self.__return_format(data)
        except:
            import traceback
            print (traceback.format_exc())

            raise DDDataError(u,"POST",headers,body,data)
        return data
    # API methods

    def info(self):
        """Info on the BigRLab server"""
        return self.get(self.__urls["info"])

    # POST /predict

    def post_predict(self,sname,data,parameters_input,parameters_mllib,parameters_output):
        """
        Makes prediction from data and model
        Parameters:
        sname -- service name as a resource
        data -- array of data URI to predict from
        parameters_input -- dict of input parameters
        parameters_mllib -- dict ML library parameters
        parameters_output -- dict of output parameters
        """
        """
        body={"service":sname,
              "parameters":{"input":parameters_input,"mllib":parameters_mllib,"output":parameters_output},
              "data":data}
        """
        
        return self.post(self.__urls["predict"],json.dumps(body))
