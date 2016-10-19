__version__ = "0.1.0"

'''
created 10.5.16

Andrew Lee 

changelog:
10.5.16

added get_cal_service function

10.19.16
added get_events and add_sub_attendees_to_cal functions
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

	return 

def get_events(calendar, start, end, num_events, time_zone_str='America/Chicago'):
	'''
	get all available events in the time frame

	inputs:
	calendar - str of google cal
	start / end - str need to be in google cal time format
	num_events - the max number of events desired to be returned
	time_zone_str - time zone of cal
	
	return df of event ids	
	'''

    eventsResult = service.events().list(
            calendarId=calendar, 
            timeMin=start, timeMax=end, timeZone=time_zone_str, maxResults=num_events, singleEvents=True, 
            orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    event_list = []
    if not events:
        print('No upcoming events found.')
    else:
        for event in events:
        # get event ids and other info about meeting
            event_id = event['id']
            event_sum = event['summary']
            start_time = event['start'].get('dateTime')

            if 'location' in event:
                location = event['location']
            else:
                location = 'no room currently booked'

            event_stats = [event_id, event_sum, start_time, location]
            event_list.append(event_stats)
        # shove in dataframe, not using all info
        df_events = pd.DataFrame(event_list, columns=['event_id', 'summary', 'start_time', 'location'])

        return df_events



def add_sub_attendees_to_cal(calendar, event_list, to_change, add_to_cal=True):
	'''
	function takes list of events and adds everyone to the event ids in df
	
	calendar - str google calendar
	event_list - list of event ids to add or subtract
	to_change - email addresses that need to be changed
	add_to_cal - boolean add or subtract (default=True)
	
	returns list of emails that failed to be added to event
	'''

    failed_to_drop_list = []
    for i in range(0,len(event_list)):
        event = service.events().get(calendarId=calendar, eventId=event_list[i]).execute()

        # if there are existing attendees keep them, if not add to dict
        if add_to_cal==True:
            try:
                event['attendees'] += to_change
            except:
                event['attendees'] =  to_change
        else:
            for email_dict in to_change:
                try:
#                     gets the position in the list 
                    email_pos = next(index for (index, d) in enumerate(event['attendees']) if d['email'] == email_dict['email'])
#                     delete from attendees
                    event['attendees'].pop(email_pos)
                except:
                    failed_to_drop_list.append(email_dict['email'])
                    None
            
        updated_event = service.events().update(calendarId=calendar, sendNotifications=True,
            eventId=event['id'], body=event).execute()
        
    return failed_to_drop_list