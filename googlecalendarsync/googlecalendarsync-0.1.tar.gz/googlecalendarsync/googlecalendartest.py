#!/usr/bin/python

# googlecalendartest.py

import time
import threading
import googleeventdao
import googlecalendarsync

CHECK_INTERVAL = 10

GOOGLECALENDARID = 'evtvaeuc5vjrn2vmj00onb8hks@group.calendar.google.com'
CREDFILE = 'test_calendar.gtoken'
GOOGLEINTERVAL = 10

# Setup Google Calendar Sync
gedao = googleeventdao.GoogleEventDao()
gcs = googlecalendarsync.GoogleCalendarSync(gedao, GOOGLECALENDARID, interval=GOOGLEINTERVAL)
gcs.authorize(CREDFILE)

gcsThread = threading.Thread(target=gcs.run, name="gcsThread")
gcsThread.daemon = True
gcsThread.start()

while True:
    print "Checking for event..."
    #print self.gedao.events
    event = gedao.peekEvent()
    if event:
        print event
    time.sleep(CHECK_INTERVAL)
