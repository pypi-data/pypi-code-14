#!/usr/bin/env python3

from __future__ import absolute_import

import json
import requests
from exceptions import *


def send_request(url, method, data, params, headers, cookies):
	"""
	Forge and send HTTP request.
	"""
	for p in params:
		url = url.replace(':'+p, str(params[p]))

	methodLowerCase = method.lower()
	
	if methodLowerCase == 'get':
		r = requests.get(url, headers=headers, cookies=cookies)
	elif methodLowerCase == 'post':
		r = requests.post(url, data=data, headers=headers, cookies=cookies)
	elif methodLowerCase == 'put':
		r = requests.put(url, data=data, headers=headers, cookies=cookies)
	elif methodLowerCase == 'delete':
		r = requests.delete(url, headers=headers, cookies=cookies)
	else:
		raise UnknowMethod(str(method))
	
	r.close()
	
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
		'content_type': content_type, 
		'status': r.status_code,
		'is_json': isjson
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
			
			if not 'data' in elem:
				elem['data'] = {}
			if not 'params' in elem:
				elem['params'] = {}
			if not 'headers' in elem:
				elem['headers'] = {}
			if not 'cookies' in elem:
				elem['cookies'] = {} 
			
			response = send_request(url, method, 
				json.dumps(elem['data']), 
				elem['params'],
				elem['headers'],
				elem['cookies']
			)
			
			return response
		return wrapper
		
	return decorator

