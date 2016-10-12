#!/usr/bin/env python
#encoding=utf-8
 
import sys  
reload(sys)  
sys.setdefaultencoding('utf-8')

import json
import requests
import time
import hashlib
from hashlib import sha1
import hmac
import urllib
import base64
from bs4 import UnicodeDammit
from Crypto.Cipher import AES

try:
  from urllib.parse import urljoin
except ImportError:
  from urlparse import urljoin

from otpsecure.base       import Base
from otpsecure.otp        import Otp
from otpsecure.callback   import Callback
from otpsecure.status     import Status
from otpsecure.error      import Error

ENDPOINT    = 'https://api.otpsecure.net/'
CLIENT_VERSION = '1.0.5'
PYTHON_VERSION = '%d.%d.%d' % (sys.version_info[0], sys.version_info[1], sys.version_info[2])

unpad = lambda s : s[:-ord(s[len(s)-1:])]

class ErrorException(Exception):
  def __init__(self, errors):
    self.errors = errors
    message = ' '.join([str(e) for e in self.errors])
    super(ErrorException, self).__init__(message)


class Client(object):
  def __init__(self, apikey, secret):
    self.apikey = apikey
    self.secret = secret
    self._supported_status_codes = [200, 201, 204, 401, 404, 405, 422]

  def request(self, path, method='GET', params={}):
  
    url = urljoin(ENDPOINT, path)
    timestamp = str(int(round(time.time() * 1000)))
    
    data = json.dumps(self.convert(params), skipkeys=True, separators=(',', ':'), ensure_ascii=False, encoding="utf-8")
    
    m = hashlib.md5()

    m.update(data)
    md5 = m.hexdigest()

    content_type = 'application/json'
    concatenar = method + '\n' + md5 + '\n' + content_type + '\n' + timestamp
    hmac_encode = hmac.new(self.secret, urllib.unquote(concatenar), sha1).hexdigest()
    hmacstr = 'Hmac %s:%s' % (self.apikey, hmac_encode)

    headers = {
      'Accept'        : content_type,
      'date'          : timestamp,
      'authorization' : hmacstr,
      'User-Agent'    : 'otpsecure/ApiClient/%s Python/%s' % (CLIENT_VERSION, PYTHON_VERSION),
      'Content-Type'  : content_type
    }

    if method == 'GET':
      response = requests.get(url, verify=False, headers=headers, params=params)
    else:
      response = requests.post(url, verify=False, headers=headers, data=data)
        
    if response.status_code in self._supported_status_codes:
      json_response = response.json()
    else:
      response.raise_for_status()

    if 'errors' in json_response:
      raise(ErrorException([Error().load(e) for e in json_response['errors']]))

    return json_response

  def otp(self, params={}):
    """Retrieve a client token and send otp sms."""
    return Otp().load(self.request('sms', 'POST', params))

  def callback(self, request):
    """Retrieve a client token and send otp sms."""
    return Callback().load(json.loads(self.decrypt(request)))

  def decrypt(self, request):
    if request.form.getlist('data')[0]:
      encrypted = request.form.getlist('data')[0]
      enc = base64.b64decode(encrypted[24:])
      iv = base64.b64decode(encrypted[:24])
      cipher = AES.new(self.secret, AES.MODE_CBC, iv )
      return unpad(cipher.decrypt( enc ))

  def convert(self, input):
    if isinstance(input, dict):
        return {self.convert(key): self.convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [self.convert(element) for element in input]
    elif isinstance(input, (str,unicode)):
        return str(UnicodeDammit(input, is_html=True).unicode_markup)
    else:
        return input

  def status(self, token, params={}):
    """Retrieve a client pdf by id."""
    params.update({'token': token})
    return Status().load(self.request('status', 'POST', params))
