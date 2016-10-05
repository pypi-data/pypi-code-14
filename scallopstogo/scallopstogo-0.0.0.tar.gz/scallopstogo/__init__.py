__version__ = "0.0.0"

'''
created 10.5.16

Andrew Lee 

changelog:
10.5.16

added get_cal_service function

'''
import json

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

def get_cal_service(storage):
	'''
	function takes json storage variable and returns calendar api connection
	'''

	# parse json from storage key
	storage = json.loads(storage.replace('\n', ''))

	access_token = storage['access_token']
	client_id = storage['client_id']
	client_secret = storage['client_secret']
	refresh_token = storage['refresh_token']
	expires_at = storage['token_response']['expires_in']
	user_agent = storage['user_agent']
	token_uri = storage['token_uri']

	# auth to google
	cred = client.GoogleCredentials(access_token,client_id,client_secret,
	        refresh_token, expires_at, token_uri,user_agent,revoke_uri="https://accounts.google.com/o/oauth2/token")
	http = cred.authorize(Http())
	cred.refresh(http)
	service = build('calendar', 'v3', credentials=cred)

	return service