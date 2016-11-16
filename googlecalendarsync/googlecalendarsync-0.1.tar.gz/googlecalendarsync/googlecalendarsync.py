"""
GoogleCalendarSync module

Author: Diamino
"""

import json
import time
import calendar
import httplib2

from apiclient import discovery
from oauth2client import file
#from oauth2client import client

TIMEZONE = 'UTC'

class GoogleCalendarSync(object):
    """
    Main class of GoogleCalendarSync
    """

    service = None

    def __init__(self, dao, calendar, interval=60, actionmap={}):
        self.dao = dao
        self.calendar = calendar
        self.interval = interval
        self.actionmap = actionmap

    def authorize(self, filename=None):

        if filename is not None:
            storage = file.Storage(filename)
            credentials = storage.get()
        else:
            credentials = self.dao.getCredentials()

        if credentials is None or credentials.invalid:
            return False

        # Create an httplib2.Http object to handle our HTTP requests and authorize it
        # with our good Credentials.
        http = httplib2.Http()
        http = credentials.authorize(http)

        # Construct the service object for the interacting with the Calendar API.
        self.service = discovery.build('calendar', 'v3', http=http)

    def run(self): # This method could be run from a seperate thread. It continuously updates the DAO.
        if self.service is None:
            # Authorization phase has failed
            return False

        events = self.service.events()

        syncToken = self.dao.getSyncToken()

        currentTime = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()) # current time in RFC3339 format

        reqargs = {'calendarId':self.calendar, 'singleEvents':True, 'timeMin':currentTime, 'timeZone':TIMEZONE, 'syncToken':syncToken}

        while True:
            results, syncToken = self.getAllItems(events, reqargs)
            print json.dumps(results, sort_keys=True, indent=4)
            self.dao.setSyncToken(syncToken)
            self.processCalendarItems(results)

            reqargs.pop('timeMin', None) # The timeMin option should be removed when the call is made with a syncToken
            reqargs['syncToken'] = syncToken
            #print self.dao.events
            time.sleep(self.interval)

    def getAllItems(self, serviceelement, arguments):
        result = []
        morepages = True
        while morepages:
            request = serviceelement.list(**arguments)
            try:
                response = request.execute()
            except:
                print('Request to Google API failed.')
                continue
            result.extend(response['items'])

            if 'nextPageToken' not in response: # This means we have retrieved all the pages
                morepages = False
            else:
                arguments['pageToken'] = response['nextPageToken']
        return result, response['nextSyncToken']

    def processCalendarItems(self, items):
        for item in items:
            if item['status'] == 'confirmed': # A new entry. Add it to the list
                action = item['summary'].lower()
                if self.actionmap != {}:
                    if action in self.actionmap:
                        action = self.actionmap[item['summary']]
                    else:
                        break
                if calendar.timegm(time.strptime(item['end']['dateTime'],"%Y-%m-%dT%H:%M:%SZ")) >= time.time():
                    self.dao.insertEvent((calendar.timegm(time.strptime(item['start']['dateTime'],"%Y-%m-%dT%H:%M:%SZ")),'start',action, item['id']))
                    self.dao.insertEvent((calendar.timegm(time.strptime(item['end']['dateTime'],"%Y-%m-%dT%H:%M:%SZ")),'end',action, item['id']))
            elif item['status'] == 'cancelled': # An entry is removed. Remove it from the list
                self.dao.removeEvent(item['id'])

