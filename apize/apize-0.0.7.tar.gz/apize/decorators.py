#!/usr/bin/env python3

from __future__ import absolute_import

import json
import requests
from http.cookiejar import CookieJar
from .exceptions import *


def send_request(url, method, 
	data, params, headers, cookies, timeout, is_json):
	"""
	Forge and send HTTP request.
	"""
	for p in params:
		url = url.replace(':'+p, str(params[p]))
		
	try:
		if data:
			if is_json:
				data = json.dumps(data)
				
			request = requests.Request(method.upper(), url, 
				data=data, headers=headers, cookies=cookies)
		else:
			request = requests.Request(method.upper(), url,
				headers=headers, cookies=cookies)
		
		## Prepare and send HTTP request.
		session = requests.Session()
		r = session.send(request.prepare(), timeout=timeout)
		
	except requests.exceptions.Timeout:
		return {
			'data': {}, 
			'cookies': CookieJar(),
			'content_type': '', 
			'status': 0, 
			'is_json': False,
			'timeout': True
		}

	try:
		content_type = r.headers.get('Content-Type', 'application/json')
		response = r.json()
		isjson = True
		
	except json.decoder.JSONDecodeError:
		content_type = r.headers.get('Content-Type', 'text/html')
		response = r.text
		isjson = False
	
	return {
		'data': response,
		'cookies': r.cookies,
		'content_type': content_type, 
		'status': r.status_code,
		'is_json': isjson,
		'timeout': False
	}


def apize(url, method='GET'):
	"""
	Convert data and params dict -> json.
	"""
	def decorator(func):
		def wrapper(*args, **kwargs):
			elem = func(*args, **kwargs)
			
			if type(elem) is not dict:
				raise BadReturnVarType(func.__name__)
			
			response = send_request(url, method, 
				elem.get('data', {}), 
				elem.get('params', {}),
				elem.get('headers', {}),
				elem.get('cookies', {}),
				elem.get('timeout', 8),
				elem.get('is_json', False)
			)
			
			return response
		return wrapper
		
	return decorator

