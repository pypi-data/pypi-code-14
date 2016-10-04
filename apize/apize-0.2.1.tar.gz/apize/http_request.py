#!/usr/bin/env python3

from __future__ import absolute_import

import json
import requests
from http.cookiejar import CookieJar


def send_request(url, method, data, 
	args, params, headers, cookies, timeout, is_json, ssl_cert):
	"""
	Forge and send HTTP request.
	"""
	## Parse url args
	for p in args:
		url = url.replace(':' + p, str(args[p]))

	try:
		if data:
			if is_json:
				headers['Content-Type'] = 'application/json'
				data = json.dumps(data)

			request = requests.Request(
				method.upper(), url, data=data, params=params, 
				headers=headers, cookies=cookies
			)
		else:
			request = requests.Request(
				method.upper(), url, params=params, headers=headers, 
				cookies=cookies
			)

		## Prepare and send HTTP request.
		session = requests.Session()
		session.verify = ssl_cert
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
