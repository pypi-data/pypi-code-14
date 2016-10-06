#!/usr/bin/env python3

from __future__ import absolute_import

from apize.exceptions import BadReturnVarType
from apize.http_request import send_request


class Apize():
	
	def __init__(self, api_url, headers={}, verify_cert=True):
		self.api_url = api_url
		self.headers = headers
		self.verify_cert = verify_cert

	def call(self, path, method='GET'):
		def decorator(func):
			def wrapper(*args, **kwargs):
				elem = func(*args, **kwargs)

				if type(elem) is not dict:
					raise BadReturnVarType(func.__name__)

				absolute_url = self.api_url + path

				## Merge global headers and custom headers.
				fin_headers = self.headers.copy()
				fin_headers.update(elem.get('headers', {}))
				
				response = send_request(absolute_url, method, 
					elem.get('data', {}),
					elem.get('args', {}),
					elem.get('params', {}),
					fin_headers,
					elem.get('cookies', {}),
					elem.get('timeout', 8),
					elem.get('is_json', False),
					elem.get('verify_cert', self.verify_cert)
				)

				return response
			return wrapper

		return decorator
