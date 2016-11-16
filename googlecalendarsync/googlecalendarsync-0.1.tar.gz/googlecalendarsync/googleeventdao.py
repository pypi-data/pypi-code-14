"""
GoogleEventDao module

This module is used together with the GoogleCalendarSync module.
It is used by GoogleCalendarSync to store events.
"""

import threading
import dao

class GoogleEventDao(dao.TriggerDao):
    """
    This DAO uses a standard list. A deque is probably faster.
    """

    syncTokens = {}
    events = [] # format of event: (time_of_event, 'start'|'end', action, google_item_id)

    lock = None

    def __init__(self):
        self.lock = threading.Lock()

    def getSyncToken(self, name='default'):
        if name in self.syncTokens:
            return self.syncTokens[name]
        else:
            return None

    def setSyncToken(self, syncToken, name='default'):
        self.syncTokens[name] = syncToken

    def getCredentials(self):
        # Not implemented yet
        return None

    def clearEvents(self):
        self.events = []

    def insertEvent(self, event):
        insertindex = None
        insertcorrection = 0 # this variable is used to correct the index used for insertion when items get deleted
        self.lock.acquire()
        # event is a tuple with the following format: (time, 'start'|'end', action, id)
        for index, listevent in enumerate(self.events[:]):
            if (listevent[3] == event[3]) and (listevent[1] == event[1]):
                # This is an updated version of an already existent entry. Remove the old version
                self.events.pop(index)
                insertcorrection = insertcorrection - 1
                continue
            if (insertindex is None) and (listevent[0] <= event[0]):
                insertindex = index + insertcorrection

        if insertindex != None:
            self.events.insert(insertindex, event)
        else:
            self.events.append(event)

        self.lock.release()

    def removeEvent(self, googleid):
        self.lock.acquire()
        # Will now iterate through the events in reverse order
        # In this way no problems arise with shifting indices
        for index, listevent in reversed(list(enumerate(self.events[:]))):
            if listevent[3] == googleid:
                self.events.pop(index)
        self.lock.release()

    def popEvent(self):
        self.lock.acquire()
        if len(self.events) == 0:
            element = None
        else:
            element = self.events.pop()
        self.lock.release()
        return element

    def peekEvent(self):
        # self.lock.acquire()
        if len(self.events) == 0:
            element = None
        else:
            element = self.events[-1]
        # self.lock.release()
        return element

