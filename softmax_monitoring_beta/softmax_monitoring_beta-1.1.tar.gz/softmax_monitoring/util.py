import requests
import json
import sys 
import os
import unirest

def callback_dummy(response):
  response.code # The HTTP status code
  response.headers # The HTTP headers
  response.body # The parsed response
  response.raw_body # The unparsed response

def dir_exists(cur_dir):
	return os.path.isdir(cur_dir)

def async_post(url_endpoint, data, token):
	unirest.post(url_endpoint, \
		headers={ "Authorization": "Token %s" % token }, \
		params=data, \
		callback=callback_dummy,
		verify=False)
	return None, None


def post(url_endpoint, data, token):
	r = requests.post(url_endpoint, data = data, verify=False, headers={'Authorization': 'Token %s' % token})
	content = r.content
	jsoned_content = json.loads(content)
	return jsoned_content, r.status_code

def get(url_endpoint, token):
	r = requests.get(url_endpoint, verify=False, headers={'Authorization': 'Token %s' % token})
	content = r.content 
	jsoned_content = json.loads(content)
	return jsoned_content, r.status_code