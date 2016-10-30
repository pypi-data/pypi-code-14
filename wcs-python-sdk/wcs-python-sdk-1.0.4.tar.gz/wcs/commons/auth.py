# -*- coding: utf-8 -*-

import base64
import hmac
import json
from .compat import urlparse
from hashlib import sha1


class Auth(object):

    """wcs auth 
    
    upload token & manager token

    """

    def __init__(self, access_key, secret_key):
        
        self.checkKey(access_key, secret_key)
        self.access_key = access_key
        self.secret_key = secret_key

    def uploadtoken(self, putPolicy):
        """
        return: uploadtoken
        """
        jsonputPolicy = json.dumps(putPolicy)
        encodePutPolicy = base64.b64encode(jsonputPolicy)
        tmp_encodePutPolicy = encodePutPolicy
        Sign = hmac.new(self.secret_key, bytes(encodePutPolicy), sha1)    
        encodeSign = base64.b64encode(Sign.hexdigest())
        return '{0}:{1}:{2}'.format(self.access_key, encodeSign, tmp_encodePutPolicy)

    def managertoken(self, url, body=None):
        """
        return: managertoken
        """
        parsed_url = urlparse(url)
        query = parsed_url.query
        path = parsed_url.path
        if query:
            if body:
                signingStr = ''.join([path,'?',query,"\n",body]) 
            else:
                signingStr = ''.join([path,'?',query,"\n"])
        else:
            if body:
                signingStr = ''.join([path,"\n",body])
            else:
                signingStr = ''.join([path,"\n"])
        SignStr = hmac.new(self.secret_key, signingStr, sha1)    
        encodeSignStr = base64.b64encode(SignStr.hexdigest())
        return '{0}:{1}'.format(self.access_key,encodeSignStr)
    
    @staticmethod
    def checkKey(access_key,secret_key):
        if not (access_key and secret_key):
            raise ValueError('invalid key')


        










