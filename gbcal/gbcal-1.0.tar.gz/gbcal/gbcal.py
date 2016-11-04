import httplib2
import os
import re
import datetime
import logging

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import config

class GBCal:
    """
    Class to manage google birthday calendar
    """
    def __init__(self, create_if_not_exist=False):
        """
        Create GBCal object
        """
        self.__service = self.__get_service()
        self.__cal_id = self.__get_calendar_id(create_if_not_exist=create_if_not_exist)
        
    def __get_service(self):
        """Get service object

        Returns:
          service object
        """
        credentials = self.__get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
        return service

    def __get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, config.CLIENT_SECRET_FILE)

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(config.CLIENT_SECRET_FILE, config.GOOGLE_API_SCOPES)
            flow.user_agent = config.GOOGLE_API_APP_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            logging.debug('Storing credentials to ' + credential_path)
        
        return credentials

    def __get_calendar_id(self, create_if_not_exist):
        """Get gbcal calendar ID

        Create calendar if not exist

        Returns:
            calendar id string
        """
        res = self.__service.calendarList().list(minAccessRole="owner", showHidden=True).execute()
        clist = res.get('items', [])

        # get calendar
        cal_id = None
        for c in clist:
            if c['summary'].lower() == config.GOOGLE_CALENDAR_NAME:
                cal_id = c['id']
                break
        
        # create calendar if not exist
        if not cal_id:
            if not create_if_not_exist:
                err = "Calendar '{}' not exist".format(config.GOOGLE_CALENDAR_NAME)
                raise Exception(err)

            cal = self.__service.calendars().insert(body={
                "kind": "calendar#calendarListEntry",
                "summary": CALENDAR_NAME,
                "timeZone": "Europe/Prague"
            }).execute()

            logging.debug("calendar {} was created".format(config.CALENDAR_NAME))
            cal_id = cal['id']
            
        return cal_id

    def get_events(self, regex=None):
        """Get calendar events

        Return:
            list of calendar events
        """
        eventsResult = self.__service.events().list(
            calendarId=self.__cal_id,
        ).execute()
        
        events = eventsResult.get('items', [])

        if regex:
            return [e for e in events if re.search(regex, e['summary'])]
        else:
            return events
    
    def add_event(self, date, name):
        if not date or not name:
            raise Exception("Invalid params in add_event")
        
        if not re.match('\d{4}\-\d{2}\-\d{2}', date):
            raise Exception("Invalid date param. Date must be in form YYYY-MM-DD")
        
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

        res = self.__service.events().insert(
            calendarId=self.__cal_id,
            body={
                "summary": name,
                "start": dict(
                    date=date,
                    timeZone="Europe/Bratislava",
                ),
                "end": dict(
                    date=date,
                    timeZone="Europe/Bratislava",
                ),
                "recurrence": ["RRULE:FREQ=YEARLY"],
            }
        ).execute()
